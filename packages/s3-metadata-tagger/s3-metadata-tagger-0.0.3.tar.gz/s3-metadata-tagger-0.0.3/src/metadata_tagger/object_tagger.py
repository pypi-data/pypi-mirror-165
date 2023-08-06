"""
The object tagger is responsible for checking whether a file
has to be tagged, fetching it, and passing it to a supplied tagging
function
"""
from contextlib import contextmanager
import tempfile
import logging
from typing import Dict, Callable, Generator

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.type_defs import HeadObjectOutputTypeDef

s3_client = boto3.client('s3')  # type: ignore


def tag_file(key: str, bucket: str,
             extraction_function: Callable[[str], Dict[str, str]]) -> Dict[str, str]:
    """
    Returns a dictionary containing the metadata extracted by the passed `extraction_function`
    from the file found in the passed `bucket` with the passed `key`.
    """
    result = False
    retries = 0
    while not result and retries < 2:
        logging.info("Attempt %s", retries)
        object_info = _get_object_info(key, bucket)
        if _already_tagged(object_info):
            logging.info("%s in %s is already tagged", key, bucket)
            return object_info["Metadata"]
        with _download_file(key, bucket) as downloaded_file:
            custom_tags = extraction_function(downloaded_file.name)
            metadata_tags = object_info["Metadata"] | custom_tags | {
                'docu-tools-tags': "v1"}
            result = _tag_remote_file(
                key, bucket, metadata_tags, object_info["ETag"])
            retries = retries + 1
            return custom_tags
    raise RuntimeError("Could not tag file succesfully")


def _get_object_info(key: str, bucket: str) -> HeadObjectOutputTypeDef:
    return s3_client.head_object(Bucket=bucket, Key=key)


@contextmanager
def _download_file(key: str, bucket: str) -> Generator:
    with tempfile.NamedTemporaryFile() as target:
        s3_client.download_file(bucket, key, target.name)
        logging.debug("Downloaded %s from %s", key, bucket)
        yield target


def _tag_remote_file(key: str, bucket: str, metadata_tags: Dict[str, str], etag: str):
    try:
        s3_client.copy_object(Key=key,
                              Bucket=bucket,
                              CopySource={"Bucket": bucket, "Key": key},
                              Metadata=metadata_tags,
                              MetadataDirective="REPLACE",
                              CopySourceIfMatch=etag)
        logging.info("Tagged %s from %s with %s", key, bucket, metadata_tags)
        return True
    except ClientError as error:
        logging.error(error)
        return False


def _already_tagged(object_info: HeadObjectOutputTypeDef) -> bool:
    metadata = object_info['Metadata']
    return 'docu-tools-tags' in metadata
