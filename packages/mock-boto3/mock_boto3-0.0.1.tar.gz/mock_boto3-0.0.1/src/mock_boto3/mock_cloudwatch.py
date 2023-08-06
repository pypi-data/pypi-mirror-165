import datetime


class MockCloudWatch(object):

    class MockPaginator:

        @staticmethod
        def paginate():
            return {
                'CompositeAlarms': [
                    {
                        'ActionsEnabled': True,
                        'AlarmActions': [
                            'string',
                        ],
                        'AlarmArn': 'AlarmArn',
                        'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2015, 1, 1),
                        'AlarmDescription': 'AlarmDescription',
                        'AlarmName': 'AlarmName',
                        'AlarmRule': 'AlarmRule',
                        'InsufficientDataActions': [
                            'InsufficientDataActions',
                        ],
                        'OKActions': [
                            'OKActions',
                        ],
                        'StateReason': 'string',
                        'StateReasonData': 'string',
                        'StateUpdatedTimestamp': datetime.datetime(2015, 1, 1),
                        'StateValue': 'OK'
                    },
                ],
                'MetricAlarms': [
                    {
                        'AlarmName': 'AlarmName',
                        'AlarmArn': 'AlarmArn',
                        'AlarmDescription': 'AlarmDescription',
                        'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2015, 1, 1),
                        'ActionsEnabled': True,
                        'OKActions': [
                            'OKAction1',
                            'OKActionN',
                        ],
                        'AlarmActions': [
                            'AlarmAction1',
                            'AlarmActionN',
                        ],
                        'InsufficientDataActions': [
                            'InsufficientDataAction1',
                            'InsufficientDataActionN',
                        ],
                        'StateValue': 'OK',
                        'StateReason': 'string',
                        'StateReasonData': 'string',
                        'StateUpdatedTimestamp': datetime.datetime(2015, 1, 1),
                        'MetricName': 'string',
                        'Namespace': 'string',
                        'Statistic': 'Sum',
                        'ExtendedStatistic': 'string',
                        'Dimensions': [
                            {
                                'Name': 'Dimension1',
                                'Value': 'Value1'
                            },
                            {
                                'Name': 'Dimension2',
                                'Value': 'Value2'
                            },
                        ],
                        'Period': 123,
                        'Unit': 'Bits',
                        'EvaluationPeriods': 123,
                        'DatapointsToAlarm': 123,
                        'Threshold': 123.0,
                        'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
                        'TreatMissingData': 'string',
                        'EvaluateLowSampleCountPercentile': 'string',
                        'Metrics': [
                            {
                                'Id': 'MetricId',
                                'MetricStat': {
                                    'Metric': {
                                        'Namespace': 'Namespace',
                                        'MetricName': 'MetricName',
                                        'Dimensions': [
                                            {
                                                'Name': 'Dimension1',
                                                'Value': 'Value1'
                                            },
                                            {
                                                'Name': 'DimensionN',
                                                'Value': 'ValueN'
                                            },
                                        ]
                                    },
                                    'Period': 123,
                                    'Stat': 'string',
                                    'Unit': 'Seconds'
                                },
                                'Expression': 'Expression',
                                'Label': 'Label',
                                'ReturnData': True,
                                'Period': 123,
                                'AccountId': 'AccountId'
                            },
                        ],
                        'ThresholdMetricId': 'string'
                    },
                ],
            }

    @staticmethod
    def get_metric_statistics(Unit=None, **kwargs):
        return {
            'Label': 'string',
            'Datapoints': [
                {
                    'Timestamp': datetime.datetime(2015, 1, 1),
                    'SampleCount': 123.0,
                    'Average': 123.0,
                    'Sum': 123.0,
                    'Minimum': 123.0,
                    'Maximum': 123.0,
                    'Unit': Unit,
                    'ExtendedStatistics': {
                        'string': 123.0
                    }
                },
            ]
        }


    def get_paginator(self, *args):
        return self.MockPaginator()