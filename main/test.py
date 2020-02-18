import datetime

from main.spider.core import Program

start = datetime.datetime.now()

Program("""let qwerty https://google.com.ua
open VAR_qwerty
concat save VAR_qwerty /q
let new 123282842
replace VAR_new 2 0
replace VAR_new 0 -
split VAR_qwerty /
open https://github.com/
open https://www.youtube.com/
open https://github.com/
open https://www.youtube.com/
open VAR_qwerty
back 6
"""
        ).run()

print('time: ' + str(datetime.datetime. now() - start))
