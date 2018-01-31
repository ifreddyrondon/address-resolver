"""
Core client functionality, common across requests.
"""

import collections
import random
import requests
import time

from datetime import datetime
from datetime import timedelta

RETRIABLE_STATUSES = {500, 503, 504}


class AbstractRestClient:
    """Performs requests to APIs services."""

    def __init__(self, base_url,
                 timeout=None, connect_timeout=None, read_timeout=None, retry_timeout=60,
                 queries_per_second=10,
                 requests_kwargs=None):
        """
        :param base_url: base url to perform requests
        :type base_url: string

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify "None" for no timeout.
        :type timeout: int

        :param connect_timeout: Connection timeout for HTTP requests, in
            seconds. You should specify read_timeout in addition to this option.
            Note that this requires requests >= 2.4.0.
        :type connect_timeout: int

        :param read_timeout: Read timeout for HTTP requests, in
            seconds. You should specify connect_timeout in addition to this
            option. Note that this requires requests >= 2.4.0.
        :type read_timeout: int

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int

        :param queries_per_second: Number of queries per second permitted.
            If the rate limit is reached, the client will sleep for the
            appropriate amount of time before it runs the current query.
        :type queries_per_second: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. See the official requests docs for more info:
            http://docs.python-requests.org/en/latest/api/#main-interface
        :type requests_kwargs: dict

        """

        self.session = requests.Session()

        if timeout and (connect_timeout or read_timeout):
            raise ValueError("Specify either timeout, or connect_timeout "
                             "and read_timeout")

        if connect_timeout and read_timeout:
            self.timeout = (connect_timeout, read_timeout)
        else:
            self.timeout = timeout

        self.retry_timeout = timedelta(seconds=retry_timeout)
        self.requests_kwargs = requests_kwargs or {}
        self.requests_kwargs.update({
            "timeout": self.timeout,
        })

        self.queries_per_second = queries_per_second
        self.sent_times = collections.deque("", queries_per_second)

        self.base_url = base_url

    def _request(self, url, method="get", first_request_time=None, retry_counter=0, requests_kwargs=None):
        """Performs HTTP GET/POST.

        :param url: URL path for the request. Should begin with a slash.
        :type url: string

        :param method: HTTP method name, support get and post.
        :type method: string

        :param first_request_time: The time of the first request (None if no
            retries have occurred).
        :type first_request_time: datetime.datetime

        :param retry_counter: The number of this retry, or zero for first attempt.
        :type retry_counter: int

        :raises ApiError: when the API returns an error.
        :raises Timeout: if the request timed out.
        :raises TransportError: when something went wrong while trying to
            exceute a request.
        """

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > self.retry_timeout:
            raise ValueError("timeout")

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=0. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 0.5 * 1.5 ** (retry_counter - 1)

            # Jitter this value by 50% and pause.
            time.sleep(delay_seconds * (random.random() + 0.5))

        requests_kwargs = requests_kwargs or {}
        final_requests_kwargs = dict(self.requests_kwargs, **requests_kwargs)

        try:
            response = self.session.request(method, url, **final_requests_kwargs)
        except requests.exceptions.Timeout:
            raise ValueError("timeout")

        if response.status_code in RETRIABLE_STATUSES:
            return self._request(url, first_request_time, retry_counter + 1, requests_kwargs)

        # Check if the time of the nth previous query (where n is
        # queries_per_second) is under a second ago - if so, sleep for
        # the difference.
        if self.sent_times and len(self.sent_times) == self.queries_per_second:
            elapsed_since_earliest = time.time() - self.sent_times[0]
            if elapsed_since_earliest < 1:
                time.sleep(1 - elapsed_since_earliest)

        self.sent_times.append(time.time())
        return response

    def _get_request_uri(self, partial_uri=""):
        if partial_uri.startswith("http"):
            return partial_uri

        return "{}{}".format(self.base_url, partial_uri)

    def get(self, uri, params=None, headers=None):
        requests_kwargs = {"params": params or {}, "headers": headers or {}}
        url = self._get_request_uri(uri)
        return self._request(url, "get", requests_kwargs=requests_kwargs)

    def post(self, uri, data=None, headers=None):
        requests_kwargs = {"json": data or {}, "headers": headers or {}}
        url = self._get_request_uri(uri)
        return self._request(url, "post", requests_kwargs=requests_kwargs)
