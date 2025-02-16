import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from scrape import scrapeUni


load_dotenv()
TOKEN = os.getenv('TOKEN')


intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

bolumler = {"tıp": 10206,
            "tip": 10206,
            "diş": 10049,
            "dis": 10049,
            "diş-hekimliği": 10049,
            "ceng": 10024,
            "pc-müh": 10024,
            "bilgisayar-mühendisliği": 10024,
            "bilgisayar-müh": 10024,
            "kimya-mühendisliği": 10127,
            "kimya-müh": 10127,
            "fizik-müh": 10071,
            "fizik-mühendisliği": 10071,
            "yazılım-müh": 10233,
            "yazılım-mühendisliği": 10233,
            "eczacılık": 10050
            }

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty")
        return

    user_message = user_message.split()
    if user_message[0] == '!netler':
        uni = user_message[1].replace("-", " ")
        bolum = user_message[2].lower()
        await message.channel.send("Selam")
        await message.channel.send(await scrape(uni, bolumler[bolum]))
    else:
        return

async def scrape(uni, bolum):
    return await scrapeUni(uni, bolum)

@client.event
async def on_ready():
    print(f"{client.user} çalışıyor")

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f"{channel} {username}: {user_message}")
    await send_message(message, user_message)

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()