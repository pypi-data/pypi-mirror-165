# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sorceress']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sorceress',
    'version': '1.7.2',
    'description': 'Python package for creating optical illusions',
    'long_description': '# sorceress 1.7\n\n[![PyPI version](https://badge.fury.io/py/sorceress.svg)](https://badge.fury.io/py/sorceress) [![Jekyll site CI](https://github.com/altunenes/sorceress/actions/workflows/jekyll.yml/badge.svg)](https://github.com/altunenes/sorceress/actions/workflows/jekyll.yml)\n[![Downloads](https://pepy.tech/badge/sorceress)](https://pepy.tech/project/sorceress)\n\n### Purpose of package\n\nThe purpose of this package is to provide creating optical illusions with simple way. Package written in Python however repo includes also JavaScript.\n\nMore importantly, we shouldn\'t take optical illusions as just fun. Optical illusions help us to research how the visual system of the brain ,which is the most complex mechanism, processes such cues. Most of the optical illusions in this package are seriously researched in the neuroscience literature. And I must say that the "causation" of the most of effects is still debated in the literature according to my humble knowledge. Optical illusions are researching not only in human vision but in other animals. So we can get a lot of insights from an evolutionary perspective.\n\nIn summary, I think this topic is very important, especially in vision studies.\n\nFor all optical illusions check this documentation: [altunenes.github.io/sorceress/](https://altunenes.github.io/sorceress/)\n\n### Getting started🚀️\n\nPackage can be found on pypi hence you can install it with using pip.\n\n```\npip install sorceress==1.7\n```\n\n```\n#importing\nimport sorceress\n#another way to import\nfrom sorceress import sorceress\n```\n\n### Features\n\n[For the API, click here](https://altunenes.github.io/sorceress/api_reference/)\n\n+ Illusions written in Python\n  - chromatic\n  - dotill\n  - realtimegrid\n  - addlines\n  - eyecolour\n  - dakinPex\n  - bruno\n  - dolboeuf\n  - kanizsa\n  - tAki2001\n  - cafewall\n  - ccob\n  - ebbinghaus\n  - whiteill\n  - enigma\n  - blackhole\n+ **Illusions written in JavaScript**\n\n- footsteps\n- thelilac\n- EyeMovements\n\n## Examples\n\n[In this page](https://altunenes.github.io/sorceress/explanations%20of%20illusions/), you can find all illusions, explanations, code and how to use. I show just few examples on this page.\n\n```\nfrom sorcerer import sorcerer\nsorcerer.chromatic("myimage.jpg","outputname" ,circle=False, method="CMCCAT2000", gif=True, Gifduration=7)\nsorcerer.addlines("myimage.png","desiredoutputname",linecolour1=(0,255,0),linecolour2=(0,255,255),linecolour3=(255,0,0))\n```\n\n## Contribution\n\nAny contribution, bug report, suggestion is always welcome.\n\n##Author\n\n+ Main Maintainer: Enes Altun\n',
    'author': 'altunenes',
    'author_email': 'enesaltun2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/altunenes/sorceress',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
