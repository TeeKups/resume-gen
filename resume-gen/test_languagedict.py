import pytest
import languagedict
import yaml

testdata = """---
foo:
  finnish: suomeksi
  english: englanniksi
bar:
  finnish:
    fizzbuzz: suomeksi
  english:
    fizzbuzz: englanniksi
list:
  - jotain
  - finnish: suomeksi
    english: englanniksi
spam: ham
"""

def test_returns_correct_language_from_dict_when_key_defined_in_two_languages():
    fin = yaml.load(testdata, Loader=languagedict.makeLanguageDictLoader('finnish'))

    assert fin['foo'] == 'suomeksi'

def test_returns_correct_language_from_dict_when_language_specific_sub_dictionaries():
    fin = yaml.load(testdata, Loader=languagedict.makeLanguageDictLoader('finnish'))

    assert fin['bar']['fizzbuzz'] == 'suomeksi'

def test_returns_correct_language_from_list_item():
    fin = yaml.load(testdata, Loader=languagedict.makeLanguageDictLoader('finnish'))

    assert str(fin['list'][1]) == 'suomeksi'

def test_returns_correct_item_when_no_multilanguage():
    fin = yaml.load(testdata, Loader=languagedict.makeLanguageDictLoader('finnish'))

    assert fin['spam'] == 'ham'
