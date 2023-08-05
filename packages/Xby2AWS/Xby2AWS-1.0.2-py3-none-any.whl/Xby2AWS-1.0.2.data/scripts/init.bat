@ECHO OFF
set RES={"resources": [{}]}
echo %RES% > resources.json

git init
pulumi new

echo import pulumi >> __main.py__
echo import pulumi_aws as aws >> __main.py__
echo import pulumi_awsx as awsx >> __main.py__
echo import json >> __main.py__
echo import traceback >> __main.py__
echo import importlib >> __main.py__
echo import BaseAWS >> __main.py__

echo with open ("resources.json", "r") as deployfile: >> __main.py__
echo     resources = json.load(deployfile) >> __main.py__

echo current_vpc = None >> __main.py__
echo current_ami = None >> __main.py__

echo for resource in resources["resources"]: >> __main.py__
echo     try: >> __main.py__
echo         assert resource["module"].startswith("pulumi_aws") or resource["module"].startswith("BaseAWS") >> __main.py__
echo         module = importlib.import_module(resource["module"]) >> __main.py__
echo         resource_class = getattr(module, resource["resource_name"]) >> __main.py__

echo         if resource["req_vpc"] and resource["req_ami"]: >> __main.py__
echo             instance = resource_class(current_ami.ami.id, current_vpc, **resource["overrides"]) >> __main.py__
echo         elif resource["req_vpc"]: >> __main.py__
echo             instance = resource_class(current_vpc, **resource["overrides"]) >> __main.py__
echo         elif resource["req_ami"]: >> __main.py__
echo             instance = resource_class(current_ami.ami.id, **resource["overrides"]) >> __main.py__
echo         else: >> __main.py__
echo             instance = resource_class(**resource["overrides"]) >> __main.py__

echo         # set current vpc, ami (if applicable). this logic could probably be made a bit more complex >> __main.py__
echo         if resource["resource_name"] == "BaseAMI": >> __main.py__
echo             current_ami = instance >> __main.py__
echo         elif resource["resource_name"] == "BaseVPC": >> __main.py__
echo             current_vpc = instance >> __main.py__

echo         # add roles to a list of roles >> __main.py__
echo         roles = {} >> __main.py__
echo         if resource["resource_name"] == "Role": >> __main.py__
echo             roles[resource["overrides"]["resource_name"]] = instance.arn >> __main.py__

echo         pulumi.export(resource["resource_name"], instance) >> __main.py__

echo     except: >> __main.py__
echo         traceback.print_exc() >> __main.py__
echo         print(resource["module"]) >> __main.py__

