import json

import requests

# consts

_GITHUB_API_URL = 'https://api.github.com/repos/%s/%s/contents/%%s'


def _get_format_path(path: str):
    if not bool(path):
        return "/"
    if path[0] != '/':
        path = '/' + path
    for sep in list('\\'):
        path = path.replace(sep, '/')
    return path


class File:
    name: str
    path: str
    sha: str
    size: int
    type: str

    def __init__(self, name: str, path: str, sha: str, size: int, _type: str):
        self.name = name
        self.path = path
        self.sha = sha
        self.size = size
        self.type = _type

        def f(s, k, v):
            raise RuntimeError()

        self.__setattr__ = f


class GithubAPI:
    __token: str
    __api_url: str

    def __init__(self, owner: str, repo: str, token: str = ""):
        self.set_token(token)
        self.__api_url = _GITHUB_API_URL % (owner, repo)

    def _get_api(self, path: str = "") -> str:
        path = _get_format_path(path)
        path = self.__api_url % path
        return path

    def set_token(self, token: str):
        self.__token = token

    def get_token(self) -> str:
        return self.__token

    def _get_headers(self, _type: str = "json"):
        res = {
            "Accept": f"application/vnd.github.{_type}"
        }
        if self.has_token():
            res["Authorization"] = f"token {self.__token}"
        return res

    def has_token(self) -> bool:
        return bool(self.__token)

    def listdir(self, path: str = ""):
        path = self._get_api(path)
        res = requests.get(path, headers=self._get_headers())
        if not res.ok:
            return list()
        res = json.loads(res.content)
        result = list()
        for item in res:
            result.append(
                File(
                    item["name"],
                    item["path"],
                    item["sha"],
                    item["size"],
                    item["type"]
                )
            )
        return result
