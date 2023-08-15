import mimetypes
import uuid
from datetime import timedelta, datetime
from typing import Union

from fastapi import HTTPException, status

from minio import Minio
from minio.datatypes import PostPolicy
from minio.error import InvalidResponseError

from app.configs.oss import get_oss_settings

oss_settings = get_oss_settings()

default_expiry_time: timedelta = timedelta(minutes=60)


def content_type_to_bucket_name(content_type: str) -> str:
    h = content_type.split("/")
    if len(h) != 2:
        return "images"

    if h[0] == "image":
        return "images"
    elif h[0] == "video":
        return "videos"
    elif h[0] == "audio":
        return "audios"
    elif h[0] == "application" or h[0] == "text":
        return "docs"
    else:
        return "images"


def content_type_to_file_suffix(content_type: str) -> str:
    if content_type == "text/plain":
        return ".txt"
    elif content_type == "image/jpeg":
        return ".jpg"
    elif content_type == "image/png":
        return ".png"
    else:
        extensions = mimetypes.guess_all_extensions(content_type)
        if len(extensions) > 0:
            return extensions[0]


def joint_object_name(
    content_type: str, file_path: str, file_name: Union[str, None]
) -> (str, str):
    file_suffix = content_type_to_file_suffix(content_type)

    new_file_name: str
    if file_name is None:
        str_uuid = uuid.uuid4().__str__()
        new_file_name = f"{str_uuid}{file_suffix}"
    else:
        new_file_name = file_name

    obj_name: str
    if file_path is not None:
        obj_name = f"/{file_path}/{new_file_name}"
    else:
        obj_name = new_file_name

    return obj_name, new_file_name


class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=oss_settings.MINIO_ENDPOINT,
            access_key=oss_settings.MINIO_ACCESS_KEY,
            secret_key=oss_settings.MINIO_SECRET_KEY,
            secure=oss_settings.MINIO_SECURE,
        )

    def _exception(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    def create_bucket(self, bucket_name: str):
        if not self.client.bucket_exists(bucket_name):
            try:
                self.client.make_bucket(bucket_name)
            except Exception as err:
                print(err)

    def presigned_post_url(self, bucket_name: str, object_name: str) -> dict[str, str]:
        policy = PostPolicy(
            bucket_name,
            datetime.utcnow() + default_expiry_time,
        )
        policy.add_starts_with_condition("key", object_name)
        policy.add_content_length_range_condition(1 * 1024 * 1024, 10 * 1024 * 1024)

        form_data = self.client.presigned_post_policy(policy)

        return form_data

    def presigned_put_url(self, bucket_name: str, object_name: str) -> str:
        url = self.client.presigned_put_object(bucket_name, object_name)
        return url
