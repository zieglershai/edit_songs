import re
# import wikipediaapi
from langdetect import detect
import wikipedia


language = {"en": ["band", "singer"], "he": ["להקה", "להקת", "זמרת", "זמר"]}




"""def wikiapi(string, lang):
    
    search artist name using wikiapi module
    :param string: song name
    :param lang: language
    :return: strength of the option
    
    wiki = wikipediaapi.Wikipedia(lang)  # open connection
    return wikisearch(string, wiki, lang)  # search"""


def wikisearch(string, wiki, lang):
    """
    search using wikiapi module
    :param string: song name
    :param wiki: wikiapi object
    :param lang: language
    :return: strength of the option
    """
    page = wiki.page(string)  # search for the page
    if string != "" and page.exists():  # if such page exist
        return strength(page, lang)  # calculate strength
    return -1


def strength(page, lang):
    """
    calculate the strength of the page
    :param page: wikiapi.page object
    :param lang: language
    :return: strength of the page or -1 if not found
    """
    summ = page.summary  #
    for word in language.get(lang):  # search for band artists generic name
        if word in summ:  # found such
            return 100  # if looking for best result need to calc strength
    return -1


def find_artist(string):
    """
    find song artist using wikipedia as source
    :param string: song name
    :return: the
    """
    lang = 'en' if detect(string) != 'he' else 'he'  # decide language
    string = nospace(string)
    string = first_search(string, lang)
    p = re.compile('(\n|\r|\t)')  # remove unnecessary chars
    string = p.sub('', string)
    return string


def first_search(string, lang):
    """
    split the sting to sub strings and call calc
    :param string: song name
    :param lang: language
    :return: artist name
    """
    wikipedia.set_lang(lang)  # set lang
    string = nospace(string)
    string = re.split('\s|-', string)  # split to words
    length = len(string)  # num of words
    for i in reversed(range(length)):
        foreword = ' '.join(string[:i + 1])  # song name from begging to end
        backword = ' '.join(string[length - i - 1:])  # song name from end to start
        temp, beststr = calc(foreword, lang)  # get value and the artist
        if temp != -1:  # if found artist in the article
            return beststr  # if looking for best result need to compare strength
        temp, beststr = calc(backword, lang)
        if temp != -1:
            return beststr
    return ""


def nospace(string):
    """
    remove prefix and suffix spacebar
    :param string: string
    :return: string with no spacebar
    """
    cond = True
    length = len(string)
    while cond:
        cond = False
        if string[0] == " ":  # the beginning
            string = string[1:]
            cond = True
            length -= 1
        if string[length-1] == " ":  # the ending
            string = string[:length-1]
            cond = True
            length -= 1
    return string


def calc(string, lang):
    """
    search and decide the chance of the artist to be related to the song
    :param string: name
    :param lang: language
    :return: value between 0- good to 100- bad  or -1 not found
    """
    temp = -1
    try:
        page = wikipedia.page(string, redirect=False)  # search page
        summ = page.summary  # get summary
        try:
            summ = summ[:150]  # only first 150 chars are relevant
        except IndexError:  # if less than 150 chars
            pass
        title = page.title  # get page title
        for word in language.get(lang):  # search for artist generic name
            if word in summ:
                temp = summ.find(word) - len(title)  # calculate the strength
                if summ.find('song') > summ.find(word) or summ.find('song') == -1:
                    return temp, title  # if it isn't song page

    except wikipedia.DisambiguationError as ex:  # if there was more than one page related to the name
        word = select_page(ex, lang)   # search for band article
        if word != "none":  # if found page
            temp = calc(word, lang)  # redo this function for the correct page
    except wikipedia.PageError:  # wikipedia module failed try wikipedia api
        temp = wikiapi(string, lang)  # search with wikiapi module
    return temp, string


def select_page(ex, lang):
    """
    search for band article from various options
    :param ex: DisambpaiguationError object
    :param lang: language
    :return: page name if found else -1
    """
    for value in ex.options:  # for each option
        for word in language.get(lang):  # search for artists generic name
            if value.find(str('(' + word + ')')) != -1:
                return value  # page found
    return "none"


