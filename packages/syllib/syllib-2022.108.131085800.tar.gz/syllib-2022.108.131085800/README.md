github 仓库操作
1. 导入GithubAPI类 `from syllib.git import GithubAPI`
2. 创建实例 `api = GithubAPI([github用户名],[github仓库名],[github token(可选)])`

`api.__init__(owner, repo, [token=""])`

owner: str 仓库拥有者

repo: str 仓库名

token: str 你的github token(可选)

`api.get_token() -> str`

返回对象绑定的token

`api.set_token(token)`

设置对象的token

`api.has_token() -> bool`

返回对象有没有绑定token

`api.get_file_content(path) -> bytes`

path: 仓库根目录下文件相对路径

返回一个bytes对象

`api.save_file_content(path, data, [message], [encoding="utf-8"])`

path: 仓库根目录下文件相对路径

data: str or bytes 文件内容

message: 可选，默认为文件路径

encoding: 当data为str类型时的解码方式

`api.listdir(path="") -> List[File]`

path: str 仓库根目录下目录相对路径，默认为根目录

返回一个list,每个对象都是File类型

