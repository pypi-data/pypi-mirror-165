import platform
from os import path as op
import io
from setuptools import setup

here = op.abspath(op.dirname(__file__))
# get the dependencies and installs
with io.open(op.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")
    if platform.system() == "Windows":
        all_reqs.append("pywin32")

install_requires = [x.strip() for x in all_reqs]

setup(name='biasmonitor',version='1.0.14',description ='BiasMonitor Diagnosis tool for fairness assessment.',author='MAS BiasMonitor',
install_requires=install_requires,python_requires='>=3.9.5',
packages=['biasmonitor.model','biasmonitor.fairness','biasmonitor.metrics','biasmonitor.config','biasmonitor.util','biasmonitor.resources'],
include_package_data=True,
zip_safe=False)
