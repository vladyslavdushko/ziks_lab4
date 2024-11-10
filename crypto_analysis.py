import sys
from math import gcd
from collections import Counter
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    Очищає текст: перетворює у нижній регістр та видаляє всі символи, крім літер українського алфавіту,
    пробілів та переносів рядків.
    """
    text = text.lower()
    allowed_chars = set(LOWER_ALPHABET + [' ', '\n'])
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
        else:
            continue  # Пропускаємо пробіли та інші символи
        frequencies[char_lower] = frequencies.get(char_lower, 0) + 1
        total_letters += 1
    for char in frequencies:
        frequencies[char] /= total_letters
    return frequencies

def get_most_frequent_letters(freq_dict, n=5):
    """
    Повертає список з n найчастіших літер.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)
    return [item[0] for item in sorted_items[:n]]

def count_ngrams(text, n):
    """
    Підраховує кількість n-грам в тексті.
    """
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return Counter(ngrams)

def get_most_frequent_ngrams(counter, n=30):
    """
    Повертає список з n найчастіших n-грам.
    """
    return counter.most_common(n)

def plot_frequency_graph(frequencies, title='Частоти літер у шифротексті'):
    """
    Побудова графіку частот літер у тексті.
    """
    letters = list(frequencies.keys())
    freqs = list(frequencies.values())

    # Сортуємо за алфавітом
    letters_sorted, freqs_sorted = zip(*sorted(zip(letters, freqs)))

    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(letters_sorted), y=list(freqs_sorted), palette='viridis', edgecolor='black')
    plt.xlabel('Літери')
    plt.ylabel('Частота')
    plt.title(title)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def plot_ngrams(ngrams, frequencies, title):
    """
    Побудова графіку частот n-грам.
    """
    plt.figure(figsize=(20, 10))
    sns.barplot(x=ngrams, y=frequencies, palette='viridis', edgecolor='black')
    plt.title(title)
    plt.xlabel('N-грам')
    plt.ylabel('Частота')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def save_frequencies_to_json(data, filename):
    """
    Зберігає частоти в JSON файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Частоти збережено у файлі '{filename}'.")

def load_frequencies_from_json(filename):
    """
    Завантажує частоти з JSON файлу.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
        return {}

