import pytest


@pytest.fixture
def request_loader(shared_datadir, datadir):
    def get_filecontents(request_filename):
        if '.graphql' not in request_filename:
            request_filename = request_filename + '.graphql'

        try:
            return (datadir / f'requests/{request_filename}').read_text()
        except FileNotFoundError:
            return (shared_datadir / f'requests/{request_filename}').read_text()

    return get_filecontents
