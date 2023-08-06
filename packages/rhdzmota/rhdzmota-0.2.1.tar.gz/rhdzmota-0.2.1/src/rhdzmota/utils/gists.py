import time
from typing import Optional

import requests


class Gist:
    URL_TEMPLATE = "https://gist.githubusercontent.com/{username}/{gist_id}/raw/{commit}/{filename}"

    def __init__(self, username: str, gist_id: str, filename: str, commit: Optional[str] = None):
        self.username = username
        self.gist_id = gist_id
        self.filename = filename
        self.commit = commit

    @property
    def url(self) -> str:
        return self.URL_TEMPLATE.format(
            username=self.username,
            gist_id=self.gist_id,
            filename=self.filename,
            commit=self.commit or ""
        )

    def get_code(self) -> str:
        response = requests.get(url=self.url)
        return response.text

    def load(self):
        # Retrieve the code snippet
        code_snippet = self.get_code()
        # Define the user namespace
        try:
            import IPython

            user_ns = getattr(IPython.get_ipython(), 'user_ns', globals())
        except ImportError:
            user_ns = {**locals(), **globals()}
        # Execute the snippet
        exec(compile(code_snippet, f"{int(time.time())}", "exec"), user_ns, user_ns)
