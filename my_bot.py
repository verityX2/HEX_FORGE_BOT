import os
from pathlib import Path
from dotenv import load_dotenv
import pyrobale

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

token = os.getenv("BOT_TOKEN")

client = pyrobale.Client(token)

@client.on_command("start")
async def start(message: pyrobale.Message):
    await message.reply("سلام! خوش اومدی 👋")

client.run()