from .mock_ssm import MockSSM

class MockDynamoDB:

    class Table:

        def __init__(self, *args):
            pass

        def put_item(*args, **kwargs):
            return {
                'Attributes': {
                    'string': 'string'
                },
                'ConsumedCapacity': {
                    'TableName': MockSSM().parameters()['LogsTable'],
                    'CapacityUnits': 5,
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                    'Table': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5,
                        'CapacityUnits': 5
                    },
                },
            }

        def get_item(*args, **kwargs):
            return kwargs

    class meta:
        class client:
            class exceptions:
                class ClientError(Exception):
                    pass
