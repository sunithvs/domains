from dotenv import load_dotenv
import os

load_dotenv(".env")
settings = os.getenv('SETTINGS')
debug = os.getenv('DEBUG')


if settings == "prod":
    print("PRODUCTION SERVER")
    from .prod_settings import *


else:
    print("DEV SERVER")
    from .dev_settings import *
