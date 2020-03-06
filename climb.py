import requests as req
from bs4 import BeautifulSoup
import re


def getdate(a):
    a = a.replace('\xa0', '')
    a = a.replace('\r','')
    a = a.replace('\n','')
    a = a.replace(' ', '')
    date = ''
    for i in a:
        if i == '年' or i == '月':
            date += '_'
        if i == '日':
            break
        try:
            date += str(int(i))
        except:    
            pass
    return date

def summary(url):
    cent = req.get(url)
    soup = BeautifulSoup(cent.text,'html.parser')
    cont = soup.find_all('p' , class_ = 'MsoNormal')
    content = ''
    for i in cont:
        content += i.text.replace('\xa0','')
    date = cont[0].text
    date = getdate(date)
    
    return content, date      
def summary2(url):
    cent = req.get(url)
    soup = BeautifulSoup(cent.text,'html.parser')
    cont = soup.find_all('div', class_='Body')
    content = ''
    for i in cont:
        content += i.text.replace('\xa0','')
    date = cont[0].text
    date = getdate(date)
    
    return content, date
def downloadtxt():
    page = 1
    while page <= 11: 
        print(f'爬第{page}頁')
        url = 'https://www.cbc.gov.tw/lp.asp?CtNode=357&CtUnit=376&BaseDSD=33&mp=1&nowPage=' + str(page) + '&pagesize=15'
        try:
            cent = req.get(url)
            soup = BeautifulSoup(cent.text,'html.parser')
            cont = soup.find_all('li', style = 'padding-left:160px')
            for i in cont:
                if "決議新聞稿" in i.find('a')['title']:
                    content, date = summary2('https://www.cbc.gov.tw/' + i.find('a')['href'])       
                    with open( './sumdata/' + date + '.txt' , 'a', encoding = 'UTF-8') as f:
                        f.write(date)
                        f.write(content)
                        print(f'{date}.txt 下載成功!')

            page += 1
            print(f'進入第{page}頁')
        except:
            print(f'網站只到{page-1}頁!')
            page = 0