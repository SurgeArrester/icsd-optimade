import os

import pytest

from icsd_optimade.client import ICSDClient


def test_login_credentials():
    if not os.getenv("ICSD_LOGIN_ID") or not os.getenv("ICSD_LOGIN_PASSWORD"):
        pytest.skip("No ICSD credentials set.")

    assert ICSDClient().login()
