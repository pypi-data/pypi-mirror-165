"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import json

class BaseEB:

    params = {
        "resource_name": "test-eb"
    }

    def __init__(self, **kwargs):
        self.variable_reassignment(**kwargs)
        self.eb = self.create_eb()

    def variable_reassignment(self, **kwargs):
        for key in kwargs:
            if key in self.params:
                self.params[key] = kwargs[key]
            else:
                print("hey this is probably an issue you should address")

    def create_eb(self):
        # Create an AWS resource (eb)
        main = aws.elasticbeanstalk.Application(**self.params)

        return main