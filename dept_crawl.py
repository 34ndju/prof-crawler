import requests
import argparse
import time
import json
import StringIO
import gzip
import csv
import codecs
import random

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

count_200 = 0
count_other = 0

index_list = ["2018-09", "2018-05", "2017-51"]#, "2017-47", "2017-43"]

def search_domain_cc(domain):
    record_list = []
    for index in index_list:
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain

        response = requests.get(cc_url)
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_list.append(json.loads(record))


    return record_list

def download_page(record):
    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    resp = requests.get(prefix + record['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
    raw_data = StringIO.StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)
    data = f.read()

    response = ""

    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n\r\n', 2)
            if header.split()[1] == "200":
                return (warc, header.split()[1], response)
            else:
                print header.split()[1]
                return (warc, header.split()[1], response)
        except:
            pass

    return (None, None, response)


def extract_external_links(html_content):
    link_list = []
    parser = BeautifulSoup(html_content, "html5lib")
    links = parser.find_all("a")

    if links:
        for link in links:
            href = link.attrs.get("href")
            if href is not None:
                if domain not in href:
                    if hrefnot in link_list and href.startswith("http"):
                        link_list.append(href)
    return link_list

count = 0
if __name__ == '__main__':
    with open("brown_corpus.tsv") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        dict_list = []
        for line in reader:
            dict_list.append(line)

        while count < 200:
            idx = random.randint(0, 2190)
            line = dict_list[idx]
            domain = line["Sources1"]

            record_list = search_domain_cc(domain)
            link_list   = []
            for record in record_list:
                downloaded = download_page(record)
                if downloaded[0]:
                    code = downloaded[1]
                    if code == "200" or code == "301" or code == "302":
                        print domain
                        print code
                        break
                else:
                    print "b"

'''
import selenium.webdriver
driver = selenium.webdriver.PhantomJS()
driver.get("file:///home/nathan/Documents/professor-crawl/htmls_test/EMPNNMDTWX3HRNGTAY7ZRAF24S2Y7QX3.html")
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
#print html
file = open("htmls_test/wtf.html", "w")
file.write(html)
file.close()
'''
