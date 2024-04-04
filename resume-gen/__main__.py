import argparse
from . import languagedict
from . import generate

parser = argparse.ArgumentParser(
    prog='resume-gen',
    description='Generate resumes from YAML',
    epilog='Copyright (c) Juhani Kupiainen 2024. All rights reserved.'
)
parser.add_argument('-i', '--input', default='resume.yaml', help='input file (resume definition in yaml)')
parser.add_argument('-o', '--output', default='resume.html', help='output file')

args = parser.parse_args()

languages = languagedict.get_supported_languages()
generate.generate(args.input, args.output, languages)
