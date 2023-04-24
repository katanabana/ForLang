import math
from textblob import Word
from User_data_managing.helpers import *
import random


class Translator(DataManager):
    def __init__(self, language):
        super(Translator, self).__init__(language)
        self.settings = SettingsManager('Translation')

    def get_definitions(self, word):
        return Word(word).definitions

    def display_translations(self, word, translations_language, receiving_function):
        # Receiving_function should receive two arguments:
        # string (translation)
        # bool value (True if translation is in dictionary and False if it's not).
        # passing translations to special function helps to deal with long response from API.
        # This way user can already see some translations before others are gotten.
        # If any error occurs using API then will be displayed only those translations
        # that have been gotten before exception raised.
        translations = []
        try:
            lm = LanguagesManager()
            from_lang = lm.get_language_abbreviation(self.language)
            to_lang = lm.get_language_abbreviation(translations_language)

            def get_translation(word):
                return Word(word).translate(from_lang, to_lang)

            def receive(translation):
                if translation and translation not in translations:
                    in_dictionary = DictionaryManager().translation_is_in_dictionary(self.language, word, translation,
                                                                                     translations_language,
                                                                                     not self.settings.get_value(8))
                    receiving_function(translation, in_dictionary)
                    translations.append(translation)

            def get_synonyms(word):
                synonyms = set()
                for synset in Word(word).synsets:
                    for lemma in synset.lemmas():
                        synonyms.add(lemma.name())
                return list(synonyms)

            translation = get_translation(word)
            receive(translation)
            # receive synonyms of translation
            for synonym in get_synonyms(translation):
                receive(synonym)
            # receive translated synonyms of word
            for synonym in get_synonyms(word):
                receive(get_translation(synonym))
        except Exception:
            pass

    def get_word(self, cursor_position, text):
        # for languages where there is word entity
        abbr = LanguagesManager().get_language_abbreviation(self.language)
        if abbr in BYTES_PER_CHAR[1] + BYTES_PER_CHAR[2]:
            length = len(text)
            start = cursor_position if cursor_position < length - 1 else length - 1
            end = start + 1
            # find where word begins
            while length > start > -1 and text[start] not in SEPARATORS:
                start -= 1
            # find where word ends
            while end < length and text[end] not in SEPARATORS:
                end += 1
            return text[start + 1:end]
        # for languages where there isn't word entity (for example those that use hieroglyphs)
        else:
            return text[cursor_position]


