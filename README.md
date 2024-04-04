# Resume generator

## Usage

```
python -m resume-gen [-h] [-i INPUT] [-o OUTPUT]

Generate resumes from YAML

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file (resume definition in yaml)
  -o OUTPUT, --output OUTPUT
                        output file
```

## Requirements

Python 3.11 or newer

## Before use

Define your resume as yaml in input file and run program.
Also run the following commands:
```
python -m venv env
. env/bin/activate # (on Linux)
env/Scripts/activate &:: (on Windows)
python -m pip install -r requirements.txt
```

You can edit the styles (mostly colors) under `generator/static/css/styles.css`

## Output

Files `finnish.html` and `english.html` will be generated under output_dir
specified with -o flag. If left unspecified, current working directory is used.

## Examples

An example resume definition is provided in resume.yaml.
It is also the default input file.

> NB! Editing the default input file `resume.yaml` is advised against as it will lead into merge conflicts.

## Licence

CC-BY-NC

Contact the author for commercial use.
