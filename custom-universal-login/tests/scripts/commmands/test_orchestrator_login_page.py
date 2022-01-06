from unittest import mock

from botocore.exceptions import ClientError

from scripts.commands import orchestrator_login_page
from scripts.commands import settings
from scripts.commands.auth0_handler import management_api
from scripts.commands.orchestrator_login_page import main
from scripts.commands.orchestrator_login_page import retrieve_bucket
from scripts.commands.orchestrator_login_page import retrieve_static_files
from tests.scripts.commmands.helper import BaseTestCase


class HandlerTests(BaseTestCase):
    def test_should_retrieve_static_files(self):
        # Arrange comment: You must have created the out files from parcel! Run "npm run build" prior test execution
        # Act
        static_files = retrieve_static_files("out", "login.*")
        # Assert
        assert static_files.js_file
        assert static_files.css_file
        assert static_files.html_file

    def test_should_retrieve_bucket(self):
        # Act
        bucket = retrieve_bucket(self.s3, settings.BUCKET_NAME)
        # Assert
        assert bucket.creation_date

    @mock.patch.object(management_api, "update_login_page_classic", wraps=management_api.update_login_page_classic)
    @mock.patch.object(orchestrator_login_page, "upload_file", wraps=orchestrator_login_page.upload_file)
    @mock.patch.object(orchestrator_login_page, "retrieve_bucket", wraps=orchestrator_login_page.retrieve_bucket)
    @mock.patch("scripts.commands.orchestrator_login_page.boto3")
    def test_should_upload_static_files(
        self, mocked_boto3, wrapped_retrieve_bucket, wrapped_upload_file, wrapped_auth0
    ):
        # Arrange
        mocked_boto3.resource.return_value = self.s3
        # Act
        main()
        # Assert
        self.bucket, _, css_file_key = wrapped_upload_file.call_args_list[0][0]
        _, _, js_file_key = wrapped_upload_file.call_args_list[1][0]
        assert wrapped_upload_file.call_count == 2
        wrapped_retrieve_bucket.assert_called_with(self.s3, self.bucket_name)
        wrapped_auth0.assert_called_once()
        assert self._object_exist(self.bucket.Object(css_file_key))
        assert self._object_exist(self.bucket.Object(js_file_key))

    def _object_exist(self, bucket_object):
        try:
            if bucket_object.last_modified:
                return True
        except ClientError as e:
            if e.response["Error"]["Message"] == "Not Found":
                return False
            else:
                raise e
