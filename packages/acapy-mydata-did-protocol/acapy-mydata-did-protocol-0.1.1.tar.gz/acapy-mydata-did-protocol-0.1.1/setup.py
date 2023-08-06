# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mydata_did',
 'mydata_did.patched_protocols',
 'mydata_did.patched_protocols.issue_credential',
 'mydata_did.patched_protocols.issue_credential.v1_0',
 'mydata_did.patched_protocols.issue_credential.v1_0.handlers',
 'mydata_did.patched_protocols.issue_credential.v1_0.messages',
 'mydata_did.patched_protocols.issue_credential.v1_0.messages.inner',
 'mydata_did.patched_protocols.issue_credential.v1_0.models',
 'mydata_did.patched_protocols.present_proof',
 'mydata_did.patched_protocols.present_proof.v1_0',
 'mydata_did.patched_protocols.present_proof.v1_0.handlers',
 'mydata_did.patched_protocols.present_proof.v1_0.messages',
 'mydata_did.patched_protocols.present_proof.v1_0.messages.inner',
 'mydata_did.patched_protocols.present_proof.v1_0.models',
 'mydata_did.patched_protocols.present_proof.v1_0.util',
 'mydata_did.v1_0',
 'mydata_did.v1_0.decorators',
 'mydata_did.v1_0.handlers',
 'mydata_did.v1_0.handlers.tests',
 'mydata_did.v1_0.messages',
 'mydata_did.v1_0.models',
 'mydata_did.v1_0.models.exchange_records',
 'mydata_did.v1_0.models.exchange_records.tests',
 'mydata_did.v1_0.models.tests',
 'mydata_did.v1_0.tests',
 'mydata_did.v1_0.utils',
 'mydata_did.v1_0.utils.did',
 'mydata_did.v1_0.utils.jsonld',
 'mydata_did.v1_0.utils.tests',
 'mydata_did.v1_0.utils.wallet']

package_data = \
{'': ['*']}

install_requires = \
['acapy-patched>=0.5.6,<0.6.0', 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'acapy-mydata-did-protocol',
    'version': '0.1.1',
    'description': 'ACA-Py plugin for MyData DID DIDComm protcol',
    'long_description': '# ACA-Py plugin for MyData DID DIDComm protcol\n\n## Acknowledgements\n\nThis repository was originally created as as a deliverable for Automated Data Agreement (ADA) Project. ADA project is part of NGI-eSSIF-Lab project that has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 871932.\n\nThe lead developer to this project is iGrant.io (Sweden), supported by Linaltec (Sweden) and PrivacyAnt (Finland).\n\n## ACA-Py Version Compatibility\n\nThis plugin is compatible with ACA-Py version 0.5.6.\n\n## Installation\n\nRequirements:\n- Python 3.6 or higher\n- ACA-Py 0.5.6\n\n### Setup Aries Cloud Agent - Python\n\nIf you already have an existing installation of ACA-Py, you can skip these steps\nand move on to [plugin installation](#plugin-installation). It is also worth\nnoting that this is not the only way to setup an ACA-Py instance. For more setup\nconfigurations, see the [Aries Cloud Agent - Python\nrepository](https://github.com/hyperledger/aries-cloudagent-python).\n\nFirst, prepare a virtual environment:\n```sh\n$ python3 -m venv env\n$ source env/bin/activate\n```\n\nInstall ACA-Py 0.5.6 into the virtual environment:\n```sh\n$ pip install aries-cloudagent==0.5.6\n```\n\n### Plugin Installation\n\nInstall this plugin into the virtual environment:\n\n```sh\n$ pip install git+https://github.com/decentralised-dataexchange/acapy-mydata-did-protocol.git@master\n```\n\n**Note:** Depending on your version of `pip`, you may need to drop or add \n`#egg=mydata_did` to install the plugin with the above command.\n\n### Plugin Loading\nStart up ACA-Py with the plugin parameter:\n```sh\n$ aca-py start \\\n    -it http 0.0.0.0 8002 \\\n    -ot http \\\n    -e "http://localhost:8002/" \\\n    --label "Agent" \\\n    --admin 0.0.0.0 8001 \\\n    --admin-insecure-mode \\\n    --auto-accept-requests \\\n    --auto-ping-connection \\\n    --auto-respond-credential-offer \\\n    --auto-respond-credential-request \\\n    --auto-store-credential \\\n    --auto-respond-presentation-proposal \\\n    --auto-respond-presentation-request \\\n    --auto-verify-presentation \\\n    --genesis-url https://indy.igrant.io/genesis \\\n    --wallet-type indy \\\n    --wallet-name "agent_wallet" \\\n    --log-level info \\\n    --wallet-key "wallet@123" \\\n    --plugin "mydata_did"\n```\n\n## Licensing\n\nCopyright (c) 2021-23 LCubed AB (iGrant.io), Sweden\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.\n\nYou may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.\n\nUnless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the LICENSE for the specific language governing permissions and limitations under the License.\n',
    'author': 'George J Padayatti',
    'author_email': 'george.padayatti@igrant.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decentralised-dataexchange/acapy-mydata-did-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
