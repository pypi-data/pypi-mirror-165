"""
Note that this file was copied from rally.__init__.py during `commit 795830af28f21f1645b8d7f2f2d4d74f34df382f <https://bitbucket.org/sdvi/monkey/commits/795830af28f21f1645b8d7f2f2d4d74f34df382f>`_
Refer to that commit for git history
"""
import posixpath
import threading
from urllib.parse import urlparse

from rally.context import _sdk_context as context, JOB_UUID, RALLY_URL, RALLY_API_TOKEN
from . import exceptions
from ._rate_limit import rate_limit
from ._vendored.requests import Session, adapters, exceptions as request_exc

_sessions = {}

# Limit API calls to 5 per second on average; larger window is more accommodating of bursts
_rate_limit_period = 10
_rate_limit_count = 50
_default_timeout = 60


class RallySession(Session):
    # You can add debug_label='RallySession' to the @rate_limit for more logging
    @rate_limit(period_seconds=_rate_limit_period, calls_per_period=_rate_limit_count)
    def request(self, method, url, *args, **kwargs):
        if not kwargs.get('timeout'):
            kwargs['timeout'] = _default_timeout

        if not url.startswith('http'):
            url = posixpath.join(context(RALLY_URL), url)

        try:
            r = super().request(method, url, *args, **kwargs)
            r.raise_for_status()
        except request_exc.HTTPError as err:
            raise exceptions.RallyApiError(err)

        return r


def _getSession():
    global _sessions

    # use existing sessions before creating others
    tid = threading.get_ident()
    session = _sessions.get(tid)
    if session:
        return session

    apiToken = context(RALLY_API_TOKEN)
    jobId = context(JOB_UUID)
    session = RallySession()
    session.mount('http://', adapters.HTTPAdapter(max_retries=3))
    session.mount('https://', adapters.HTTPAdapter(max_retries=3))
    session.headers.update({
        'X-SDVI-Client-Application': 'evaluate-{}'.format(jobId),
        'Content-Type': 'application/json'
    })
    if apiToken:
        session.headers['Authorization'] = 'Bearer {}'.format(apiToken)

    assert context(RALLY_URL), "api_root must be set"

    parsed = urlparse(context(RALLY_URL))
    if parsed.netloc == 'dev.sdvi.com':
        session.verify = False  # self-signed certificates

    _sessions[tid] = session
    return session


def _getResourceByName(resource, name):
    s = _getSession()
    if not isinstance(name, str):
        raise TypeError ("name must be string")
    resp = s.get(f'v2/{resource}', params={'filter': f'{{"name":"{name}"}}'})

    results = resp.json()['data']
    if len(results) == 0:
        raise exceptions.NotFound(f'{resource} {name}')

    if len(results) > 1:
        raise ValueError(f'ambiguous {resource} identifier {name}')

    return results[0]


def _getAssetByName(name, fullRep=False):
    result = _getResourceByName('assets', name)
    if fullRep:
        return result
    else:
        return str(result['id'])


def _nonRallyRequest(*args, **kwargs):
    """ For requests requiring a different session from Rally's.

    - Sets retry policies to 3 for http/https
    - Sets connect timeout to 60s and read timeout to 60s
    """
    if not kwargs.get('timeout'):
        kwargs['timeout'] = _default_timeout
    with Session() as s:
        s.mount('http://', adapters.HTTPAdapter(max_retries=3))
        s.mount('https://', adapters.HTTPAdapter(max_retries=3))
        return s.request(*args, **kwargs)
