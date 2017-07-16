from bears.configfiles.AnsibleLintBear import AnsibleLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
---
- hosts: webservers
  vars:
    http_port: 8080
  tasks:
  - name: check version
    yum: name=httpd
"""

bad_file = """
---
- hosts: webservers
  vars:
    http_port: 8080
  tasks:
  - name: check version
    yum: name=httpd state=latest
"""

AnsibleLintBearTest = verify_local_bear(AnsibleLintBear,
                                        valid_files=(good_file,),
                                        invalid_files=(bad_file,))
