from setuptools import setup, find_packages

setup(
    name="SeleniumAPI",
    version="0.9",
    packages=find_packages(),
    install_requires=[
        'selenium'
    ],
    author="Tony Gonzalez",
    author_email="economiaug@gmail.com",
    description="Perform API calls with a selenium driver as the middleman",
)
