import logging
import time

from lxml.etree import XPathSyntaxError, XPathEvalError

DEV = False
PROD = True
VAR = 'VAR_'
CONCAT = 'CONCAT_'
SPLIT = 'SPLIT_'
COMPARE = 'COMPARE_'
LOOP = 'LOOP_'
URL = 'URL_'

db_logger = logging.getLogger('db')


class Function:
    name = 'Function name'
    state = False

    def __init__(self, _id, f_str=''):
        self.full_str = f_str
        self.id = _id
        self.parts = f_str.split()

    def __set_name(self, v: str):
        self.name = v

    def __set_state(self, v: bool):
        self.state = v

    def explanation(self):
        pass

    def check_syntax(self):
        """Method that checks syntax of function"""
        print('Method that checks syntax of function')


class Open(Function):
    name = 'open'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 2 and self.parts[0] == self.name:
            return {'passed': True}
        else:
            return {'passed': False, 'mgs': f'Error in syntax construction with {self.name} function'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "Production" if self.state else "Development/Testing",
            'can': "will open given URL",
            'use': "open URL",
            'access': ' - '
        }

        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        if self.parts[1] in variables.keys():
            kwargs.get('opened_urls').append(variables[self.parts[1]])
            kwargs.get('driver').get(variables[self.parts[1]])
        else:
            kwargs.get('opened_urls').append(self.parts[1])
            kwargs.get('driver').get(self.parts[1])


class Back(Function):
    name = 'back'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 2 and self.parts[1].isdigit():
            return {'passed': True}
        else:
            return {'passed': False, 'mgs': f'Error in syntax construction with {self.name} function'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "will take you back a given number of steps (open links)",
            'use': "back number_of_steps",
            'access': ' - '
        }

        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        if int(self.parts[1]) <= len(kwargs.get('opened_urls')):
            length = len(kwargs.get('opened_urls')) - 1
            url = kwargs.get('opened_urls')[length - int(self.parts[1])]
            kwargs.get('opened_urls').pop(length - int(self.parts[1]))
            Open(self.id, f'open {url}').execute(variables, **kwargs)


class Sleep(Function):
    name = 'sleep'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 2:
            if self.parts[1].isdigit():
                if int(self.parts[1]) <= 60:
                    return {'passed': True}
                else:
                    return {'passed': False,
                            'mgs': f'Error in syntax construction with {self.name} function - max 60 sec'}
            else:
                return {'passed': False,
                        'mgs': f'Error in syntax construction with {self.name} function - must be integer'}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "will stop the execution of the code for the specified number of seconds",
            'use': "sleep number_of_seconds",
            'access': ' - '
        }
        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        print(f'Sleep on {self.parts[1]} sec')
        time.sleep(int(self.parts[1]))


class Let(Function):
    name = 'let'
    state = DEV

    def check_syntax(self):
        if (len(self.parts) == 2 or len(self.parts) == 3) and self.parts[0] == self.name:
            return {'passed': True}
        else:
            return {'passed': False, 'mgs': f'Error in syntax construction with {self.name} function'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "create variables and set values for them. You can access using VAR_[VARIABLE_NAME]",
            'use': "let VARIABLE_NAME value",
            'access': 'VAR_VARIABLE_NAME'
        }

        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        if not self.parts[1] in variables.keys():
            try:
                if self.parts[2]:
                    variables.update({VAR + self.parts[1]: self.parts[2]})
                else:
                    variables.update({VAR + self.parts[1]: ''})
            except IndexError:
                pass


