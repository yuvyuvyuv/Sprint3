import os
import datetime
import nltk
from nltk.corpus import words
import string
import pickle

from bytes_to_code import generate_qr_code

DIR_PATH = "C:\\Users\\Public\\Documents\\top_secret"
IMG_PATH = "C:\\Users\\Public\\Documents\\top_secret\\top_image.jpg"
DIR_PATH = "C:\\Users\\TLP-001\\Desktop\\Talpiot\\Sprint3\\data_for_checks"
HEBREW_WORDS_PATH = "data_for_checks/hebrew_words.pkl"
# nltk.download("words")

# Load Hebrew words from pkl file
with open("data_for_checks/hebrew_words.pkl", "rb") as f:
    hebrew_words = pickle.load(f)


class EnglishWordChecker:
    def __init__(self):
        self.english_words = set(words.words())

    def is_english_word(self, word):
        return word.lower() in self.english_words

    def count_english_words_in_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)

        # Split text into words
        word_list = text.split()

        # Count English words
        english_word_count = sum(1 for word in word_list if self.is_english_word(word))

        return english_word_count


class HebrewWordChecker:
    def __init__(self):
        self.hebrew_words = hebrew_words

    def is_hebrew_word(self, word):
        return word in self.hebrew_words

    def count_hebrew_words_in_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)

        # Split text into words
        word_list = text.split()

        # Count Hebrew words
        hebrew_word_count = sum(1 for word in word_list if self.is_hebrew_word(word))

        return hebrew_word_count


class FileMetadata:
    def __init__(self, file_path, english_word_checker, hebrew_word_checker):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_format = os.path.splitext(file_path)[1]
        self.file_size = os.path.getsize(file_path)
        self.char_count = 0
        self.found_english_words = 0
        self.found_hebrew_words = 0
        if self.file_format == ".txt":
            with open(file_path, "r", encoding='utf-8') as file:
                self.char_count = len(file.read())
            if hebrew_word_checker.count_hebrew_words_in_file(file_path) > 0:
                self.found_hebrew_words = 1
            if english_word_checker.count_english_words_in_file(file_path) > 0:
                self.found_english_words = 1
        self.creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        self.modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        self.access_time = datetime.datetime.fromtimestamp(os.path.getatime(file_path))


def list_files_in_directory():
    dir_path = DIR_PATH
    try:
        file_names = os.listdir(dir_path)
        return file_names
    except FileNotFoundError:
        return f"Error: The directory '{dir_path}' does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def char_count_priority(char_count):
    if char_count < 200:
        length = 200 - char_count
    else:
        length = char_count - 200
    return length


def rank_files(file_names):
    files_with_metadata = {}
    english_word_checker = EnglishWordChecker()
    hebrew_word_checker = HebrewWordChecker()
    for file_name in file_names:
        files_with_metadata[file_name] = FileMetadata(os.path.join(DIR_PATH, file_name), english_word_checker,
                                                      hebrew_word_checker)

    sorted_files = sorted(files_with_metadata.items(), key=lambda x: (
        x[1].file_format != ".txt",  # Prioritize .txt files
        -x[1].found_hebrew_words,  # Prioritize Hebrew words
        char_count_priority(x[1].char_count),  # Prioritize around 200 characters
        -x[1].found_english_words,  # Prioritize English words
        x[1].file_size  # Prioritize smaller files
    ))
    return sorted_files


def file_to_barcodes(file_path, file_number):
    file_path = os.path.join(DIR_PATH, file_path)
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # split text into chunks of 100 characters
        chunk_size = 100
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        # generate QR codes for each chunk
        qr_codes = []
        start_barcode = generate_qr_code("data_for_checks\start_file.txt", "start_barcode.png")
        qr_codes.append(start_barcode)
        for i, chunk in enumerate(chunks):
            output_file = f"qr_code_{file_number}_{i}.png"
            image_path = generate_qr_code(chunk, output_file)
            image_path = generate_qr_code(chunk, output_file)

            # convert data type to png
            qr_codes.append(image_path)
        end_barcode = generate_qr_code("data_for_checks\end_file.txt", "end_barcode.png")
        qr_codes.append(end_barcode)
        return qr_codes


def all_files_to_barcodes(file_paths):
    all_qr_codes = []
    for i, file_path in enumerate(file_paths):
        all_qr_codes.extend(file_to_barcodes(file_path[0], i))
    return all_qr_codes

file_names = [file[0] for file in rank_files(list_files_in_directory()) if file[1].file_format == ".txt"]
print(file_names)
all_files_to_barcodes(file_names)
