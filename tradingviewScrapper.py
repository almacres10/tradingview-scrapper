from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import date
import os

def tradingviewScrapper():

    urls = [
        'https://www.tradingview.com/markets/stocks-indonesia/market-movers-52wk-high',
        'https://www.tradingview.com/markets/stocks-indonesia/market-movers-ath',
        'https://www.tradingview.com/markets/stocks-indonesia/market-movers-gainers'
    ]

    root_path = r'C:\Users\817932702\Downloads'


    for url in urls:
        try:
            # Pengambilan konten
            page = urlopen(url)
            html = page.read().decode("utf-8")
            
            # Membuat objek BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            rows = soup.find_all('tr')

            parts = url.split('market-movers-')
            typeurl = parts[1]
            today = date.today().strftime('%y-%m-%d')

            data = []

            # Loop melalui setiap baris dan mendapatkan data dari elemen <td>
            for row in rows:
                # Mendapatkan semua elemen <td> dalam baris
                cells = row.find_all('td')

                # Mendapatkan isi teks dari setiap sel dan menambahkannya ke list data
                row_data = [cell.text.strip() for cell in cells]
                data.append(row_data)

            th_elements = rows[0].find_all('th')
            headers = [th.text.strip() for th in th_elements]

            # Membuat DataFrame dari list data
            df = pd.DataFrame(data, columns=headers)
            filename = f'Data_{str(typeurl)}_{str(today)}.xlsx'
            csv_path = os.path.join(root_path, filename)
            df.to_excel(csv_path, index=False)
            print(f'Data {url} berhasil discrapping.')
            
        except HTTPError as e:
                print('Error accessing')

tradingviewScrapper()
