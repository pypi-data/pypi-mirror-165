import json

class MockSecretsManager:

    def get_secret_value(self, SecretId=None):
        return json.dumps({
            'SecretString': {
                'username': 'username',
                'password': 'password',
                'host': 'host',
                'port': 'port'
            }
        })
