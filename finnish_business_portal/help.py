
import re

from .settings.url.parameters import SEARCH as PARAMS_SEARCH, REGISTERS as REGISTERS_SEARCH
from .core.connection import get_page

from .opendata import opendata


def show_api(func=print):
    paths = opendata.paths
    out = 'Seach Parameters\n'
    padding = '    '
    for path, methods in paths.items():
        out += f'{padding}Path: {path}\n'
        for method, search in methods.items():
            summary = search["summary"]
            out += f'{padding*2}Method: {method}\n'
            out += f'{padding*2}Summary: {summary}\n'
            for param in search["parameters"]:

                description = param["description"]
                link = re.findall(r'(?<=<a href=")[^"]+(?=")', param["description"])
                description = re.sub(r'<a href="[^"]+">', '', description).strip().replace('</a>', '')

                default_val = param.get("defaultValue", None)
                enum = param.get("enum", None)
                minimum, maximum = param.get("minimum", None), param.get("maximum", None)

                out += f'{padding*3}Parameter: {param["name"]}\n'
                out += f'{padding*4}Description: {description}\n'
                if link:
                    link = link[0]
                    is_full_link = link.startswith('http')
                    if not is_full_link:
                        link = '/'+link if not link.startswith('/') else link
                        link = opendata.url+link
                    out += f'{padding*5}See: {link}\n'
                out += f'{padding*4}Required: {param["required"]}\n'
                if default_val:
                    out += f'{padding*4}Default: {default_val}\n'
                if enum:
                    out += f'{padding*4}Valid values: {enum}\n'
                if minimum or maximum:
                    out += f'{padding*4}Valid range: {minimum} - {maximum}\n'
    func(out)

def show_paths(func=print):
    paths = opendata.paths
    out = 'Paths\n'
    padding = '    '
    for path, methods in paths.items():
        methods = {key: val["summary"] for key, val in methods.items()}
        methods = [f'{key}: {val}' for key, val in methods.items()]
        out += f'{padding}{path}\n'
        out += f'{padding*2}{methods}\n'
    func(out)

def show_registers(func=print):
    registers = REGISTERS_SEARCH
    
    maxlen_regs = max(len(reg) for reg in registers)
    maxlen_description = max(len(desc) for desc in registers.values())

    out = 'Registers'
    out += f'\n{"-"*(maxlen_regs+maxlen_description+3)}'
    out += '\n' + '\n'.join([f'{reg}: {" "*(maxlen_regs-len(reg))} {description}' for reg, description in registers.items()])
    out += f'\n{"-"*(maxlen_regs+maxlen_description+3)}\n'

    func(out)

def get_search_parameters():
    search_params = PARAMS_SEARCH
    registers = REGISTERS_SEARCH
    return {key:str for key in search_params}

def get_codes():
    # http://avoindata.prh.fi/tr-codes_v1.fi.txt
    # http://avoindata.prh.fi/tr-type_v1.fi.txt
    page = get_page("http://avoindata.prh.fi/tr-codes_v1.fi.txt")
    cont = [code.split('\t') for code in page.text.split('\n')]
    return {row[0]:row[-1] for row in cont if row[0] != ''}


def get_codes_industry():
    raise NotImplementedError

def get_codes_company_form():
    return _get_codes("http://avoindata.prh.fi/tr-company_v1.fi.txt")

def _get_codes(url):
    page = get_page(url)
    cont = [code.split('\t') for code in page.text.split('\n')]
    return {row[0]:row[-1] for row in cont if row[0] != ''}