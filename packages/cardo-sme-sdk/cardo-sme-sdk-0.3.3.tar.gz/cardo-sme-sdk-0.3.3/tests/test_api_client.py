from unittest import mock
from unittest.mock import MagicMock

import pytest

from sme_sdk import BatchCreationFailed


def test_form_url_prefix_urls_with_host(api_client):
    """
    Ensure that the form_url method prefixes the url with the host and takes
    care of the leading and trailing slashes.
    """
    assert api_client._form_url('/api/v1/login') == 'http://localhost:8080/api/v1/login'


@mock.patch('sme_sdk.api.requests.post')
def test_create_new_batch_return_response_data_at_success(
    mock_post: MagicMock,
    mock_blob_storage,
    success_response,
    api_client,
):
    """
    Ensure that the create_new_batch method accepts any blob storage.
    The only condition is that the blob storage has to implement BlobStorageClient abs class.
    """
    mock_post.return_value = success_response
    response = api_client.create_new_batch(data=None, blob_storage_client=mock_blob_storage)

    mock_post.assert_called_once()
    assert response == success_response.json()


@mock.patch('sme_sdk.api.requests.post')
def test_create_new_batch_raise_error_at_failure(
    mock_post: MagicMock,
    mock_blob_storage,
    failed_response,
    api_client,
):
    """
    Ensure that the create_new_batch method accepts any blob storage.
    The only condition is that the blob storage has to implement BlobStorageClient abs class.
    """
    mock_post.return_value = failed_response

    with pytest.raises(BatchCreationFailed):
        api_client.create_new_batch(data=None, blob_storage_client=mock_blob_storage)
