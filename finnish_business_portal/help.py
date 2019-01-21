from .settings.url.parameters import SEARCH as PARAMS_SEARCH, REGISTERS as REGISTERS_SEARCH

def show_search_parameters(func=print):
    search_params = PARAMS_SEARCH
    
    maxlen_params = max(len(param) for param in search_params)
    maxlen_description = max(len(desc) for desc in search_params.values())

    out = 'Seach Parameters'
    out += f'\n{"-"*(maxlen_params+maxlen_description+3)}'
    out += '\n' + '\n'.join([f'{param}: {" "*(maxlen_params-len(param))} {description}' for param, description in search_params.items()])
    out += f'\n{"-"*(maxlen_params+maxlen_description+3)}\n'

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