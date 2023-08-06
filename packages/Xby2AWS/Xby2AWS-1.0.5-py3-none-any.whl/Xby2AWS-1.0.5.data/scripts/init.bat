@ECHO OFF

pulumi new python
git init
set RES={"resources": [{}]}
echo %RES% > resources.json

echo import pulumi >> __main__.py
echo import pulumi_aws as aws >> __main__.py
echo import pulumi_awsx as awsx >> __main__.py
echo import json >> __main__.py
echo import traceback >> __main__.py
echo import importlib >> __main__.py
echo import BaseAWS >> __main__.py

echo with open ("resources.json", "r") as deployfile: >> __main__.py
echo     resources = json.load(deployfile) >> __main__.py

echo current_vpc = None >> __main__.py
echo current_ami = None >> __main__.py

echo for resource in resources["resources"]: >> __main__.py
echo     try: >> __main__.py
echo         assert resource["module"].startswith("pulumi_aws") or resource["module"].startswith("BaseAWS") >> __main__.py
echo         module = importlib.import_module(resource["module"]) >> __main__.py
echo         resource_class = getattr(module, resource["resource_name"]) >> __main__.py

echo         if resource["req_vpc"] and resource["req_ami"]: >> __main__.py
echo             instance = resource_class(current_ami.ami.id, current_vpc, **resource["overrides"]) >> __main__.py
echo         elif resource["req_vpc"]: >> __main__.py
echo             instance = resource_class(current_vpc, **resource["overrides"]) >> __main__.py
echo         elif resource["req_ami"]: >> __main__.py
echo             instance = resource_class(current_ami.ami.id, **resource["overrides"]) >> __main__.py
echo         else: >> __main__.py
echo             instance = resource_class(**resource["overrides"]) >> __main__.py

echo         # set current vpc, ami (if applicable). this logic could probably be made a bit more complex >> __main__.py
echo         if resource["resource_name"] == "BaseAMI": >> __main__.py
echo             current_ami = instance >> __main__.py
echo         elif resource["resource_name"] == "BaseVPC": >> __main__.py
echo             current_vpc = instance >> __main__.py

echo         # add roles to a list of roles >> __main__.py
echo         roles = {} >> __main__.py
echo         if resource["resource_name"] == "Role": >> __main__.py
echo             roles[resource["overrides"]["resource_name"]] = instance.arn >> __main__.py

echo         pulumi.export(resource["resource_name"], instance) >> __main__.py

echo     except: >> __main__.py
echo         traceback.print_exc() >> __main__.py
echo         print(resource["module"]) >> __main__.py

