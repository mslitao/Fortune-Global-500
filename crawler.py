import general_func
from bs4 import BeautifulSoup

import sys
import os

def read_json(jo):
    items =[]
    for item in jo['default']['topics']:
        items.append(item['title'] + '|' +item['type'])

    seperator = ', '
    suggestions =seperator.join(items)
    return suggestions

#print(urllib.parse.quote('face book'))

def crawl_info(url):
    content_html = general_func.url_open(url, from_encoding='gbk')
    soup = BeautifulSoup(content_html, "html.parser")

    divs = []
    try:
        divs = soup.find('div', {'class': 'highlightedStats__wrapper--VuLob'})\
            .find('ul')\
            .find_all('li')
    except:
        print url

    country = ''
    try:
        country = divs[1].find('div').text.strip()
    except:
        print url
    #                                  dataTable__wrapper--2Y2vt dataTable__wrapper--2Y2vt
    divs = soup.find('div', {'class': 'dataTable__wrapper--2Y2vt dataTable__wrapper--2Y2vt'}) \
        .find('table') \
        .find_all('tr')
    #print(len(divs))
    ceo = divs[0].find_all('td')[1].find('div').text.strip()
    sector =divs[1].find_all('td')[1].text.strip()
    industry = divs[2].find_all('td')[1].text.strip()
    hqlocation = divs[3].find_all('td')[1].text.strip()
    website = divs[4].find_all('td')[1].text.strip()
    yearsonlist = divs[5].find_all('td')[1].text.strip()
    employees = divs[6].find_all('td')[1].text.strip()

    #print(industry)

    #print(sector)
    return {'country': country,
            'ceo': ceo,
             'sector': sector,
             'industry': industry,
            'hqlocation': hqlocation,
            'website': website,
            'yearsonlist': yearsonlist,
            'employees': employees
            }


def crawl(soup):
    compList = []
    divs = soup.find_all('div', {'class': 'rt-tr-group'})
    print(len(divs))

    index = 0
    for divItem in divs:
        valDivs = divItem.find_all('div', {'class': 'rt-td'})
        #print(len(valDivs))
        #print(valDivs[0].find('a')['href'])
        index +=1

        detailUrl = valDivs[0].find('a')['href']
        detailInfo = crawl_info(detailUrl)
        compList.append(
            {'rank': valDivs[0].text.strip(),
             'name': valDivs[1].text.strip(),
             'revenues': valDivs[2].text.strip(),
             'revenues_percent_change': valDivs[3].text.strip(),
             'profits': valDivs[4].text.strip(),
             'assets': valDivs[5].text.strip(),
             'profits_percent_change': valDivs[6].text.strip(),
             'employees': valDivs[7].text.strip(),
             'rank_change': valDivs[8].text.strip(),
             'url':detailUrl,
             'country': detailInfo['country'],
             'sector': detailInfo['sector'],
             'industry': detailInfo['industry'],
             'ceo': detailInfo['ceo'],
             'hqlocation': detailInfo['hqlocation'],
             'website': detailInfo['website']
             });
        if(index > 100):
            break

    return compList

if __name__ == '__main__':
    outputDir = '<Local Folder>';
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    reload(sys)
    sys.setdefaultencoding('utf8')

    #content_html = general_func.url_open('https://fortune.com/global500/2019/bp', from_encoding='gbk')

    indexList = {1,2,3,4,5}
    for index in indexList:
        url = "E:\\UIUC\\Python500\\Fortune" + str(index) + ".html"
        page = open(url)

        soup = BeautifulSoup(page.read(), "html.parser")
        results = crawl(soup)

        data_fw = open(os.path.join(outputDir, 'Fortune-Global-2019-'+ str(index)+ '.tsv'), 'w')
        print(results)
        for item in results:
            data_fw.write(item["rank"] + "\t" + item["name"] + "\t" + item["revenues"] + "\t" + item["revenues_percent_change"] +
                         "\t" + item["profits"] +"\t" + item["assets"]+"\t" + item["profits_percent_change"]+"\t" + item["employees"]+
                          "\t" + item["rank_change"] +"\t" + item["url"]+"\t" + item["country"] +"\t" + item["sector"] +"\t" + item["industry"] +
                          "\t" + item["ceo"] +"\t" + item["hqlocation"] +"\t" + item["website"]
                          )
            data_fw.write("\n")

        print("finished")