import boto3

class S3:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key=aws_secret_access_key
    def push(self,bucket,local_path,remote_path):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        s3 = session.resource('s3')
        s3.Bucket(bucket).upload_file(local_path, remote_path)