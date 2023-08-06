

# Galaxy to Janis Translation

Galaxy2janis is a productivity tool which translates Galaxy tool wrappers and workflows into the Janis language. <br>
It accepts either a Galaxy wrapper (.xml) or workflow (.ga) and will produce a Janis definition (.py).

This software is part the [Portable Pipelines Project](https://www.melbournebioinformatics.org.au/project/ppp/) which produces technologies to make workflow execution and sharing easier. 

Galaxy2janis is currently available in pre-release form.

**Contributing:**  Please get in touch by [raising an issue](https://github.com/GraceAHall/galaxy2janis/issues) so we can communicate via email or zoom.<br>
**Bugs:** Please submit any bugs by [raising an issue](https://github.com/GraceAHall/galaxy2janis/issues) to help improve the software!<br> 

This program may fail when parsing legacy galaxy tools, or those written in unforseen ways. 

<br>

## Contents

- [Quickstart Guide](#quickstart-guide)
- [Description](#description)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Producing CWL WDL Nextflow](#producing-cwl-wdl-nextflow)
- [Making Runnable](#making-runnable)
- [Supported Features](#supported-features)

## Quickstart Guide

Galaxy2janis is available as a PyPI package. 
It requires python ≥ 3.10. 

```
# create & activate environemnt
python3.10 -m venv venv
source venv/bin/activate
```

```
# install package
pip install galaxy2janis
```

```
# translate galaxy tool
galaxy2janis tool [PATH]
galaxy2janis tool sample_data/abricate/abricate.xml

# translate galaxy workflow
galaxy2janis workflow [PATH]
galaxy2janis workflow sample_data/assembly.ga
```

The `sample_data` folder contains the files above and can be used to test your installation. 

<br>

## Description

#### What does this program do?

This program was created to aid workflow migration. It was designed to be a productivity tool by helping the user port a workflow from one specification to another. 

Given a *galaxy tool wrapper* or *galaxy workflow*, it will extract as much information as possible, and will create a similar definition in ***[Janis](https://janis.readthedocs.io/en/latest/index.html)***. Once in Janis, `janis translate` can be used to output an equivalent CWL/WDL/Nextflow definition.

For tool translations, the main software requirement will be identified and translated to Janis. A container will also be identified which can run the output Janis tool.

For workflow translations, the workflow itself will be translated to a Janis definition, alongside each tool used in the workflow.

#### What does this program not do?

Galaxy2janis is a *productivity tool*. It does not provide *runnable* translations.

It aims to produce a human readable output, and to match the structure of the ingested workflow. Users are expected to make some ***manual edits*** to finalise the workflow. See the [Making Runnable Section](#making-runnable) for details. 

<br>

## Inputs

#### Tool translation

```
usage: galaxy2janis tool [OPTIONS] infile.xml

positional arguments:
  infile                path to tool.xml file to parse.

options:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir OUTDIR
                        output folder to place translation
```

A local copy of the galaxy tool wrapper is needed. To download a tool wrapper: 
- Select the tool in galaxy
- View its toolshed entry *(top-left caret dropdown, 'See in Tool Shed')*
- Download the wrapper as a zip file *(repository actions -> 'Download as a zip file')*

<img src='./media/download_wrapper.png' width='320px'>

The unzipped file is the wrapper for that galaxy tool. 

Once the wrapper has been obtained, the path to the specific tool to translate must be specified. For example, if you downloaded the abricate tool you may something similar to this structure:

```
abricate/
├── abricate.xml
├── macros.xml
└── test-data
    ├── Acetobacter.fna
    ├── MRSA0252.fna
    └── output_db-card.txt
```

To translate abricate.xml:
```
galaxy2janis tool abricate/abricate.xml
```

<br>

#### Workflow Translation

```
usage: galaxy2janis workflow [OPTIONS] infile.ga

positional arguments:
  infile                path to workflow.ga file to parse.

options:
  -h, --help            show this help message and exit
  -o OUTDIR, --outdir OUTDIR
                        output folder to place translation
```

A local copy of the galaxy workflow is needed. There are two methods to download a workflow:

1. Download from workflow editor<br>
<img src='./media/download_workflow_editor.png' width='600px'>

2. Download from Galaxy Training Network (GTN)<br>
<img src='./media/download_workflow_gtn.png' width='380px'>

These will download a galaxy workflow file in *.ga* format. 

To translate the workflow:
```
galaxy2janis workflow downloaded_workflow.ga
```

Each tool used in the workflow will be downloaded and translated automatically during the process. 

<br>

## Outputs

Tool translations produce a single Janis tool definition for in the input galaxy wrapper. 

Workflow translations produce an output folder containing multiple files. Workflows need multiple entities such as tool definitions, the main workflow file, scripts, and a place to provide input values to run the workflow. The current output structure is as follows: 

```
[translated_workflow]/
├── inputs.yaml             # input values
├── logs                
├── subworkflows    
├── tools                   # tool definitions
│   ├── scripts             # tool scripts
│   ├── untranslated        # untranslated tool logic (galaxy)
│   └── wrappers            # translated tool wrappers (galaxy)
└── workflow.py             # main workflow file
```

<br>

## Producing CWL WDL Nextflow

#### Janis Translate

Galaxy -> Janis -> CWL/WDL/Nextflow

This program ingests Galaxy definitions to produce Janis definitions. <br>
Janis' inbuilt `translate` functionality can subsequently output to the languages seen above. 

For example, translating the `abriate` tool from Galaxy to CWL:

```
# galaxy -> janis
galaxy2janis tool abricate/abricate.xml         (produces abricate.py)

# janis -> CWL
janis translate abricate.py > abricate.cwl
```

<br>

## Making Runnable

It is the responsibility of the user to make final edits & bring the workflow to a runnable state.

This tool is designed to increase productivity when migrating workflows; as such, the outputs it produces favour readability over completeness. 

To aid users in this process, some hints are supplied and sources files are retained. 

#### Hints

Some basic hints are provided to help users check the output. This information helps the user confirm everything looks correct, and make edits when it isn't quite right. 

***quast*** step in translated workflow: 
<img src='./media/tool_step.png' width='750px'><br>
A galaxy workflow was translated to Janis using galaxy2janis. A step within the workflow uses quast, which we see reflected in our output `workflow.py` file.  The actual quast tool being used in the step above is a Janis definition and will appear in the `tools/` output directory. 

#UNKNOWN1=w.unicycler.outAssembly,  # (CONNECTION)

When a tool input value appears commented out, the program was unable to link it to a software input. This may happen because the galaxy wrapper modifies the galaxy input before it is wired to an actual software input. In these cases, the user would need to either identify which tool input it maps to, or if none exists, open the translated `quast` tool and create one. 


#### Source Files

These can be viewed to gain more context on what a source galaxy tool was intended to do. The main software command will have been translated into a Janis tool, but some details may have been left out in the process. 

`tools/untranslated`

Contains untranslated galaxy tool logic. Galaxy tool wrappers may perform multiple tasks when executed. The main software tool being wrapped will execute, but some preprocessing or postprocessing steps may also be performed. A common structure is as follows:
- Preprocessing (symlinks / making directories / creating a genome index)
- Main software requirement (actual tool execution)
- Postprocessing (index or sort output / create additional output files / summaries)

Galaxy2janis translates the main software requirement into a Janis definition. Preprocessing and postprocessing logic are placed into the `tools/untranslated` folder as a reference, so the user can see what has been ignored. 

`tools/wrappers`

Contains galaxy tools which were translated. They are the 'source files' which we used to create Janis tool definitions while the workflow was being parsed.  Can be used as reference when tool translations weren't good quality. <br>
Galaxy wrappers have a distinct style, so see the [galaxy tool xml documentation](https://docs.galaxyproject.org/en/latest/dev/schema.html) for details. 

<br>

## Supported Features

This project is in active development. Many features are planned, and will be released over time.  

#### unsupported

Features

- \<command> `#def #set #if #for` cheetah logic
- \<command> `Rscript -e` (inline Rscripts)
- \<param> `type="color"` params
- xml features seen in 1% of tools 

Wrappers

- `emboss` suite of tool wrappers known to fail due to legacy features.


