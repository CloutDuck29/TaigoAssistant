from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", "-1000000000"))  # Значение по умолчанию
