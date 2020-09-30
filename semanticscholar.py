'''
MIT License

Copyright (c) 2019 Daniel Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import requests
from tenacity import (retry,
                      wait_fixed,
                      retry_if_exception_type,
                      stop_after_attempt)

class SemanticScholar:

    url = 'https://api.semanticscholar.org/v1'
    auth_header = {}
    timeout = 0
    incl_unkn_refs = False

    def __init__(self, api_url=None, api_key=None, timeout=2, include_unknown_references=False):
        if not None==api_url: self.url = api_url
        if not None==api_key: self.auth_header = {'x-api-key': api_key}
        self.timeout = timeout
        self.incl_unkn_refs = include_unknown_references

    def paper(self, id, timeout=None, include_unknown_references=None) -> dict:

        '''Paper lookup

        :param str id: S2PaperId, DOI or ArXivId.
        :param float timeout: an exception is raised
            if the server has not issued a response for timeout seconds
        :param bool include_unknown_references :
            (optional) include non referenced paper.
        :returns: paper data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''
        # Default behaviour for optional arguments
        if None==timeout: timeout = self.timeout
        if None==include_unknown_references: include_unknown_references = self.incl_unkn_refs

        data = self.__get_data('paper', id, timeout, include_unknown_references)

        return data


    def author(self, id, timeout=None) -> dict:

        '''Author lookup

        :param str id: S2AuthorId.
        :param float timeout: an exception is raised
            if the server has not issued a response for timeout seconds
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''
        # Default behaviour for optional arguments
        if None==timeout: timeout = self.timeout

        data = self.__get_data('author', id, timeout, False)

        return data


    @retry(
        wait=wait_fixed(30),
        retry=retry_if_exception_type(ConnectionRefusedError),
        stop=stop_after_attempt(10)
        )
    def __get_data(self, method, id, timeout, include_unknown_references) -> dict:

        '''Get data from Semantic Scholar API

        :param str method: 'paper' or 'author'.
        :param str id: id of the correponding method
        :param float timeout: an exception is raised
            if the server has not issued a response for timeout seconds
        :returns: data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        data = {}
        method_types = ['paper', 'author']
        if method not in method_types:
            raise ValueError(
                'Invalid method type. Expected one of: {}'.format(method_types))

        url = '{}/{}/{}'.format(self.url, method, id)
        if include_unknown_references:
            url += '?include_unknown_references=true'
        r = requests.get(url, timeout=timeout, headers=self.auth_header)

        if r.status_code == 200:
            data = r.json()
            if len(data) == 1 and 'error' in data:
                data = {}
        elif r.status_code == 403:
            raise PermissionError('HTTP status 403 Forbidden.')
        elif r.status_code == 429:
            raise ConnectionRefusedError('HTTP status 429 Too Many Requests.')

        return data