class BooksManager(DataManager):
    def __init__(self, language):
        super(BooksManager, self).__init__(language)
        self.settings = SettingsManager('Reading')
        self.default_book_name = self.settings.get_value(9)
        self.directory_for_saving_books = PATH_TO_DATA_DIRECTORY + '\\Books'

    def add_book_by_file_path(self, file_path, book_name):
        # replaces content of book if book with such name already exists
        # if book_name wasn't passed default book name will be set
        content = get_file_content(file_path)
        self.add_book_by_content(content, book_name)

    def add_book_by_content(self, content, book_name):
        # replaces content of book if book with such name already exists
        # if book_name wasn't passed default book name will be set
        if not self.__get_book_id(book_name):
            query = 'INSERT INTO Books (name, language_id) Values (?, ?)'
            lang_id = LanguagesManager().get_language_id(self.language)
            self.execute(query, book_name, lang_id)
        book_id = self.__get_book_id(book_name)
        path = self.__get_path_to_book(book_id)
        write_content_to_file(path, content)

    def get_names_of_all_books(self):
        return self.get_all_book_names()

    def get_current_page_content(self, book_name):
        # if book with this name and on this language exists in database file
        # but file where content of book should be stored doesn't exist
        # method returns None
        path = self.__get_path_to_book(self.__get_book_id(book_name))
        try:
            # finding bytes that must be read to get current page text
            # it useful if size of book is large so unnecessary bytes won't be read
            page_number = self.get_current_page_number(book_name)
            bytes_per_page = self.__get_bytes_per_page()
            return get_file_content(path, (page_number - 1) * bytes_per_page, bytes_per_page)
        except FileExistsError:
            return

    def __get_bytes_per_page(self):
        bytes_per_char = 4
        for number_of_bytes in BYTES_PER_CHAR:
            if self.language in BYTES_PER_CHAR[number_of_bytes]:
                bytes_per_char = number_of_bytes
        return self.settings.get_value(7) * bytes_per_char

    @dec_convert_result_to_single_value
    def get_current_page_number(self, book_name):
        query = 'SELECT Books.current_page FROM Books JOIN Languages ON Languages.id = Books.language_id ' \
                'WHERE Books.name = ? and Languages.name = ?'
        return self.execute(query, book_name, self.language)

    def get_number_of_pages(self, book_name):
        size_of_book = os.stat(self.__get_path_to_book(self.__get_book_id(book_name))).st_size
        return math.ceil(size_of_book / self.__get_bytes_per_page())

    def __change_page(self, offset, book_name):
        query = 'UPDATE Books SET current_page = current_page + ? WHERE name = ? AND language_id = ?'
        self.execute(query, offset, book_name, LanguagesManager().get_language_id(self.language))

    def next_page(self, book_name):
        self.__change_page(1, book_name)

    def previous_page(self, book_name):
        self.__change_page(-1, book_name)

    def delete_book(self, book_name):
        # deletes book from database file and deletes file where book content is stored
        # if book doesn't exist in database file it won't change
        # if file with book content doesn't exist no file will be deleted
        book_id = self.__get_book_id(book_name)
        query = 'DELETE FROM Books WHERE id = ?'
        self.execute(query, book_id)
        try:
            os.remove(self.__get_path_to_book(book_id))
        except FileNotFoundError:
            pass

    @dec_convert_result_to_list_of_values
    def get_all_book_names(self):
        query = 'SELECT Books.name FROM Books JOIN Languages ON Books.language_id = Languages.id' \
                ' WHERE Languages.name = ?'
        return self.execute(query, self.language)

    def get_default_book_name(self):
        books = self.get_all_book_names()
        if self.default_book_name in books:
            i = 1
            while self.default_book_name + str(i) in books:
                i += 1
            return self.default_book_name + str(i)
        else:
            return self.default_book_name

    def __get_path_to_book(self, book_id):
        return f'{self.directory_for_saving_books}\\{book_id}.txt'

    @dec_convert_result_to_single_value
    def __get_book_id(self, book_name):
        query = 'SELECT Books.id FROM Books JOIN Languages ON Books.language_id = Languages.id WHERE Books.name = ? ' \
                'AND Languages.name = ?'
        return self.execute(query, book_name, self.language)


