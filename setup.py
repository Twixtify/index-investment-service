from setuptools import setup, find_packages

setup(
    name="investopy",
    version="0.0.1",
    author="Twixstify",
    packages=find_packages(),
    requires=["pandas",
              "numpy",
              "requests",
              "beautifulsoup4",
              "selenium"]
)
