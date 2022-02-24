# Импорт библиотек для парсинга данных
import requests
from bs4 import BeautifulSoup
# Импорт библиотек для работы с Word
import os
from docx import Document
from docx.shared import Pt
from docx.shared import Mm
# Импорт библиотек для работы с консолью
import click


# Функция для парсинга
def pars(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('p')
    heading = soup.find_all('h1')

    texts = []
    for quote in quotes:
        if quote.find('a'):
            text_href = quote.find('a').text
            href = quote.find('a')['href']
            texts.append(quote.text.replace(text_href, text_href+f"[{href}]"))
        else:
            texts.append(quote.text)

    return texts, heading


def doc(texts, heading, url):
    document = Document()
    style = document.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(16)
    #document.add_heading(heading[0].text)
    run = document.add_paragraph().add_run(heading[0].text)
    run.font.size = Pt(24)
    run.bold = True
    document.add_paragraph(" ")
    for text in texts:
        paragraph = document.add_paragraph(text)
        fmt = paragraph.paragraph_format
        fmt.space_before = Mm(0)
        fmt.space_after = Mm(0)
        paragraph = document.add_paragraph(" ")
        fmt = paragraph.paragraph_format
        fmt.space_before = Mm(0)
        fmt.space_after = Mm(0)

    if "?" in url:
        url = url.replace("?", "/")

    path = url.split("://")[1].split("/")
    path = '\\'.join([str(x) for x in path])
    if not os.path.exists(path):
        os.makedirs(path)
    all_path = os.getcwd()+"\\"+path+'\\restyled.docx'
    document.save(all_path)
    return all_path


@click.command()
@click.option('--url', prompt='Укажите ссылку на сайт', help='Ссылка на тот сайт, информацию откуда вы хотите взять')
def cl_command(url):
    texts, heading = pars(url)
    all_path = doc(texts, heading, url)
    click.echo(f"файл создан по пути: {all_path}")


if __name__ == '__main__':
    #cl_command()
    #url = 'https://lenta.ru/news/2022/02/21/smoll/'
    url = 'https://www.gazeta.ru/tech/2022/02/18/14549965.shtml?updated'
    #url = "https://www.forbes.ru/finansy/456757-cb-nacal-valutnye-intervencii-dla-stabilizacii-rubla?utm_source=yxnews&utm_medium=desktop"
    texts, heading = pars(url)
    doc(texts, heading, url)
