class MockMWAA:

    def create_web_login_token(self, Name=None):
        return {
            'WebServerHostname': 'WebServerHostName',
            'WebToken': 'WebToken'
        }
