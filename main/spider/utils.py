DEV = False
PROD = True
VAR = 'VAR_'
CONCAT = 'CONCAT_'
SPLIT = 'SPLIT_'
COMPARE = 'COMPARE_'
LOOP = 'LOOP_'
URL = 'URL_'


class Function:
    name = 'Function name'
    state = False

    def __init__(self, f_str=None):
        self.full_str = f_str
        self.parts = f_str.split()

    def __set_name(self, v: str):
        self.name = v

    def __set_state(self, v: bool):
        self.state = v

    @staticmethod
    def explanation():
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

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
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

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):

        if int(self.parts[1]) <= len(kwargs.get('opened_urls')):
            length = len(kwargs.get('opened_urls')) - 1
            url = kwargs.get('opened_urls')[length - int(self.parts[1])]
            kwargs.get('opened_urls').pop(length - int(self.parts[1]))
            Open(f'open {url}').execute(variables, **kwargs)


class Let(Function):
    name = 'let'
    state = DEV

    def check_syntax(self):
        if (len(self.parts) == 2 or len(self.parts) == 3) and self.parts[0] == self.name:
            return {'passed': True}
        else:
            return {'passed': False, 'mgs': f'Error in syntax construction with {self.name} function'}

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
        if not self.parts[1] in variables.keys():
            try:
                if self.parts[2]:
                    variables.update({VAR + self.parts[1]: self.parts[2]})
                else:
                    variables.update({VAR + self.parts[1]: ''})
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

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
        tmp = ''
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

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
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

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
        variables[self.parts[1]] = variables[self.parts[1]].replace(self.parts[2], self.parts[3])


class Add(Function):
    name = 'add'
    state = DEV

    def check_syntax(self):
        if len(self.parts) == 3 and self.parts[2].isdigit() and self.parts[1].isdigit():
            return {'passed': True}
        else:
            return {'passed': False,
                    'mgs': f'Error in syntax construction with {self.name} function or you forgot some params'}

    @staticmethod
    def explanation():
        pass

    def execute(self, variables, **kwargs):
        variables[self.parts[1]] = int(variables[self.parts[1]]) + int(self.parts[2])


class CheckSyntax:

    def __init__(self, code: str):
        self.code = code

    def check(self):
        check_result = []
        lines = self.code.splitlines()
        for line in lines:
            parts = line.split()
            try:
                f = eval(parts[0].capitalize())(line)
                result = f.check_syntax()
                check_result.append(result)
            except NameError:
                check_result.append({'passed': False, 'msg': f'Error! Name {parts[0]} is not defined.'})

        if all(r['passed'] is True for r in check_result):
            return True, lines
        else:
            return False, check_result
