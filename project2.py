# importing some modules
from PyQt5.QtWidgets import QLineEdit, QApplication, QPushButton, QVBoxLayout, QWidget, QFormLayout, QGroupBox, QScrollArea, QLabel
from PyQt5.QtGui import QPixmap, QImage, QFont
import sys
import requests
from bs4 import BeautifulSoup

# defining the main class that inherites from QWidget library
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.RawURL = 'https://www.bing.com/images/search?q={}&form=HDRSC2&first=1&tsc=ImageHoverTitle'
        self.results = []

        # defining name of window
        self.title = 'Bing Image Search'
        self.left = 500
        self.top = 200

        # setting name of window
        self.setWindowTitle(self.title)
        # setting a minimum size for window
        self.setMinimumHeight(750)
        self.setMinimumWidth(1150)

        self.formlayout = QFormLayout()

        groupbox = QGroupBox()
        groupbox.setLayout(self.formlayout)
        # making a scrollable area
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)

        # setting layout
        layout = QVBoxLayout()
        layout.addWidget(scroll)

        # making search box, search button and clear results button
        self.make_SearchBox()
        self.make_search_button()
        self.make_clear_results_button()

        # setting layout to 'layout'
        self.setLayout(layout)
        # showing thee window
        self.show()

    # a method that makes searchbox
    def make_SearchBox(self):
        self.SearchBox = QLineEdit()
        self.SearchBox.setFont(QFont("Arial", 20))
        # adding searchbox to scrollable area
        self.formlayout.addRow(self.SearchBox)

    # a method that will search the given sentence in searchbox in bing.com
    def search(self):
        subject = self.SearchBox.text()
        # making the url completer.
        subject = subject.replace(' ', '+')
        Url = self.RawURL.format(subject)
        # collecting data from internet
        r = requests.get(Url)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        # filterig html code
        pics_row = soup.find('ul', {'class': 'dgControl_list'})
        pics = pics_row.findAll('img', {'class': 'mimg'})

        # downloading images and showing them
        for tag in pics:
            url = tag.get('src')
            img = self.download_pictures(url)
            self.display_image(img)

    # a method that downloads the picture using url
    def download_pictures(self, url):
        img = QImage()
        img.loadFromData(requests.get(url).content)
        return img
    
    # a method that displays the image
    def display_image(self, img):
        img_lable = QLabel()
        img_lable.setPixmap(QPixmap(img))
        self.formlayout.addRow(img_lable)
        self.results.append(img_lable)

    # a method that makes search button
    def make_search_button(self):
        search_button = QPushButton("Click to search")
        search_button.setStyleSheet('background-color:orange')
        # connecting button to search function
        search_button.clicked.connect(self.search)
        # adding button to the scrollable area
        self.formlayout.addRow(search_button)

    def make_clear_results_button(self):
        # making a button to clear the page and show the main menu.
        clear_result_button = QPushButton('Clear results')
        # setting yellow color for clear_result button
        clear_result_button.setStyleSheet('background-color:yellow')

        clear_result_button.clicked.connect(self.clear_results)
        # adding clear_result button to scrollable widget
        self.formlayout.addRow(clear_result_button)

    # a function that clears the pictures
    def clear_results(self):
        for label in self.results:
            label.deleteLater()
        self.results = []


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())