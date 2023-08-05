"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import json

class BaseEKS:

    params = {
        "resource_name": "test-eks"
    }

    def __init__(self, vpc, *args, **kwargs):
        self.variable_reassignment(**kwargs)
        self.params["vpc_config"] = vpc.instance.private_subnet_ids.apply(lambda id: id[0])
        self.eks = self.create_eks()

    def variable_reassignment(self, **kwargs):
        for key in kwargs:
            if key in self.params:
                self.params[key] = kwargs[key]
            else:
                print("hey this is probably an issue you should address")

    def create_eks(self):
        # Create an AWS resource (eks)
        main = aws.eks.Cluster(**self.params)

        return main