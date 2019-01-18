from .settings.url.parameters import SEARCH as PARAMS_SEARCH

def show_search_parameters(func=print):
    search_params = PARAMS_SEARCH
    
    maxlen_params = max(len(param) for param in search_params)
    maxlen_description = max(len(desc) for desc in search_params.values())

    out = 'Seach Parameters'
    out += f'\n{"-"*(maxlen_params+maxlen_description+3)}'
    out += '\n' + '\n'.join([f'{param}: {" "*(maxlen_params-len(param))} {description}' for param, description in search_params.items()])
    out += f'\n{"-"*(maxlen_params+maxlen_description+3)}\n'
    if func is not None:
        func(out)
    return out

