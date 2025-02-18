import aiohttp
from bs4 import BeautifulSoup
import asyncio


async def scrapeUni(uniName, bolumKodu):
    url = f"https://yokatlas.yok.gov.tr/netler-tablo.php?b={bolumKodu}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            htmlText = await response.text()  # Asenkron olarak HTML içeriğini al

    soup = BeautifulSoup(htmlText, "html.parser")
    results = []

    for row in soup.select("tr"):
        a_tag = row.select_one("td small a")

        if a_tag:
            a_text = a_tag.text.strip()  # <a> içindeki metni al
            if uniName in a_text:
                containingATag = a_tag.find_parent("td")

                tdDatas = row.find_all("td")

                uniInfos = [td.text.strip() for td in tdDatas if td != containingATag]

                if len(uniInfos) >= 15 and uniInfos[1] == "2024":  # Dizi boyutunu kontrol et
                    formatted_text = f"""
Üniversite Adı: {a_text}
Türü: {uniInfos[2]}

TYT Netleri:
  • Türkçe: {uniInfos[7]}
  • Sosyal: {uniInfos[8]}
  • Matematik: {uniInfos[9]}
  • Fen: {uniInfos[10]}

AYT Netleri:
  • Matematik: {uniInfos[11]}
  • Fizik: {uniInfos[12]}
  • Kimya: {uniInfos[13]}
  • Biyoloji: {uniInfos[14]}
                    """
                    results.append(formatted_text.strip())

    return "\n\n".join(results) if results else "Sonuç bulunamadı."



if __name__ == "__main__":
    test_result = asyncio.run(scrapeUni("BOĞAZİÇİ ÜNİVERSİTESİ", 10024))  # Örnek test
    print(test_result)
