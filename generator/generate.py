import jinja2 as jinja
import yaml
import markdown
import datetime
import os

from . import languagedict

PROGRAM_ROOT=os.path.dirname(__file__)

env = jinja.Environment(
    loader=jinja.FileSystemLoader(f'{PROGRAM_ROOT}/templates'),
    autoescape=jinja.select_autoescape()
)

def process_markdown(md: str):
    return markdown.markdown(str(md))

def format_phone_number(number: str):
    if len(number) == 13:
        return f'{number[0:4]} (0) {number[4:6]} {number[6:9]} {number[9:13]}'
    elif len(number) == 10:
        return f'+358 (0) {number[1:3]} {number[3:6]} {number[6:10]}'
    else:
        raise RuntimeError(f'{number} is not a valid phone number')

def read_file(path):
    with open(str(path), 'rt') as f:
        return f.read()

env.filters['markdown'] = process_markdown
env.filters['phonenumber'] = format_phone_number
env.filters['readfile'] = read_file

def generate(input: str, output: str, language: str):
    loader = languagedict.makeLanguageDictLoader(language)

    with open(str(input), 'rt') as f:
        resume = yaml.load(f, loader)

    with open('keywords.yaml', 'rt') as f:
        keywords = yaml.load(f, loader)

    html = env.get_template('resume.j2').render(
        **resume,
        keywords=keywords,
        year=datetime.date.today().strftime('%Y'),
        stylesheet=f'{PROGRAM_ROOT}/static/css/styles.css',
    )

    with open(f'{output}/{language}.html', 'wt') as f:
        f.write(html)

