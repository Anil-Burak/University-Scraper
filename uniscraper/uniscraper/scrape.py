import aiohttp
from bs4 import BeautifulSoup
import asyncio
import os, dotenv

# TODO: Sıralama eklemek çok yavaşlatıyor, başka bir yöntem bulunmalı.

dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')

headers = {'User-Agent':
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}  # Trying to make bot seem like a human


async def scrapeUni(uniName, bolumKodu, siralama):
    url = f"https://yokatlas.yok.gov.tr/netler-tablo.php?b={bolumKodu}"

    session = aiohttp.ClientSession()
    async with session.get(url, headers=headers) as response:
        htmlText = await response.text()

    soup = BeautifulSoup(htmlText, "html.parser")
    results = []
    siralamalar = ""  # If it's not needed, it will only return an empty string
    for row in soup.select("tr"):
        a_tag = row.select_one("td small a")

        if a_tag:
            a_text = a_tag.text.strip()
            if uniName in a_text:
                containingATag = a_tag.find_parent("td")

                tdDatas = row.find_all("td")

                uniInfos = [td.text.strip() for td in tdDatas if td != containingATag]

                if uniInfos[1] == "2024" and siralama:
                    link = a_tag.get("href").strip("lisans")

                    async with session.get(
                            f"https://proxy.scrapeops.io/v1/?api_key={API_KEY}"
                            f"&url=https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_3{link}",  # If proxy is not used, the site catches the bot.
                            headers=headers) as siralamaResponse:

                        siralamaText = await siralamaResponse.text()
                        siralamaSoup = BeautifulSoup(siralamaText, "html.parser")
                        siralamaInfos = siralamaSoup.select("tr td")
                        if siralamaInfos:
                            siralamalar = f"""\nGenel Kontenjan: {siralamaInfos[11].text}\nOkul Birincisi: {siralamaInfos[16].text}"""

                if len(uniInfos) >= 15 and uniInfos[1] == "2024":
                    formatted_text = f"""
__Üniversite Adı:__ {a_text}
Türü: {uniInfos[2]}
{siralamalar}

OBP: {uniInfos[5]}
**TYT Netleri:**
  • Türkçe: {uniInfos[7]}
  • Sosyal: {uniInfos[8]}
  • Matematik: {uniInfos[9]}
  • Fen: {uniInfos[10]}

**AYT Netleri:**
  • Matematik: {uniInfos[11]}
  • Fizik: {uniInfos[12]}
  • Kimya: {uniInfos[13]}
  • Biyoloji: {uniInfos[14]}
-----------------------------------------------------
                    """
                    results.append(formatted_text.strip())
    await session.close()
    return "\n\n".join(results) if results else "Sonuç bulunamadı."


if __name__ == "__main__":
    test_result = asyncio.run(scrapeUni("MARMARA ÜNİVERSİTESİ", 10206, 1))
    print(test_result)
