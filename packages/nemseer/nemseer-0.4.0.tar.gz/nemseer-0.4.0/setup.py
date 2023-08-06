# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nemseer', 'nemseer.forecast_type']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21,<22',
 'beautifulsoup4>=4,<5',
 'dask>=2022.7.1,<2023.0.0',
 'netCDF4>=1.6.0,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'packaging>=21.3,<22.0',
 'pandas>=1.2,<2.0',
 'psutil>=5.9.1,<6.0.0',
 'pyarrow>=9.0.0,<10.0.0',
 'requests>=2,<3',
 'tqdm>=4.64.0,<5.0.0',
 'xarray>=2022,<2023']

setup_kwargs = {
    'name': 'nemseer',
    'version': '0.4.0',
    'description': 'A package for downloading and handling forecasts for the National Electricity Market (NEM) from the Australian Energy Market Operator (AEMO).',
    'long_description': '# nemseer\n\n[![PyPI version](https://badge.fury.io/py/nemseer.svg)](https://badge.fury.io/py/nemseer)\n[![Continuous Integration and Deployment](https://github.com/UNSW-CEEM/NEMSEER/actions/workflows/cicd.yml/badge.svg)](https://github.com/UNSW-CEEM/NEMSEER/actions/workflows/cicd.yml)\n[![Documentation Status](https://readthedocs.org/projects/nemseer/badge/?version=latest)](https://nemseer.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/UNSW-CEEM/NEMSEER/branch/master/graph/badge.svg?token=BO69YSQIGI)](https://codecov.io/gh/UNSW-CEEM/NEMSEER)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA package for downloading and handling historical forecast data for the National Electricity Market (NEM) produced by the Australian Energy Market Operator (AEMO).\n\n## Development progress\n\nWhile this package is currently under development, `nemseer` can currently be used to download and cache historical forecast data from AEMO. Future releases will focus on handling downloaded data.\n\nFor a high-level overview of development, check out the [roadmap](./ROADMAP.md).\n\n## Installation\n\n```bash\npip install nemseer\n```\n\n## Overview\n\n`nemseer` allows you to access historical AEMO [pre-dispatch](https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/data-nem/market-management-system-mms-data/pre-dispatch) and [Projected Assessment of System Adequacy (PASA)](https://wa.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-forecasting-and-planning/forecasting-and-reliability/projected-assessment-of-system-adequacy) forecast data available through the [MMSDM Historical Data SQLLoader](https://nemseer.readthedocs.io/en/latest/glossary.html#term-MMSDM-Historical-Data-SQLLOader).\n\n![forecast_overview](docs/source/_static/forecast_timeframes.png)\n\n<sub><sup>Source: [Reserve services in the National Electricity Market, AEMC, 2021](https://www.aemc.gov.au/sites/default/files/2020-12/AEMC_Reserve%20services%20in%20the%20NEM%20directions%20paper_05.01.2021.pdf)</sup></sub>\n\nWhereas PASA processes are primarily used to assess resource adequacy (i.e. *"can operational demand be met in the forecast horizon with a sufficient safety (reserve) margin?"*) based on technical inputs and assumptions for resources in the market, pre-dispatch processes incorporate the latest set of market participant offers and thus produce regional prices forecasts[^1] for energy and frequency control ancillary services [(FCAS)](https://aemo.com.au/-/media/files/electricity/nem/security_and_reliability/ancillary_services/guide-to-ancillary-services-in-the-national-electricity-market.pdf). A more detailed overview of the various pre-dispatch and PASA processes can be found in the [glossary](https://nemseer.readthedocs.io/en/latest/glossary.html).\n\n[^1]: We use the term *"forecast"* loosely, especially given that pre-dispatch "forecasts" change once participants update offer information (e.g. through rebidding). Rather, the purpose of these *"ahead processes"* is to provide system and market information to participants to inform their decision-making. However, to avoid confusion, we use the words "*"forecast"* and *"forecast types"* in `nemseer`.\n\n`nemseer` enables you to download and work with data from the following forecast types (where available, AEMO process and table descriptions are linked):\n\n1. 5-minute pre-dispatch (`P5MIN`: [Table descriptions](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_222.htm#1))\n2. [Pre-dispatch](https://www.aemo.com.au/-/media/files/electricity/nem/security_and_reliability/power_system_ops/procedures/so_op_3704-predispatch.pdf?la=en) (`PREDISPATCH`: [Table descriptions](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_260.htm#1))\n3. Pre-dispatch Projected Assessment of System Adequacy (`PDPASA`: [Tables and Descriptions](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_467.htm#1))\n4. [Short Term Projected Assessment of System Adequacy](https://wa.aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/pasa/stpasa-process-description.pdf) (`STPASA`: [Table descriptions](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_335.htm#1))\n5. [Medium Term Projected Assessment of System Adequacy](https://wa.aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/pasa/mt-pasa-process-description-v62.pdf?la=en) (`MTPASA`: [Table descriptions](https://nemweb.com.au/Reports/Current/MMSDataModelReport/Electricity/MMS%20Data%20Model%20Report_files/MMS_210.htm#1))\n\nAnother helpful reference for PASA information is AEMO\'s [Reliability Standard Implementation Guidelines](https://www.aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/rsig/reliability-standard-implementation-guidelines.pdf?la=en).\n\n### ST PASA Replacement Project\n\nNote that the methodologies for PD PASA and ST PASA are being reviewed by AEMO. In particular, the ST PASA Replacement project will combine PD PASA and ST PASA into ST PASA. For more detail, refer to the [final determination of the rule change](https://www.aemc.gov.au/sites/default/files/2022-05/ERC0332%20-%20Updating%20Short%20Term%20PASA%20-%20Final%20determination.pdf) and the [AEMO ST PASA Replacement Project home page](https://aemo.com.au/en/initiatives/trials-and-initiatives/st-pasa-replacement-project).\n\n## Usage\n\n### Glossary\n\nThe [glossary](https://nemseer.readthedocs.io/en/latest/glossary.html) contains overviews of the PASA and pre-dispatch processes, and descriptions of terminology relevant to using `nemseer`.\n\n### Quick start\n\nCheck out the [Quick start](https://nemseer.readthedocs.io/en/latest/quick_start.html) for examples of how you can use `nemseer`.\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](./CONTRIBUTING.md), which also includes steps to install `nemseer` for development.\n\nPlease note that this project is released with a [Code of Conduct](./CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`nemseer` was created by Abhijith Prakash. It is licensed under the terms of the [BSD 3-Clause license](./LICENSE).\n\n## Credits\n\n`nemseer` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\nThanks to Nick Gorman for his help in reviewing elements of `nemseer`.\n',
    'author': 'Abhijith Prakash',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
