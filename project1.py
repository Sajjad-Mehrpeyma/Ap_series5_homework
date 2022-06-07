from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QFormLayout, QGroupBox, QScrollArea, QLabel
import sys
import requests
from bs4 import BeautifulSoup

# collecting webpage using requests module
r = requests.get('https://boston.craigslist.org/search/jjj?')
content = r.content
soup = BeautifulSoup(content, 'html.parser')


# collecting links and job descriptions
def job_collector(soup):
    # in the jobs dictionary items will be {url_completer : job_name}
    jobs = {}
    rows = soup.find_all('a', {'class': "result-title hdrlnk"})
    for row in rows:
        try:
            link = row.get('href')
            job_title = row.text
            jobs[job_title] = link

        except:
            pass

    return jobs


# collecting job names with their abbreviated form(it will be added to url later)
def job_title(soup):
    # in the drop_menu dictionary items will be like {jjj : all}
    drop_menu = {}

    drop_menu_items = soup.find('select', {'id': 'subcatAbb'})
    for item in drop_menu_items:
        try:
            job_url = item.get('value')
            job = item.text
            drop_menu[job_url] = job

        except:
            pass

    return drop_menu


# main class to define our window
class Window(QWidget):
    def __init__(self, soup):
        super().__init__()
        # we put our buttons here. it is used for deleting buttons
        self.buttons = []
        # collecting job titles from internet.
        self.job_titles = job_title(soup)

        # defining name of window
        self.title = 'Job Finder'
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

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        # making a button to clear the page and show the main menu.
        clear_result = QPushButton('Clear results')
        # connecting clear_result buttonn to a function that is defined further
        clear_result.clicked.connect(lambda: Window.back_to_menu(self))
        # setting yellow color for clear_result button
        clear_result.setStyleSheet('background-color:yellow')
        # adding clear_result button to scrollable widget
        self.formlayout.addRow(clear_result)
        Window.create_title_menu(self, self.create_jobs_menu)

        # setting layout to 'layout'
        self.setLayout(layout)
        # showing thee window
        self.show()

    # a method for creating first(title) menu.
    def create_title_menu(self, func):
        # making buttons for each title.for example a button for 'business', another button for 'admin'.
        for counter in range(len(self.job_titles)):
            button_name = list(self.job_titles.keys())[counter]
            title = list(self.job_titles.values())[counter]
            btn = self.make_button(button_name, title, func)

            # adding button to the scrollable window
            self.formlayout.addRow(btn)

    # a method for making buttons,button name is buttons name
    # title is what is going to be written on the button
    # func is the function that is going to connect with the button
    def make_button(self, button_name, title, func):
        # button name is also the url completer. for example 'button name' for 'all' button is 'jjj'
        # if we put 'jjj' in the 'https://boston.craigslist.org/search/{}?' url it will goes to target page.
        url = button_name

        button_name = QPushButton(title)
        button_name.setFixedHeight(60)
        # connecting the button to the func function
        button_name.clicked.connect(lambda: func(url))
        # appending the button to self.buttons. we use it to clear the page
        self.buttons.append(button_name)
        return button_name

    # a method for craeting jobs menu that appears after title menu
    def create_jobs_menu(self, url_completer):
        raw_url = "https://boston.craigslist.org/search/{}?"
        # putting the url completer in the raw url to go to the target page
        completed_url = raw_url.format(url_completer)
        # getting webpage through requests library
        r = requests.get(completed_url)
        content = r.content
        new_soup = BeautifulSoup(content, 'html.parser')
        # collecting jobs useing job collector method that is defined outside of the class
        self.jobs = job_collector(new_soup)

        # removing buttons from screen to put new buttons instead
        for button in self.buttons:
            button.deleteLater()
        self.buttons = []

        # creating new buttons for jobs and adding them to scrollable window
        for job in self.jobs:
            link = self.jobs[job]
            btn = self.make_button(link, job, self.create_description_menu)
            self.formlayout.addRow(btn)

    # this method makes the menu for job descriptions
    def create_description_menu(self, url):
        # collecting webpage with requests library
        r = requests.get(url)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        # removing some part of the soup because it is not needed
        soup.p.extract()
        raw_data = soup.findAll('section', {'id': 'postingbody'})

        data = str(raw_data[0].text).replace(
            'QR Code Link to This Post', "")[5:]

        # removing buttons from jobs menuu to replace them with new ones
        for button in self.buttons:
            button.deleteLater()
        self.buttons = []

        # making a lable to put the data in it
        self.description = QLabel(self)
        self.description.setText(data)
        # self.description label ti the scrollable window
        self.formlayout.addRow(self.description)

    # definig a method that is used in the clear_result button. it clears everything and makes the titles menu
    def back_to_menu(self):
        # deleting the buttons
        for button in self.buttons:
            button.deleteLater()
        self.buttons = []

        # if the description is available it will remove it. else, it will do nothing
        try:
            self.formlayout.removeRow(self.description)
        except:
            pass

        # creating title menu
        Window.create_title_menu(self, self.create_jobs_menu)


App = QApplication(sys.argv)
window = Window(soup)
sys.exit(App.exec())
