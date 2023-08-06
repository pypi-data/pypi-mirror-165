import datetime

class ValidationException(Exception): pass

class MockStepFunctions:

    def start_execution(self, stateMachineArn=None, name=None, **kwargs):
        if len(name) > 80:
            raise ValidationException
        return {
            'executionArn': 'arn:aws:states:region:123456789012:execution:CashFlowStateMachine:ab012c3d-e456-7f89-01a2-34567890b123',
            'startDate': datetime.datetime.today()
        }