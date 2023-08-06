import json
import base64
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

    def __repr__(self):
        return f'{self.type}(name="{self.name}", path="{self.path}", sha={self.sha}, size={self.size})'


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

    def _get_file_sha(self, api: str):
        res = requests.get(api, headers=self._get_headers())
        if not res.ok:
            return ""
        res = json.loads(res.content)
        if res.get("sha") is not None:
            return res["sha"]
        return ""

    def has_token(self) -> bool:
        return bool(self.__token)

    def get_file_content(self, path: str, encoding: str = "utf-8"):
        path = self._get_api(path)
        res = requests.get(path, headers=self._get_headers("raw"))
        res.encoding = encoding
        if not res.ok:
            return None
        return res.content

    def save_file_content(self, path: str, data, message = None, encoding: str = "utf-8") -> bool:
        if not isinstance(data, (str, bytes)):
            raise ValueError("data must be str or bytes")
        if isinstance(data, str):
            data = data.encode(encoding)
        data = base64.b64encode(data).decode(encoding)
        path = _get_format_path(path)
        if message is None:
            message = path
        path = self._get_api(path)
        params = {
            "message": message,
            "content": data
        }
        sha = self._get_file_sha(path)
        if sha != "":
            params["sha"] = sha
        res = requests.put(path, headers=self._get_headers(), params=params)
        return res.ok

    def listdir(self, path: str = "") -> list:
        path = self._get_api(path)
        res = requests.get(path, headers=self._get_headers())
        if not res.ok:
            return list()
        res = json.loads(res.content)
        if not isinstance(res, list):
            return list()
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
