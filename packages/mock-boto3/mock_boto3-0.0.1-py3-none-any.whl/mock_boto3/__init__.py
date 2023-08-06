from .mock_athena import MockAthena
from .mock_config import MockConfig
from .mock_cloudwatch import MockCloudWatch
from .mock_ec2 import MockEC2
from .mock_logs import MockLogs
from .mock_mwaa import MockMWAA
from .mock_redshift_data import MockRedshiftData
from .mock_dynamodb import MockDynamoDB
from .mock_rds import MockRDS
from .mock_s3 import MockS3
from .mock_secrets_manager import MockSecretsManager
from .mock_security_hub import MockSecurityHub
from .mock_stepfunctions import MockStepFunctions
from .mock_sts import MockSTS
from .mock_ssm import MockSSM
from .mock_lambda import MockLambda

def client(service, region_name=None, **kwargs):
    return {
        'athena': MockAthena,
        'config': MockConfig,
        'cloudwatch': MockCloudWatch,
        'ec2': MockEC2,
        'logs': MockLogs,
        'lambda': MockLambda,
        'mwaa': MockMWAA,
        'rds': MockRDS,
        'redshift-data': MockRedshiftData,
        's3': MockS3,
        'secretsmanager': MockSecretsManager,
        'securityhub': MockSecurityHub,
        'ssm': MockSSM,
        'sts': MockSTS,
        'stepfunctions': MockStepFunctions,
    }[service]()

def resource(service, *args, **kwargs):
    return dict(
        dynamodb=MockDynamoDB(),
    )[service]


class session:
    class Session:

        def __init__(self, **kwargs):
            pass

        def client(self, service, *args, **kwargs):
            return client(service)

        def resource(self, service, *args, **kwargs):
            return resource(service)


def create_event(s3_key):
    return dict(
        Records=[
            {
                "s3": {
                    "bucket":{"name": "gl-cdm-dev-polysystems"},
                    "object":{"key": s3_key}
                }
            }
        ]
    )

def assert_function_writes_files(func, filepath, *args, **kwargs):
    delete(filepath)
    assert not file_exists(filepath)
    func(*args, **kwargs)
    assert file_exists(filepath)
    delete(filepath)