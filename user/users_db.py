import os
from dotenv import load_dotenv
from dependencies import pwd_hasher


load_dotenv()


users_data = {
    os.environ["APP_USERNAME"]: {
        "username": os.environ.get("APP_USERNAME"),
        "full_name": os.environ.get("FULL_NAME"),
        "email": os.environ.get("EMAIL"),
        "hashed_password": pwd_hasher.hash(os.environ.get("PASSWORD")),
        "disabled": os.environ.get("DISABLED").lower() == "true",
    }
}
