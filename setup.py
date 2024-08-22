
from setuptools import setup, find_packages

setup(
    name="bots",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "google-cloud-pubsub",
        "google-cloud-aiplatform",
        "psycopg2-binary==2.9.9",
        "xgboost==2.1.0",
        "shap==0.46.0",
        "tensorflow==2.17.0",
        "tensorflow-text==2.17.0",
        "tensorflow-hub==0.16.1",
        "python-dotenv==1.0.1",
        "ollama==0.2.1",
        "matplotlib==3.9.2"
    ]
)