class Get(Function):
    name = 'get'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 3 and self.parts[0] == self.name:
            temp = self.parts[2].split('|')
            if temp[0] == 'xpath' and len(temp) == 2:
                return {'passed': True}
        else:
            return {'passed': False, 'mgs': f'Error in syntax construction with {self.name} function'}

    def xpath(self, tree, expression):
        try:
            elements = tree.xpath(expression)
        except (XPathSyntaxError, XPathEvalError) as error:
            print(error)
            return

        if len(elements) == 1:
            return elements[0].text
        else:
            return elements

    def explanation(self):
        text = {
            'func': self.name,
            'state': "Production" if self.state else "Development/Testing",
            'can': "get data from opened URL using xpath. You can collect one or multiple elements depends on xpath expression.",
            'use': "get VARIABLE_NAME xpath|expression",
            'access': 'VAR_VARIABLE_NAME'
        }

        return text

    def execute(self, variables, **kwargs):
        expression = self.parts[2].split('|')[1]
        result = self.xpath(kwargs.get('tree'), expression)
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        if not self.parts[1] in variables.keys():
            try:
                variables.update({VAR + self.parts[1]: result})
            except IndexError:
                pass


class Concat(Function):
    name = 'concat'
    state = DEV

    def check_syntax(self):
        if len(self.parts) >= 3 and self.parts[0] == self.name and not self.parts[1].startswith(
                (VAR, CONCAT, SPLIT, LOOP)):
            return {'passed': True}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function or you forgot some params'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "concatenate data separated by space",
            'use': "concat VARIABLE_NAME_TO_SAVE variable/value .. variable/value",
            'access': 'CONCAT_VARIABLE_NAME_TO_SAVE'
        }

        return text

    def execute(self, variables, **kwargs):
        tmp = ''
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        for part in self.parts[2:]:
            if part in variables.keys():
                tmp += variables[part]
            else:
                tmp += str(part)

        variables.update({CONCAT + self.parts[1]: tmp})


class Split(Function):
    name = 'split'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 3:
            return {'passed': True}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "used to split variable by setted separator",
            'use': "split VARIABLE_NAME separator",
            'access': 'SPLIT_VARIABLE_NAME_[id of element]'
        }

        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        if self.parts[1] in variables.keys():
            n_var = self.parts[1].replace(VAR, '')
            spl = variables[self.parts[1]].split(self.parts[2])
            for idx, val in enumerate(spl):
                variables.update({f'{SPLIT}{n_var}_{idx}': val})
        else:
            pass


class Replace(Function):
    name = 'replace'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 4:
            return {'passed': True}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function or you forgot some params'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "return a copy with all occurrences of substring old replaced by new. Saving in the same variable name. ",
            'use': "replace VARIABLE_NAME part_to_replace new_part",
            'access': 'VAR_VARIABLE_NAME'
        }

        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        variables[self.parts[1]] = variables[self.parts[1]].replace(self.parts[2], self.parts[3])


class Add(Function):
    name = 'add'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 3:
            if self.parts[2].isdigit() and self.parts[1].isdigit():
                return {'passed': True}
            else:
                return {'passed': False,
                        'mgs': f'Error in syntax construction with {self.name} function - you must use only digits'}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function or you forgot some params'}

    def explanation(self):
        text = {
            'func': self.name,
            'state': "production" if self.state else "development/testing",
            'can': "add variable with given number",
            'use': "add VARIABLE_NAME number",
            'access': 'VAR_VARIABLE_NAME'
        }
        return text

    def execute(self, variables, **kwargs):
        db_logger.info(f'Function {self.name} - OK|{self.id}')
        variables[self.parts[1]] = int(variables[self.parts[1]]) + int(self.parts[2])


class CheckSyntax:

    def __init__(self, _id, code: str):
        self.code = code
        self.id = _id

    def check(self):
        check_result = []
        lines = self.code.splitlines()
        # print('CH SYN', lines)
        for line in lines:
            parts = line.split()
            try:
                f = eval(parts[0].capitalize())(self.id, line)
                result = f.check_syntax()
                check_result.append(result)
            except NameError:
                check_result.append({'passed': False, 'msg': f'Error! Name {parts[0]} is not defined.'})

        if all(r['passed'] is True for r in check_result):
            return True, lines
        else:
            return False, check_result
