from PyQt5 import QtGui
import os

class ThemeManager:
    """
    the theme manager takes care of the theme
    """

    def __init__(self):
        self.theme = "bright" # current state

        self.dark_theme = [QtGui.QColor(50, 50, 50 , 255),
                           QtGui.QColor(120, 120, 120, 255),
                           QtGui.QColor(255, 0, 55 , 120), # transaction lines
                            QtGui.QColor(255, 255, 255 , 255),
                            QtGui.QColor(255, 255, 255, 255),
                            QtGui.QColor(180, 180, 180, 255),
                            QtGui.QColor(255, 0, 55 , 255), # box labels
                            QtGui.QColor(120,120,120,80) # background
                           ]

        self.bright_theme =[QtGui.QColor(50, 50, 50 , 255),
                           QtGui.QColor(20, 20, 20, 255),
                           QtGui.QColor(50, 50, 50 , 80), # transaction lines
                            QtGui.QColor(80, 80, 80 , 255),
                            QtGui.QColor(255, 2, 2, 255),
                            QtGui.QColor(45, 44, 255, 255),
                            QtGui.QColor(50, 50, 50 , 255), # box labels
                            QtGui.QColor(80,80,80,100) # background
                           ]

        self.colors = {
            "dark": self.dark_theme,
            "bright": self.bright_theme
        }

        self.style_dark = {
            "main": self.read_file("styles/dark/main.txt")
            }

        self.style_bright ={
            "main": self.read_file("styles/bright/main.txt")
        }

        self.styles  = {
        "bright": self.style_bright,
        "dark": self.style_dark
        }


    def get_color(self,category):
        """
        get the color given the current theme
        :param category: int, which layer of the color theme you want
        """
        return self.colors[self.theme][category]

    def get_stylesheet(self,category):
        return self.styles[self.theme][category]


    def get_notification_style(self):
        # style of notifiaction window

        notification_styles = {
            "dark": "QLabel{color:black}",
            "bright": "QLabel{color:black}"
        }

        return notification_styles[self.theme]

    def get_table_style(self):

        dark_table_style = """
QTableView{color: black;
selection-color: rgb(0, 0, 0);
color:white;
background-color: rgb(21, 21, 21);
font: 8pt "MS Sans Serif";
font-size:10pt;
padding: 8pt;}

QTableWidget::item{padding: 15px}
"""
        bright_table_style = """
QTableView{color: black;
selection-color: rgb(223, 224, 227);
color:black;
background-color: rgb(243, 244, 247);
font: 8pt "MS Sans Serif";
font-size:10pt;
padding: 8pt;}

QTableWidget::item{padding: 15px}
"""

        table_styles = {
            "dark": dark_table_style,
            "bright": bright_table_style
        }

        return table_styles[self.theme]


    def get_background_style(self):
        # background color for dialogs

        dark_bg_style="""
QDialog{
background-color: rgb(50, 50, 50);
}

QPlainTextEdit{
background-color: rgb(29, 29, 29);
color: rgb(221, 221, 221);
}

QLineEdit{
color: rgb(221, 221, 221);
padding: 2px 2px;
font-size: 12pt;
}
"""

        bright_bg_style="""
QDialog{
background-color: rgb(253, 253, 253);
}

QPlainTextEdit{
background-color: rgb(243, 244, 247);
color: rgb(15, 15, 15);
}

QLineEdit{
color: rgb(15, 15, 15);
padding: 2px 2px;
font-size: 12pt;
}
"""

        notification_styles = {
            "dark": dark_bg_style,
            "bright": bright_bg_style
        }

        return notification_styles[self.theme]



    def read_file(self,fname):

        # fname = "./attune/src/styles/" + fname
        home = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(home, fname)

        with open(fname,"r") as file:
            return str(file.read())
