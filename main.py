# Импорт библиотек для парсинга данных
import os

import requests
from bs4 import BeautifulSoup
# Импорт библиотек для работы с Word
from docx import Document
from docx.shared import Pt


# Функция для парсинга
def pars(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('main')

    text = ""
    for quote in quotes:
        text += quote.text

    return text


def doc(text, url):
    document = Document()
    style = document.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)
    document.add_paragraph(text)
    head = document.add_heading('Основы работы с файлами Microsoft Word на Python.')

    path = url.split("://")[1].split("/")
    path = '\\'.join([str(x) for x in path])
    if not os.path.exists(path):
        os.makedirs(path)
    document.save(os.getcwd()+"\\"+path+'restyled.docx')


if __name__ == '__main__':
    url = 'https://lenta.ru/news/2022/02/21/smoll/'
    text = pars(url)
    doc(text, url)