def contains_known_words(text, word_list):
    """
    Перевіряє, чи містить текст відомі слова з word_list.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in word_list:
            return True
    return False

def find_possible_keys(alphabet, cipher_freq_letters, language_freq_letters):
    """
    Знаходить можливі ключі на основі найчастіших літер.
    Використовує set для уникнення дублікатів.
    """
    possible_keys = set()
    for y1_char in cipher_freq_letters:
        for y2_char in cipher_freq_letters:
            if y1_char == y2_char:
                continue
            for x1_char in language_freq_letters:
                for x2_char in language_freq_letters:
                    if x1_char == x2_char:
                        continue
                    try:
                        y1 = LOWER_ALPHABET.index(y1_char)
                        y2 = LOWER_ALPHABET.index(y2_char)
                        x1 = LOWER_ALPHABET.index(x1_char)
                        x2 = LOWER_ALPHABET.index(x2_char)
                    except ValueError:
                        continue
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
                    possible_keys.add((a_candidate, b_candidate))
    return list(possible_keys)

def score_decrypted_text(decrypted_text, known_words, bigram_freq, trigram_freq):
    """
    Оцінює розшифрований текст на основі наявності відомих слів та відповідності біграм і триграм.
    """
    score = 0
    # Перевірка наявності відомих слів
    for word in known_words:
        if word in decrypted_text:
            score += 1
    # Аналіз біграм
    decrypted_bigrams = count_ngrams(decrypted_text.replace(' ', ''), 2)
    for bg in decrypted_bigrams:
        if bg in bigram_freq:
            score += bigram_freq[bg]
    # Аналіз триграм
    decrypted_trigrams = count_ngrams(decrypted_text.replace(' ', ''), 3)
    for tg in decrypted_trigrams:
        if tg in trigram_freq:
            score += trigram_freq[tg]
    return score

def main():
    # Шлях до зашифрованого тексту
    encrypted_file = 'encrypted_affine.txt'
    try:
        with open(encrypted_file, 'r', encoding='utf-8') as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print(f"Файл '{encrypted_file}' не знайдено.")
        return

    cleaned_cipher = clean_text(cipher_text)

    # Частотний аналіз літер
    cipher_frequencies = get_letter_frequencies(cleaned_cipher)
    cipher_freq_letters = get_most_frequent_letters(cipher_frequencies, n=5)
    print(f"Найчастіші літери в шифротексті: {cipher_freq_letters}")

    # Побудова графіку частот літер
    plot_frequency_graph(cipher_frequencies)

    # Частотний аналіз біграм
    bigrams = count_ngrams(cleaned_cipher.replace(' ', ''), 2)
    top_bigrams = get_most_frequent_ngrams(bigrams, n=30)
    bigram_freq = {bg: freq for bg, freq in top_bigrams}
    save_frequencies_to_json(bigram_freq, 'top30_bigrams_encrypted_affine.json')
    plot_ngrams([bg for bg, _ in top_bigrams], [freq for _, freq in top_bigrams], 'Топ-30 біграм у шифротексті')

    # Частотний аналіз триграм
    trigrams = count_ngrams(cleaned_cipher.replace(' ', ''), 3)
    top_trigrams = get_most_frequent_ngrams(trigrams, n=30)
    trigram_freq = {tg: freq for tg, freq in top_trigrams}
    save_frequencies_to_json(trigram_freq, 'top30_trigrams_encrypted_affine.json')
    plot_ngrams([tg for tg, _ in top_trigrams], [freq for _, freq in top_trigrams], 'Топ-30 триграм у шифротексті')

    # Завантаження референсних частот біграм та триграм
    # Припустимо, вони збережені у файлах 'top30_bigrams.json' та 'top30_trigrams.json'
    ref_bigram_freq = load_frequencies_from_json('top30_bigrams.json')
    ref_trigram_freq = load_frequencies_from_json('top30_trigrams.json')

    # Найчастіші літери української мови
    language_freq_letters = ['о', 'а', 'і', 'е', 'н', 'т']

    # Знаходження можливих ключів на основі частотного аналізу літер
    possible_keys = find_possible_keys(LOWER_ALPHABET, cipher_freq_letters, language_freq_letters)
    print(f"Знайдено {len(possible_keys)} можливих ключів.")

    # Список відомих слів для перевірки
    known_words = ['і', 'в', 'на', 'що', 'не', 'я', 'з', 'у', 'як', 'та', 'це', 'до', 'то', 'від', 'за', 'по', 'мені', 'ти', 'ми', 'вони']

    # Криптоаналіз: спроба знайти ключі на основі частотного аналізу
    key_scores = []
    for a, b in possible_keys:
        decrypted_text = affine_decrypt(cleaned_cipher, a, b)
        if decrypted_text:
            score = score_decrypted_text(decrypted_text, known_words, ref_bigram_freq, ref_trigram_freq)
            if score > 0:
                key_scores.append((a, b, score, decrypted_text))

    # Відсортувати ключі за оцінкою
    key_scores = sorted(key_scores, key=lambda x: x[2], reverse=True)

    # Вивести найкращі ключі
    for a, b, score, decrypted_text in key_scores[:5]:  # Вивести топ-5
        print(f"\nМожливий ключ: a = {a}, b = {b}, оцінка = {score}")
        print("Розшифрований текст:")
        print(decrypted_text)
        print('-' * 50)

    if not key_scores:
        print("Не знайдено можливих ключів для шифротексту за допомогою частотного аналізу.")
    else:
        print("Криптоаналіз завершено.")

if __name__ == "__main__":
    main()
