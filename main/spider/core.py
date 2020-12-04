from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree, html

from .utils import *


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

    def __init__(self, code: str):
        self.code = code
        self.chs = CheckSyntax(code)

    def get_page_text(self):
        self.tree = html.fromstring(self.driver.page_source)
        # return self.tree.xpath('//title')[0].text

    def run(self):
        # First Step - checking is syntax OK
        passed, data = self.chs.check()
        # Second Step - if OK, start execute code
        if passed:
            for line in data:
                kwargs = {}
                parts = line.split()
                function = eval(parts[0].capitalize())(line)
                if parts[0] == 'open' or parts[0] == 'back':
                    kwargs.update({'driver': self.driver, 'opened_urls': self.opened_urls})
                elif parts[0] == 'get':
                    self.get_page_text()
                    kwargs.update({'tree': self.tree})
                function.execute(self.variables, **kwargs)
            print(self.variables)
            print(self.opened_urls)
        else:
            print(data)  # Print Errors

    def __del__(self):
        print('Browser will be closed')
        self.driver.quit()
