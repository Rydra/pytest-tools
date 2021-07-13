import pytest


@pytest.fixture
def request_loader(datadir):
    def get_filecontents(request_filename):
        if '.graphql' not in request_filename:
            request_filename = request_filename + '.graphql'

        return (datadir / f'requests/{request_filename}').read_text()

    return get_filecontents


@pytest.fixture
def shared_request_loader(shared_datadir):
    def get_filecontents(request_filename):
        if '.graphql' not in request_filename:
            request_filename = request_filename + '.graphql'

        return (shared_datadir / f'requests/{request_filename}').read_text()

    return get_filecontents
