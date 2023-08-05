from .lib2 import Crawler
import json
import os

dirname = os.path.dirname(__file__)

class CachedQuery:
    def __init__(self) -> None:
        self.cached = {}

    def loadFile(self, name: str) -> str:
        if name in self.cached:
            return self.cached[name]

        with open(os.path.join(dirname, f"queries/{name}.txt"), "r") as f:
            content = f.read()

        self.cached[name] = content

        return content

    def loadFileAsJson(self, name: str) -> str:
        content = self.loadFile(name)
        obj = json.loads(content)

        return obj

class EntryUtils:
    def __init__(self) -> None:
        self.cachedQuery = CachedQuery()
        self.cookies = None

    def postQuery(self, query: str, var):
        crawler = Crawler()

        if self.cookies:
            crawler.loadCookiesFromStr(self.cookies)

        data = crawler.postPage({
            "url": "https://playentry.org/graphql",
            "header": {
                "content-type": "application/json"
            },
            "body": json.dumps({
                "query": query,
                "variables": var
            })
        })

        self.cookies = crawler.exportCookies()

        try:
            parsed = json.loads(data)

            return {
                "status": crawler.status(),
                "data": parsed,
                "jsonParsed": True,
                "request": crawler.lastResponse.request
            }
        except:
            return {
                "status": crawler.status(),
                "data": None,
                "jsonParsed": False,
                "request": crawler.lastResponse.request
            }

        

    def postQueryPath(self, path: str, var):
        q = self.cachedQuery.loadFileAsJson(path)

        return self.postQuery(q, var)



    def createAccount(self, username: str, password: str, gender: str, nickname: str=None, email: str=None, grade: str="11", role: str="member", mobileKey: str="", passwordConfirm: str=None):
        if not passwordConfirm:
            passwordConfirm = password

        if not nickname:
            nickname = username

        return self.postQueryPath("createaccount", {
            "username": username,
            "password": password,
            "passwordConfirm": passwordConfirm,
            "role": role,
            "gender": gender,
            "mobileKey": mobileKey,
            "grade": grade,
            "email": email
        })

    def login(self, username: str, password: str, rememberme: bool=True):
        return self.postQueryPath("login", {
            "username": username,
            "password": password,
            "rememberme": rememberme
        })

    

