from pydantic import BaseModel
# Import the necessary module
from dotenv import load_dotenv
import os

load_dotenv()

class RapidApiConfig(BaseModel):
    use_rapidapi: bool = os.getenv("USE_RAPIDAPI", False)
    use_rapidapi_checking: bool = os.getenv("USE_RAPIDAPI_CHECKING", False)
