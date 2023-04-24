from User_data_managing.user_data_managers import *
from UI_files.standard_language_page_interface import Ui_Form
from Widgets.widgets import *


# function that can be used to remove all widgets from a layout (requires one argument - layout to remove widgets from)
def delete_items_from_layout(layout):
    count = layout.count()
    for i in range(count):
        item = layout.itemAt(0)
        widget = item.widget()
        if widget:
            widget.setParent(None)
        else:
            layout = item.layout()
            delete_items_from_layout(layout)
            layout.setParent(None)


# standard language page class that is added to the main window
class StandardLanguagePage(QWidget):
    def __init__(self, language, app, parent=None):
        super(QWidget, self).__init__(parent)
        self.language = language
        self.app = app
        self.my_set_UI()

    def my_set_UI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_for_language_name.setText(self.language)

        # connect data managers
        self.books_manager = BooksManager(self.language)
        self.dict_manager = DictionaryManager(self.language)
        self.translator = Translator(self.language)
        self.statistics_manager = StatisticsManager(self.language)
        self.learning_manager = LearningManager(self.language)
        self.language_manager = LanguagesManager(self.language)

        # connect buttons for switching between pages and load content on this pages
        self.ui.home_btn.clicked.connect(self.home_btn_event)
        self.ui.books_btn.clicked.connect(self.books_btn_event)
        self.ui.dictionary_btn.clicked.connect(self.dictionary_btn_event)
        self.ui.learn_words_btn.clicked.connect(self.learn_btn_event)

        # connect buttons on pages to events
        self.ui.add_book_btn.clicked.connect(self.add_book)
        self.ui.start_learn_words_btn.clicked.connect(self.start_training)

        # set the home page to stacked widget as a default page and show it's content on the screen
        self.home_btn_event()

    # allows you to switch between pages and removes buttons if this is the last ot the first page
    def check_change_page_buttons(self, name):
        # removes the next page button if this is the last page
        if self.books_manager.get_current_page_number(name) == self.books_manager.get_number_of_pages(name):
            self.ui.next_page_btn.hide()
        # show the next page button if this is not the last page
        else:
            self.ui.next_page_btn.show()

        # removes the previous page button if this is the first page
        if self.books_manager.get_current_page_number(name) == 1:
            self.ui.previous_page_btn.hide()
        # show the previous page button if this is not the first page
        else:
            self.ui.previous_page_btn.show()

    # creates a widget with a word and a translation and then add it to the dictionary page
    def add_word_with_translation_to_dictionary(self, word=None, translation=None, language=None):
        word_with_translation_widget = WordAndTranslationWidget(self, word, translation, language)
        self.ui.verticalLayout_for_dictionary_page.addWidget(word_with_translation_widget)

    # show translation of word in right menu of current book page
    def show_word_translations(self, word):
        # delete all items from layout that in the right menu
        delete_items_from_layout(self.ui.verticalLayout_right_menu_current_book_page)

        # indicates the language in which words should be translated
        translations_language = self.language_manager.get_translation_language()

        # create a menu widget that will show the word that should be translated
        right_menu_widget = TranslationsWidget(self, word, translations_language)
        # add right menu widget to layout
        self.ui.verticalLayout_right_menu_current_book_page.addWidget(right_menu_widget)
        # displays all possible translations of the word in the right menu widget
        self.translator.display_translations(word, translations_language, right_menu_widget.add_translation)

    # method that starts training
    def learn_btn_event(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.learn_words_page)

    # set the home page to stacked widget and display user's statistic
    def home_btn_event(self):
        # set the home page
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
        # display user statistic
        self.ui.label_books_count.setText(str(self.statistics_manager.get_number_of_books()))
        self.ui.label_learned_words_count.setText(str(self.statistics_manager.get_number_of_learned_words()))
        self.ui.label_unlearned_words_count.setText(str(self.statistics_manager.get_number_of_unlearned_words()))

    # set the dictionary page to stacked widget and display user's words
    def dictionary_btn_event(self):
        # set the dictionary page to stacked widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.dictionary_page)

        # delete all items from layout
        delete_items_from_layout(self.ui.verticalLayout_for_dictionary_page)

        # adds all words with translation that are in the dictionary
        for word, translation, lang in self.dict_manager.get_all_words_and_translations():
            # create a widget that will display the word and its translation and the language in which it was translated
            word_with_translation_widget = WordAndTranslationWidget(self, word, translation, lang)
            # add widget to layout
            self.ui.verticalLayout_for_dictionary_page.addWidget(word_with_translation_widget)

    # set the books page to stacked widget and display user's books
    def books_btn_event(self):
        # set the books page to stacked widget
        delete_items_from_layout(self.ui.verticalLayout_for_book_content)
        self.ui.stackedWidget.setCurrentWidget(self.ui.books_page)
        self.ui.book_content = BookContent(self)
        self.ui.verticalLayout_for_book_content.addWidget(self.ui.book_content)

        delete_items_from_layout(self.ui.verticalLayout_for_books_page)
        # load names with images of my books to books_page
        names = self.books_manager.get_names_of_all_books()
        for name in names:
            widget = BookNameWithImageCustomWidget(name, self)
            self.ui.verticalLayout_for_books_page.addWidget(widget)
            widget.ui.label_for_book_name.setText(name)

    def next_page(self, name):
        self.books_manager.next_page(name)
        self.ui.book_content.setPlainText(self.books_manager.get_current_page_content(name))
        self.check_change_page_buttons(name)

    def previous_page(self, name):
        self.books_manager.previous_page(name)
        self.ui.book_content.setPlainText(self.books_manager.get_current_page_content(name))
        self.check_change_page_buttons(name)

    def add_book(self):
        CallAddBookDialog(self)
        self.books_btn_event()

    def start_training(self):
        self.ui.start_learn_words_btn.hide()

        self.exercises = [ExerciseWidget(self, word) for word in self.learning_manager.get_words_to_learn()]
        self.current_exercise_number = -1
        self.training_result = 0
        self.load_exercise()

    def load_exercise(self):
        self.current_exercise_number += 1
        delete_items_from_layout(self.ui.verticalLayout_for_training)
        if self.current_exercise_number < len(self.exercises):
            self.ui.verticalLayout_for_training.addWidget(self.exercises[self.current_exercise_number])
        else:
            message = f'Training completed!\nYour result:\n{self.training_result}/{len(self.exercises)}'
            self.ui.verticalLayout_for_training.addWidget(QLabel(message))
            self.current_exercise_number = -1