class DictionaryManager(DataManager):

    def get_all_words_and_translations(self):
        query = 'SELECT Words.word, Dictionary.translation_id FROM Dictionary JOIN Words ON ' \
                'Dictionary.word_id = Words.id JOIN Languages ON Words.language_id = Languages.id ' \
                'WHERE Languages.name = ?'
        answer = []
        for word, translation_id in self.execute(query, self.language):
            answer.append((word, *self.__get_word_and_lang(translation_id)))
        return answer

    def add_word_and_translation(self, word, translation, translation_language):
        # if word and its translation into language that method takes as parameter already are in dictionary
        # database file won't change
        self.__insert_into_words(word, LanguagesManager().get_language_id(self.language))
        self.__insert_into_words(translation, LanguagesManager().get_language_id(translation_language))
        self.__insert_into_dictionary(self.get_word_id(word, self.language),
                                      self.get_word_id(translation, translation_language))

    def delete_translations_of_word(self, word, translation=None, translation_language=None):
        # deletes certain translation in certain language if both translation and translation language are specified
        # deletes certain translation in any language if only translation is specified
        # deletes all translations in certain language if only translation language is specified
        # deletes all translations in any language if neither is specified
        delete = self.__get_translation_ids(word, self.language, translation, translation_language)
        word_id = self.get_word_id(word, self.language)
        for translation_id in delete:
            self.__delete_from_dictionary(word_id, translation_id)

    def get_grouped_words_and_translations(self, translations_language=None):
        # returns dictionary where every key is a word and
        # value is a tuple of its translations into passed language if with_languages is True
        # otherwise value is a tuple of tuples (translation, translation_language)
        ans = {}
        for word in self.get_all_words():
            translations = self.get_all_translations_of_word(word, translations_language)
            ans[word] = tuple(translations)
        return ans

    @dec_convert_result_to_single_value
    def get_word_id(self, word, language):
        query = 'SELECT Words.id FROM Words JOIN Languages ON Words.language_id = Languages.id WHERE word = ? ' \
                'AND Languages.name = ?'
        return self.execute(query, word, language)

    def __get_word_and_lang(self, word_id):
        query = 'SELECT Words.word, Languages.abbreviation FROM Words JOIN Languages ' \
                'ON Words.language_id = Languages.id WHERE Words.id = ?'
        return self.execute(query, word_id)[0]

    def __insert_into_dictionary(self, word_id, translation_id):
        query = 'SELECT word_id FROM Dictionary WHERE word_id = ? and translation_id = ?'
        if not self.execute(query, word_id, translation_id):
            query = 'INSERT INTO Dictionary (word_id, translation_id) VALUES (?, ?)'
            self.execute(query, word_id, translation_id)

    def __insert_into_words(self, word, language_id):
        query = 'SELECT id FROM Words WHERE word = ? and language_id = ?'
        if not self.execute(query, word, language_id):
            query = 'INSERT INTO Words (word, language_id) Values (?, ?)'
            self.execute(query, word, language_id)

    def __delete_from_dictionary(self, word_id, translation_id):
        query = 'DELETE FROM Dictionary WHERE word_id = ? AND translation_id = ?'
        self.execute(query, word_id, translation_id)

    @dec_convert_result_to_list_of_values
    def __get_translation_ids(self, word, word_language, translation=None, translation_language=None):
        args = [self.get_word_id(word, word_language)]
        additional_conditions = []
        query = 'SELECT Dictionary.translation_id FROM Dictionary JOIN Words ON Dictionary.translation_id = Words.id ' \
                'JOIN Languages ON Languages.id = Words.language_id WHERE Dictionary.word_id = ?'
        if translation or translation_language:
            if translation:
                additional_conditions.append('Words.word = ?')
                args.append(translation)
            if translation_language:
                additional_conditions.append('Languages.abbreviation = ?')
                args.append(translation_language)
            query += ' AND ' + ' AND '.join(additional_conditions)
        return self.execute(query, *args)

    def get_all_translations_of_word(self, word, translations_language=None, incorrect=False):
        # if translation language passed returns list of translations
        # otherwise returns list of tuples (translation, language of translation)
        args = [self.get_word_id(word, self.language)]
        cols = 'Words.word'
        condition = f'Dictionary.word_id {"!" * incorrect}= ?'
        if translations_language:
            condition += ' AND Languages.name = ?'
            args.append(translations_language)
        else:
            cols += ', Languages.abbreviation'
        query = f'SELECT {cols} FROM Words JOIN Dictionary ON Words.id = Dictionary.translation_id JOIN Languages ON' \
                f' Languages.id = Words.language_id WHERE {condition}'
        if translations_language:
            return dec_convert_result_to_list_of_values(self.execute)(query, *args)
        else:
            return self.execute(query, *args)

    @dec_convert_result_to_list_of_values
    def get_all_words(self):
        query = 'SELECT DISTINCT Words.word FROM Dictionary JOIN Words ON Dictionary.word_id = Words.id JOIN ' \
                'Languages ON Words.language_id = Languages.id WHERE Languages.name = ?'
        return self.execute(query, self.language)

    def translation_is_in_dictionary(self, language, word, translation, translation_language, case_sensitive):
        word_id = self.get_word_id(word, language)
        if word_id:
            args = [word_id]
            query = 'SELECT Words.word FROM Words JOIN Dictionary ON Dictionary.translation_id = Words.id'
            if translation_language:
                query += ' JOIN Languages ON Languages.id = Words.language_id'
            query += ' WHERE Dictionary.word_id = ?'
            if case_sensitive:
                query += ' AND Words.word = ?'
                args.append(translation)
            else:
                query += ' AND LOWER(Words.word) = ?'
                args.append(translation.lower())
            if translation_language:
                query += ' AND Languages.abbreviation = ?'
                args.append(translation_language)
            return bool(self.execute(query, *args))
        else:
            return False


