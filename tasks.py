from selenium import webdriver
from bs4 import BeautifulSoup as bs
from bs4 import Comment
from bs4.element import Comment
import itertools
import csv
import re

from lxml import etree
from xml.etree.ElementTree import ElementTree
from lxml.etree import tostring

def write_coord_csv(html):

    seen = set()

    file = open("out.csv", "w")
    file.write("text_content, top_left, top_right, bottom_left, bottom_right")
    file.write("\n")

    driver = webdriver.Chrome()
    driver.get("data:text/html;charset=utf-8," + html)

    # annotate xpos and ypos for images
    for img_sel_elem in driver.find_elements_by_tag_name("img"):
        center = (img_sel_elem.location["x"] + img_sel_elem.size["width"]/2, img_sel_elem.location["y"] + img_sel_elem.size["height"]/2)
        driver.execute_script("arguments[0].setAttribute('xpos','%s')" % str( int(center[0]) ), img_sel_elem)
        driver.execute_script("arguments[0].setAttribute('ypos','%s')" % str( int(center[1]) ), img_sel_elem)

    # remove all scripts
    soup = bs(driver.page_source, "html5lib")
    [x.extract() for x in soup.findAll('script')]

    # remove all comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    e = etree.HTML(str(soup))
    tree = etree.ElementTree(e)
    text_elements = [element for element in e.getiterator() if element.text and len(element.text) > 1]

    # extract all text and annotate xpos and ypos for text
    for elem in text_elements:
        xpath = tree.getpath(elem)
        text_content = elem.text
        if xpath not in seen:
            seen.add(xpath)
            element = driver.find_element_by_xpath(xpath)
            area = element.size["width"] * element.size["height"]
            if area > 0:
                text_content = "%s" % element.text
                text_content.replace("\n", " ").replace("\r", " ").replace("\"", "&quot")

                if len(text_content) > 1:
                    top_left = (element.location["x"], element.location["y"])
                    top_right = (element.location["x"] + element.size["width"], element.location["y"])
                    bottom_left = (element.location["x"], element.location["y"] + element.size["height"])
                    bottom_right = (element.location["x"] + element.size["width"], element.location["y"] + element.size["height"])

                    center = (element.location["x"] + element.size["width"]/2, element.location["y"] + element.size["height"]/2)

                    elem.set("xpos", str( int(center[0]) ))
                    elem.set("ypos", str( int(center[1]) ))

                    line = "\"{0}\",\"{1}\",\"{2}\",\"{3}\",\"{4}\"".format(text_content, top_left, top_right, bottom_left, bottom_right)

                    seen.add(text_content)

                    file.write(line)
                    file.write("\n")

    new_html = open("out.html", "w")
    new_html.write(tostring(e))
    new_html.close()


if __name__ == "__main__":
    #file = open("html/http__www.forwarddatalab.org_.html", "r")
    #file = open("kevin.html", "r")
    file = open("html/Forward Data Lab.html", "r")
    html = file.read()
    file.close()
    write_coord_csv(html)
