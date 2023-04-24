from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QCheckBox, QPushButton, QFileDialog, QDialog, QVBoxLayout, \
    QHBoxLayout, QLabel, QFormLayout, QRadioButton, QLineEdit
from UI_files.ui_exersize_1 import Ui_Form as Ui_exercise_1
from UI_files.ui_word_and_translation_custom_widget import Ui_Form as Ui_Word_and_translation
from UI_files.ui_translation_with_add_to_dict_btn_custom_widget import Ui_Form as Ui_translation
from UI_files.ui_book_name_with_image_custom_widget import Ui_Form as Ui_book
from UI_files.ui_right_menu_current_book_page_custom_widget import Ui_Form as Ui_translations


# CUSTOM WIDGETS

class ReplaceDialog(QDialog):
    def __init__(self, parent_dialog):
        super(ReplaceDialog, self).__init__()
        self.parent_dialog = parent_dialog
        self.parent_dialog.answer = False
        self.lt_main = QVBoxLayout()
        self.lt_pbs = QHBoxLayout()
        self.pb_replace = QPushButton('Replace')
        self.pb_cancel = QPushButton('Cancel')

        self.setLayout(self.lt_main)
        self.lt_main.addWidget(QLabel('Book with such name already exists. Replace it?'))
        self.lt_main.addLayout(self.lt_pbs)
        [self.lt_pbs.addWidget(i) for i in [self.pb_replace, self.pb_cancel]]

        self.pb_replace.clicked.connect(self.replace)
        self.pb_cancel.clicked.connect(self.cancel)

    def replace(self):
        self.parent_dialog.answer = True
        self.close()

    def cancel(self):
        self.close()


class CallAddBookDialog(QDialog):
    def __init__(self, lang_page):
        self.lang_page = lang_page
        self.answer = False
        super(CallAddBookDialog, self).__init__()
        self.lt_main = QVBoxLayout(self)
        self.lt_apply = QHBoxLayout()
        self.lt_path = QHBoxLayout()
        self.lt_properties = QFormLayout()

        self.rb_add_book_by_file = QRadioButton("Choose file")
        self.rb_add_book_by_content = QRadioButton("Enter text of book")
        self.pb_add = QPushButton("Add book")
        self.pb_cancel = QPushButton("Cancel")
        self.label_path = QLineEdit()
        self.label_path.setDisabled(True)
        self.pb_choose_path = QPushButton('Open Explorer')
        self.pte_text = QPlainTextEdit()
        self.le_name = QLineEdit()

        self.lt_main.addLayout(self.lt_properties)
        self.lt_main.addWidget(self.rb_add_book_by_file)
        self.lt_main.addLayout(self.lt_path)
        self.lt_main.addWidget(self.rb_add_book_by_content)
        self.lt_main.addWidget(self.pte_text)
        self.lt_main.addLayout(self.lt_apply)
        self.lt_apply.addWidget(self.pb_add)
        self.lt_apply.addWidget(self.pb_cancel)
        self.lt_path.addWidget(self.label_path)
        self.lt_path.addWidget(self.pb_choose_path)
        self.lt_properties.addRow('Name:', self.le_name)

        self.rb_add_book_by_file.clicked.connect(self.choose_option)
        self.rb_add_book_by_content.clicked.connect(self.choose_option)
        self.rb_add_book_by_file.click()
        self.pb_choose_path.clicked.connect(self.choose_path)
        default_name = self.lang_page.books_manager.get_default_book_name()
        self.le_name.setText(default_name)
        self.pb_add.clicked.connect(self.add_book)
        self.pb_cancel.clicked.connect(self.cancel)
        self.pte_text.textChanged.connect(self.update_add_pb)
        self.exec()

    def choose_option(self):
        if self.sender() == self.rb_add_book_by_file:
            self.pte_text.hide()
            self.apply_to_all_children_widgets(lambda widget: widget.show(), self.lt_path)
        else:
            self.pte_text.show()
            self.apply_to_all_children_widgets(lambda widget: widget.hide(), self.lt_path)
        self.update_add_pb()

    def choose_path(self):
        file_name = QFileDialog.getOpenFileName(self, 'Choose file', '', 'Text file (*.txt)')[0]
        self.label_path.setText(file_name)
        self.update_add_pb()

    def add_book(self):
        if self.le_name.text() in self.lang_page.books_manager.get_names_of_all_books():
            d = ReplaceDialog(self)
            d.exec()
            if self.answer:
                self.add_book_chosen_way()
        else:
            self.add_book_chosen_way()

    def add_book_chosen_way(self):
        if self.rb_add_book_by_file.isChecked():
            self.lang_page.books_manager.add_book_by_file_path(self.label_path.text(), self.le_name.text())
        else:
            self.lang_page.books_manager.add_book_by_content(self.pte_text.toPlainText(), self.le_name.text())
        self.close()

    def update_add_pb(self):
        if self.rb_add_book_by_file.isChecked():
            value = bool(self.label_path.text())
        else:
            value = bool(self.pte_text.toPlainText())
        self.pb_add.setEnabled(value)

    def cancel(self):
        self.close()

    def apply_to_all_children_widgets(self, function, main_layout):
        count = main_layout.count()
        for i in range(count):
            item = main_layout.itemAt(i)
            widget = item.widget()
            layout = item.layout()
            if widget:
                function(widget)
            elif layout:
                self.apply_to_all_children_widgets(function, layout)


