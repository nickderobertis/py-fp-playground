from typing import TypedDict

import requests
from returns.io import IOResult, impure_safe
from returns.result import safe
from returns.pipeline import flow
from returns.pointfree import bind_result

class UserProfile(TypedDict):
    pass


def fetch_user_profile(user_id: int) -> IOResult['UserProfile', Exception]:
    """Fetches `UserProfile` TypedDict from foreign API."""
    woo = _make_request(2).bind_result(_parse_json)

    res = flow(
        user_id,
        _make_request,
        # before: def (Response) -> UserProfile
        # after safe: def (Response) -> ResultE[UserProfile]
        # after bind_result: def (IOResultE[Response]) -> IOResultE[UserProfile]
        bind_result(_parse_json),
    )
    return res

@impure_safe
def _make_request(user_id: int) -> requests.Response:
    response = requests.get('/api/users/{0}'.format(user_id))
    response.raise_for_status()
    return response

@safe
def _parse_json(response: requests.Response) -> 'UserProfile':
    return response.json()