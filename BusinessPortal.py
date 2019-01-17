
from core.parameter_validation import validate_params
from search_funcs import search_companies, search_companies_deep
from io_interface import load_params, save_results

import sys

class CLI:

    _menu = '''
Main menu:
1) Load Search Parameters from file
2) Input Search Parameters
3) Run search
4) Show search results
5) Info
0) End
'''[1:-1]

    _input_str = 'Option: '
    _end_str = 'End of Program.'


    _commands = {
        '1': 'load_params',
        '2': 'input_params',
        '3': 'run_search',
        '4': 'show_results',
        '5': 'save_results',
        '6': 'show_info',
        '0': '_end'
    }

    def __init__(self):
        pass
            
    def run(self):
        'Run the command line window'
        while True:
            print(self._menu)
            command = input(self._input_str)
            try:
                func = getattr(self, self._commands[command])
            except:
                print(f"Command {command} not found.")
                continue
            try:
                func()
            except Exception as err:
                print(err)


    def load_params(self):
        params = load_params(filename=input("File name: "))
        validate_params(**params)
        self.search_params = params

    def input_params(self):
        key = None
        params = {}
        while True:
            key = input("Parameter name (enter to exit): ")
            if key == "":
                break
            val = input('Parameter value (use "|" as separator): ')
            val = val.split('|')
            params[key] = val

        validate_params(**params)
        self.search_params = params

    def run_search(self):
        while True:
            com = input("Run thorough search? y/n ")
            if com.lower() == "y":
                result = search_companies_deep(**self.search_params)
                break
            elif com.lower() == "n":
                result = search_companies(**self.search_params)
                break
            else:
                continue

        self.search_result = result

    def show_results(self):
        print(self.search_result)

    def save_results(self):
        save_results(self.search_result, filename=input("File name: "))


    def _end(self):
        print(self._end_str)
        sys.exit()


if __name__ == "__main__":
    cli = CLI()
    cli.run()