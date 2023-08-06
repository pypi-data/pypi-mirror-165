from setuptools import find_packages
from setuptools import setup

setup(
    name="enstat",
    license="MIT",
    author="Tom de Geus",
    author_email="tom@geus.me",
    description="Ensemble averages",
    long_description="Ensemble averages",
    keywords="Statistics, Ensemble",
    url="https://github.com/tdegeus/enstat",
    packages=find_packages(),
    use_scm_version={"write_to": "enstat/_version.py"},
    setup_requires=["setuptools_scm"],
    install_requires=["numpy"],
)
