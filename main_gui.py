# -*- coding: utf-8 -*-
import os
import artist_tools, img_tools, xml_tools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog
from tinytag import TinyTag
import xml.etree.ElementTree as ET
import re
import eyed3
import workers


xml_path = os.path.join(os.getcwd(), r"env\Lib\artists_list.xml")
img_path = os.path.join(os.getcwd(), r'env\Lib\imaeges\temp0.jpg')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(652, 556)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.left_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_frame.setGeometry(QtCore.QRect(-1, -1, 171, 491))
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.dir_lbl = QtWidgets.QLabel(self.left_frame)
        self.dir_lbl.setGeometry(QtCore.QRect(20, 10, 121, 21))
        self.dir_lbl.setObjectName("dir_lbl")
        self.song_list_lbl = QtWidgets.QLabel(self.left_frame)
        self.song_list_lbl.setGeometry(QtCore.QRect(20, 70, 81, 20))
        self.song_list_lbl.setObjectName("song_list_lbl")
        self.song_list = QtWidgets.QListView(self.left_frame)
        self.song_list.setGeometry(QtCore.QRect(20, 90, 131, 321))
        self.song_list.setObjectName("song_list")
        self.next_btn = QtWidgets.QPushButton(self.left_frame)
        self.next_btn.setGeometry(QtCore.QRect(90, 440, 61, 23))
        self.next_btn.setObjectName("next_btn")
        self.prev_btn = QtWidgets.QPushButton(self.left_frame)
        self.prev_btn.setGeometry(QtCore.QRect(20, 440, 61, 23))
        self.prev_btn.setObjectName("prev_btn")
        self.left_box = QtWidgets.QGroupBox(self.left_frame)
        self.left_box.setGeometry(QtCore.QRect(10, 10, 161, 461))
        self.left_box.setTitle("")
        self.left_box.setObjectName("left_box")
        self.dir_set_btn = QtWidgets.QPushButton(self.left_box)
        self.dir_set_btn.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.dir_set_btn.setObjectName("dir_set_btn")
        self.left_box.raise_()
        self.dir_lbl.raise_()
        self.song_list_lbl.raise_()
        self.song_list.raise_()
        self.next_btn.raise_()
        self.prev_btn.raise_()
        self.top_frame = QtWidgets.QFrame(self.centralwidget)
        self.top_frame.setGeometry(QtCore.QRect(170, 10, 481, 191))
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")
        self.name_lbl = QtWidgets.QLabel(self.top_frame)
        self.name_lbl.setGeometry(QtCore.QRect(20, 10, 191, 16))
        self.name_lbl.setObjectName("name_lbl")
        self.title_lbl = QtWidgets.QLabel(self.top_frame)
        self.title_lbl.setGeometry(QtCore.QRect(20, 50, 181, 16))
        self.title_lbl.setObjectName("title_lbl")
        self.artist_lbl = QtWidgets.QLabel(self.top_frame)
        self.artist_lbl.setGeometry(QtCore.QRect(20, 90, 181, 16))
        self.artist_lbl.setObjectName("artist_lbl")
        self.cur_img = QtWidgets.QLabel(self.top_frame)
        self.cur_img.setGeometry(QtCore.QRect(330, 20, 121, 111))
        self.cur_img.setAutoFillBackground(True)
        self.cur_img.setText("")
        self.cur_img.setObjectName("cur_img")
        self.top_box = QtWidgets.QGroupBox(self.top_frame)
        self.top_box.setGeometry(QtCore.QRect(0, 0, 481, 191))
        self.top_box.setTitle("")
        self.top_box.setObjectName("top_box")
        self.top_box.raise_()
        self.name_lbl.raise_()
        self.title_lbl.raise_()
        self.artist_lbl.raise_()
        self.cur_img.raise_()
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(170, 200, 481, 281))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.left_img_frame = QtWidgets.QFrame(self.frame)
        self.left_img_frame.setGeometry(QtCore.QRect(0, 0, 241, 281))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.left_img_frame.setPalette(palette)
        self.left_img_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_img_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_img_frame.setObjectName("left_img_frame")
        self.img_left = QtWidgets.QLabel(self.left_img_frame)
        self.img_left.setGeometry(QtCore.QRect(60, 40, 121, 111))
        self.img_left.setAutoFillBackground(True)
        self.img_left.setText("")
        self.img_left.setObjectName("img_left")
        self.left_img_title = QtWidgets.QLabel(self.left_img_frame)
        self.left_img_title.setGeometry(QtCore.QRect(90, 10, 91, 16))
        self.left_img_title.setObjectName("left_img_title")
        self.left_artist_lbl = QtWidgets.QLabel(self.left_img_frame)
        self.left_artist_lbl.setGeometry(QtCore.QRect(10, 210, 111, 16))
        self.left_artist_lbl.setObjectName("left_artist_lbl")
        self.lef_artist_edit = QtWidgets.QLineEdit(self.left_img_frame)
        self.lef_artist_edit.setGeometry(QtCore.QRect(80, 210, 113, 20))
        self.lef_artist_edit.setObjectName("lef_artist_edit")
        self.left_title_edit = QtWidgets.QLineEdit(self.left_img_frame)
        self.left_title_edit.setGeometry(QtCore.QRect(80, 170, 113, 20))
        self.left_title_edit.setObjectName("left_title_edit")
        self.left_title_lbl = QtWidgets.QLabel(self.left_img_frame)
        self.left_title_lbl.setGeometry(QtCore.QRect(10, 170, 91, 16))
        self.left_title_lbl.setObjectName("left_title_lbl")
        self.left_set_btn = QtWidgets.QPushButton(self.left_img_frame)
        self.left_set_btn.setGeometry(QtCore.QRect(90, 240, 61, 23))
        self.left_set_btn.setObjectName("left_set_btn")
        self.left_img_box = QtWidgets.QGroupBox(self.left_img_frame)
        self.left_img_box.setGeometry(QtCore.QRect(0, 0, 241, 271))
        self.left_img_box.setTitle("")
        self.left_img_box.setObjectName("left_img_box")
        self.left_img_box.raise_()
        self.img_left.raise_()
        self.left_img_title.raise_()
        self.left_artist_lbl.raise_()
        self.lef_artist_edit.raise_()
        self.left_title_edit.raise_()
        self.left_title_lbl.raise_()
        self.left_set_btn.raise_()
        self.right_img_frame = QtWidgets.QFrame(self.frame)
        self.right_img_frame.setGeometry(QtCore.QRect(240, 0, 241, 281))
        self.right_img_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_img_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_img_frame.setObjectName("right_img_frame")
        self.right_img_title = QtWidgets.QLabel(self.right_img_frame)
        self.right_img_title.setGeometry(QtCore.QRect(90, 10, 91, 16))
        self.right_img_title.setObjectName("right_img_title")
        self.right_title_lbl = QtWidgets.QLabel(self.right_img_frame)
        self.right_title_lbl.setGeometry(QtCore.QRect(10, 170, 91, 16))
        self.right_title_lbl.setObjectName("right_title_lbl")
        self.right_artist_edit = QtWidgets.QLineEdit(self.right_img_frame)
        self.right_artist_edit.setGeometry(QtCore.QRect(80, 210, 113, 20))
        self.right_artist_edit.setObjectName("right_artist_edit")
        self.right_title_edit = QtWidgets.QLineEdit(self.right_img_frame)
        self.right_title_edit.setGeometry(QtCore.QRect(80, 170, 113, 20))
        self.right_title_edit.setObjectName("right_title_edit")
        self.right_set_btn = QtWidgets.QPushButton(self.right_img_frame)
        self.right_set_btn.setGeometry(QtCore.QRect(90, 240, 61, 23))
        self.right_set_btn.setObjectName("right_set_btn")
        self.right_img_box = QtWidgets.QGroupBox(self.right_img_frame)
        self.right_img_box.setGeometry(QtCore.QRect(0, 0, 241, 271))
        self.right_img_box.setTitle("")
        self.right_img_box.setObjectName("right_img_box")
        self.right_artist_lbl = QtWidgets.QLabel(self.right_img_box)
        self.right_artist_lbl.setGeometry(QtCore.QRect(10, 210, 111, 16))
        self.right_artist_lbl.setObjectName("right_artist_lbl")
        self.right_img = QtWidgets.QLabel(self.right_img_box)
        self.right_img.setGeometry(QtCore.QRect(60, 40, 121, 111))
        self.right_img.setAutoFillBackground(True)
        self.right_img.setText("")
        self.right_img.setObjectName("right_img")
        self.right_img_box.raise_()
        self.right_img_title.raise_()
        self.right_title_lbl.raise_()
        self.right_artist_edit.raise_()
        self.right_title_edit.raise_()
        self.right_set_btn.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 652, 21))
        self.menubar.setObjectName("menubar")
        self.menumenu = QtWidgets.QMenu(self.menubar)
        self.menumenu.setObjectName("menumenu")
        self.menuUpdate_artists_list = QtWidgets.QMenu(self.menumenu)
        self.menuUpdate_artists_list.setObjectName("menuUpdate_artists_list")
        self.menuRename_songs = QtWidgets.QMenu(self.menumenu)
        self.menuRename_songs.setObjectName("menuRename_songs")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCreate_defult_dir = QtWidgets.QAction(MainWindow)
        self.actionCreate_defult_dir.setObjectName("actionCreate_defult_dir")
        self.actionThis_Directory = QtWidgets.QAction(MainWindow)
        self.actionThis_Directory.setObjectName("actionThis_Directory")
        self.actionSelect_directory = QtWidgets.QAction(MainWindow)
        self.actionSelect_directory.setObjectName("actionSelect_directory")
        self.actionAuto_Update = QtWidgets.QAction(MainWindow)
        self.actionAuto_Update.setObjectName("actionAuto_Update")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionView_And_Edit_Phrases = QtWidgets.QAction(MainWindow)
        self.actionView_And_Edit_Phrases.setObjectName("actionView_And_Edit_Phrases")
        self.actionAdd_Artist = QtWidgets.QAction(MainWindow)
        self.actionAdd_Artist.setObjectName("actionAdd_Artist")
        self.actionFind_All_Cover_Art = QtWidgets.QAction(MainWindow)
        self.actionFind_All_Cover_Art.setObjectName("actionFind_All_Cover_Art")
        self.menuUpdate_artists_list.addAction(self.actionAuto_Update)
        self.menuUpdate_artists_list.addAction(self.actionAdd_Artist)
        self.menuRename_songs.addSeparator()
        self.menuRename_songs.addAction(self.actionThis_Directory)
        self.menuRename_songs.addAction(self.actionSelect_directory)
        self.menuRename_songs.addSeparator()
        self.menuRename_songs.addAction(self.actionView_And_Edit_Phrases)
        self.menuRename_songs.addSeparator()
        self.menuRename_songs.addAction(self.actionFind_All_Cover_Art)
        self.menumenu.addAction(self.menuUpdate_artists_list.menuAction())
        self.menumenu.addAction(self.menuRename_songs.menuAction())
        self.menumenu.addSeparator()
        self.menumenu.addAction(self.actionCreate_defult_dir)
        self.menumenu.addSeparator()
        self.menumenu.addAction(self.actionExit)
        self.menubar.addAction(self.menumenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # till here template code
        self.song_list_lbl.raise_()
        self.song_list.raise_()
        self.song_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.song_list.setAlternatingRowColors(True)
        self.song_list.autoFillBackground()
        self.songs_array = []
        self.connect_btns()
        self.song_path = os.getcwd()
        self.locate_mp3("")
        self.edit_list()
        self.set_right_image(True)
        self.song_was_selected = False
        self.curr_song = None

    def retranslateUi(self, MainWindow):
        """
        designer self made code
        none changes were made
        :param MainWindow:
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dir_lbl.setText(_translate("MainWindow", "Directory value"))
        self.song_list_lbl.setText(_translate("MainWindow", "Songs List"))
        self.next_btn.setText(_translate("MainWindow", "Next"))
        self.prev_btn.setText(_translate("MainWindow", "Previous"))
        self.dir_set_btn.setText(_translate("MainWindow", "Select Directory"))
        self.name_lbl.setText(_translate("MainWindow", "Song Name"))
        self.title_lbl.setText(_translate("MainWindow", "Title :"))
        self.artist_lbl.setText(_translate("MainWindow", "Artist"))
        self.left_img_title.setText(_translate("MainWindow", "Recomended"))
        self.left_artist_lbl.setText(_translate("MainWindow", "Artist"))
        self.left_title_lbl.setText(_translate("MainWindow", "Title :"))
        self.left_set_btn.setText(_translate("MainWindow", "Set"))
        self.right_img_title.setText(_translate("MainWindow", "Self Editing"))
        self.right_title_lbl.setText(_translate("MainWindow", "Title :"))
        self.right_set_btn.setText(_translate("MainWindow", "Set"))
        self.right_artist_lbl.setText(_translate("MainWindow", "Artist"))
        self.menumenu.setTitle(_translate("MainWindow", "Options"))
        self.menuUpdate_artists_list.setTitle(_translate("MainWindow", "Update Artists List"))
        self.menuRename_songs.setTitle(_translate("MainWindow", "Rename Songs"))
        self.actionCreate_defult_dir.setText(_translate("MainWindow", "Select Defult Dir"))
        self.actionThis_Directory.setText(_translate("MainWindow", "This Directory"))
        self.actionSelect_directory.setText(_translate("MainWindow", "Select Directory"))
        self.actionAuto_Update.setText(_translate("MainWindow", "Auto Update"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionView_And_Edit_Phrases.setText(_translate("MainWindow", "View And Edit Phrases"))
        self.actionAdd_Artist.setText(_translate("MainWindow", "Add Artist"))
        self.actionFind_All_Cover_Art.setText(_translate("MainWindow", "Find All Cover Art"))


    def connect_btns(self):
        """
        connect the gui buttons
        :return: none
        """
        self.dir_set_btn.clicked.connect(self.select_dir)
        self.right_img.mousePressEvent = self.select_img
        self.right_img.mouseDoubleClickEvent = self.select_dir
        self.song_list.doubleClicked.connect(self.new_song_selected)
        self.actionAuto_Update.triggered.connect(self.create_artist_list)
        self.actionAdd_Artist.triggered.connect(add_artist_dailog)
        self.left_set_btn.clicked.connect(self.set_new_details)
        self.actionThis_Directory.triggered.connect(self.update_songs_tags)
        self.actionFind_All_Cover_Art.triggered.connect(self.set_new_arts)

    def update_songs_tags(self, event):

        artist_tools.update_songs_tags(self.song_path, self.songs_array)

    def set_new_details(self, event):
        path = os.path.join(self.song_path, self.curr_song + ".mp3")
        if self.song_was_selected:
            artist_tools.set_new_details(path, artist=self.lef_artist_edit.text(),
                                         title=self.left_title_edit.text(), img=img_path)
    def set_new_arts(self, event):
        """
        send all the song in the file and replace thier album art cover
        :param event:
        :return:
        """
        img_tools.album_art(self.songs_array, self.song_path)

    def set_right_image(self, first):
        """
        let the user uplaod image to the right frame
        :param first:
        :return:
        """
        if first:  # when launching the app use the default img
            img_tools.create_piximg(self.right_img, os.getcwd() + r'\env\Lib\imaeges\empty_img.jpg')
        else:  # start looking for the img in the user folder
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "",
                                                                 "Image Files (*.png *jpg *jpeg *.bmp)")
            if file_name:  # only if a pic was selected
                img_tools.create_piximg(self.right_img, file_name)

    def new_song_selected(self,event):
        """
        as new song is chosen update window
        :param event: none
        :return: none
        """
        self.curr_song = self.song_list.selectedIndexes()[0].data()  # get song name
        file_path = os.path.join(self.song_path, self.curr_song) + ".mp3"
        file = TinyTag.get(file_path, image=True)  # create tiny object
        self.set_curr_details(self.curr_song, file, file_path)  # top  frame update
        self.set_rec_details(self.curr_song, file)  # left frame update
        self.song_was_selected = True

    def set_curr_details(self, song, file, file_path):
        """
        update top frame as new song is chosen
        :return:
        """
        self.set_cur_lbls(song, file)  # update labels
        self.set_cur_img(file_path)  # update image

    def set_cur_lbls(self, song, file):
        """
        set the labels at the top frame
        :param song: the file name (string)
        :param file: the mp3 file (tiny tag object)
        :return: none
        """
        self.name_lbl.setText(song)
        self.title_lbl.setText("Title :   " + str(file.title))  # set title
        self.artist_lbl.setText("Artist:   " + str(file.artist))  # set artist

    def set_cur_img(self, file_path):
        """
        get tiny object and display the image from it
        :param file: none
        :return: none
        """
        path = os.path.join(os.getcwd(), r'env\Lib\imaeges\cur_img.jpg')
        audio = eyed3.load(file_path)
        if len(audio.tag.images) != 0:
            with open(path, 'wb') as sss:  # transfer it from tumb file to real file
                sss.write(audio.tag.images[0].image_data)  # create the image file
            img_tools.create_piximg(self.cur_img, path)  # display it
        else:
            img_tools.create_piximg(self.cur_img, os.path.join(os.getcwd(), r'env\Lib\imaeges\empty_img.jpg'))


    def set_rec_details(self, song, file):
        """
        set the left frame details as new song is selected
        :return:
        """
        artist, song = self.find_artist_name(song, file)  # find and display artist name
        self.lef_artist_edit.setText(artist)
        self.left_title_edit.setText(song)
        self.set_rec_img(artist + song)  # find and display image

    def set_rec_img(self, song):
        arr = []
        query = song.replace(' ', '+')  # get vaild query
        query = query.replace('/', '')
        query = query.replace('\\', '')
        img_tools.find_img(arr, query)  # get array of urls
        img_tools.download_img(arr)  # download urls
        img_tools.create_piximg(self.img_left, img_path)

    def locate_mp3(self, path):
        """
        locate all the mp3 file in the current dir
        :return
        """
        if path == "": # boot songs list (only first time)
            path = xml_tools.dir_select(xml_path)  # get default value
            self.song_path = path  # set to the default value
            if path is None:
                path = os.getcwd()  # if there is no one choose working one
        else:  # after selecting new working dir
            path = self.song_path  # if there is already selected path
        self.songs_array = [path + "\\" + file for file in os.listdir(path) if
               os.path.isfile(path + "\\" + file)]  # take all the file
        self.songs_array = [os.path.splitext(os.path.basename(file))[0] for file in self.songs_array if os.path.splitext(file)[1] == ".mp3"]
        # and take only their names

    def edit_list(self):
        """
        add all songs in song array to the listbox
        :return:
        """
        model = QtGui.QStandardItemModel()
        self.song_list.setModel(model)
        for i in self.songs_array:
            item = QtGui.QStandardItem(i)  # transfer the song name into qt object
            model.appendRow(item)

    def select_dir(self):
        default_path = xml_tools.dir_select(xml_path)  # get the default songs path
        dialog = QtWidgets.QFileDialog(None, "Select Directory")  # create dialog
        dialog.setDirectory(default_path)  # set opening dir
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)  # set only dir available
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)  # set style
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)  # another style thing
        if dialog.exec():  # if dialog poped
            self.song_path = dialog.selectedFiles()[0]
            self.locate_mp3("secoend")  # not first time
            self.edit_list()  # recreate songs list
            xml_tools.dir_change(xml_path, path =self.song_path)  # change deaf dir

    def select_img(self, event):
        """
        let the user upload image
        :param event:
        :return:
        """
        self.set_right_image(False)  # call the function

    def find_artist_name(self, song, file):
        """
        set recommended frame song details
        :param song: song name string
        :param file: tiny tag object
        :return:
        """
        self.lef_artist_edit.setText("")  # reset labels
        self.left_title_edit.setText("")
        dic = {'songs_path': self.song_path, 'songs_array': self.songs_array}
        artist, title = artist_tools.find_artist_name(song, file, paths=dic)  # get the values
        return artist, title  # return it so it can be printed

    def create_artist_list(self, **kwargs):
        artist_tools.create_artist_list(xml_path, self.song_path, self.songs_array)  # recreate or update the xml file


def name_normal(artist):
    """
    remove extra the from words
    :param artist:
    :return:
    """
    artist = artist.lower()
    if len(artist)>3 and artist[:4] == "the ":
        artist = artist[4:]
    return artist.replace('"', "''")


def add_artist_dailog(song_array, songs_path):
    """
    manually add artist to the list
    not completed def still need to add cases
    and to be moved to corrrect file (artist tools)
    :return:
    """
    text, result = QInputDialog.getText()
    if result:
        if not os.path.isfile(xml_path):  # file isn't existed
            xml_tools.create_xml_file(songs_path, song_array)
        tree = xml_tools.is_readable_xml(xml_path, songs_path)
        root = tree.getroot()
        root = tree.find("artists")
        artist = name_normal(text)
        string = ".//artist[@value='{}']".format(artist)
        if root.find(string) is None:
            ET.SubElement(root, "artist", {"value": artist})
            tree.write(xml_path, encoding='utf-8')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
