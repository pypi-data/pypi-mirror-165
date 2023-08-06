class MockSecurityHub(object):

    class exceptions:
        class InternalException(Exception): pass
        class InvalidInputException(Exception): pass
        class InvalidAccessException(Exception): pass
        class LimitExceededException(Exception): pass

    def get_findings(self, **kwargs):
        return {
            "ResponseMetadata": {
                "RequestId": "123456a7-bcd8-9012-34ef-56a7bc890123",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "date": "Mon, 25 Dec 1942 21:15:15 GMT",
                    "content-type": "application/json",
                    "content-length": "9775",
                    "connection": "keep-alive",
                    "x-amzn-requestid": "123456a7-bcd8-9012-34ef-56a7bc890123",
                    "access-control-allow-origin": "*",
                    "access-control-allow-headers": "Authorization,Date,X-Amz-Date,X-Amz-Security-Token,X-Amz-Target,content-type,x-amz-content-sha256,x-amz-user-agent,x-amzn-platform-id,x-amzn-trace-id",
                    "x-amz-apigw-id": "TeRjhEuCoAMFiLg=",
                    "access-control-allow-methods": "GET,POST,OPTIONS,PUT,PATCH,DELETE",
                    "access-control-expose-headers": "x-amzn-errortype,x-amzn-requestid,x-amzn-errormessage,x-amzn-trace-id,x-amz-apigw-id,date",
                    "x-amzn-trace-id": "Root=1-12a345b6-7c89012345678de901f2345g",
                    "access-control-max-age": "86400"
                },
                "RetryAttempts": 0
            },
            "Findings": [
                {
                    "SchemaVersion": "2018-10-08",
                    "Id": "arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.6/finding/a1234bc5-678d-90e1-fa2b-345c6789012d",
                    "ProductArn": "arn:aws:securityhub:us-east-1::product/aws/securityhub",
                    "ProductName": "Security Hub",
                    "CompanyName": "AWS",
                    "Region": "us-east-1",
                    "GeneratorId": "aws-foundational-security-best-practices/v/1.0.0/RDS.6",
                    "AwsAccountId": "123456789012",
                    "Types": [
                        "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
                    ],
                    "FirstObservedAt": "1945-12-20T17:03:25.020Z",
                    "LastObservedAt": "1945-12-25T12:15:48.685Z",
                    "CreatedAt": "1945-12-20T17:03:25.020Z",
                    "UpdatedAt": "1945-12-25T12:15:44.388Z",
                    "Severity": {
                        "Product": 10,
                        "Label": "LOW",
                        "Normalized": 10,
                        "Original": "LOW"
                    },
                    "Title": "RDS.6 Enhanced monitoring should be configured for RDS DB instances",
                    "Description": "This control checks whether enhanced monitoring is enabled for your RDS DB instances.",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For directions on how to fix this issue, consult the AWS Security Hub Foundational Security Best Practices documentation.",
                            "Url": "https://docs.aws.amazon.com/console/securityhub/RDS.6/remediation"
                        }
                    },
                    "ProductFields": {
                        "StandardsArn": "arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
                        "StandardsSubscriptionArn": "arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0",
                        "ControlId": "RDS.6",
                        "RecommendationUrl": "https://docs.aws.amazon.com/console/securityhub/RDS.6/remediation",
                        "RelatedAWSResources:0/name": "securityhub-rds-enhanced-monitoring-enabled-87438d11",
                        "RelatedAWSResources:0/type": "AWS::Config::ConfigRule",
                        "StandardsControlArn": "arn:aws:securityhub:us-east-1:123456789012:control/aws-foundational-security-best-practices/v/1.0.0/RDS.6",
                        "aws/securityhub/ProductName": "Security Hub",
                        "aws/securityhub/CompanyName": "AWS",
                        "aws/securityhub/annotation": "Enhanced Monitoring interval for this Amazon RDS instance is not configured.",
                        "Resources:0/Id": "arn:aws:rds:us-east-1:123456789012:db:DbInstanceIdentifier0",
                        "aws/securityhub/FindingId": "arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.6/finding/a1234bc5-678d-90e1-fa2b-345c6789012d"
                    },
                    "Resources": [
                        {
                            "Type": "AwsRdsDbInstance",
                            "Id": "arn:aws:rds:us-east-1:123456789012:db:DbInstanceIdentifier0",
                            "Partition": "aws",
                            "Region": "us-east-1",
                            "Details": {
                                "AwsRdsDbInstance": {
                                    "CACertificateIdentifier": "rds-ca-2019",
                                    "DBInstanceIdentifier": "DbInstanceIdentifier0",
                                    "DBInstanceClass": "db.r5.2xlarge",
                                    "DbInstancePort": 0,
                                    "DbiResourceId": "db-BCDEFGHIJKLMNOPQRSTUVWX12YZA",
                                    "DBName": "massgov_pfml_prod",
                                    "DeletionProtection": False,
                                    "Endpoint": {
                                        "Address": "DbInstanceIdentifier0.a1bcdefghijk.us-east-1.rds.amazonaws.com",
                                        "Port": 5432,
                                        "HostedZoneId": "HostedZoneId"
                                    },
                                    "Engine": "postgres",
                                    "EngineVersion": "12.10",
                                    "IAMDatabaseAuthenticationEnabled": True,
                                    "InstanceCreateTime": "1945-12-20T17:03:41.483Z",
                                    "KmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/1a2b0345-cd67-8901-2e34-f5678fab901c",
                                    "PubliclyAccessible": False,
                                    "StorageEncrypted": True,
                                    "VpcSecurityGroups": [
                                        {
                                            "VpcSecurityGroupId": "sg-0be281b4acd7091ad",
                                            "Status": "active"
                                        }
                                    ],
                                    "MultiAz": False,
                                    "DbInstanceStatus": "stopped",
                                    "MasterUsername": "pfml",
                                    "AllocatedStorage": 499,
                                    "PreferredBackupWindow": "08:05-08:35",
                                    "BackupRetentionPeriod": 35,
                                    "DbParameterGroups": [
                                        {
                                            "DbParameterGroupName": "DbParameterGroupName",
                                            "ParameterApplyStatus": "in-sync"
                                        }
                                    ],
                                    "AvailabilityZone": "us-east-1b",
                                    "DbSubnetGroup": {
                                        "DbSubnetGroupName": "name-name-name-private",
                                        "DbSubnetGroupDescription": "name-name-name-private",
                                        "VpcId": "vpc-0c2bb62737af2dea3",
                                        "SubnetGroupStatus": "Complete",
                                        "Subnets": [
                                            {
                                                "SubnetIdentifier": "subnet-12ab3cdef45a678b9",
                                                "SubnetAvailabilityZone": {
                                                    "Name": "us-east-1a"
                                                },
                                                "SubnetStatus": "Active"
                                            },
                                            {
                                                "SubnetIdentifier": "subnet-2ab3cdef45a678b91",
                                                "SubnetAvailabilityZone": {
                                                    "Name": "us-east-1b"
                                                },
                                                "SubnetStatus": "Active"
                                            }
                                        ]
                                    },
                                    "PreferredMaintenanceWindow": "sun:02:05-sun:02:35",
                                    "LatestRestorableTime": "1945-06-03T20:19:34.000Z",
                                    "AutoMinorVersionUpgrade": False,
                                    "LicenseModel": "postgresql-license",
                                    "Iops": 1000,
                                    "OptionGroupMemberships": [
                                        {
                                            "OptionGroupName": "default:postgres-12",
                                            "Status": "in-sync"
                                        }
                                    ],
                                    "StorageType": "io1",
                                    "CopyTagsToSnapshot": True,
                                    "MonitoringInterval": 0,
                                    "PerformanceInsightsEnabled": False,
                                    "EnabledCloudWatchLogsExports": [
                                        "postgresql",
                                        "upgrade"
                                    ],
                                    "MaxAllocatedStorage": 1000
                                }
                            }
                        }
                    ],
                    "Compliance": {
                        "Status": "FAILED"
                    },
                    "WorkflowState": "NEW",
                    "Workflow": {
                        "Status": "NEW"
                    },
                    "RecordState": "ACTIVE",
                    "Note": {
                        "Text": "SENT TO SPLUNK: ",
                        "UpdatedBy": "SplunkSecurityHubLambda",
                        "UpdatedAt": "1945-12-25T12:17:55.507Z"
                    },
                    "FindingProviderFields": {
                        "Severity": {
                            "Label": "LOW",
                            "Original": "LOW"
                        },
                        "Types": [
                            "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
                        ]
                    }
                },
                {
                    "SchemaVersion": "2018-10-08",
                    "Id": "arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.6/finding/b123c456-7890-1234-efa5-67b89012c345",
                    "ProductArn": "arn:aws:securityhub:us-east-1::product/aws/securityhub",
                    "ProductName": "Security Hub",
                    "CompanyName": "AWS",
                    "Region": "us-east-1",
                    "GeneratorId": "aws-foundational-security-best-practices/v/1.0.0/RDS.6",
                    "AwsAccountId": "123456789012",
                    "Types": [
                        "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
                    ],
                    "FirstObservedAt": "1945-06-07T13:53:32.999Z",
                    "LastObservedAt": "1945-12-25T04:37:52.854Z",
                    "CreatedAt": "1945-06-07T13:53:32.999Z",
                    "UpdatedAt": "1945-12-25T04:37:45.580Z",
                    "Severity": {
                        "Product": 10,
                        "Label": "LOW",
                        "Normalized": 10,
                        "Original": "LOW"
                    },
                    "Title": "RDS.6 Enhanced monitoring should be configured for RDS DB instances",
                    "Description": "This control checks whether enhanced monitoring is enabled for your RDS DB instances.",
                    "Remediation": {
                        "Recommendation": {
                            "Text": "For directions on how to fix this issue, consult the AWS Security Hub Foundational Security Best Practices documentation.",
                            "Url": "https://docs.aws.amazon.com/console/securityhub/RDS.6/remediation"
                        }
                    },
                    "ProductFields": {
                        "StandardsArn": "arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
                        "StandardsSubscriptionArn": "arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0",
                        "ControlId": "RDS.6",
                        "RecommendationUrl": "https://docs.aws.amazon.com/console/securityhub/RDS.6/remediation",
                        "RelatedAWSResources:0/name": "securityhub-rds-enhanced-monitoring-enabled-87438d11",
                        "RelatedAWSResources:0/type": "AWS::Config::ConfigRule",
                        "StandardsControlArn": "arn:aws:securityhub:us-east-1:123456789012:control/aws-foundational-security-best-practices/v/1.0.0/RDS.6",
                        "aws/securityhub/ProductName": "Security Hub",
                        "aws/securityhub/CompanyName": "AWS",
                        "aws/securityhub/annotation": "Enhanced Monitoring interval for this Amazon RDS instance is not configured.",
                        "Resources:0/Id": "arn:aws:rds:us-east-1:123456789012:db:DbInstanceIdentifier1",
                        "aws/securityhub/FindingId": "arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:123456789012:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.6/finding/b123c456-7890-1234-efa5-67b89012c345"
                    },
                    "Resources": [
                        {
                            "Type": "AwsRdsDbInstance",
                            "Id": "arn:aws:rds:us-east-1:123456789012:db:DbInstanceIdentifier1",
                            "Partition": "aws",
                            "Region": "us-east-1",
                            "Details": {
                                "AwsRdsDbInstance": {
                                    "CACertificateIdentifier": "rds-ca-2019",
                                    "DBInstanceIdentifier": "DbInstanceIdentifier1",
                                    "DBInstanceClass": "db.r5.2xlarge",
                                    "DbInstancePort": 0,
                                    "DbiResourceId": "db-1ABCD2EF3GHIJ7KLMNOP4Q1RS",
                                    "DBName": "massgov_pfml_prod",
                                    "DeletionProtection": False,
                                    "Endpoint": {
                                        "Address": "DbInstanceIdentifier1.a1bcdefghijk.us-east-1.rds.amazonaws.com",
                                        "Port": 5432,
                                        "HostedZoneId": "HostedZoneId"
                                    },
                                    "Engine": "postgres",
                                    "EngineVersion": "12.10",
                                    "IAMDatabaseAuthenticationEnabled": True,
                                    "InstanceCreateTime": "1945-06-07T13:55:03.898Z",
                                    "KmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/1a2b0345-cd67-8901-2e34-f5678fab901c",
                                    "PubliclyAccessible": False,
                                    "StorageEncrypted": True,
                                    "VpcSecurityGroups": [
                                        {
                                            "VpcSecurityGroupId": "sg-0be281b4acd7091ad",
                                            "Status": "active"
                                        }
                                    ],
                                    "MultiAz": False,
                                    "DbInstanceStatus": "backing-up",
                                    "MasterUsername": "pfml",
                                    "AllocatedStorage": 499,
                                    "PreferredBackupWindow": "08:05-08:35",
                                    "BackupRetentionPeriod": 35,
                                    "DbParameterGroups": [
                                        {
                                            "DbParameterGroupName": "DbParameterGroupName",
                                            "ParameterApplyStatus": "in-sync"
                                        }
                                    ],
                                    "AvailabilityZone": "us-east-1a",
                                    "DbSubnetGroup": {
                                        "DbSubnetGroupName": "name-name-name-private",
                                        "DbSubnetGroupDescription": "name-name-name-private",
                                        "VpcId": "vpc-0c2bb62737af2dea3",
                                        "SubnetGroupStatus": "Complete",
                                        "Subnets": [
                                            {
                                                "SubnetIdentifier": "subnet-12ab3cdef45a678b9",
                                                "SubnetAvailabilityZone": {
                                                    "Name": "us-east-1a"
                                                },
                                                "SubnetStatus": "Active"
                                            },
                                            {
                                                "SubnetIdentifier": "subnet-2ab3cdef45a678b91",
                                                "SubnetAvailabilityZone": {
                                                    "Name": "us-east-1b"
                                                },
                                                "SubnetStatus": "Active"
                                            }
                                        ]
                                    },
                                    "PreferredMaintenanceWindow": "sun:02:05-sun:02:35",
                                    "LatestRestorableTime": "1945-12-25T04:29:31.000Z",
                                    "AutoMinorVersionUpgrade": False,
                                    "LicenseModel": "postgresql-license",
                                    "Iops": 1000,
                                    "OptionGroupMemberships": [
                                        {
                                            "OptionGroupName": "default:postgres-12",
                                            "Status": "in-sync"
                                        }
                                    ],
                                    "StorageType": "io1",
                                    "CopyTagsToSnapshot": True,
                                    "MonitoringInterval": 0,
                                    "PerformanceInsightsEnabled": False,
                                    "EnabledCloudWatchLogsExports": [
                                        "postgresql",
                                        "upgrade"
                                    ],
                                    "MaxAllocatedStorage": 1000
                                }
                            }
                        }
                    ],
                    "Compliance": {
                        "Status": "FAILED"
                    },
                    "WorkflowState": "NEW",
                    "Workflow": {
                        "Status": "NEW"
                    },
                    "RecordState": "ACTIVE",
                    "FindingProviderFields": {
                        "Severity": {
                            "Label": "LOW",
                            "Original": "LOW"
                        },
                        "Types": [
                            "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
                        ]
                    }
                }
            ]
        }

    def batch_update_findings(self, FindingIdentifiers=None, **kwargs):
        return {
            'ProcessedFindings': FindingIdentifiers,
            'UnprocessedFindings': [
                {
                    'FindingIdentifier': {
                        'Id': 'string',
                        'ProductArn': 'string'
                    },
                    'ErrorCode': 'string',
                    'ErrorMessage': 'string'
                },
            ]
        }