import boto3, tarfile, mimetypes

from typing import Callable
from io import BytesIO


def read_object_string(bucket: str, s3_path_file: str) -> str:
    with BytesIO(get_object(bucket, s3_path_file)['Body'].read()) as fin:
        return fin.read().decode("utf-8")


def get_object(bucket: str, s3_path_file: str):
    return boto3.resource('s3').meta.client.get_object(Bucket=bucket, Key=s3_path_file)


def upload_file(source_file: str, bucket: str, path_to_desttionation_file: str):
    mime_type, _ = mimetypes.guess_type(source_file)
    if mime_type:
        boto3.resource('s3').meta.client.upload_file(source_file, bucket, path_to_desttionation_file, ExtraArgs={'ContentType': mime_type})
    else:
        boto3.resource('s3').meta.client.upload_file(source_file, bucket, path_to_desttionation_file)


def put_dir(bucket: str, s3_path_dir: str, **kw):
    if not s3_path_dir.endswith("/"):
        raise Exception(f"`s3_path_dir` argument do not end with `/`. Got `{s3_path_dir}`")
   
    boto3.resource('s3').meta.client.put_object(Bucket=bucket, Key=s3_path_dir, **kw)


def put_string_file(bucket: str, s3_path_file: str, file_str: str, **kw):
    boto3.resource('s3').meta.client.put_object(Bucket=bucket, Key=s3_path_file, Body=file_str.encode("utf-8"), **kw)
    

def upload_tar_file_extracted_on_the_fly(tar_file: tarfile.TarFile, bucket: str, file_transfer_callback: Callable = None) -> None:
    """
    Upload a tar file and extracted on the fly

    :param tarfile.TarFile tar_file: tar file or gzip tar file
    :param str bucket: S3 bucket
    :param Callable file_transfer_callback: A method which takes a number of bytes transferred to be periodically called during the copy.
    """
    for tar_info in tar_file:
        if tar_info.isdir():
            put_dir(bucket, f"{tar_info.name[2:]}/") # "./build/assets/"

        else:
            mime_type, _ = mimetypes.guess_type(tar_info.name)
            if mime_type:
                boto3.resource('s3').meta.client.upload_fileobj(
                    Fileobj=BytesIO(tar_file.extractfile(tar_info).read()),
                    Bucket=bucket,
                    Key=tar_info.name[2:], # "./build/assets/temp7.png"
                    Callback=file_transfer_callback,
                    ExtraArgs={'ContentType': mime_type}
                )
            else:
                boto3.resource('s3').meta.client.upload_fileobj(
                    Fileobj=BytesIO(tar_file.extractfile(tar_info).read()),
                    Bucket=bucket,
                    Key=tar_info.name[2:], # "./build/assets/temp7.png"
                    Callback=file_transfer_callback
                )


def download_file(desttionation_file: str, bucket: str, path_to_source_file: str):
    boto3.resource('s3').meta.client.download_file(bucket, path_to_source_file, desttionation_file)


def empty_bucket(bucket: str):
    # S3:DeleteObject
    # S3:DeleteObjectVersion
    s3 = boto3.resource('s3')
    bucket_versioning = s3.BucketVersioning(bucket)
    if bucket_versioning.status == 'Enabled':
        return s3.Bucket(bucket).object_versions.delete()
    else:
        return s3.Bucket(bucket).objects.all().delete()


def list(bucket: str, s3_path_file: str) -> list[str]:
    response = boto3.resource('s3').meta.client.list_objects_v2(Bucket=bucket, Prefix=s3_path_file)
    if response["KeyCount"] == 0:
        return []
    return [x["Key"] for x in response["Contents"]]


def is_file_existed(bucket: str, s3_path_file: str) -> bool:
    results = list(bucket, s3_path_file)
    if len(results) > 1:
        raise Exception(f"There are results when list S3 bucket `{bucket}` with prefix `{s3_path_file}`")
    elif len(results) == 1:
        if results[0] != s3_path_file:
            raise Exception(f"Find a result `{results[0]}` with different key when list S3 bucket `{bucket}` with prefix `{s3_path_file}`")
        return True
    else:
        return False


def wait_until_file_existed(bucket: str, s3_path_file: str, wait_times: int, wait_interval):
    waiter = boto3.resource('s3').meta.client.get_waiter('object_exists')
    waiter.wait(
        Bucket=bucket,
        Key=s3_path_file,
        WaiterConfig={
            "Delay": wait_interval,
            "MaxAttempts": wait_times
        }
    )
