from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .utils import *

db_logger = logging.getLogger('db')


class Browser:
    name = 'Chrome'
    path = "/usr/lib/chromium-browser/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    print('Browser opens')


class Program(Browser):
    tree = None
    opened_urls = []
    variables = {}

    def __init__(self, _id, code: str):
        self.code = code
        self.id = _id
        self.chs = CheckSyntax(_id, code)
        db_logger.debug(f'Program started|{_id}')

    def get_page_text(self):
        self.tree = html.fromstring(self.driver.page_source)

    def run(self):
        # First Step - checking is syntax OK
        passed, data = self.chs.check()
        db_logger.debug(f'Checking syntax|{self.id}')
        # Second Step - if OK, start execute code
        if passed:
            db_logger.info(f'Syntax - OK|{self.id}')
            for line in data:
                kwargs = {}
                parts = line.split()
                function = eval(parts[0].capitalize())(self.id, line)
                if parts[0] == 'open' or parts[0] == 'back':
                    kwargs.update({'driver': self.driver, 'opened_urls': self.opened_urls})
                elif parts[0] == 'get':
                    self.get_page_text()
                    kwargs.update({'tree': self.tree})
                function.execute(self.variables, **kwargs)
            print(self.variables)
            print(self.opened_urls)
        else:
            for line in data:
                db_logger.error(f'{line}|{self.id}')
            print(data)  # Print Errors

    def __del__(self):
        print('Browser will be closed')
        db_logger.info(f'Stopping program|{self.id}')
        self.driver.quit()
