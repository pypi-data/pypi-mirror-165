from .mock_paginator import MockPaginator
class MockLambda(object):

    class Paginator():

        @staticmethod
        def paginate():
            return {
                'Functions': [
                    {
                        'FunctionName': 'FunctionName',
                        'FunctionArn': f'arn:aws:lambda:REGION:123456789012:function:FunctionName',
                        'Runtime': 'python3.7',
                        'Role': f'arn:aws:iam::123456789012:role/FunctionName',
                        'Handler': f'FunctionName.handler',
                        'CodeSize': 1234,
                        'Description': 'Description',
                        'Timeout': 123,
                        'MemorySize': 123,
                        'LastModified': '1900-12-12T12:59:59.657+0000',
                        'CodeSha256': 'ABCabCaa0bAbCABcABCaBc1ABcABcaBCA01ABCaBcAB=',
                        'Version': '$LATEST',
                        'VpcConfig': {
                            'SubnetIds': [
                                'subnet-01234ab0c56d7890d',
                                'subnet-01234ab0c56d7890d',
                                'subnet-01234ab0c56d7890d',
                                'subnet-01234ab0c56d7890d',
                            ],
                            'SecurityGroupIds': [
                                'sg-012a34b56def78901',
                                'sg-012a34b56def78901',
                                'sg-012a34b56def78901',
                                'sg-012a34b56def78901',
                            ],
                            'VpcId': 'vpc-1a23456a123a456bd'
                        },
                        'TracingConfig': {'Mode': 'PassThrough'},
                        'RevisionId': 'fba95d87-de7b-4a20-99d1-5fe4780acdc7',
                        'KMSKeyArn': 'arn:aws:kms:REGION:123456789012:key/12ab3456-c789-0123-45d6-78e9f0a12bcd'
                    },
                ],
                'NextToken': 'NextToken'
            }

    def get_paginator(self, action):
        return self.Paginator()

    @staticmethod
    def get_function(FunctionName=None, **kwargs):
        return {
            "ResponseMetadata": None,
            "Configuration": {
                "FunctionName": FunctionName,
                "FunctionArn": f"arn:aws:lambda:REGION:123456789012:function:{FunctionName}",
                "Runtime": "python3.8",
                "Role": f'arn:aws:iam::123456789012:role/{FunctionName}',
                "Handler": f'{FunctionName}.handler',
                "CodeSize": 1234,
                "Description": 'Description',
                "Timeout": 123,
                "MemorySize": 123,
                "LastModified": '1900-12-12T12:59:59.657+0000',
                "CodeSha256": 'ABCabCaa0bAbCABcABCaBc1ABcABcaBCA01ABCaBcAB=',
                "Version": "$LATEST",
                "TracingConfig": {
                    "Mode": "PassThrough"
                },
                "RevisionId": 'fba95d87-de7b-4a20-99d1-5fe4780acdc7',
                "State": "Active",
                "LastUpdateStatus": "Successful",
                "PackageType": "Zip",
                "Architectures": [
                    "x86_64"
                ]
            },
            "Code": {
                "RepositoryType": "S3",
                "Location": 'url'
            },
            "Tags": {
                "key1": "value1",
                "key2": "value2",
                "key3": "value3",
                "keyN": "valueN",
            }
        }