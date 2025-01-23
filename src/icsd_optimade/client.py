import os

import httpx

from icsd_optimade import __version__


class ICSDClient:
    """A wrapper for the ICSD API."""

    base_url: str = "https://icsd.fiz-karlsruhe.de/api/ws"
    icsd_auth_token: str
    icsd_login_id: str | None
    icsd_login_password: str | None
    _session: httpx.Client | None = None
    _headers: dict[str, str] = {}
    _timeout: httpx.Timeout = httpx.Timeout(10.0, read=60.0)

    def __init__(self):
        self._http_client = httpx.Client
        # Check for `ICSD_LOGIN_ID` and `ICSD_LOGIN_PASSWORD` environment variables
        self.icsd_login_id = os.getenv("ICSD_LOGIN_ID")
        self.icsd_login_password = os.getenv("ICSD_LOGIN_PASSWORD")
        if not self.icsd_login_id or not self.icsd_login_password:
            raise RuntimeError(
                "No ICSD user credentials found, please set the `ICSD_LOGIN_ID` and `ICSD_LOGIN_PASSWORD` environment variables."
            )

        self.headers["User-Agent"] = f"icsd-optimade ingester/{__version__}"
        self.headers["Accepts"] = "application/json"

        auth_token = self.login()
        self.headers["icsd-auth-token"] = auth_token

    def login(self) -> str:
        """Login with user credentials and return the ICSD auth token."""
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        login_resp = self.session.post(
            f"{self.base_url}/auth/login",
            data={"loginid": self.icsd_login_id, "password": self.icsd_login_password},
            follow_redirects=True,
            headers=self.headers,
        )
        if login_resp.status_code != 200:
            raise RuntimeError(
                f"Failed to authenticate to ICSD at {self.base_url!r}: {login_resp.status_code=}. Please check your credentials."
            )
        self.headers.pop("Content-Type")
        return login_resp.headers["icsd-auth-token"]

    @property
    def session(self) -> httpx.Client:
        if self._session is None:
            return self._http_client(headers=self.headers, timeout=self.timeout)
        return self._session

    @property
    def headers(self) -> dict[str, str]:
        """Any headers to send with each request to the datalab API."""
        return self._headers

    @property
    def timeout(self) -> httpx.Timeout:
        """A timeout object to use for the datalab API session."""
        return self._timeout
