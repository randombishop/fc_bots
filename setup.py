
from setuptools import setup, find_packages

setup(
    name="bots",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "bots": ["models/**/*"],
    },
    install_requires=[
      "pandas==2.2.2",
      "xgboost==2.1.0",
      "shap==0.46.0",
      "tensorflow==2.17.0",
      "tensorflow-text==2.17.0",
      "tensorflow-hub==0.16.1",
      "ollama==0.2.1",
      "wordcloud==1.9.3",
      "matplotlib==3.9.2",
      "nltk==3.9.1",
      "langdetect==1.0.9",  
      "dune_client==1.7.7",
      "google-cloud-storage==2.18.2",
      "google-cloud-aiplatform==1.59.0",
      "python-dotenv==1.0.1"
    ]
)

