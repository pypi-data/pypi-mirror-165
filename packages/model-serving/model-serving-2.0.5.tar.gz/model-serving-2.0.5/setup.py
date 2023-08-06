from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("VERSION") as f:
    version = f.read().strip()

setup(
    name="model-serving",
    version=version,
    description='Gunicorn Flask based library for serving ML Models, built by the ml-ops and science team at Aylien',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    readme="README.md",
    packages=["aylien_model_serving","examples","test"],
    data_files=['requirements.txt','LICENSE','VERSION','README.md'],
    install_requires=requirements,
    include_package_data=True
)
