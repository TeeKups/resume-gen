import jinja2 as jinja
import yaml
import markdown
import datetime
import os
import base64

from . import languagedict

PROGRAM_ROOT = os.path.dirname(__file__)

env = jinja.Environment(
    loader=jinja.FileSystemLoader(f'{PROGRAM_ROOT}/templates'),
    autoescape=jinja.select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
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


def stars(amount):
    return amount * '''<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"/></svg>'''

def base64_image(path: str):
    try:
        extension = os.path.splitext(path)[1][1:]
        with open(path, 'rb') as image:
            image_data = base64.b64encode(image.read()).decode()
            return f'data:image/{extension};base64,{image_data}'

    except IndexError:
        raise RuntimeException(f"Extension of file {path} is not a valid MIME type.")

env.filters['markdown'] = process_markdown
env.filters['phonenumber'] = format_phone_number
env.filters['readfile'] = read_file
env.filters['stars'] = stars
env.filters['base64_image'] = base64_image



def render_inner_html(source: str, language: str):
    loader = languagedict.makeLanguageDictLoader(language)

    with open(str(source), 'rt') as f:
        resume = yaml.load(f, loader)

    with open('keywords.yaml', 'rt') as f:
        keywords = yaml.load(f, loader)

    html = env.get_template('resume_inner_html.j2').render(
        **resume,
        keywords=keywords,
        year=datetime.date.today().strftime('%Y')
    )

    return html


def generate(input: str, output: str, languages: list[str]):
    languages = ({
        'language': language,
        'inner_html': render_inner_html(input, language)
    } for language in languages)

    html = env.get_template('resume.j2').render(
        languages=languages,
        stylesheet=f'{PROGRAM_ROOT}/static/css/styles.css',
        scripts=[f'{PROGRAM_ROOT}/static/js/language.js']
    )

    with open(f'{output}', 'wt') as f:
        f.write(html)
