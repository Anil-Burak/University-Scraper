import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from scrape import scrapeUni
import json

load_dotenv()
TOKEN = os.getenv('TOKEN')


intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


def load_bolumler():
    with open("bolumler.json", "r", encoding="utf-8") as file:
        return json.load(file)


bolumler = load_bolumler()


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty")
        return

    user_message = user_message.split()

    if user_message[0] == "!help":
        await message.channel.send("**Sadece net bilgileri için:** \n"
                                   "->    !netler ÜNİVERSİTE-İSMİ bölüm")
        await message.channel.send("**Netler ve sıralamalar için:**\n"
                                   "->   !sn ÜNİVERSİTE-İSMİ bölüm\n"
                                   "**Bu komuta yanıt biraz daha uzun sürede gelecektir.**")

    if user_message[0] == '!netler':
        try:
            uni = user_message[1].replace("-", " ")
            bolum = bolumler[user_message[2].lower()]
            await message.channel.send("Selam")
            await message.channel.send(await scrape(uni, bolum, 0))
        except KeyError:
            await message.channel.send("Girdiğiniz bölüm bulunamadı")
            return
        except:
            await message.channel.send("Doğru şekilde girmediniz")
            return

    elif user_message[0] == '!sn':
        try:
            uni = user_message[1].replace("-", " ")
            bolum = bolumler[user_message[2].lower()]
            await message.channel.send("Selam")
            await message.channel.send(await scrape(uni, bolum, 1))
        except KeyError:
            await message.channel.send("Girdiğiniz bölüm bulunamadı")
            return
        except:
            await message.channel.send("Doğru şekilde girmediniz")
            return

    else:
        return


async def scrape(uni, bolum,siralama):
    return await scrapeUni(uni, bolum,siralama)


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
