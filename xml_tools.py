import xml.etree.ElementTree as ET
from tinytag import TinyTag
import os
import re

xml_path = os.path.join(os.getcwd(), r"env\Lib\artists_list.xml")


def create_xml_file(**kwargs):
    """
    initial the main xml file
    :param xml_path:
    :return:
    """
    file = open(xml_path, 'w')
    file.write("<tree>\n<artists>\n</artists>\n<other>\n<forbidden>\n</forbidden>\n<mp3_dir></mp3_dir>\n</other>\n</tree>")  # tree base
    file.close()
    forbidden_reset(xml_path)
    if kwargs.get('paths'):
        update_artist_list(xml_path, paths=kwargs, skip_check=True)



def is_readable_xml(xml_path, **kwargs):
    """
    :param xml_path: path to xml file
    :param kwargs:
    :return: et object
    """
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:  # file isn't readable or exist
        create_xml_file(**kwargs)  # create one
        tree = ET.parse(xml_path)
    except FileNotFoundError:
        create_xml_file(**kwargs)  # create one
        tree = ET.parse(xml_path)
    return tree


def forbidden_reset(xml_path):
    """
    initial all the forbidden words
    :param xml_path: path to file
    :return:
    """
    words = ["(official music video)", "(official video clip)", "(official videoclip)", "official music video",
             "(official music video)", "(Official Video)", "clip official", "(official)", "official", "(with lyrics)", "with lyrics",
             "(lyrics)", "lyrics", "(audio)"]
    tree = ET.parse(xml_path)
    root = tree.getroot()
    root = root.find('other')
    root = root.find('forbidden')
    for word in words:
        ET.SubElement(root, "word", {"value": word})
    tree.write(xml_path, encoding='utf-8')


def update_artist_list(xml_path, **kwargs):
    """
    add all known artist from song path to xml path
    :param xml_path: path to xml file
    :param songs_path: path do songs folder
    :param songs_array: songs array
    :return:
    """
    songs_array = kwargs.get('paths').get('songs_array')
    songs_path = kwargs.get('paths').get('songs_path')
    counter = 0
    if kwargs.get('skip_check'):
        tree = is_readable_xml(xml_path)
    root = tree.getroot()
    root = tree.find("artists")
    for song in songs_array:
        try:
            file = TinyTag.get(os.path.join(songs_path, song + ".mp3"))
            artist = file.artist
            if artist is not None:  # artist value isn't blank
                artist = re.sub("'|\"", '', artist)
                string = ".//artist[@value='{}']".format(artist)
                if root.find(string) is None:
                    ET.SubElement(root, "artist",{"value": artist.lower()})
                    tree.write(xml_path, encoding='utf-8')
                """else:
                    print(type(root.find("[@value={}]".format(file.artist))))"""
        except Exception:  # unsupported files
            counter += 1


def add_artist(name):
    """

    :param name:
    :return:
    """
    tree = is_readable_xml(xml_path)
    root = tree.getroot()
    root = root.find("artists")
    name = re.sub("'|\"", '', name)
    string = r".//artist[@value='{}']".format(name.lower())
    if root.find(string) is None:
        ET.SubElement(root, "artist", {"value": name.lower()})
        tree.write(xml_path, encoding='utf-8')


def find_artist(song, **kwargs):
    """

    :param song:
    :return:
    """
    tree = is_readable_xml(xml_path, **kwargs)
    root = tree.find("artists")
    for child in root.iter('artist'):
        name = child.get('value')
        if song.find(name) != -1:
            artist = name
            return artist


def dir_select(xml_path, **kwargs):
    """
    :param xml_path:
    :param kwargs:
    :return: default mp3 file dir
    """
    tree = is_readable_xml(xml_path, **kwargs)
    root = tree.find("other")
    root = root.find("mp3_dir")
    if root is not None:
        return root.text
    return None


def dir_change(xml_path, **kwargs):
    """
    get called as new folder is selected
    :param xml_path:
    :param kwargs:
    :return:
    """
    tree = is_readable_xml(xml_path, **kwargs)
    root = tree.find("other")
    root = root.find("mp3_dir")
    if root is None:
        root = root.find("other")
        elem = ET.SubElement(root, "mp3_dir")
        root.append(elem)
    text = kwargs.get("path")
    root.text = text
    tree.write(xml_path, encoding='utf-8')
