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
# Импорт библиотке для работы с json(файлом настройки)
import json


# Функция для парсинга
def pars(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    setting = json.loads(open('setting.json', encoding="utf-8").read())
    # Нахождение текстовой информации
    quotes = soup.find_all(setting.get('pars_teg'), {"class": not setting.get('ignore_class')})
    heading = soup.find_all('h1')  # Нахождение заголовка

    texts = []
    for quote in quotes:
        #print(quote)
        if quote.find('a'):
            text_href = quote.find('a').text
            href = quote.find('a')['href']
            texts.append(quote.text.replace(text_href, text_href+f"[{href}]"))
        else:
            texts.append(quote.text)

    return texts, heading


# Формирование word документа
def doc(texts, heading, url):
    document = Document()
    style = document.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(16)
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


# Фунция для работы в консоле
@click.command()
@click.option('--url', prompt='Укажите ссылку на сайт', help='Ссылка на тот сайт, информацию откуда вы хотите взять')
def cl_command(url):
    texts, heading = pars(url)
    all_path = doc(texts, heading, url)
    click.echo(f"файл создан по пути: {all_path}")


# Добавить новую инструкцию в файл настроек
def add_setting(name, val):
    setting = json.loads(open('setting.json', encoding="utf-8").read())  # dict
    setting[name].append(val)
    with open('setting.json', "w") as file:
        json.dump(setting, file)


# Удалить инструкцию из файла настроек
def delete_setting(name, val):
    setting = json.loads(open('setting.json', encoding="utf-8").read())  # dict
    setting[name].remove(val)
    with open('setting.json', "w") as file:
        json.dump(setting, file)


if __name__ == '__main__':
    #cl_command()
    #url = 'https://lenta.ru/news/2022/02/21/smoll/'
    #url = 'https://www.gazeta.ru/tech/2022/02/18/14549965.shtml?updated'
    #url = "https://www.forbes.ru/finansy/456757-cb-nacal-valutnye-intervencii-dla-stabilizacii-rubla?utm_source=yxnews&utm_medium=desktop"
    #url = 'http://holyday/'
    #texts, heading = pars(url)
    #doc(texts, heading, url)
    delete_setting('pars_teg', 'test')
