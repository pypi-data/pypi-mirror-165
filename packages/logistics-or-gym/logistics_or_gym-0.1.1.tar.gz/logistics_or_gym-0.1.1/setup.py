# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logistics_or_gym', 'logistics_or_gym.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym', 'numpy>=1.23.2,<1.24.0']

setup_kwargs = {
    'name': 'logistics-or-gym',
    'version': '0.1.1',
    'description': 'or-problems formulated as gym environments to solve logisitcal-problems',
    'long_description': ' [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n![Tests Workflow](https://github.com/HublyGroup/logistics-or-gym/actions/workflows/python-app.yml/badge.svg)\n [![PyPI version](https://badge.fury.io/py/logistics-or-gym.svg)](https://badge.fury.io/py/logistics-or-gym)\n\n![Logo](img/4x/logo2.png#gh-dark-mode-only)\n![LogoBlack](img/4x/logo-black.png#gh-light-mode-only)\n\n# Introduction\nLogistics-OR-gym is a "collection" of Open AI Gym environments ment to simualte logistical problems such as routing, \ncontainer filling and supply chain \n# Install\nYou can install the envs using pypi\n````shell\npip install logistics-or-gym\n````\nPython versions supported are: >=3.8 <3.11\n\n# Available Environments\n## Routing\n### Heterogeneous Capacitated Vehicle Routing Problem (HCVRP)\nHCVRP simulates routing problems when the number of vehicles is >=1 (This means it also covers the case for CVRP if only\nthat is needed) and different speeds. This implementation follows the one from:\n````cite\n@article{Li2021,\n   abstract = {Existing deep reinforcement learning (DRL) based methods for solving the capacitated vehicle routing problem (CVRP) intrinsically cope with homogeneous vehicle fleet, in which the fleet is assumed as repetitions of a single vehicle. Hence, their key to construct a solution solely lies in the selection of the next node (customer) to visit excluding the selection of vehicle. However, vehicles in real-world scenarios are likely to be heterogeneous with different characteristics that affect their capacity (or travel speed), rendering existing DRL methods less effective. In this paper, we tackle heterogeneous CVRP (HCVRP), where vehicles are mainly characterized by different capacities. We consider both min-max and min-sum objectives for HCVRP, which aim to minimize the longest or total travel time of the vehicle(s) in the fleet. To solve those problems, we propose a DRL method based on the attention mechanism with a vehicle selection decoder accounting for the heterogeneous fleet constraint and a node selection decoder accounting for the route construction, which learns to construct a solution by automatically selecting both a vehicle and a node for this vehicle at each step. Experimental results based on randomly generated instances show that, with desirable generalization to various problem sizes, our method outperforms the state-of-the-art DRL method and most of the conventional heuristics, and also delivers competitive performance against the state-of-the-art heuristic method, i.e., SISR. Additionally, the results of extended experiments demonstrate that our method is also able to solve CVRPLib instances with satisfactory performance.},\n   author = {Jingwen Li and Yining Ma and Ruize Gao and Zhiguang Cao and Andrew Lim and Wen Song and Jie Zhang},\n   doi = {10.1109/TCYB.2021.3111082},\n   journal = {IEEE Transactions on Cybernetics},\n   keywords = {Computer architecture,Decoding,Deep reinforcement learning (DRL),Optimization,Reinforcement learning,Routing,Search problems,Vehicle routing,heterogeneous CVRP (HCVRP),min-max objective,min-sum objective.},\n   month = {10},\n   publisher = {Institute of Electrical and Electronics Engineers Inc.},\n   title = {Deep Reinforcement Learning for Solving the Heterogeneous Capacitated Vehicle Routing Problem},\n   url = {http://arxiv.org/abs/2110.02629 http://dx.doi.org/10.1109/TCYB.2021.3111082},\n   year = {2021},\n}\n````\nTo use the environment simply use the gym library to create it:\n````python\nimport gym\ngym.make("hcvrp-v0")\n````\nThe arguments you can pass are: \n````python\nn_vehicles=3, \nn_nodes=50\n````\n\nThere will be more arguments later. All fields are public so in the meantime just rewrite the properties\n\n# TODO\n- [X] HCVRP\n- [ ] Container filling (3D binpacking)\n- [ ] Dynamic HCVRP (For delivery)\n- [ ] Supply Chain Management (Not yet decided on which ones)\n# Credit\n',
    'author': 'hadisdev',
    'author_email': 'hadi.salameh@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HublyGroup/logistics-or-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
