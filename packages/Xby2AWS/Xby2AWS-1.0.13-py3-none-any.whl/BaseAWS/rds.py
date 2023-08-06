"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import json

class BaseRDS:

    params = {
        "instance_class": "db.t4g.micro",
        "allocated_storage": 8,
        "engine": "PostgreSQL",
        "password": "password",
        "username": "username",
        "resource_name": "test-rds"
    }

    def __init__(self, vpc, **kwargs): 
        self.variable_reassignment(**kwargs)
        self.params["db_subnet_group_name"] = vpc.instance.private_subnet_ids.apply(lambda id: id[0])
        self.create_rds()

    def variable_reassignment(self, **kwargs):
        for key in kwargs:
            if key in self.params:
                self.params[key] = kwargs[key]
            else:
                print("hey this is probably an issue you should address")

    def create_rds(self):
        # Create an AWS resource (rds)
        main = aws.rds.Instance(**self.params)