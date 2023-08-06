import datetime
class MockRDS:

    def generate_db_auth_token(self, **kwargs):
        return 'https://DBAuthToken'

    def describe_db_instances(DBInstanceIdentifier=None, **kwargs):
        return {
            'Marker': 'string',
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'string',
                    'DBInstanceClass': 'string',
                    'Engine': 'string',
                    'DBInstanceStatus': 'string',
                    'AutomaticRestartTime': datetime.datetime(2015, 1, 1),
                    'MasterUsername': 'string',
                    'DBName': 'string',
                    'Endpoint': {
                        'Address': 'string',
                        'Port': 123,
                        'HostedZoneId': 'string'
                    },
                    'AllocatedStorage': 123,
                    'InstanceCreateTime': datetime.datetime(2015, 1, 1),
                    'PreferredBackupWindow': 'string',
                    'BackupRetentionPeriod': 123,
                    'DBSecurityGroups': [
                        {
                            'DBSecurityGroupName': 'string',
                            'Status': 'string'
                        },
                    ],
                    'VpcSecurityGroups': [
                        {
                            'VpcSecurityGroupId': 'string',
                            'Status': 'string'
                        },
                    ],
                    'DBParameterGroups': [
                        {
                            'DBParameterGroupName': 'string',
                            'ParameterApplyStatus': 'string'
                        },
                    ],
                    'AvailabilityZone': 'string',
                    'DBSubnetGroup': {
                        'DBSubnetGroupName': 'string',
                        'DBSubnetGroupDescription': 'string',
                        'VpcId': 'string',
                        'SubnetGroupStatus': 'string',
                        'Subnets': [
                            {
                                'SubnetIdentifier': 'string',
                                'SubnetAvailabilityZone': {
                                    'Name': 'string'
                                },
                                'SubnetOutpost': {
                                    'Arn': 'string'
                                },
                                'SubnetStatus': 'string'
                            },
                        ],
                        'DBSubnetGroupArn': 'string'
                    },
                    'PreferredMaintenanceWindow': 'string',
                    'PendingModifiedValues': {
                        'DBInstanceClass': 'string',
                        'AllocatedStorage': 123,
                        'MasterUserPassword': 'string',
                        'Port': 123,
                        'BackupRetentionPeriod': 123,
                        'MultiAZ': True,
                        'EngineVersion': 'string',
                        'LicenseModel': 'string',
                        'Iops': 123,
                        'DBInstanceIdentifier': 'string',
                        'StorageType': 'string',
                        'CACertificateIdentifier': 'string',
                        'DBSubnetGroupName': 'string',
                        'PendingCloudwatchLogsExports': {
                            'LogTypesToEnable': [
                                'string',
                            ],
                            'LogTypesToDisable': [
                                'string',
                            ]
                        },
                        'ProcessorFeatures': [
                            {
                                'Name': 'string',
                                'Value': 'string'
                            },
                        ],
                        'IAMDatabaseAuthenticationEnabled': True,
                        'AutomationMode': 'full',
                        'ResumeFullAutomationModeTime': datetime.datetime(2015, 1, 1)
                    },
                    'LatestRestorableTime': datetime.datetime(2015, 1, 1),
                    'MultiAZ': True,
                    'EngineVersion': 'string',
                    'AutoMinorVersionUpgrade': True,
                    'ReadReplicaSourceDBInstanceIdentifier': 'string',
                    'ReadReplicaDBInstanceIdentifiers': [
                        'string',
                    ],
                    'ReadReplicaDBClusterIdentifiers': [
                        'string',
                    ],
                    'ReplicaMode': 'open-read-only',
                    'LicenseModel': 'string',
                    'Iops': 123,
                    'OptionGroupMemberships': [
                        {
                            'OptionGroupName': 'string',
                            'Status': 'string'
                        },
                    ],
                    'CharacterSetName': 'string',
                    'NcharCharacterSetName': 'string',
                    'SecondaryAvailabilityZone': 'string',
                    'PubliclyAccessible': True,
                    'StatusInfos': [
                        {
                            'StatusType': 'string',
                            'Normal': True,
                            'Status': 'string',
                            'Message': 'string'
                        },
                    ],
                    'StorageType': 'string',
                    'TdeCredentialArn': 'string',
                    'DbInstancePort': 123,
                    'DBClusterIdentifier': 'string',
                    'StorageEncrypted': True,
                    'KmsKeyId': 'string',
                    'DbiResourceId': 'string',
                    'CACertificateIdentifier': 'string',
                    'DomainMemberships': [
                        {
                            'Domain': 'string',
                            'Status': 'string',
                            'FQDN': 'string',
                            'IAMRoleName': 'string'
                        },
                    ],
                    'CopyTagsToSnapshot': True,
                    'MonitoringInterval': 123,
                    'EnhancedMonitoringResourceArn': 'string',
                    'MonitoringRoleArn': 'string',
                    'PromotionTier': 123,
                    'DBInstanceArn': 'string',
                    'Timezone': 'string',
                    'IAMDatabaseAuthenticationEnabled': True,
                    'PerformanceInsightsEnabled': True,
                    'PerformanceInsightsKMSKeyId': 'string',
                    'PerformanceInsightsRetentionPeriod': 123,
                    'EnabledCloudwatchLogsExports': [
                        'string',
                    ],
                    'ProcessorFeatures': [
                        {
                            'Name': 'string',
                            'Value': 'string'
                        },
                    ],
                    'DeletionProtection': True,
                    'AssociatedRoles': [
                        {
                            'RoleArn': 'string',
                            'FeatureName': 'string',
                            'Status': 'string'
                        },
                    ],
                    'ListenerEndpoint': {
                        'Address': 'string',
                        'Port': 123,
                        'HostedZoneId': 'string'
                    },
                    'MaxAllocatedStorage': 123,
                    'TagList': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ],
                    'DBInstanceAutomatedBackupsReplications': [
                        {
                            'DBInstanceAutomatedBackupsArn': 'string'
                        },
                    ],
                    'CustomerOwnedIpEnabled': True,
                    'AwsBackupRecoveryPointArn': 'string',
                    'ActivityStreamStatus': 'stopped',
                    'ActivityStreamKmsKeyId': 'string',
                    'ActivityStreamKinesisStreamName': 'string',
                    'ActivityStreamMode': 'sync',
                    'ActivityStreamEngineNativeAuditFieldsIncluded': True|False,
                    'AutomationMode': 'full',
                    'ResumeFullAutomationModeTime': datetime.datetime(2015, 1, 1),
                    'CustomIamInstanceProfile': 'string',
                    'BackupTarget': 'string'
                },
            ]
        }


    def describe_db_clusters(DBClusterIdentifier=None, **kwargs):
        return {
            'Marker': 'string',
            'DBClusters': [
                {
                    'AllocatedStorage': 123,
                    'AvailabilityZones': [
                        'string',
                    ],
                    'BackupRetentionPeriod': 123,
                    'CharacterSetName': 'string',
                    'DatabaseName': 'string',
                    'DBClusterIdentifier': 'string',
                    'DBClusterParameterGroup': 'string',
                    'DBSubnetGroup': 'string',
                    'Status': 'string',
                    'AutomaticRestartTime': datetime.datetime(2015, 1, 1),
                    'PercentProgress': 'string',
                    'EarliestRestorableTime': datetime.datetime(2015, 1, 1),
                    'Endpoint': 'string',
                    'ReaderEndpoint': 'string',
                    'CustomEndpoints': [
                        'string',
                    ],
                    'MultiAZ': True,
                    'Engine': 'string',
                    'EngineVersion': 'string',
                    'LatestRestorableTime': datetime.datetime(2015, 1, 1),
                    'Port': 123,
                    'MasterUsername': 'string',
                    'DBClusterOptionGroupMemberships': [
                        {
                            'DBClusterOptionGroupName': 'string',
                            'Status': 'string'
                        },
                    ],
                    'PreferredBackupWindow': 'string',
                    'PreferredMaintenanceWindow': 'string',
                    'ReplicationSourceIdentifier': 'string',
                    'ReadReplicaIdentifiers': [
                        'string',
                    ],
                    'DBClusterMembers': [
                        {
                            'DBInstanceIdentifier': 'string',
                            'IsClusterWriter': True,
                            'DBClusterParameterGroupStatus': 'string',
                            'PromotionTier': 123
                        },
                    ],
                    'VpcSecurityGroups': [
                        {
                            'VpcSecurityGroupId': 'string',
                            'Status': 'string'
                        },
                    ],
                    'HostedZoneId': 'string',
                    'StorageEncrypted': True,
                    'KmsKeyId': 'string',
                    'DbClusterResourceId': 'string',
                    'DBClusterArn': 'string',
                    'AssociatedRoles': [
                        {
                            'RoleArn': 'RoleArn1',
                            'Status': 'string',
                            'FeatureName': 'string'
                        },
                        {
                            'RoleArn': 'RoleArn2',
                            'Status': 'string',
                            'FeatureName': 'string'
                        },
                        {
                            'RoleArn': 'RoleArn3',
                            'Status': 'string',
                            'FeatureName': 'string'
                        },
                        {
                            'RoleArn': 'RoleArnN',
                            'Status': 'string',
                            'FeatureName': 'string'
                        },
                    ],
                    'IAMDatabaseAuthenticationEnabled': True,
                    'CloneGroupId': 'string',
                    'ClusterCreateTime': datetime.datetime(2015, 1, 1),
                    'EarliestBacktrackTime': datetime.datetime(2015, 1, 1),
                    'BacktrackWindow': 123,
                    'BacktrackConsumedChangeRecords': 123,
                    'EnabledCloudwatchLogsExports': [
                        'string',
                    ],
                    'Capacity': 123,
                    'EngineMode': 'string',
                    'ScalingConfigurationInfo': {
                        'MinCapacity': 123,
                        'MaxCapacity': 123,
                        'AutoPause': True,
                        'SecondsUntilAutoPause': 123,
                        'TimeoutAction': 'string',
                        'SecondsBeforeTimeout': 123
                    },
                    'DeletionProtection': True,
                    'HttpEndpointEnabled': True,
                    'ActivityStreamMode': 'sync',
                    'ActivityStreamStatus': 'started',
                    'ActivityStreamKmsKeyId': 'string',
                    'ActivityStreamKinesisStreamName': 'string',
                    'CopyTagsToSnapshot': True,
                    'CrossAccountClone': True,
                    'DomainMemberships': [
                        {
                            'Domain': 'string',
                            'Status': 'string',
                            'FQDN': 'string',
                            'IAMRoleName': 'string'
                        },
                    ],
                    'TagList': [
                        {
                            'Key': 'Key1',
                            'Value': 'Value1'
                        },
                        {
                            'Key': 'Key2',
                            'Value': 'Value2'
                        },
                        {
                            'Key': 'Key3',
                            'Value': 'Value1'
                        },
                        {
                            'Key': 'KeyN',
                            'Value': 'ValueN'
                        },
                    ],
                    'GlobalWriteForwardingStatus': 'enabled',
                    'GlobalWriteForwardingRequested': True,
                    'PendingModifiedValues': {
                        'PendingCloudwatchLogsExports': {
                            'LogTypesToEnable': [
                                'string',
                            ],
                            'LogTypesToDisable': [
                                'string',
                            ]
                        },
                        'DBClusterIdentifier': 'string',
                        'MasterUserPassword': 'string',
                        'IAMDatabaseAuthenticationEnabled': True,
                        'EngineVersion': 'string'
                    },
                    'DBClusterInstanceClass': 'string',
                    'StorageType': 'string',
                    'Iops': 123,
                    'PubliclyAccessible': False,
                    'AutoMinorVersionUpgrade': True,
                    'MonitoringInterval': 123,
                    'MonitoringRoleArn': 'string',
                    'PerformanceInsightsEnabled': True,
                    'PerformanceInsightsKMSKeyId': 'string',
                    'PerformanceInsightsRetentionPeriod': 123
                },
            ]
        }