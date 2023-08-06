### this is a lib of python
you can use `syllib.__version__` to show the version

## functions

### in package `syllib`
function `install(name: str)` (from syllib.pip)

install a package from https://pypi.org/simple

result: None


function `uninstall(name: str)` (from syllib.pip)

uninstall a package

result: None


function `abs_import(path: str, _globals=None, _locals=None, fromlist=(), level=0) -> module`

it can import a package from a far away path

path: a string of path

_globals: a dictionary like globals()

_locals: a dictionary like locals()

fromlist: a list or tuple

if enabled,it works like:

`from [path] import [fromlist]`

result: a module


### in package `syllib.xes`
function `get_cookies() -> str`

result: a string of cookies(in xueersi)


function `get_run_token() -> str`

result: a string of token(in the cookies)


function `send(mobile: int, content: str) -> bool`

        mobile: the mobile number of who you want to send
        content: a string of content what you want to send

result: True(success) or False(failed)

### in package `syllib.tools`
function `get_run_dir() -> str`

result: a string where 'python.exe'

### in package `syllib.config`
class `Config(name: str, auto_save: bool = True)`

You can use `cfg = Config([name,[auto_save]])` to create a config file
the file saves at the python path
it saves by module pickle

function `Config.read`

read saved file


function `Config.save`

save the attributes


function `Config.__getitem__`,`Config.__setitem__` and `Config.__delitem__`

works like python dictionary

