import sys
from math import gcd
from collections import Counter
import json

# Український алфавіт (тільки малі літери)
UKRAINIAN_ALPHABET = [
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з',
    'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
    'ь', 'ю', 'я'
]

def clean_text(text):
    """
    Очищає текст: перетворює у нижній регістр та видаляє всі символи,
    крім літер українського алфавіту, пробілів та переносів рядків.
    """
    allowed_chars = set(UKRAINIAN_ALPHABET + [' ', '\n'])
    cleaned = ''.join(char for char in text if char.lower() in allowed_chars or char in [' ', '\n'])
    return cleaned

def count_letters(text):
    """
    Підраховує кількість кожної літери в тексті, ігноруючи регістр.
    """
    return Counter(char.lower() for char in text if char.lower() in UKRAINIAN_ALPHABET)

def relative_frequency(counter):
    """
    Обчислює відносну частоту появи кожної літери.
    """
    total = sum(counter.values())
    if total == 0:
        return {letter: 0 for letter in UKRAINIAN_ALPHABET}
    return {letter: count / total for letter, count in counter.items()}

def affine_decrypt(cipher, a, b, alphabet):
    """
    Дешифрує текст, зашифрований афінним шифром, зберігаючи регістр літер.
    """
    m = len(alphabet)
    a_inv = None
    for i in range(m):
        if (a * i) % m == 1:
            a_inv = i
            break
    if a_inv is None:
        raise ValueError(f"Мультиплікативний обернений до a={a} не існує.")
    
    decrypted = ''
    for char in cipher:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            y = alphabet.index(char.lower())
            x = (a_inv * (y - b)) % m
            decrypted_char = alphabet[x]
            if is_upper:
                decrypted_char = decrypted_char.upper()
            decrypted += decrypted_char
        else:
            decrypted += char  # Залишаємо символи, які не в алфавіті (пробіли, перенос рядка, розділові знаки)
    return decrypted

def calculate_similarity(freq1, freq2):
    """
    Обчислює подібність між двома частотними словниками
    за методом сумарної абсолютної різниці.
    Чим менша подібність, тим більше схожість.
    """
    similarity = 0.0
    for letter in UKRAINIAN_ALPHABET:
        similarity += abs(freq1.get(letter, 0) - freq2.get(letter, 0))
    return similarity

def affine_cracking(cipher, alphabet, freq_reference):
    """
    Виконує криптоаналіз зашифрованого тексту методом афінного шифру
    з використанням брутфорс-підходу та частотного аналізу.
    """
    cipher_freq = relative_frequency(count_letters(cipher))
    
    best_similarity = float('inf')
    best_keys = []
    
    # Перебираємо всі можливі ключі (a, b)
    for a in range(1, len(alphabet)):
        if gcd(a, len(alphabet)) != 1:
            continue
        for b in range(0, len(alphabet)):
            try:
                decrypted = affine_decrypt(cipher, a, b, alphabet)
                decrypted_freq = relative_frequency(count_letters(decrypted))
                similarity = calculate_similarity(decrypted_freq, freq_reference)
                
                if similarity < best_similarity:
                    best_similarity = similarity
                    best_keys = [(a, b, decrypted)]
                elif similarity == best_similarity:
                    best_keys.append((a, b, decrypted))
            except Exception as e:
                continue
    
    if best_keys:
        print(f"\nЗнайдено ключів з найнижчою подібністю {best_similarity:.6f}:")
        for (a, b, decrypted) in best_keys:
            print(f"\nСпроба ключів a={a}, b={b}:")
            print(decrypted)
    else:
        print("Не вдалося знайти можливі ключі.")

def perform_crypto_analysis(encrypted_file, alphabet, freq_reference):
    """
    Виконує криптоаналіз для одного зашифрованого файлу.
    """
    try:
        with open(encrypted_file, 'r', encoding='utf-8') as file:
            cipher = file.read()
            cipher = clean_text(cipher)
    except Exception as e:
        print(f"Помилка при обробці файлу {encrypted_file}: {e}")
        return
    
    print(f"\nКриптоаналіз файлу: {encrypted_file}")
    affine_cracking(cipher, alphabet, freq_reference)

def main():
    """
    Основна функція, яка пропонує меню для виконання криптоаналізу.
    """
    print("Лабораторна робота №4: Криптоаналіз з Використанням Афінного Шифру")
    print("Можливі дії:")
    print("1. Криптоаналіз зашифрованих текстів")
    print("2. Вихід")
    
    # Завантаження референсних частот українських літер
    try:
        with open('freq_reference.json', 'r', encoding='utf-8') as json_file:
            freq_reference = json.load(json_file)
    except FileNotFoundError:
        print("Файл freq_reference.json не знайдено. Будь ласка, виконайте завдання 1 з окремого корпусу текстів перед криптоаналізом.")
        return
    
    while True:
        choice = input("\nВиберіть дію (1-2): ")
        
        if choice == '1':
            # Криптоаналіз зашифрованих текстів
            print("\n--- Криптоаналіз зашифрованих текстів ---")
            encrypted_file = 'encrypted.txt'  # Використовуємо один файл
            perform_crypto_analysis(encrypted_file, UKRAINIAN_ALPHABET, freq_reference)
        
        elif choice == '2':
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Будь ласка, виберіть номер від 1 до 2.")

if __name__ == "__main__":
    main()
