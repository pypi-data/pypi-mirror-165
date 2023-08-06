import json

from random import shuffle


class MockSSM:

    key = list("1234567890abcdef0")
    shuffle(key)

    def parameters(self):
        return {
            '/aws/service/ami-windows-latest/Windows_Server-2019-English-Full-Base': 'ami-' + ''.join(self.key),
            'EC2Key': 'EC2Key',
            'EC2SecurityGroupId': 'EC2SecurityGroupId',
            'EC2InstanceProfile': 'EC2InstanceProfile',
            'CashFlowStateMachine': 'CashFlowStateMachine',
            'CrossAccountAthenaCatalog': 'CrossAccountAthenaCatalog',
            'CrossAccountAthenaDatabase': 'CrossAccountAthenaDatabase',
            'CrossAccountAthenaRole': 'CrossAccountAthenaRole',
            'CrossAccountAthenaS3OutputLocation': 'CrossAccountAthenaS3OutputLocation',
            'CrossAccountAthenaWorkgroup': 'CrossAccountAthenaWorkgroup',
            'CrossAccountRedshiftClusterDBName': 'CrossAccountRedshiftClusterDBName',
            'CrossAccountRedshiftRole': 'CrossAccountRedshiftRole',
            'CrossAccountRedshiftSecret': 'CrossAccountRedshiftSecret',
            'CrossAccountRedshiftClusterId': 'CrossAccountRedshiftClusterId',
            'CrossAccountS3Role': 'CrossAccountS3Role',
            'CrossAccountSecretsManagerRole': 'CrossAccountSecretsManagerRole',
            'gl_acdm_run_polysystems_automation_role': 'AutomationRoleArn',
            'KMSKeyId': 'KMSKeyId',
            'LogsTable': 'LogsTable',
            'RedshiftS3Access': 'RedshiftS3Access',
            'SecurityGroupIds': 'SecurityGroupId1,SecurityGroupIdN',
            's3_role': 'S3Role',
            'TriggerBucket': 'TriggerBucket',
        }

    def get_parameter(self, Name=None):
        try:
            return dict(Parameter=dict(Value=self.parameters()[Name]))
        except KeyError:
            raise self.exceptions.ParameterNotFound

    def create_document(self, Content=None, Name=None, DocumentFormat=None, Tags=None, **kwargs):
        return {
            'DocumentDescription': {
                'Name': Name,
                'Parameters': json.loads(Content)["parameters"],
                'DocumentType': 'Automation',
                'DocumentFormat': DocumentFormat,
                'Tags': Tags,
            }
        }

    def start_automation_execution(self, DocumentName):
        return {
            'AutomationExecutionId': 'AutomationExecutionId'
        }

    class exceptions:
        class ParameterNotFound(Exception):
            pass

        class InvalidDocumentContent(Exception):
            pass

        class DocumentLimitExceeded(Exception):
            pass
