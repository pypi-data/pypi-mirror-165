# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hume', 'hume.batch', 'hume.common', 'hume.common.config']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'hume',
    'version': '0.1.2',
    'description': 'Hume AI Python Client',
    'long_description': '# Hume AI Python SDK\n\nThe Hume AI Python SDK makes it easy to call Hume APIs from Python applications.\n\nTo get started, [sign up for a Hume account](https://beta.hume.ai/sign-up)!\n\n## Requirements\n\nPython versions between 3.8 and 3.10 are supported\n\n## Installation\n\n```\npip install hume\n```\n\n## Example Usage\n\n### Submit a new batch job\n\n> Note: Your personal API key can be found in the profile section of [beta.hume.ai](https://beta.hume.ai)\n\n```python\nfrom hume import HumeBatchClient\n\nclient = HumeBatchClient("<your-api-key>")\nurls = ["https://tinyurl.com/hume-img"]\njob = client.submit_face(urls)\n\nprint(job)\nprint("Running...")\n\nresult = job.await_complete()\nresult.download_predictions("predictions.json")\n\nprint("Predictions downloaded!")\n```\n\n### Rehydrate a batch job from a job ID\n\n```python\nfrom hume import HumeBatchClient\n\nclient = HumeBatchClient("<your-api-key>")\n\njob_id = "<your-job-id>"\njob = client.get_job(job_id)\n\nprint(job)\n```\n\n## Documentation\n\nLearn more about Hume\'s expressive communication platform on [our homepage](https://hume.ai) or our [platform docs](https://help.hume.ai/basics/about-hume-ai)\n\nSee example requests and responses for all available endpoints in the [Hume API Reference](https://docs.hume.ai)\n\n## Support\n\nIf you\'ve found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!\n',
    'author': 'Hume AI Dev',
    'author_email': 'dev@hume.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HumeAI/hume-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
