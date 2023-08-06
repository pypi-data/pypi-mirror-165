from os import listdir

class MockPaginator:

    def get_s3_keys(self, Prefix):
        try:
            return listdir(Prefix)
        except FileNotFoundError:
            return listdir(f'tests/{Prefix}')

    def paginate(self, Bucket=None, Prefix=None):
        return (
            {
                'Contents': [
                    {
                        'Key': filename,
                        'LastModified': 'datetime(2015, 1, 1)',
                        'ETag': 'string',
                        'Size': 123,
                        'StorageClass': "'STANDARD'|'REDUCED_REDUNDANCY'|'GLACIER'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'DEEP_ARCHIVE'|'OUTPOSTS'",
                        'Owner': {
                            'DisplayName': 'string',
                            'ID': 'string'
                        }
                    }
                ]
            }
            for filename in self.get_s3_keys(Prefix)
        )
