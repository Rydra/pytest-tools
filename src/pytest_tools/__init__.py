from json import JSONDecodeError
from unittest.mock import MagicMock

import pytest
from funcy import rcompose, autocurry
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher


def pipe(value, *funcs):
    func = rcompose(*funcs)
    return func(value)


scenariostep = autocurry
acceptancetest = pytest.mark.acceptancetest
integrationtest = pytest.mark.integrationtest(acceptancetest)


class HasStatusCode(BaseMatcher):
    def __init__(self, status_code):
        self.status_code = status_code

    def _matches(self, item):
        try:
            return item.status_code == self.status_code
        except AttributeError:
            return False

    def describe_mismatch(self, item, mismatch_description):
        try:
            body = item.json()
        except (TypeError, JSONDecodeError):
            body = None
        message = f'{item.status_code}'
        if body:
            message += f' and the returned body was {item.json()}'
        mismatch_description.append_text('was ').append_text(message)

    def describe_to(self, description):
        description.append_text(f'status code {self.status_code} to be returned')


def has_status_code(status_code):
    return HasStatusCode(status_code)


class HasBeenCalledWith(BaseMatcher):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.mismatch_message = None

    def _matches(self, item):
        if not isinstance(item, MagicMock):
            self.mismatch_message = 'is not a mock instance'
            return False

        try:
            item.assert_any_call(*self.args, **self.kwargs)
            return True
        except AssertionError as e:
            self.mismatch_message = str(e)
            return False

    def describe_mismatch(self, item, mismatch_description):
        arg_tuple = item.call_args
        if arg_tuple:
            args, kwargs = arg_tuple
            message = 'called with '
            message += f'args: {args}, kwargs: {kwargs}'
        else:
            message = 'not called'

        mismatch_description.append_text('was ').append_text(message)

    def describe_to(self, description):
        description.append_text(
            f'called with the args: {self.args}, kwargs: {self.kwargs}')


def called_with(*args, **kwargs):
    return HasBeenCalledWith(*args, **kwargs)


@scenariostep
def then_the_response_body_is(expected_response, ctx, status_code=None):
    if status_code:
        assert_that(ctx.response, has_status_code(status_code))

    if callable(expected_response):
        expected_response = expected_response(ctx)

    if not isinstance(expected_response, Matcher):
        expected_response = is_(expected_response)

    assert_that(ctx.response.json(), expected_response)
    return ctx


@scenariostep
def then_it_should_match(value, matcher, ctx):
    if callable(matcher):
        matcher = matcher(ctx)

    if not isinstance(matcher, Matcher):
        matcher = is_(matcher)

    assert_that(value, matcher)
    return ctx

