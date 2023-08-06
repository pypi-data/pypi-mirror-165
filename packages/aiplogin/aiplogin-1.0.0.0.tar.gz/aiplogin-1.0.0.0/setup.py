from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "requirements.txt")) as f:
    requirements = [l for l in f.readlines() if l]

setup(
    name="aiplogin",
    version="1.0.0.0",
    description="AI Platform utilities",
    author="Nick Chang",
    author_email="chichang@ea.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="login",
    packages=find_packages(),
    install_requires=requirements,
    extras_require={},
    zip_safe=False
)