class TranslationsWidget(QWidget):
    def __init__(self, language_page, word, language_of_translation, parent=None):
        super(QWidget, self).__init__(parent)

        self.ui = Ui_translations()
        self.ui.setupUi(self)

        self.language_page = language_page
        self.word = word
        self.language_of_translation = language_of_translation
        self.ui.word_btn.setText(self.word)

    def add_translation(self, translation, in_dictionary):
        widget = TranslationWidget(self.language_page, self, in_dictionary, translation)
        self.ui.verticalLayout_for_translations.addWidget(widget)
        self.language_page.app.processEvents()


class BookNameWithImageCustomWidget(QWidget):
    def __init__(self, book_name, language_page, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_book()
        self.ui.setupUi(self)

        self.language_page = language_page
        self.book_name = book_name

        self.ui.label_for_book_name.setText(book_name)

        self.ui.choose_book_btn.clicked.connect(self.open_book)
        self.ui.del_btn.clicked.connect(self.del_book)

    def open_book(self):
        self.language_page.ui.stackedWidget.setCurrentWidget(self.language_page.ui.read_current_book_page)
        self.language_page.ui.book_content.setPlainText(
            self.language_page.books_manager.get_current_page_content(self.book_name))
        self.language_page.check_change_page_buttons(self.book_name)
        self.language_page.ui.next_page_btn.clicked.connect(lambda: self.language_page.next_page(self.book_name))
        self.language_page.ui.previous_page_btn.clicked.connect(
            lambda: self.language_page.previous_page(self.book_name))

    def del_book(self):
        self.language_page.books_manager.delete_book(self.book_name)
        self.language_page.books_btn_event()


class TranslationWidget(QWidget):
    def __init__(self, language_page, right_menu, in_dict, translation, parent=None):
        super(QWidget, self).__init__(parent)

        self.ui = Ui_translation()
        self.ui.setupUi(self)

        self.language_page = language_page
        self.right_menu = right_menu
        self.word = self.right_menu.word
        self.translation = translation
        self.language = self.right_menu.language_of_translation
        self.in_dict = in_dict

        if self.in_dict:
            self.ui.add_btn.hide()

        self.ui.translation_btn.setText(translation)

        self.ui.add_btn.clicked.connect(self.add_to_dict)

    def add_to_dict(self):
        self.language_page.dict_manager.add_word_and_translation(self.word, self.translation, self.language)

        self.ui.add_btn.hide()


class WordAndTranslationWidget(QWidget):
    def __init__(self, language_page, word, translation, language, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_Word_and_translation()
        self.ui.setupUi(self)
        self.language_page = language_page
        self.ui.word_btn.setText(word)
        self.ui.translation_btn.setText(translation)
        self.ui.language_btn.setText(language)
        self.word = word
        self.translation = translation
        self.language = language
        self.ui.del_btn.clicked.connect(self.del_event)

    def del_event(self):
        self.language_page.dict_manager.delete_translations_of_word(self.word, self.translation, self.language)
        self.language_page.dictionary_btn_event()


class BookContent(QPlainTextEdit):
    def __init__(self, language_page, parent=None):
        super(BookContent, self).__init__(parent)
        self.language_page = language_page

    def mousePressEvent(self, event):
        super(BookContent, self).mousePressEvent(event)
        cursor_pos = self.textCursor().position()
        word = self.language_page.translator.get_word(cursor_pos, self.toPlainText())
        self.language_page.show_word_translations(word)

    def keyPressEvent(self, event):
        pass


class ExerciseWidget(QWidget):
    def __init__(self, language_page, word, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_exercise_1()
        self.ui.setupUi(self)

        self.language_page = language_page
        self.translations = self.language_page.learning_manager.get_correct_and_incorrect_translations(word)
        self.word = word

        self.ui.next_btn.clicked.connect(self.next)

        self.ui.verticalLayout_for_variants.addWidget(QPushButton(word))
        self.answers = []
        for trans, lang in self.translations:
            cb = QCheckBox(' - '.join([trans, lang]))
            self.answers.append((trans, lang, cb))
            self.ui.verticalLayout_for_variants.addWidget(cb)

    def next(self):
        self.language_page.load_exercise()
        answers_are_correct = True
        for trans, lang, cb in self.answers:
            correct = self.language_page.learning_manager.translation_is_correct(self.word, trans, lang)
            checked_wrong = not correct and cb.isChecked()
            not_checked_correct = correct and not cb.isChecked()
            if checked_wrong or not_checked_correct:
                answers_are_correct = False
                break
        if answers_are_correct:
            self.language_page.training_result += 1