class LearningManager(DataManager):
    def __init__(self, language):
        super(LearningManager, self).__init__(language)
        self.settings = SettingsManager('Learning')
        self.dictionary = DictionaryManager(language)

    def get_correct_and_incorrect_translations(self, word):
        # translation is considered as correct only if it's in dictionary
        translations_language = self.settings.get_value(1)
        total = 5 + self.settings.get_value(6) * 2
        all_correct = self.dictionary.get_all_translations_of_word(word, translations_language)
        max_correct = min(total - 1, len(all_correct))
        number_of_correct = random.randint(1, max_correct)
        correct = random.sample(all_correct, number_of_correct)
        if self.settings.get_value(3):
            all_incorrect_from_dictionary = self.dictionary.get_all_translations_of_word(word, translations_language,
                                                                                         True)
            max_incorrect_from_dict = min(total - number_of_correct, len(all_incorrect_from_dictionary))
            number_of_incorrect_from_dictionary = random.randint(0, max_incorrect_from_dict)
            incorrect_from_dictionary = random.sample(all_incorrect_from_dictionary,
                                                      number_of_incorrect_from_dictionary)
        else:
            incorrect_from_dictionary = []
            number_of_incorrect_from_dictionary = 0
        number_of_random_incorrect = total - number_of_correct - number_of_incorrect_from_dictionary
        random_incorrect = []
        if self.language == 'en':
            alpha = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
            lang = 'ru'
        else:
            alpha = 'abcdefghijklmnopqrstuvwxyz'
            lang = 'en'
        for i in range(number_of_random_incorrect):
            random_word = ''.join(random.choices(alpha, k=random.randint(4, 8)))
            if translations_language:
                random_incorrect.append(random_word)
            else:
                random_incorrect.append((random_word, lang))

        answer = correct + incorrect_from_dictionary + random_incorrect
        random.shuffle(answer)
        return answer

    def translation_is_correct(self, word, translation, translation_lang):
        return self.dictionary.translation_is_in_dictionary(self.language, word, translation, translation_lang,
                                                            self.settings.get_value(4))

    def increase_word_score(self, word, translation, translation_lang):
        query = 'UPDATE Dictionary SET score = score + 1 WHERE word_id = ? AND translation_id = ?'
        self.execute(query, self.dictionary.get_word_id(word, self.language),
                     self.dictionary.get_word_id(translation, translation_lang))

    def get_words_to_learn(self):
        words = self.dictionary.get_all_words()
        number = min(len(words), self.settings.get_value(2))
        return random.sample(words, number)


class LanguagesManager(DataManager):

    def get_language_being_studied(self):
        return self.__get_current_language('study')

    def get_translation_language(self):
        return self.__get_current_language('translate')

    def set_language_being_studied(self, language):
        self.__set_current_language('study', language)

    def set_translation_language(self, language):
        self.__set_current_language('translate', language)

    @dec_convert_result_to_list_of_values
    def __get_available_languages(self, kind):
        opposite = 'study' if kind == 'translate' else 'translate'
        query = f'SELECT name FROM Languages WHERE NOT {opposite}'
        return self.execute(query)

    def get_available_to_learn_langs(self):
        return self.__get_available_languages('study')

    def get_available_translation_langs(self):
        return self.__get_available_languages('translate')

    @dec_convert_result_to_single_value
    def get_language_abbreviation(self, language_name):
        query = 'SELECT abbreviation FROM Languages WHERE name = ?'
        return self.execute(query, language_name)

    @dec_convert_result_to_single_value
    def get_language_id(self, language):
        query = 'SELECT id FROM Languages WHERE name = ?'
        return self.execute(query, language)

    @dec_convert_result_to_single_value
    def __get_current_language(self, kind):
        query = f'SELECT name FROM Languages WHERE {kind}'
        return self.execute(query)

    def __set_current_language(self, kind, language):
        for value, condition in [(1, '='), (0, '!=')]:
            query = f'UPDATE Languages SET {kind} = {value} WHERE name {condition} ?'
            self.execute(query, language)


class StatisticsManager(DataManager):
    def get_number_of_learned_words(self):
        return self.__get_number_of_words(self.language)

    def get_number_of_unlearned_words(self):
        return self.__get_number_of_words(self.language, False)

    @dec_convert_result_to_single_value
    def get_number_of_books(self):
        query = 'SELECT COUNT(Books.id) FROM Books JOIN Languages ON Languages.id = Books.language_id WHERE ' \
                'Languages.name = ?'
        return self.execute(query, self.language)

    @dec_convert_result_to_single_value
    def __get_number_of_words(self, language, learned=True):
        score = LearningManager(language).settings.get_value(5)
        query = f'SELECT COUNT(DISTINCT Words.word) FROM Words JOIN Dictionary ON Words.id = Dictionary.word_id JOIN ' \
                f'Languages ON Languages.id = Words.language_id WHERE Dictionary.score {["<", ">="][learned]}  ? AND ' \
                f'Languages.name = ?'
        return self.execute(query, score, language)
