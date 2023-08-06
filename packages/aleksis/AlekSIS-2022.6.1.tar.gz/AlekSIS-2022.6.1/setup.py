# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis_meta']

package_data = \
{'': ['*']}

install_requires = \
['aleksis-app-alsijil>=2.1.1,<2.2.0',
 'aleksis-app-chronos>=2.4.1,<2.5.0',
 'aleksis-app-csvimport>=2.3,<2.4',
 'aleksis-app-dashboardfeeds>=2.1,<2.2',
 'aleksis-app-hjelp>=2.1,<2.2',
 'aleksis-app-ldap>=2.2,<2.3',
 'aleksis-app-matrix>=1.0,<1.1',
 'aleksis-app-resint>=2.2,<2.3',
 'aleksis-app-stoelindeling>=1.0.1,<1.1.0',
 'aleksis-app-untis>=2.3.2,<2.4.0',
 'aleksis-core[sentry,ldap,s3]>=2.10.2,<2.11.0']

setup_kwargs = {
    'name': 'aleksis',
    'version': '2022.6.1',
    'description': 'Free School Information System Distribution',
    'long_description': 'AlekSIS® — All-libre extensible kit for school information systems\n==================================================================\n\nWhat AlekSIS® is\n----------------\n\n`AlekSIS®`_ is a web-based school information system (SIS) which can be used to\nmanage and/or publish organisational subjects of educational institutions.\n\nFormerly two separate projects (BiscuIT and SchoolApps), developed by\n`Teckids e.V.`_ and a team of students at `Katharineum zu Lübeck`_, they\nwere merged into the AlekSIS project in 2020.\n\nAlekSIS is a platform based on Django, that provides central funstions\nand data structures that can be used by apps that are developed and provided\nseperately. The AlekSIS team also maintains a set of official apps which\nmake AlekSIS a fully-featured software solutions for the information\nmanagement needs of schools.\n\nBy design, the platform can be used by schools to write their own apps for\nspecific needs they face, also in coding classes. Students are empowered to\ncreate real-world applications that bring direct value to their environment.\n\nAlekSIS is part of the `schul-frei`_ project as a component in sustainable\neducational networks.\n\nThis package\n------------\n\nThe ``aleksis`` package is a meta-package, which simply depends on the core\nand all official apps as requirements. The dependencies are semantically versioned\nand limited to the current `minor` version. If installing the distribution meta-package,\nall apps will be kept up to date with bugfixes, but not introduce new features or breakage.\n\nOfficial apps\n-------------\n\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| App name                             | Purpose                                                                                     |\n+======================================+=============================================================================================+\n| `AlekSIS-App-Chronos`_               | The Chronos app provides functionality for digital timetables.                              |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-DashboardFeeds`_        | The DashboardFeeds app provides functionality to add RSS or Atom feeds to dashboard         |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Hjelp`_                 | The Hjelp app provides functionality for aiding users.                                      |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-LDAP`_                  | The LDAP app provides functionality to import users and groups from LDAP                    |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Untis`_                 | This app provides import and export functions to interact with Untis, a timetable software. |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Alsijil`_               | This app provides an online class register.                                                 |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-CSVImport`_             | This app provides import functions to import data from CSV files.                           |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Resint`_                | This app provides time-base/live documents.                                                 |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Matrix`_                | This app provides integration with matrix/element.                                          |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n| `AlekSIS-App-Stoelindeling`_         | This app provides functionality for creating seating plans.                                 |\n+--------------------------------------+---------------------------------------------------------------------------------------------+\n\n\nLicence\n-------\n\n::\n\n  Licenced under the EUPL, version 1.2 or later, by Teckids e.V. (Bonn, Germany).\n\n  For details, please see the README file of the official apps.\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\nTrademark\n---------\n\nAlekSIS® is a registered trademark of the AlekSIS open source project, represented\nby Teckids e.V. Please refer to the `trademark policy`_ for hints on using the trademark\nAlekSIS®.\n\n.. _AlekSIS®: https://aleksis.org/\n.. _Teckids e.V.: https://www.teckids.org/\n.. _Katharineum zu Lübeck: https://www.katharineum.de/\n.. _European Union Public Licence: https://eupl.eu/\n.. _schul-frei: https://schul-frei.org/\n.. _AlekSIS-Core: https://edugit.org/AlekSIS/official/AlekSIS-App-Core\n.. _AlekSIS-App-Chronos: https://edugit.org/AlekSIS/official/AlekSIS-App-Chronos\n.. _AlekSIS-App-DashboardFeeds: https://edugit.org/AlekSIS/official/AlekSIS-App-DashboardFeeds\n.. _AlekSIS-App-Hjelp: https://edugit.org/AlekSIS/official/AlekSIS-App-Hjelp\n.. _AlekSIS-App-LDAP: https://edugit.org/AlekSIS/official/AlekSIS-App-LDAP\n.. _AlekSIS-App-Untis: https://edugit.org/AlekSIS/official/AlekSIS-App-Untis\n.. _AlekSIS-App-Alsijil: https://edugit.org/AlekSIS/official/AlekSIS-App-Alsijil\n.. _AlekSIS-App-CSVImport: https://edugit.org/AlekSIS/official/AlekSIS-App-CSVImport\n.. _AlekSIS-App-Resint: https://edugit.org/AlekSIS/official/AlekSIS-App-Resint\n.. _AlekSIS-App-Matrix: https://edugit.org/AlekSIS/official/AlekSIS-App-Matrix\n.. _AlekSIS-App-Stoelindeling: https://edugit.org/AlekSIS/official/AlekSIS-App-Stoelindeling\n.. _trademark policy: https://aleksis.org/pages/about\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
