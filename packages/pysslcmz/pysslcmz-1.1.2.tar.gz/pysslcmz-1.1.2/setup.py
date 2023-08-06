# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysslcmz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysslcmz',
    'version': '1.1.2',
    'description': 'Implements SSLCOMMERZ payment gateway in python based web apps.',
    'long_description': "# SSLCOMMERZ Payment Gateway implementation in Python\nProvides a python module to implement payment gateway in python based web apps.\n\n## Installation\nVia PIP\n```bash\npip install pysslcmz\n```\n## Projected use\n```python\nfrom pysslcmz.payment import SSLCSession\nfrom decimal import Decimal\n\nmypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='your_sslc_store_id', sslc_store_pass='your_sslc_store_passcode')\n\nmypayment.set_urls(success_url='example.com/success', fail_url='example.com/failed', cancel_url='example.com/cancel', ipn_url='example.com/payment_notification')\n\nmypayment.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')\n\nmypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')\n\nmypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')\n\n# If you want to post some additional values\nmypayment.set_additional_values(value_a='cusotmer@email.com', value_b='portalcustomerid', value_c='1234', value_d='uuid')\n\nresponse_data = mypayment.init_payment()\n```\n\n## Response parameters\n### When Successfull with Auth and Payloads provided\n> status\n\n> sessionkey\n\n> GatewayPageURL\n\n#### Example\n```python\n>>> response_data['status']\nSUCCESS\n>>> response_data['sessionkey']\nF650E87F23DD2A8FFCB4E4E333C13B28\n>>> response_data['GatewayPageURL']\nhttps://sandbox.sslcommerz.com/EasyCheckOut/testcdef650e87f23dd2a8ffcb4234fasf3b28\n```\n\n### When Failed\n> status\n\n> failedreason\n\n#### Example\n```python\n>>> response_data['status']\nFAILED\n>>> response_data['failedreason']\n'Store Credential Error Or Store is De-active'\n```",
    'author': 'Piecoders IT Solutions',
    'author_email': 'piecodersit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/piecoders/pyssl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
