import os
from dotenv import load_dotenv

load_dotenv()

# IBM Cloud Configuration
IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY", "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_SPACE_ID = os.getenv("IBM_SPACE_ID", "")
IBM_WATSONX_URL = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
GRANITE_MODEL = os.getenv("GRANITE_MODEL", "ibm/granite-13b-chat-v2")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"