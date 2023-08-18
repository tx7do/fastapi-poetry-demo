import mimetypes
import os
import uuid
from datetime import timedelta, datetime
from typing import Union

from fastapi import HTTPException, status

from minio import Minio
from minio.datatypes import PostPolicy
from minio.deleteobjects import DeleteObject
from minio.error import S3Error

from app.configs.oss import get_oss_settings

oss_settings = get_oss_settings()


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
    client: Minio | None = None
    policy = ('{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":['
              '"s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::%s"]},{"Effect":"Allow",'
              '"Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::%s/*"]}]}')

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

    def exists_bucket(self, bucket_name):
        """ 判断桶是否存在
        :param bucket_name: 桶名称
        :return:
        """
        return self.client.bucket_exists(bucket_name=bucket_name)

    def create_bucket(self, bucket_name: str, is_policy: bool = True):
        """ 创建桶 + 赋予策略
        :param bucket_name: 桶名
        :param is_policy: 是否使用自定义策略
        :return:
        """
        if self.exists_bucket(bucket_name=bucket_name):
            return False
        else:
            self.client.make_bucket(bucket_name=bucket_name)

        if is_policy:
            policy = self.policy % (bucket_name, bucket_name)
            self.client.set_bucket_policy(bucket_name=bucket_name, policy=policy)
        return True

    def get_bucket_list(self):
        """ 列出存储桶
        :return:
        """
        buckets = self.client.list_buckets()
        bucket_list = []
        for bucket in buckets:
            bucket_list.append(
                {"bucket_name": bucket.name, "create_time": bucket.creation_date}
            )
        return bucket_list

    def remove_bucket(self, bucket_name):
        """ 删除桶
        :param bucket_name:
        :return:
        """
        try:
            self.client.remove_bucket(bucket_name=bucket_name)
        except S3Error as e:
            print("[error]:", e)
            return False
        return True

    def bucket_list_files(self, bucket_name, prefix):
        """ 列出存储桶中所有对象
        :param bucket_name: 同名
        :param prefix: 前缀
        :return:
        """
        try:
            files_list = self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True)
            for obj in files_list:
                print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
                      obj.etag, obj.size, obj.content_type)
        except S3Error as e:
            print("[error]:", e)

    def bucket_policy(self, bucket_name):
        """ 列出桶存储策略
        :param bucket_name:
        :return:
        """
        try:
            policy = self.client.get_bucket_policy(bucket_name)
        except S3Error as e:
            print("[error]:", e)
            return None
        return policy

    def download_file(self, bucket_name, file, file_path, stream=1024*32):
        """ 从bucket 下载文件 + 写入指定文件
        """
        try:
            data = self.client.get_object(bucket_name, file)
            with open(file_path, "wb") as fp:
                for d in data.stream(stream):
                    fp.write(d)
        except S3Error as e:
            print("[error]:", e)

    def fget_file(self, bucket_name, file, file_path):
        """
        下载保存文件保存本地
        :param bucket_name:
        :param file:
        :param file_path:
        :return:
        """
        self.client.fget_object(bucket_name, file, file_path)

    def copy_file(self, bucket_name, file, file_path):
        """
        拷贝文件（最大支持5GB）
        :param bucket_name:
        :param file:
        :param file_path:
        :return:
        """
        self.client.copy_object(bucket_name, file, file_path)

    def upload_file(self, bucket_name, file, file_path, content_type):
        """
        上传文件 + 写入
        :param bucket_name: 桶名
        :param file: 文件名
        :param file_path: 本地文件路径
        :param content_type: 文件类型
        :return:
        """
        try:
            with open(file_path, "rb") as file_data:
                file_stat = os.stat(file_path)
                self.client.put_object(bucket_name, file, file_data, file_stat.st_size, content_type=content_type)
        except S3Error as e:
            print("[error]:", e)

    def fput_file(self, bucket_name: str, object_name, file_path):
        """
        上传文件
        :param bucket_name: 桶名
        :param object_name: 文件名
        :param file_path: 本地文件路径
        :return:
        """
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
        except S3Error as e:
            print("[error]:", e)

    def stat_object(self, bucket_name, file):
        """
        获取文件元数据
        :param bucket_name:
        :param file:
        :return:
        """
        try:
            data = self.client.stat_object(bucket_name, file)
            print(data.bucket_name)
            print(data.object_name)
            print(data.last_modified)
            print(data.etag)
            print(data.size)
            print(data.metadata)
            print(data.content_type)
        except S3Error as e:
            print("[error]:", e)

    def remove_file(self, bucket_name, file):
        """
        移除单个文件
        :return:
        """
        self.client.remove_object(bucket_name, file)

    def remove_files(self, bucket_name, file_list):
        """
        删除多个文件
        :return:
        """
        delete_object_list = [DeleteObject(file) for file in file_list]
        for del_err in self.client.remove_objects(bucket_name, delete_object_list):
            print("del_err", del_err)

    def get_file(self, bucket_name: str, remote_obj: str):
        return self.client.get_object(bucket_name, remote_obj)

    def presigned_post_url(self, bucket_name: str, object_name: str, minutes: float = 60) -> tuple[dict[str, str | bytes], str, str]:
        """ 获取POST方法的预签名链接

        :param bucket_name: 文件桶名
        :param object_name: 文件名
        :param minutes: 有效期
        :return: 表单数据，上传链接，下载链接
        """

        policy = PostPolicy(
            bucket_name,
            datetime.utcnow() + timedelta(minutes=minutes),
        )
        policy.add_starts_with_condition("key", object_name)
        policy.add_content_length_range_condition(1 * 1024 * 1024, 10 * 1024 * 1024)

        form_data = self.client.presigned_post_policy(policy)

        upload_url = f"{oss_settings.MINIO_UPLOAD_HOST}/{bucket_name}"
        download_url = f"{oss_settings.MINIO_DOWNLOAD_HOST}/{bucket_name}/{object_name}"

        return form_data, upload_url, download_url

    def presigned_put_url(self, bucket_name: str, object_name: str, minutes: float = 60) -> tuple[str, str, str]:
        """获取PUT方法的预签名链接

         :param bucket_name: 文件桶名
         :param object_name: 文件名
         :param minutes: 有效期
         :return: 原始链接，上传链接，下载链接
         """

        url = self.client.presigned_put_object(bucket_name, object_name, expires=timedelta(minutes=minutes))

        upload_url = url.replace(
            oss_settings.MINIO_ENDPOINT, oss_settings.MINIO_UPLOAD_HOST
        )
        download_url = f"{oss_settings.MINIO_DOWNLOAD_HOST}/{bucket_name}/{object_name}"

        return url, upload_url, download_url

    def presigned_get_file(self, bucket_name: str, object_name: str, days: float = 1):
        """ 获取一个GET方法的预签名链接
        :param bucket_name: 文件桶名
        :param object_name: 文件名
        :param days: 链接有效期：天数，默认为一天。
        :return:
        """
        return self.client.presigned_get_object(bucket_name, object_name, expires=timedelta(days=days))
