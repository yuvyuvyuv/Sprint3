import os
import datetime
import nltk
from nltk.corpus import words
import string
DIR_PATH = "C:\\Users\\Public\\Documents\\top_secret"
nltk.download("words")


class EnglishWordChecker:
    def __init__(self):
        self.english_words = set(words.words())

    def is_english_word(self, word):
        return word.lower() in self.english_words

    def count_english_words_in_file(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)

        # Split text into words
        word_list = text.split()

        # Count English words
        english_word_count = sum(1 for word in word_list if self.is_english_word(word))

        return english_word_count


class FileMetadata:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_format = os.path.splitext(file_path)[1]
        self.file_size = os.path.getsize(file_path)
        self.char_count = 0
        if self.file_format == ".txt":
            with open(file_path, "r") as file:
                self.char_count = len(file.read())
        self.creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        self.modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        self.access_time = datetime.datetime.fromtimestamp(os.path.getatime(file_path))
        self.found_words = 0
        if self.file_format == ".txt":
            english_word_checker = EnglishWordChecker()
            self.found_words = english_word_checker.count_english_words_in_file(file_path)


def list_files_in_directory(dir_path):
    try:
        file_names = os.listdir(dir_path)
        return file_names
    except FileNotFoundError:
        return f"Error: The directory '{dir_path}' does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def rank_files(file_names):
    files_with_metadata = {}
    for file_name in file_names:
        files_with_metadata[file_name] = FileMetadata(os.path.join(DIR_PATH, file_name))

    # sort file with this logic, should be short files, best if text files around 200 chars, best if english words
    # put .txt first, heavy files last
    sorted_files = sorted(files_with_metadata.items(), key=lambda x: (x[1].file_format != ".txt", x[1].char_count, -x[1].found_words, x[1].file_size))
    return sorted_files


