import random
from collections import Counter
import re
import matplotlib.pyplot as plt
import json

# Український алфавіт
LOWER_ALPHABET = [
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з',
    'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
    'ь', 'ю', 'я'
]

UPPER_ALPHABET = [char.upper() for char in LOWER_ALPHABET]

ALPHABET = LOWER_ALPHABET + UPPER_ALPHABET
ALPHABET_SET = set(ALPHABET)
m = len(LOWER_ALPHABET)  # Розмір алфавіту (33)

def clean_text(text):
    """
    Очищає текст: видаляє всі символи, крім літер українського алфавіту,
    пробілів та переносів рядків.
    """
    allowed_chars = ALPHABET_SET.union({' ', '\n'})
    cleaned = ''.join(char for char in text if char in allowed_chars)
    return cleaned

def generate_substitution_cipher():
    """
    Генерує випадкову моноалфавітну підстановку (таблицю відповідностей).
    """
    shuffled_lower = LOWER_ALPHABET.copy()
    random.shuffle(shuffled_lower)
    substitution_map = {original: shuffled for original, shuffled in zip(LOWER_ALPHABET, shuffled_lower)}
    # Створюємо також карту для великих літер
    substitution_map.update({original.upper(): shuffled.upper() for original, shuffled in zip(LOWER_ALPHABET, shuffled_lower)})
    return substitution_map

def encrypt_substitution(plain, substitution_map):
    """
    Шифрує текст за допомогою моноалфавітного шифру підстановки,
    зберігаючи регістр літер, пробіли та переноси рядків.
    """
    encrypted = ''.join(substitution_map.get(char, char) for char in plain)
    return encrypted

def decrypt_substitution(cipher, substitution_map):
    """
    Дешифрує текст за допомогою моноалфавітного шифру підстановки,
    зберігаючи регістр літер, пробіли та переноси рядків.
    """
    reverse_map = {v: k for k, v in substitution_map.items()}
    decrypted = ''.join(reverse_map.get(char, char) for char in cipher)
    return decrypted

def get_letter_frequencies(text):
    """
    Підраховує частоти літер у тексті, ігноруючи пробіли та переноси рядків.
    """
    text = text.lower()
    letters = [char for char in text if char in LOWER_ALPHABET]
    frequency = Counter(letters)
    total = sum(frequency.values())
    frequencies = {char: count / total for char, count in frequency.items()}
    return frequencies

def get_most_frequent_letters(counter, n=5):
    """
    Повертає список з n найчастіших літер.
    """
    return [item[0] for item in counter.most_common(n)]

def plot_frequency_graph(frequencies, title='Частоти літер'):
    """
    Побудова графіку частот літер у тексті.
    """
    letters = list(frequencies.keys())
    freqs = list(frequencies.values())

    # Сортуємо за алфавітом
    letters_sorted, freqs_sorted = zip(*sorted(zip(letters, freqs)))

    plt.figure(figsize=(12, 6))
    plt.bar(letters_sorted, freqs_sorted, color='skyblue')
    plt.xlabel('Літери')
    plt.ylabel('Частота')
    plt.title(title)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def find_possible_mappings(cipher_freq_letters, language_freq_letters):
    """
    Знаходить можливі відповідності між найчастішими літерами шифротексту та мови.
    """
    mappings = {}
    for cipher_char, lang_char in zip(cipher_freq_letters, language_freq_letters):
        mappings[cipher_char] = lang_char
    return mappings

def apply_mapping(cipher, mapping):
    """
    Застосовує часткову карту відповідності для дешифрування тексту.
    """
    decrypted = ''
    for char in cipher:
        if char in mapping:
            decrypted += mapping[char]
        else:
            decrypted += char  # Залишаємо символ без змін
    return decrypted

def contains_known_words(text, word_list):
    """
    Перевіряє, чи містить текст відомі слова з word_list.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in word_list:
            return True
    return False

def main():
    # Крок 1: Генерація випадкової підстановки та шифрування тексту
    substitution_map = generate_substitution_cipher()

    # Зчитування відкритого тексту
    input_file = 'text_for_encryption.txt'
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            plain_text = f.read()
    except FileNotFoundError:
        print(f"Файл {input_file} не знайдено. Будь ласка, створіть файл з текстом для шифрування.")
        return

    cleaned_plain = clean_text(plain_text)
    encrypted_text = encrypt_substitution(cleaned_plain, substitution_map)

    # Збереження шифротексту та підстановки
    with open('encrypted_substitution.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_text)

    with open('substitution_map.json', 'w', encoding='utf-8') as f:
        json.dump(substitution_map, f, ensure_ascii=False, indent=4)

    print("Текст зашифровано та збережено у 'encrypted_substitution.txt'.")
    print("Підстановка збережена у 'substitution_map.json'.")

    # Крок 2: Криптоаналіз шифротексту
    cipher_file = 'encrypted_substitution.txt'
    try:
        with open(cipher_file, 'r', encoding='utf-8') as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print(f"Файл {cipher_file} не знайдено.")
        return

    cleaned_cipher = clean_text(cipher_text)
    cipher_frequencies = get_letter_frequencies(cleaned_cipher)
    cipher_counter = Counter([char for char in cleaned_cipher.lower() if char in LOWER_ALPHABET])
    cipher_freq_letters = get_most_frequent_letters(cipher_counter, n=5)
    print(f"Найчастіші літери в шифротексті: {cipher_freq_letters}")

    # Побудова графіку частот шифротексту
    plot_frequency_graph(cipher_frequencies, title='Частоти літер у шифротексті')

    # Найчастіші літери української мови (можна уточнити залежно від джерела)
    language_freq_letters = ['о', 'а', 'і', 'е', 'н']  # Можна додати 'т', 'р' тощо

    # Знаходження можливих відповідностей
    possible_mappings = find_possible_mappings(cipher_freq_letters, language_freq_letters)
    print(f"Можливі відповідності: {possible_mappings}")

    # Застосування знайдених відповідностей для початкового дешифрування
    decrypted_partial = apply_mapping(cipher_text, possible_mappings)
    print("\nПочатковий результат дешифрування з частковими відповідностями:")
    print(decrypted_partial)
    print('-' * 50)

    # Додатковий крок: Пошук повної відповідності
    # Для цього потрібно використовувати більш складні методи, наприклад, перевірку наявності відомих слів,
    # або використовувати алгоритми оптимізації (Hill-Climbing, Genetic Algorithms тощо).
    # Тут ми обмежимося початковим частковим дешифруванням.

    # Варіант автоматичного розширення відповідностей може бути доданий за необхідності

if __name__ == "__main__":
    main()
