class MockConfig:

    def put_evaluations(self, Evaluations=None, **kwargs):
        return {
            'FailedEvaluations': [
                {
                    'ComplianceResourceType': item['ComplianceResourceType'],
                    'ComplianceResourceId': item['ComplianceResourceId'],
                    'ComplianceType': 'NON_COMPLIANCE', # 'COMPLIANT'|'NON_COMPLIANT'|'NOT_APPLICABLE'|'INSUFFICIENT_DATA',
                    'Annotation': 'Annotation',
                    'OrderingTimestamp': item['OrderingTimestamp']
                } for item in Evaluations
            ]
        }