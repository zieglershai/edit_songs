import bs4 as bs
import urllib.request
import re, time
import artist_tools
from selenium import webdriver
import signal

def heb_query(string):
    """
    change heberw to utf based query
    :param string: original query
    :return: utf-8 hex based code
    """
    string = (string.encode("utf-8"))
    string = str(string).replace('\\x', '%')  # change encoding format
    string = string.replace(' ', '+')
    string = string.upper()
    return string[2:len(string)-1]  # remove b' prefix


def nospace(string):
    """
    remove all prefix and suffix space
    :param string: string
    :return:string with no spaces padding
    """
    cond = True
    length = len(string)
    while cond:
        cond = False
        if string[0] == " ":  # the beginnig
            string = string[1:]
            cond = True
            length -= 1
        if string[length-1] == " ":  # the ending
            string = string[:length-1]
            cond = True
            length -= 1
    return string


def find_artist(string):
    """
    return the artist of the giveen if such was found otherwise return "" object
    :param string: the song name
    :return: artist name (string)
    """
    string = nospace(string)
    artist = shironet(string)  # hebrew search
    if artist is None:
        artist = azlyrics(string)  # language search
    return artist

def shironet(string):
    """
    search for artinst name in shironet
    :param string: song name
    :return: artist value
    """
    string = re.split('\s|\-', string)  # split to words
    length = len(string)  # num of words
    for i in reversed(range(length)):
        foreword = ' '.join(string[:i + 1])
        backword = ' '.join(string[length - i - 1:])
        artist = shironet_aux(foreword)  # search artist
        if artist is not None:  # found one
            return artist
        artist = shironet_aux(backword)
        if artist is not None:
            return artist
    return ""  # didnt find one


def shironet_aux(string):
    """
    search artist in shironet
    :param string: song name
    :return: artist name of the song
    """
    quary = "https://shironet.mako.co.il/search?q="
    quary = quary + heb_query(string)  # get the song name in query format
    source = urllib.request.urlopen(quary).read()
    soup = bs.BeautifulSoup(source, 'lxml')  # use bs4 object
    try:
        element = soup.find('a', class_="search_link_name_big")  # search result box by css
        element = element.find_next('a')  # get the artist box
        return element.text
    except AttributeError:
        return ""  # if element is none


def azlyrics(string):
    """
    search artist in azlyrics site
    :param string: song name
    :return: artist name of the song
    """
    query = "https://search.azlyrics.com/search.php?q=" + heb_query(string)  # get the song name in query format
    source = urllib.request.urlopen(query).read()
    soup = bs.BeautifulSoup(source, 'lxml')  # get bs4 object of the page
    try:
        for element in soup.find_all('div', class_="panel"):
            if element.text.find("Song results:") != -1:
                return element.find_all('b')[2].text  # get the artist name
    except AttributeError:  # didnt find anything
        return ""
    except IndexError:  # page format was changed
        return ""


def query_make(string):
    """
    taking a simple string and transform it to google search query
    :param string:
    :return:
    """
    string = string + " genius"
    string = string.replace(' ', '+')  # get vaild query
    string = string.replace('/', '')
    string = string.replace('\\', '')
    return string.replace('+&+', '+')


def google_sarch(string):
    """
    search for the artist and the title in google search page
    :param string:
    :return:
    """
    query = query_make(string)
    url = "https://www.google.com/search?q=" + query
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(req)
    except:
        url = "https://www.google.com/search?q=" + heb_query(query)
        req = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(req)
    source = page.read()
    soup = bs.BeautifulSoup(source, 'lxml')  # use bs4 object
    elements = soup.find_all('h3', class_="LC20lb DKV0Md")  # search result box by css
    for element in elements:
        text = element.text
        if text.find("מילים לשיר ") != -1:  # hebrew song which shironet has
            index = text.find("-")
            return text[index+2:text.find("-", index+1)-1], text[11:index-1]
        else:  # probably english song
            result = term_search(text)
            if result is not None:
                return result[0], result[1]
    return sel_search(url)  # return values


def term_search(text):
    """

    :return:
    """
    words = [" Lyrics | Genius Lyrics", " Lyrics - Genius", " Lyrics - ...", " Lyrics - ...",
             " Lyrics | Genius ...", " - Genius", " Lyrics | ...", " ... - Genius"]  # all possible patterns
    for phrase in words:  # for each possible pattern
        if text.find(phrase) != -1:  # if pattern suits
            text = text.replace(phrase, "")  # extract info
            index = text.rfind("–")
            return text[:index - 1], text[index + 1:]


def sel_search(url):
    """
    after google search failed use seleinum to find java made info
    """
    driver = webdriver.PhantomJS(executable_path = r"C:\Users\Shai\Downloads\phantomjs\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs")
    driver.set_window_size(1120, 550)
    driver.get(url)
    time.sleep(0.5)
    soup = bs.BeautifulSoup(driver.page_source, 'lxml')
    elements = soup.find_all('div', class_="BNeawe vvjwJb AP7Wnd")  # search result box by css
    for element in elements:
        text = element.text
        result = term_search(text)
        if result is not None:
            driver.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
            driver.quit()
            return result[0], result[1]
    return "", ""  # return values


def album_search(string):
    """
    this data is created by java script so it better to use selenium
    link:https://stackoverflow.com/questions/19918153/getting-different-results-for-web-scraping

    :param string:
    :return:
    """
    string = string + " album"
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url)
    time.sleep(0.5)
    soup = bs.BeautifulSoup(driver.page_source, 'lxml')
    elements = soup.find_all('div', class_="BNeawe vvjwJb AP7Wnd")  # search result box by css
    words = [" Lyrics | Genius Lyrics", " Lyrics - Genius", " Lyrics - ...", " Lyrics - ...",
             " Lyrics | Genius ...", " - Genius"]  # all possible patterns
    name = ""
    artist = ""
    for element in elements:
        text = element.text
        for phrase in words:  # for each possible pattern
            if text.find(phrase) != -1:  # if pattern suits
                text = text.replace(phrase, "")  # extract info
                index = text.rfind("–")
                artist = text[:index - 1]
                name = text[index + 1:]
                driver.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
                driver.quit()
                return artist, name  # return values
    return artist, name  # return values
    elements = soup.find_all('a', class_="FLP8od")  # search result box by css