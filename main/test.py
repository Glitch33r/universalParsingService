import datetime

from main.spider.core import Program

start = datetime.datetime.now()

Program("""let qwerty https://google.com.ua
open VAR_qwerty
concat save VAR_qwerty /q
let new 123282842
replace VAR_new 2 0
replace VAR_new 0 -
split VAR_qwerty //
open https://github.com/
sleep 5
open https://www.youtube.com/
open https://github.com/
get title xpath|//title
open https://www.youtube.com/
sleep 2
open VAR_qwerty
sleep 2
back 6
"""
        ).run()

print('time: ' + str(datetime.datetime. now() - start))

from main.spider.utils import Function


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


for cls in all_subclasses(Function):
    print(cls().explanation())