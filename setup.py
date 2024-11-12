
from setuptools import setup, find_packages

setup(
    name="bots",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
      "dune_client==1.7.7",
      "pandas==2.2.2",
      "google-cloud-storage",
      "ollama==0.2.1",
      "wordcloud==1.9.3",
      "matplotlib==3.9.2",
      "python-dotenv==1.0.1"
    ]
)

