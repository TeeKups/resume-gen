import argparse
from . import languagedict
from . import generate

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', default='resume.yaml', help='output directory')
parser.add_argument('-o', '--output', default='.', help='output directory')

args = parser.parse_args()

for language in languagedict.get_supported_languages():
    generate.generate(args.input, args.output, language)
