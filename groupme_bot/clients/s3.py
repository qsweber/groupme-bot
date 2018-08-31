import boto3
import botocore


class S3Client():
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def _get_file_obj(self, bucket, key):
        return self.s3.Object(bucket, key)

    def get_file_updated_at(self, bucket, key):
        try:
            return self._get_file_obj(bucket, key).last_modified
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return None
            else:
                raise

    def get_file_contents(self, bucket, key):
        obj = self._get_file_obj(bucket, key)

        return obj.get()['Body'].read()
