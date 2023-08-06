# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sta_awscli']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete==2.0.0',
 'beautifulsoup4==4.11.1',
 'boto3==1.24.59',
 'botocore==1.27.59',
 'bs4==0.0.1',
 'certifi==2022.6.15',
 'charset-normalizer==2.1.1',
 'colorama==0.4.5',
 'decorator==5.1.1',
 'idna==3.3',
 'jmespath==1.0.1',
 'numpy==1.23.2',
 'opencv-python==4.6.0.66',
 'packaging==21.3',
 'pillow==9.2.0',
 'pwinput==1.0.2',
 'pyparsing==3.0.9',
 'pyreadline3==3.4.1',
 'pytesseract==0.3.10',
 'python-dateutil==2.8.2',
 'requests==2.28.1',
 's3transfer==0.6.0',
 'six==1.16.0',
 'soupsieve==2.3.2.post1',
 'urllib3==1.26.12',
 'validators==0.20.0']

entry_points = \
{'console_scripts': ['sta-awscli = sta_awscli.sta_awscli:main']}

setup_kwargs = {
    'name': 'sta-awscli',
    'version': '2.0.8',
    'description': 'MFA for AWS CLI using SafeNet Trusted Access (STA)',
    'long_description': '# sta-awscli\n## MFA for AWS CLI using SafeNet Trusted Access (STA)\n\n\nThis script allows using SafeNet Trusted Access (STA) IDP based authentication when working with AWSCLI. At the moment, the supported configuration is using Keycloak (https://www.keycloak.org) as an "agent" between STA and AWS, allowing us to support AWS with multiple accounts and roles.\nThe script assumes STA and Keycloak are configured and working for SAML based access to AWS.\n\nThe script supports all STA authentication methods, including manual OTP, Push based OTP and GriDsure.\nGriDsure support is experimental and requires "tesseract" v4.0 and above to be installed on the host (https://tesseract-ocr.github.io/tessdoc/Installation.html).\n\n## Configuration\n\nOn first execution, the script will collect the required information to create a configuration file (sta-awscli.config) that is stored in ~\\\\.aws folder. It\'s possible to run the script with -c switch to specify an alternative location for the config file or --update-config to overwrite existing configurations.\n\nThe configuration file includes:  \n\n- AWS Region\n- Keycloak URL\n- Keycloak version\n- Keycloak Realm Name\n- AWS application name in Keycloak\n\nFor example:\n```\n[config]\naws_region =  \ncloud_idp =  \nis_new_kc =  \ntenant_reference_id =  \naws_app_name =  \n```\n## Usage\n\nOnce the configuration is created, a connection is established to STA through Keycloak and the user will be asked to provide a username, based on STA authentication policy, AD Password and OTP. If the user only has single token (MobilePASS+ or GriDsure) assigned, the authentication will be triggered automatically (Push for MobilePASS+ or the pattern grid presented for GriDsure). For auto triggered Push - the user can cancel the Push using CTRL+C to manually enter OTP.\nIf the user has multiple tokens assigned, the user is aksed to provide an OTP, but still has the abbility to trigger Push ("p" or blank OTP) and GriDsure ("g").\n\nAfter successful  authentication, if a user has a single role assigned, an Access Token is generated and stored in .aws\\credentials file. If the user has multiple roles assigned, the user is presented with the list of available roles to select the desired role and an Access Token is generated and stored.\n\n```\n $ sta-awscli -h                                   \nsta-awscli (version) MFA for AWS CLI using SafeNet Trusted Access (STA)\n\nusage: sta-awscli [-h] [-v] [-c CLI_CONFIG_PATH] [--update-config] [-u USERNAME] \n                  [-r [REGION] | --region [{eu-north-1,ap-south-1,eu-west-3,eu-west-2,eu-west-1,\n                                            eu-central-1,ap-northeast-3,ap-northeast-2,ap-northeast-1,\n                                            ap-east-1,ap-southeast-1,ap-southeast-2,sa-east-1,\n                                            ca-central-1,us-east-1,us-east-2,us-west-1,us-west-2}]]\noptions:\n  -h, --help            show this help message and exit\n  -v, --version         show program\'s version number and exit\n  -c CLI_CONFIG_PATH, --config CLI_CONFIG_PATH\n                        Specify script configuration file path\n  --update-config       Force update sta-awscli configuration file\n  -u USERNAME, --username USERNAME\n                        Specify your SafeNet Trusted Access Username\n  -r [REGION]           Specify any AWS region (without input checking)\n  --region [REGION]     Specify AWS region (e.g. us-east-1)\n```\n\n',
    'author': 'Gur Talmor, Cina Shaykhian and Alex Basin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thalesdemo/sta-awscli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
