import sys
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

# Український алфавіт
UKRAINIAN_ALPHABET = [
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з',
    'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
    'ь', 'ю', 'я'
]

def clean_text(text):
    """
    Очищає текст: перетворює у нижній регістр та видаляє всі символи, крім літер українського алфавіту та пробілів.
    """
    text = text.lower()
    allowed_chars = set(UKRAINIAN_ALPHABET + [' '])
    cleaned = ''.join(char for char in text if char in allowed_chars)
    return cleaned

def count_letters(text):
    """
    Підраховує кількість кожної літери в тексті.
    """
    return Counter(text.replace(' ', ''))

def relative_frequency(counter):
    """
    Обчислює відносну частоту появи кожної літери.
    """
    total = sum(counter.values())
    return {letter: count / total for letter, count in counter.items()}

def plot_alphabetical(freq_dict, title):
    """
    Будує діаграму відносної частоти літер у алфавітному порядку.
    """
    letters = sorted(freq_dict.keys())
    frequencies = [freq_dict[letter] for letter in letters]
    
    plt.figure(figsize=(12,6))
    sns.barplot(x=letters, y=frequencies, palette='viridis')
    plt.title(title)
    plt.xlabel('Літери')
    plt.ylabel('Відносна частота')
    plt.tight_layout()
    plt.show()

def plot_sorted(freq_dict, title):
    """
    Будує діаграму відносної частоти літер, відсортовану за спаданням.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    letters, frequencies = zip(*sorted_items)
    
    plt.figure(figsize=(12,6))
    sns.barplot(x=letters, y=frequencies, palette='magma')
    plt.title(title)
    plt.xlabel('Літери')
    plt.ylabel('Відносна частота')
    plt.tight_layout()
    plt.show()

def print_sorted_sequence(freq_dict):
    """
    Виводить послідовність літер за спаданням частоти появи.
    """
    sorted_letters = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    sequence = ''.join([letter for letter, freq in sorted_letters])
    print("\nПослідовність літер за спаданням частоти:")
    print(sequence)

def main(file_paths):
    """
    Основна функція для підрахунку та виводу частотних характеристик літер.
    """
    combined_counter = Counter()
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned = clean_text(text)
                letter_counts = count_letters(cleaned)
                combined_counter.update(letter_counts)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
            continue
    
    freq = relative_frequency(combined_counter)
    
    # Збереження частот у файл
    with open('freq_reference.json', 'w', encoding='utf-8') as json_file:
        json.dump(freq, json_file, ensure_ascii=False, indent=4)
    print("\nЧастоти літер збережено у файлі freq_reference.json")
    
    # Діаграма алфавітного порядку
    plot_alphabetical(freq, 'Відносна частота літер (алфавітний порядок)')
    
    # Діаграма сортування за частотою
    plot_sorted(freq, 'Відносна частота літер (сортування за частотою)')
    
    # Послідовність літер за спаданням частоти
    print_sorted_sequence(freq)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python3 task1_letter_frequency.py <file1> <file2> ...")
    else:
        main(sys.argv[1:])
