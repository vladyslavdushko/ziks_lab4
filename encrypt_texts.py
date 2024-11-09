import sys
import random
from math import gcd

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

def get_affine_keys(m):
    """
    Генерує випадкові ключі a та b для афінного шифру, де a взаємно просте з m.
    """
    while True:
        a = random.randint(1, m-1)
        if gcd(a, m) == 1:
            break
    b = random.randint(0, m-1)
    return a, b

def affine_encrypt(text, a, b, alphabet):
    """
    Шифрує текст за допомогою афінного шифру, зберігаючи регістр літер.
    """
    m = len(alphabet)
    encrypted = ''
    for char in text:
        if char.lower() in alphabet:
            is_upper = char.isupper()
            x = alphabet.index(char.lower())
            y = (a * x + b) % m
            encrypted_char = alphabet[y]
            if is_upper:
                encrypted_char = encrypted_char.upper()
            encrypted += encrypted_char
        else:
            encrypted += char  # Залишаємо символи, які не в алфавіті (пробіли, перенос рядка, розділові знаки)
    return encrypted

def save_encrypted_text(encrypted_text, a, b):
    """
    Зберігає зашифрований текст у файл та ключі у keys.txt.
    """
    with open('encrypted_affine.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    
    with open('keys.txt', 'w', encoding='utf-8') as key_file:
        key_file.write(f"a={a}\nb={b}\n")
    
    print(f"\nТекст зашифрований з використанням ключів a={a}, b={b} та збережений у encrypted_affine.txt.")
    print("Ключі шифрування збережено у файлі keys.txt.")

def main():
    """
    Основна функція для шифрування тексту з файлу.
    """
    input_file = 'text_for_encryption.txt'
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Файл {input_file} не знайдено. Будь ласка, створіть файл з текстом для шифрування.")
        return
    
    cleaned_text = clean_text(text)
    m = len(UKRAINIAN_ALPHABET)
    a, b = get_affine_keys(m)
    encrypted_text = affine_encrypt(cleaned_text, a, b, UKRAINIAN_ALPHABET)
    save_encrypted_text(encrypted_text, a, b)

if __name__ == "__main__":
    main()
    