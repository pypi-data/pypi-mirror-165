class MockRedshiftData:

    class exceptions:
        class ValidationException(Exception):
            pass

        class ExecuteStatementException(Exception):
            pass

        class ActiveStatementsExceededException(Exception):
            pass

    def execute_statement(self, ClusterIdentifier=None, Database=None, DbUser=None, SecretArn=None, **kwargs):
        self.cluster_identifier = ClusterIdentifier
        return {
            'ClusterIdentifier': ClusterIdentifier,
            'Database': Database,
            'DbUser': 'DbUser' if not DbUser else DbUser,
            'Id': 'Id',
            'SecretArn': SecretArn
        }

    def get_statement_result(self, Id=None):
        return {
            'ColumnMetadata': [
                {
                    'columnDefault': 'string',
                    'label': 'string',
                    'length': 123,
                    'name': 'string',
                    'nullable': 123,
                    'precision': 123,
                    'scale': 123,
                    'schemaName': 'string',
                    'tableName': 'string',
                    'typeName': 'string'
                },
            ],
            'NextToken': 'string',
            'Records': [
                [
                    {
                        'blobValue': b'bytes',
                        'booleanValue': True|False,
                        'doubleValue': 123.0,
                        'isNull': True|False,
                        'longValue': 123,
                        'stringValue': 'string'
                    },
                ],
            ],
            'TotalNumRows': 123
        }

    def describe_statement(self, Id=None):
        return {
            'ClusterIdentifier': self.cluster_identifier,
            'CreatedAt': 'datetime(2015, 1, 1)',
            'Database': 'string',
            'DbUser': 'string',
            'Duration': 123,
            'Error': 'string',
            'Id': Id,
            'QueryParameters': [
                {
                    'name': 'string',
                    'value': 'string'
                },
            ],
            'QueryString': 'string',
            'RedshiftPid': 123,
            'RedshiftQueryId': 123,
            'ResultRows': 123,
            'ResultSize': 123,
            'SecretArn': 'string',
            'Status': 'FINISHED', #"'SUBMITTED'|'PICKED'|'STARTED'|'FINISHED'|'ABORTED'|'FAILED'|'ALL'",
            'SubStatements': [
                {
                    'CreatedAt': 'datetime(2015, 1, 1)',
                    'Duration': 123,
                    'Error': 'string',
                    'HasResultSet': True|False,
                    'Id': 'string',
                    'QueryString': 'string',
                    'RedshiftQueryId': 123,
                    'ResultRows': 123,
                    'ResultSize': 123,
                    'Status': 'FINISHED', #"'SUBMITTED'|'PICKED'|'STARTED'|'FINISHED'|'ABORTED'|'FAILED'",
                    'UpdatedAt': 'datetime(2015, 1, 1)'
                },
            ],
            'UpdatedAt': 'datetime(2015, 1, 1)'
        }