import sys
from math import gcd
from collections import Counter
import json
import re
import matplotlib.pyplot as plt  # Додано для побудови графіків

# Український алфавіт
LOWER_ALPHABET = [
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з',
    'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
    'ь', 'ю', 'я'
]

UPPER_ALPHABET = [char.upper() for char in LOWER_ALPHABET]

ALPHABET = LOWER_ALPHABET + UPPER_ALPHABET
ALPHABET_DICT = {char: idx for idx, char in enumerate(ALPHABET)}

m = len(LOWER_ALPHABET)  # Розмір алфавіту для модульних операцій (33)

def clean_text(text):
    """
    Очищає текст: видаляє всі символи, крім літер українського алфавіту,
    пробілів та переносів рядків.
    """
    allowed_chars = set(ALPHABET + [' ', '\n'])
    cleaned = ''.join(char for char in text if char in allowed_chars)
    return cleaned

def modinv(a, m):
    """
    Обчислює мультиплікативний обернений до a за модулем m.
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def extended_gcd(a, b):
    """
    Розширений алгоритм Евкліда.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def affine_encrypt(plain, a, b):
    """
    Шифрує текст за допомогою афінного шифру, зберігаючи регістр літер,
    пробіли та переноси рядків.
    """
    encrypted = ''
    for char in plain:
        if char in LOWER_ALPHABET:
            x = LOWER_ALPHABET.index(char)
            y = (a * x + b) % m
            encrypted_char = LOWER_ALPHABET[y]
            encrypted += encrypted_char
        elif char in UPPER_ALPHABET:
            x = UPPER_ALPHABET.index(char)
            y = (a * x + b) % m
            encrypted_char = UPPER_ALPHABET[y]
            encrypted += encrypted_char
        else:
            encrypted += char  # Залишаємо пробіли, переноси та інші символи без змін
    return encrypted

def affine_decrypt(cipher, a, b):
    """
    Дешифрує текст за допомогою афінного шифру, зберігаючи регістр літер,
    пробіли та переноси рядків.
    """
    a_inv = modinv(a, m)
    if a_inv is None:
        return None
    decrypted = ''
    for char in cipher:
        if char in LOWER_ALPHABET:
            y = LOWER_ALPHABET.index(char)
            x = (a_inv * (y - b)) % m
            decrypted_char = LOWER_ALPHABET[x]
            decrypted += decrypted_char
        elif char in UPPER_ALPHABET:
            y = UPPER_ALPHABET.index(char)
            x = (a_inv * (y - b)) % m
            decrypted_char = UPPER_ALPHABET[x]
            decrypted += decrypted_char
        else:
            decrypted += char  # Залишаємо пробіли, переноси та інші символи без змін
    return decrypted

def get_letter_frequencies(text):
    """
    Підраховує частоти літер у тексті, ігноруючи пробіли та переноси рядків.
    """
    frequencies = {}
    total_letters = 0
    for char in text:
        if char in LOWER_ALPHABET:
            char_lower = char
        elif char in UPPER_ALPHABET:
            char_lower = char.lower()
        else:
            continue  # Пропускаємо пробіли та інші символи
        frequencies[char_lower] = frequencies.get(char_lower, 0) + 1
        total_letters += 1
    for char in frequencies:
        frequencies[char] /= total_letters
    return frequencies

def get_most_frequent_letters(frequencies, n=5):
    return [item[0] for item in sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:n]]

def find_possible_keys(alphabet, cipher_freq_letters, language_freq_letters):
    m = len(LOWER_ALPHABET)
    possible_keys = []
    for y1_char in cipher_freq_letters:
        for y2_char in cipher_freq_letters:
            if y1_char == y2_char:
                continue
            for x1_char in language_freq_letters:
                for x2_char in language_freq_letters:
                    if x1_char == x2_char:
                        continue
                    y1 = LOWER_ALPHABET.index(y1_char)
                    y2 = LOWER_ALPHABET.index(y2_char)
                    x1 = LOWER_ALPHABET.index(x1_char)
                    x2 = LOWER_ALPHABET.index(x2_char)
                    delta_x = (x1 - x2) % m
                    delta_y = (y1 - y2) % m
                    if gcd(delta_x, m) != 1:
                        continue
                    inv_delta_x = modinv(delta_x, m)
                    if inv_delta_x is None:
                        continue
                    a_candidate = (delta_y * inv_delta_x) % m
                    if gcd(a_candidate, m) != 1:
                        continue
                    b_candidate = (y1 - a_candidate * x1) % m
                    possible_keys.append((a_candidate, b_candidate))
    return possible_keys

def contains_known_words(text, word_list):
    """
    Перевіряє, чи містить текст відомі слова з word_list.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in word_list:
            return True
    return False

def plot_frequency_graph(frequencies):
    """
    Побудова графіку частот літер у тексті.
    """
    import matplotlib.pyplot as plt

    letters = list(frequencies.keys())
    freqs = list(frequencies.values())

    # Сортуємо за алфавітом
    letters, freqs = zip(*sorted(zip(letters, freqs)))

    plt.figure(figsize=(12, 6))
    plt.bar(letters, freqs, color='skyblue')
    plt.xlabel('Літери')
    plt.ylabel('Частота')
    plt.title('Частоти літер у шифротексті')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def main():
    encrypted_file = 'encrypted_affine.txt'
    try:
        with open(encrypted_file, 'r', encoding='utf-8') as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print(f"Файл {encrypted_file} не знайдено.")
        return

    cleaned_cipher = clean_text(cipher_text)

    cipher_frequencies = get_letter_frequencies(cleaned_cipher)
    cipher_freq_letters = get_most_frequent_letters(cipher_frequencies, n=5)
    print(f"Найчастіші літери в шифротексті: {cipher_freq_letters}")

    # Побудова графіку частот
    plot_frequency_graph(cipher_frequencies)

    # Найчастіші літери української мови
    language_freq_letters = ['о', 'а', 'і', 'е', 'н', 'т']

    possible_keys = find_possible_keys(LOWER_ALPHABET, cipher_freq_letters, language_freq_letters)
    print(f"Знайдено {len(possible_keys)} можливих ключів.")

    # Завантажуємо список відомих слів (можна використовувати частотний словник української мови)
    # Для прикладу, використовуємо короткий список
    known_words = ['і', 'в', 'на', 'що', 'не', 'я', 'з', 'у', 'як', 'та']

    for a, b in possible_keys:
        decrypted_text = affine_decrypt(cipher_text, a, b)
        if decrypted_text:
            if contains_known_words(decrypted_text, known_words):
                print(f"\nМожливий ключ: a = {a}, b = {b}")
                print("Розшифрований текст:")
                print(decrypted_text)
                print('-' * 50)
                # Можна додати перевірку на кількість відомих слів та вибрати найкращий варіант

if __name__ == "__main__":
    main()
