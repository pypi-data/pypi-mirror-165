import requests, json, re, datetime

validURL = ["https://playentry.org/graphql", "https://playentry.org/rest/picture"]

def checkPostOptions(options):
    if "url" in options:
        url = options["url"].strip()
        if url not in validURL:
            return [False, "Url argument is not a valid graphql link"]
        else:
            if "header" not in options:
                return [False, "Missing header argument"]
            elif "body" not in options:
                return [False, "Missing body argument"]
            else:
                return [True, ""]
    else:
        return [False, "Missing url argument"]

class CSRF:
    content = None
    time = datetime.datetime.now().timestamp()
    bot = requests.session()
    cookies = bot.cookies

    @staticmethod
    def getCSRFToken(strict=True):
        if (not CSRF.content) or datetime.datetime.now().timestamp() - CSRF.time > 3600 or strict: # 1시간마다
            CSRF.time = datetime.datetime.now().timestamp()
            pl = CSRF.bot.get("https://playentry.org/").text
            s = re.search(r"<meta name=\"csrf-token\" content=\"(.*?)\"/>", pl)
            if s:
                CSRF.content = s.group(1)
            else:
                CSRF.content = None
            return CSRF.content
        else:
            return CSRF.content

    @staticmethod
    def getcsrfcookie():
        CSRF.cookies = CSRF.bot.cookies
        return CSRF.cookies.get("_csrf", "")

class Crawler:
    def __init__(self) -> None:
        self.bot = requests.session()
        self.cookies = self.bot.cookies
        self.used = False
        self.lastStatus = 200
        self.lastResponse = False

    def postPage(self, options: dict, d401=False):
        if self.used == True:
            raise Exception("The current crawler is already used. Create a new crawler.")
        else:
            check = checkPostOptions(options)

            headers = dict(options["header"])
            if "csrf" in options:
                d = options["csrf"]
            else:
                d = self.getCSRFToken(strict=False)

            headers["csrf-token"] = d

            if check[0] == False:
                raise Exception(check[1])
            if d401:
                res = self.bot.post(options["url"], options["body"], headers=headers)
            else:
                res = self.bot.post(options["url"], options["body"], headers=headers)

            self.lastResponse = res
            self.lastStatus = res.status_code
            self.cookies = self.bot.cookies
            return res.text
    
    def saveCookies(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump(requests.utils.dict_from_cookiejar(self.cookies), f)

    def loadCookies(self, filename: str) -> None:
        with open(filename, 'r') as f:
            cookies = requests.utils.cookiejar_from_dict(json.load(f))
            self.bot.cookies.update(cookies)

    def exportCookies(self) -> str:
        return json.dumps(requests.utils.dict_from_cookiejar(self.cookies))

    def loadCookiesFromStr(self, s: str):
        cookies = requests.utils.cookiejar_from_dict(json.loads(s))
        self.bot.cookies.update(cookies)

    def status(self):
        return self.lastStatus

    def getCSRFToken(self, strict=True):
        token = CSRF.getCSRFToken(strict=strict)
        self.cookies.set("_csrf", CSRF.getcsrfcookie())
        return token

