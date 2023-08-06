import requests
from carehttp import check_suffix
from carehttp.user_agents import get_user_agent
from requests.exceptions import *
from retrying import retry
from loguru import logger


def _retry_if_err(exception, cls):
    """Return True if we should retry, False otherwise."""
    if cls.mark:
        obj = cls.mark
    else:
        obj = cls.url  # what object does it for

    logger.error(f'{obj} {cls.fetch_type.upper()} attempt{cls.attempt} ERR: {exception}')

    # What kind of requests error we retry
    err_types = [
        HTTPError,
        ConnectionError,
        ProxyError,
        SSLError,
        Timeout,
        ConnectTimeout,
        ReadTimeout,
    ]
    for t in err_types:
        if isinstance(exception, t):
            return True


class Carehttp:
    def __init__(self, session=None, mark=None, tries=5, delay=1, max_delay=30, random_ua=False):
        self.session = session
        self.mark = mark  # Could be title, target name, but not url
        self.attempt = 0
        self.method = None
        self.url = None
        self.random_ua = random_ua  # Whether to use random useragent

        # retry setting
        self.tries = tries
        self.delay = delay * 1000
        self.max_delay = max_delay * 1000

        # Decorate functions to be retried
        retry_decorator = retry(
            stop_max_attempt_number=self.tries,  # retry times
            wait_exponential_multiplier=self.delay,  # Wait 2^x * 1000 milliseconds between each retry
            wait_exponential_max=self.max_delay,
            retry_on_exception=lambda exc: _retry_if_err(exc, self),
        )

        self.get = retry_decorator(self.get)
        self.post = retry_decorator(self.post)

    def _req(self, method, url, **kwargs):
        self.url = url
        self.attempt += 1  # requests attempt times

        self._log_type(url, method)

        self.set_random_useragent(kwargs)

        response = None
        try:
            if self.session:
                response = self.session.request(method, url, **kwargs)
            else:
                response = requests.request(method, url, **kwargs)
            return response
        except Exception as e:
            raise e
        finally:
            response and response.close()

    def get(self, url, params=None, **kwargs):
        return self._req('get', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self._req('post', url, data=data, json=json, **kwargs)

    def set_random_useragent(self, kwargs_dict):
        """Set useragent to headers"""
        if self.random_ua:
            if 'headers' in kwargs_dict:
                if isinstance(kwargs_dict['headers'], dict):
                    kwargs_dict['headers']['user-agent'] = get_user_agent()
            else:
                kwargs_dict['headers'] = {
                    'user-agent': get_user_agent()
                }

    def _log_type(self, url, method):
        """Change fetch type"""
        suffix_type = check_suffix.check_type(url)
        if suffix_type:
            self.fetch_type = suffix_type
        else:
            self.fetch_type = method


if __name__ == '__main__':
    headers = {
        'xxx': 'xxx'
    }
    s = requests.Session()
    # r = Carehttp(session=s, mark='title').get(url='https://media.architecturaldigest.com/photos/62816958c46d4bf6875e71ff/master/pass/Gardening%20mistakes%20to%20avoid.jpg', timeout=0.1)
    r = Carehttp(session=s, mark='title', random_ua=True).get(url='https://media.architecturaldigest.com/photos/62816958c46d4bf6875e71ff/master/pass/Gardening%20mistakes%20to%20avoid.jpg', headers=headers, timeout=2)
    print(r.text)
