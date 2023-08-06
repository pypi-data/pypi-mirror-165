class MockSTS:

    def assume_role(self, RoleArn, **kwargs):
        return {
            'Credentials': {
                'AccessKeyId': 'AccessKeyId',
                'SecretAccessKey': 'SecretAccessKey',
                'SessionToken': 'SessionToken',
            },
            'AssumedRoleUser': {
                'AssumedRoleId': 'AssumedRoleId',
                'Arn': RoleArn
            },

        }

    def get_caller_identity(self):
        return {
            'UserId': 'UserId:Username@domain', 
            'Account': '123456789012', 
            'Arn': 'arn:aws:sts::123456789012:assumed-role/AssumedRole/Username@domain',
        }