import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from UI_files.main_window import Ui_MainWindow
from Widgets.standard_language_page import StandardLanguagePage
from User_data_managing.user_data_managers import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.my_set_UI()

    def my_set_UI(self):
        self.setWindowIcon(QIcon('UI_files/icon.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # (0 - size is not maximized, 1 - size is maximized)
        self.setWindowTitle('ForLang')
        self.window_size_status = 0
        self.language_manager = LanguagesManager()
        self.ui.comboBox_for_language.currentIndexChanged.connect(self.cb_study_triggered)
        self.ui.comboBox_for_translation_lang.currentIndexChanged.connect(self.cb_translate_triggered)
        self.reload_study_combobox()
        self.reload_translate_combobox()
        self.change_language_being_studied()
        self.change_translation_language()
        self.cb_study_should_be_triggered = True
        self.cb_translate_should_be_triggered = True

    def cb_study_triggered(self):
        if self.cb_study_should_be_triggered:
            self.change_language_being_studied()

    def cb_translate_triggered(self):
        if self.cb_translate_should_be_triggered:
            self.change_translation_language()

    def reload_study_combobox(self):
        self.cb_study_should_be_triggered = False
        self.ui.comboBox_for_language.clear()
        for i, language in enumerate(self.language_manager.get_available_to_learn_langs()):
            self.ui.comboBox_for_language.addItem(language)
            if language == self.language_manager.get_language_being_studied():
                self.ui.comboBox_for_language.setCurrentIndex(i)
        self.cb_study_should_be_triggered = True

    def reload_translate_combobox(self):
        self.cb_translate_should_be_triggered = False
        self.ui.comboBox_for_translation_lang.clear()
        for i, language in enumerate(self.language_manager.get_available_translation_langs()):
            self.ui.comboBox_for_translation_lang.addItem(language)
            if language == self.language_manager.get_translation_language():
                self.ui.comboBox_for_translation_lang.setCurrentIndex(i)
        self.cb_translate_should_be_triggered = True

    def change_language_being_studied(self):
        index = self.ui.comboBox_for_language.currentIndex()
        language = self.language_manager.get_available_to_learn_langs()[index]
        page = StandardLanguagePage(language, app)
        self.ui.stackedWidget.insertWidget(index, page)
        self.ui.stackedWidget.setCurrentWidget(page)
        self.language_manager.set_language_being_studied(language)
        self.reload_translate_combobox()

    def change_translation_language(self):
        index = self.ui.comboBox_for_translation_lang.currentIndex()
        language = self.language_manager.get_available_translation_langs()[index]
        self.language_manager.set_translation_language(language)
        self.reload_study_combobox()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_w = MainWindow()
    main_w.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
