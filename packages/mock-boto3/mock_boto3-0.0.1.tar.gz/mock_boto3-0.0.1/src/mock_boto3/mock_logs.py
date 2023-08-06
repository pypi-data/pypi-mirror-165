class MockLogs:

    log_groups = {'logGroups': []}
    log_streams = {'logStreams': []}

    class exceptions:
        class ResourceAlreadyExistsException(Exception): pass
        class InvalidSequenceTokenException(Exception): pass
        class ResourceNotFoundException(Exception): pass

    def describe_log_groups(self, **kwargs):
        return self.log_groups

    def describe_log_streams(self, **kwargs):
        return self.log_streams

    def create_log_group(self, logGroupName):
        for log_group in self.log_groups["logGroups"]:
            try:
                log_group[logGroupName]
            except KeyError:
                pass
            else:
                raise self.exceptions.ResourceAlreadyExistsException
        self.log_groups['logGroups'].append(
            dict(logGroupName=logGroupName)
        )

    def create_log_stream(self, logGroupName, logStreamName=None):
        for log_stream in self.log_streams["logStreams"]:
            try:
                log_stream[logStreamName]
            except KeyError:
                pass
            else:
                raise self.exceptions.ResourceAlreadyExistsException
        self.log_streams['logStreams'].append(
            dict(logStreamName=logStreamName)
        )

    def delete_log_stream(self, logStreamName=None, **kwargs):
        for log_stream in self.log_streams["logStreams"]:
            if log_stream["logStreamName"] == logStreamName:
                self.log_streams["logStreams"].remove(log_stream)

    def delete_log_group(self, logGroupName=None, **kwargs):
        for log_group in self.log_groups["logGroups"]:
            if log_group["logGroupName"] == logGroupName:
                self.log_groups["logGroups"].remove(log_group)

    def put_log_events(*args, **kwargs):
        return {
            'nextSequenceToken': 'string',
            'rejectedLogEventsInfo': {
                'tooNewLogEventStartIndex': 123,
                'tooOldLogEventEndIndex': 123,
                'expiredLogEventEndIndex': 123
            }
        }
