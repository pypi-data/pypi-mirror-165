


from galaxy2janis.logs import logging
from galaxy2janis import expressions

from typing import Optional

from galaxy2janis.gx.gxtool import XMLToolDefinition
from galaxy2janis.expressions.patterns import LINUX_STATEMENT_DELIMS

from .CommandString import CommandString
from .DynamicCommandStatement import DynamicCommandStatement
from .MainStatementInferrer import MainStatementInferrer
from .RealisedTokenValues import RealisedTokenFactory


def gen_command_string(
    source: str, 
    the_string: str, 
    xmltool: Optional[XMLToolDefinition]=None,
    requirement: Optional[str]=None
    ) -> CommandString:

    if xmltool and not requirement:
        requirement = xmltool.metadata.get_main_requirement().name
    assert(requirement)

    statements = _gen_command_statements(the_string, xmltool)
    statement_dict = _split_pre_main_post_statements(statements, source, requirement)
    return _init_command_string(statement_dict)

def gen_command_statement(statement: str, xmltool: Optional[XMLToolDefinition]=None) -> DynamicCommandStatement:
    factory = RealisedTokenFactory(xmltool)
    realised_tokens = factory.try_tokenify(statement)
    return DynamicCommandStatement(statement, realised_tokens)

def _gen_command_statements(the_string: str, xmltool: Optional[XMLToolDefinition]=None) -> list[DynamicCommandStatement]:
    statements: list[DynamicCommandStatement] = []
    for cmdstmt in _split_text_statements(the_string):
        statements.append(gen_command_statement(cmdstmt, xmltool))
    return statements

def _split_text_statements(the_string: str) -> list[str]:
    statements: list[str] = []
    
    delim_matches = expressions.get_matches(the_string, LINUX_STATEMENT_DELIMS)
    quoted_sections = expressions.get_quoted_sections(the_string)

    # has to be reverse order otherwise m.start() and m.end() are out of place
    for m in sorted(delim_matches, key=lambda x: x.start(), reverse=True): 
        if quoted_sections[m.start()] == False and quoted_sections[m.end()] == False:
            left_split = the_string[:m.start()]
            right_split = the_string[m.end():]
            statements = [right_split] + statements # prepend
            the_string = left_split

    statements = [the_string] + statements # prepend the final split (left this time)
    return statements

def _split_pre_main_post_statements(
    statements: list[DynamicCommandStatement], 
    source: str, 
    requirement: str) -> dict[str, list[DynamicCommandStatement]]:

    out: dict[str, list[DynamicCommandStatement]] = {'pre': [], 'main': [], 'post': []}
    inferrer = MainStatementInferrer(statements, source, requirement)
    main_index = inferrer.infer()
    
    for i, statement in enumerate(statements):
        if i < main_index:
            out['pre'].append(statement)
        elif i == main_index:
            out['main'].append(statement)
        else:
            out['post'].append(statement)

    return out

def _init_command_string(statement_dict: dict[str, list[DynamicCommandStatement]]) -> CommandString:
    if statement_dict['pre']:
        logging.has_preprocessing()
    if statement_dict['post']:
        logging.has_postprocessing()
    return CommandString(
        main=statement_dict['main'][0], 
        preprocessing=statement_dict['pre'], 
        postprocessing=statement_dict['post'],
    )