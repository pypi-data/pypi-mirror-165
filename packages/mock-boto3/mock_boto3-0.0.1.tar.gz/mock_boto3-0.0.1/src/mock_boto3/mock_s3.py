import os
import pathlib

from .mock_paginator import MockPaginator
from .mock_waiter import MockWaiter

class MockS3Object:

    def __init__(self, Key=None, Bucket=None):
        self.key = f'tests/{Key}'
        self.bucket = Bucket

    def get_local_object(self, key):
        with open(key, 'rb') as file:
            return file.read()

    def read(self):
        try:
            return self.get_local_object(self.key)
        except FileNotFoundError:
            return self.get_local_object(f"tests/{self.key}")


class MockS3:

    @staticmethod
    def get_object(Bucket, Key):
        return dict(Body=MockS3Object(Bucket=Bucket, Key=Key))

    @staticmethod
    def put_object(Key=None, Body=None, **kwargs):
        try:
            os.makedirs(f"tests/{pathlib.Path(Key).parent}")
        except FileExistsError:
            print(f"Folder: tests/{pathlib.Path(Key).parent} Exists")
        with open(f"tests/{Key}", "w") as file:
            file.write(Body)
        return {
            'ResponseMetadata': {
                'HTTPStatusCode': 200
            }
        }

    @staticmethod
    def get_waiter(*args):
        return MockWaiter()

    @staticmethod
    def head_object(Key=None, **kwargs):
        try:
            return dict(ContentLength=os.path.getsize(f"tests/{Key}"))
        except FileNotFoundError:
            return dict(ContentLength=os.path.getsize(Key))

    @staticmethod
    def get_paginator(action):
        return MockPaginator()

    @staticmethod
    def get_bucket_versioning(Bucket):
        return dict(Status='Enabled', MFADelete='Disabled')

    @staticmethod
    def get_bucket_location(Bucket):
        return {'LocationConstraint': 'region'}

    @staticmethod
    def get_bucket_encryption(Bucket):
        return {
            'ServerSideEncryptionConfiguration': {
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID': 'KmsKeyId'
                        },
                        'BucketKeyEnabled': True
                    },
                ]
            }
        }

    @staticmethod
    def get_bucket_tagging(Bucket):
        return {
            'TagSet': [
                {'Key': f'Key{number}', 'Value': f'Value{number}'}
                for number in range(1, 5)
            ]
        }

    @staticmethod
    def get_public_access_block(Bucket):
        return {
            'PublicAccessBlockConfiguration': {
                'BlockPublicAcls': True|False,
                'IgnorePublicAcls': True|False,
                'BlockPublicPolicy': True|False,
                'RestrictPublicBuckets': True|False
            }
        }

    @staticmethod
    def get_bucket_policy(Bucket):
        return {
            "Id": "ExamplePolicy",
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowSSLRequestsOnly",
                    "Action": "s3:*",
                    "Effect": "Deny",
                    "Resource": [
                        "arn:aws:s3:::DOC-EXAMPLE-BUCKET",
                        "arn:aws:s3:::DOC-EXAMPLE-BUCKET/*"
                    ],
                    "Condition": {
                        "Bool": {
                            "aws:SecureTransport": "false"
                        }
                    },
                    "Principal": "*"
                }
            ]
        }

    @staticmethod
    def get_bucket_logging(Bucket):
        return {
            'LoggingEnabled': {
                'TargetBucket': 'string',
                'TargetGrants': [
                    {
                        'Grantee': {
                            'DisplayName': 'string',
                            'EmailAddress': 'string',
                            'ID': 'string',
                            'Type': 'CanonicalUser',
                            'URI': 'URI'
                        },
                        'Permission': 'READ'
                    },
                ],
                'TargetPrefix': 'string'
            }
        }

    @staticmethod
    def get_object_lock_configuration(Bucket):
        return {
            'ObjectLockConfiguration': {
                'ObjectLockEnabled': 'Enabled',
                'Rule': {
                    'DefaultRetention': {
                        'Mode': 'COMPLIANCE',
                        'Days': 123,
                        'Years': 123
                    }
                }
            }
        }

    @staticmethod
    def get_bucket_notification_configuration(Bucket):
        return {
            'TopicConfigurations': [
                {
                    'Id': 'string',
                    'TopicArn': 'TopicArn',
                    'Events': [
                        's3:ObjectCreated:*','s3:ObjectCreated:Put','s3:ObjectCreated:CompleteMultipartUpload',
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'prefix',
                                    'Value': 'string'
                                },
                            ]
                        }
                    }
                },
            ],
            'QueueConfigurations': [
                {
                    'Id': 'string',
                    'QueueArn': 'QueueArn',
                    'Events': [
                        's3:ObjectCreated:*','s3:ObjectCreated:Put','s3:ObjectCreated:CompleteMultipartUpload',
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': 'string'
                                },
                            ]
                        }
                    }
                },
            ],
            'LambdaFunctionConfigurations': [
                {
                    'Id': 'string',
                    'LambdaFunctionArn': 'LambdaFunctionArn',
                    'Events': [
                        's3:ObjectCreated:*','s3:ObjectCreated:Put','s3:ObjectCreated:CompleteMultipartUpload',
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': 'string'
                                },
                            ]
                        }
                    }
                },
            ],
            'EventBridgeConfiguration': {}
        }

    class exceptions:
        class NoSuchKey(Exception):
            pass
