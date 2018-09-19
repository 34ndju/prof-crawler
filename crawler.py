from bs4 import BeautifulSoup as bs
from selenium import webdriver
from pyvirtualdisplay import Display
import os
import time
import re

base = "https://cs.illinois.edu"
directory = "htmls"
timeout = 2
surr_text_max_len = 30

def is_link(url):
    if url.find("http") == 0 or url[0] == "/":
        return True
    else:
        return False

def extract_soup(link):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    try:
        driver.get(link)
        html = driver.page_source

        display.stop()
        driver.quit()

        soup = bs(html, "html5lib")

        return soup
    except:
        return None

def extract_links(soup):
    links = []
    for a in soup.find_all("a", href=True):
        link = a['href']
        if is_link(link):
            if link[0] == "/":
                link = base + link
            links.append(link)
    return links

def get_surr_text(tag):
    text = []
    stack = []

    stack.append(tag)
    curr = tag.parent

    prev_text = ""
    post_text = ""

    while len(curr.text.strip()) == 0:
        stack.append(curr)
        if curr.parent:
            curr = curr.parent

    containing_parent = stack[-1]

    curr = containing_parent.previous_sibling
    while curr and len(prev_text) < surr_text_max_len:
        try:
            if len(curr.text.strip()) > 0:
                prev_text = curr.text.replace("\n", "").replace("\t", "").strip() + " " + prev_text
        except:
            pass
        curr = curr.previous_sibling

    curr = containing_parent.next_sibling
    while curr and len(post_text) < surr_text_max_len:
        try:
            if len(curr.text.strip()) > 0:
                post_text = curr.text.replace("\n", " ").replace("\t", " ").strip() + " " + post_text
        except:
            pass
        curr = curr.next_sibling

    return [prev_text, post_text]


def crawl(start_link, depth, visited):
    if depth == 0 or start_link in visited:
        return

    print "sleeping"
    time.sleep(timeout)
    print "awake"
    visited.add(start_link)
    print start_link

    if not os.path.exists(directory):
        os.makedirs(directory)

    soup = extract_soup(start_link)
    if not soup:
        return
    links = extract_links(soup)

    for img in soup.find_all("img"):
        print get_surr_text(img)

    new_filename = "{0}/{1}".format(directory, start_link.replace("/", "*")) # resolves nesting with "/" in links

    file = open(new_filename, "w")
    file.write(str(soup))
    file.close()

    if start_link.find(base) > -1:
        for link in links:
            crawl(link, depth-1, visited)

if __name__ == "__main__":
    crawl(base, 2, set())
