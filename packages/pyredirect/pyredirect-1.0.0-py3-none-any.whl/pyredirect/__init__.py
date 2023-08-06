from requests import request as _request
from re import match as _match

API_BASE_URL = "https://redirect.lactua.repl.co"

def _is_url(text):
    return bool(_match(
        r"(https?|ftp)://" 
        r"(\w+(\-\w+)*\.)?" 
        r"((\w+(\-\w+)*)\.(\w+))" 
        r"(\.\w+)*" 
        r"([\w\-\._\~/]*)*(?<!\.)" 
    , text))

def _api(
        method,
        endpoint,
        headers={},
        json={}
    ):
    return _request(
        method,
        API_BASE_URL+endpoint,
        headers=headers,
        json=json
    )

class Redirection:

    def __init__(
        self,
        name,
        secret_key
    ) -> None:
        resp = _api('GET', f'/get/{name}', json={'secret_key':secret_key})

        if resp.status_code != 200:
            raise Exception("Invalid redirection")

        json = resp.json()

        self.name = name
        self.redirections = json['redirections']
        self.url = API_BASE_URL+'/redirect/'+name
        self.secret_key = secret_key

    def create(
        name: str,
        redirections: dict
    ):
        if len(name) < 1 or len(name) > 20:
            raise Exception("Redirection name length must be at least 1 and below 20")
        
        if not 'default' in list(redirections.keys()):
            raise Exception("Redirections must contain a default redirection")

        if not all(_is_url(url) for url in redirections.values()):
            raise Exception("Redirections url must respect the format of an URL")

        resp = _api('POST', '/new', json={'name':name,'redirections':redirections})

        if resp.text == "the redirection name already exists.":
            raise Exception("Redirection name already exists")

        json = resp.json()

        url = json['url']
        secret_key = json['secret_key']

        return Redirection(
            name,
            secret_key
        )

    def delete(self) -> None:
        _api('DELETE', f'/delete/{self.name}', json={'secret_key': self.secret_key})