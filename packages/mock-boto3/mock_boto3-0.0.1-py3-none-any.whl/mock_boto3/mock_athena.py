class MockAthena:

    @staticmethod
    def start_query_execution(
        QueryString=None,
        QueryExecutioonContext=None,
        **kwargs
    ):
        return {'QueryExecutionId': 'string'}