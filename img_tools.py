from urllib import request, parse
import urllib
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import artist_tools

def download_img(arr):
    index = 0
    counter = 0
    error = 0
    for __ in arr:
        try:
            path = os.path.join(os.getcwd(), r'env\Lib\imaeges')
            request.urlretrieve(arr[index], path + r"\temp{}.jpg".format(counter))
            counter += 1

        except urllib.error.HTTPError:
            error += 1
        except urllib.error.URLError:
            pass
        except:
            pass
        index += 1
        if counter == 2:  # image limit can be change
            return


def find_img(arr, query):
    url = "https://www.google.com/search?tbm=isch&q=" + query
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(req)
    except:
        url = "https://www.google.com/search?tbm=isch&q=" + heb_url(query)
        req = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(req)
    page = page.read()
    string = str(page)
    length = len(string)
    index_s = 0
    condition = False

    for index in range(length-3):
        if string[index: index+4] == "http":  # begin with http
            condition = True
            index_s = index

        if condition and string[index:index+4] == ".jpg":  # end with jpg
            temp = string[index_s:index+4]
            if temp.find('u003d') == -1:
                arr.append(string[index_s:index+4])
            condition = False

def heb_url(query):
    """
    change heberw to utf based query
    :param string: original query
    :return: utf-8 hex based code
    """
    string = (query.encode("utf-8"))
    string = str(string).replace('\\x', '%')  # change encoding format
    string = string.replace(' ', '+')
    string = string.upper()
    return string[2:len(string) - 1]  # remove b' prefix


def create_piximg(frame, file_name):
    pixmap = QtGui.QPixmap(file_name)
    pixmap = pixmap.scaled(frame.width(), frame.height(), QtCore.Qt.KeepAspectRatio)
    frame.setPixmap(pixmap)
    frame.setAlignment(QtCore.Qt.AlignCenter)

def album_art(song_array, path):
    """
    get song array and their dir and replace all their album art cover from google image
    :param song_array: the songs
    :param song_path: the path
    :return: nothing
    """
    arr = []
    img_path = os.path.join(os.getcwd(), r'env\Lib\imaeges\temp0.jpg')
    for song in song_array:
        arr = []
        query = song.replace(' ', '+')  # get vaild query
        query = query.replace('/', '') # should refers it to outer function
        query = query.replace('\\', '')
        query = query.replace('+&+', '+')
        find_img(arr, query)  # get array of urls
        download_img(arr)
        song_path = os.path.join(path, song + ".mp3")
        artist_tools.set_new_details(song_path, img=img_path)

