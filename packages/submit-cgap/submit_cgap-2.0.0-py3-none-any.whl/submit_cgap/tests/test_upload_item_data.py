import pytest

from dcicutils.misc_utils import ignored, override_environ
from dcicutils.s3_utils import HealthPageKey
from unittest import mock
from .. import submission as submission_module
from ..base import KeyManager
from ..scripts.upload_item_data import main as upload_item_data_main
from ..scripts import upload_item_data as upload_item_data_module
from .testing_helpers import system_exit_expected


TEST_ENCRYPT_KEY = 'encrypt-key-for-testing'


@pytest.mark.parametrize("keyfile", [None, "foo.bar"])
@pytest.mark.parametrize("mocked_s3_encrypt_key_id", [None, TEST_ENCRYPT_KEY])
def test_upload_item_data_script(keyfile, mocked_s3_encrypt_key_id):

    def test_it(args_in, expect_exit_code, expect_called, expect_call_args=None):

        with override_environ(CGAP_KEYS_FILE=keyfile):
            with mock.patch.object(upload_item_data_module,
                                   "upload_item_data") as mock_upload_item_data:
                with mock.patch.object(submission_module, "get_health_page") as mock_get_health_page:

                    mock_get_health_page.return_value = {HealthPageKey.S3_ENCRYPT_KEY_ID: mocked_s3_encrypt_key_id}

                    with system_exit_expected(exit_code=expect_exit_code):
                        # Outside of the call, we will always see the default filename for cgap keys
                        # but inside the call, because of a decorator, the default might be different.
                        # See additional test below.
                        assert KeyManager.keydicts_filename() == KeyManager.DEFAULT_KEYDICTS_FILENAME

                        def mocked_upload_item_data(*args, **kwargs):
                            ignored(args, kwargs)
                            # We don't need to test this function's actions because we test its call args below.
                            # However, we do need to run this one test from the same dynamic context,
                            # so this is close enough.
                            if KeyManager.keydicts_filename() == (keyfile or KeyManager.DEFAULT_KEYDICTS_FILENAME):
                                exit(0)
                            else:
                                # This case is not expected to be reached but must be here for testing to catch
                                exit(1)  # pragma: no cover

                        mock_upload_item_data.side_effect = mocked_upload_item_data
                        upload_item_data_main(args_in)
                        raise AssertionError("upload_item_data_main should not exit normally.")  # pragma: no cover
                    assert mock_upload_item_data.call_count == (1 if expect_called else 0)

    test_it(args_in=[], expect_exit_code=2, expect_called=False)  # Missing args
    test_it(args_in=['some.file'], expect_exit_code=0, expect_called=True, expect_call_args={
        'item_filename': 'some.file',
        'env': None,
        'server': None,
        'uuid': None,
        'no_query': False,
    })
    expect_call_args = {
        'item_filename': 'some.file',
        'env': None,
        'server': None,
        'uuid': 'some-guid',
        'no_query': False,
    }
    test_it(args_in=['-u', 'some-guid', 'some.file'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['some.file', '-u', 'some-guid'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'item_filename': 'some.file',
        'env': 'some-env',
        'server': 'some-server',
        'uuid': 'some-guid',
        'no_query': False,
    }
    test_it(args_in=['some.file', '-e', 'some-env', '--server', 'some-server', '-u', 'some-guid'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    test_it(args_in=['-e', 'some-env', '--server', 'some-server', '-u', 'some-guid', 'some.file'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
    expect_call_args = {
        'item_filename': 'some.file',
        'env': 'some-env',
        'server': 'some-server',
        'uuid': 'some-guid',
        'no_query': True,
    }
    test_it(args_in=['some.file', '-e', 'some-env', '--server', 'some-server', '-u', 'some-guid', '-nq'],
            expect_exit_code=0,
            expect_called=True,
            expect_call_args=expect_call_args)
