from selenium import webdriver
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
import itertools
import requests
import urllib2

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# credit to https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def get_imgs_xy_test(link):

    page = requests.get(link)

    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    height = driver.execute_script("return document.body.scrollHeight")
    print "BC"
    print height

    driver.get(link)
    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')

    #soup = bs(driver.page_source, "html5lib")
    soup = bs(html, "html5lib")

    for elem in soup.find_all("img"):
        #print xpath_soup(elem)
        xpath = xpath_soup(elem)
        if xpath.find("noscript") < 0 and tag_visible(elem):
            element = driver.find_element_by_xpath(xpath)
            area = element.size["width"] * element.size["height"]
            if area > 0:
                print xpath
                print element.location
                print element.size
                #print element.text

file = open("university-pages.txt", "r")
links = file.read().split("\n")

for link in links:
    print link
    get_imgs_xy_test(link)

'''
for link in links:
    print link
    get_imgs_xy_test(link)
'''

'''
import lxml.html
dom =  lxml.html.fromstring(page.content)

for link in dom.xpath('//img'): # select the url in href for all a tags(links)
    print link.location
'''




'''
driver = webdriver.Firefox()
#driver = webdriver.PhantomJS()

driver.get("https://en.wikipedia.org/wiki/Donald_Glover")
element = driver.find_element_by_tag_name("img")

print element.location
print element.text
'''

'''
from lxml import html
import requests

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)
#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices
'''
