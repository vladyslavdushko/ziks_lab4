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

def count_ngrams(text, n):
    """
    Підраховує кількість n-грам в тексті.
    """
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    return Counter(ngrams)

def relative_frequency_ngrams(counter):
    """
    Обчислює відносну частоту появи кожної n-грам.
    """
    total = sum(counter.values())
    return {ngram: count / total for ngram, count in counter.items()}

def print_top_ngrams(freq_dict, top_n=30, ngram_type='Триграм'):
    """
    Виводить топ-N найбільш імовірних n-грам.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)[:top_n]
    print(f"\nТоп {top_n} {ngram_type}:")
    for ngram, freq in sorted_items:
        print(f"{ngram}: {freq:.4f}")

def plot_trigrams(freq_dict, title):
    """
    Будує діаграму відносної частоти 30 найбільш імовірних триграм.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)[:30]
    trigrams, frequencies = zip(*sorted_items)
    
    plt.figure(figsize=(20,10))
    sns.barplot(x=trigrams, y=frequencies, palette='plasma')
    plt.title(title)
    plt.xlabel('Триграми')
    plt.ylabel('Відносна частота')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def create_trigrams_matrix(freq_dict):
    """
    Створює теплову карту частот появи триграм.
    """
    letters = UKRAINIAN_ALPHABET
    matrix = pd.DataFrame(0, index=letters, columns=letters)
    
    for trigram, freq in freq_dict.items():
        if len(trigram) == 3:
            first, second, third = trigram
            if first in letters and second in letters and third in letters:
                # Для теплової карти ми можемо розглядати тільки першу дві літери
                matrix.at[first, second] += freq  # Або інший підхід для триграм
                # Зверніть увагу: матриця для триграм складніша, тому для спрощення ми використовуємо тільки перші дві літери
    plt.figure(figsize=(12,10))
    sns.heatmap(matrix, annot=False, cmap='Greens')
    plt.title('Матриця частот триграм')
    plt.xlabel('Друга літера')
    plt.ylabel('Перша літера')
    plt.tight_layout()
    plt.show()

def save_frequencies_to_json(data, filename):
    """
    Зберігає частоти в JSON файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Частоти збережено у файлі '{filename}'.")

def main(file_paths):
    """
    Основна функція для підрахунку та виводу частотних характеристик триграм.
    """
    combined_trigrams = Counter()
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned = clean_text(text)
                trigrams = count_ngrams(cleaned.replace(' ', ''), 3)
                combined_trigrams.update(trigrams)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
            continue
    
    freq_trigrams = relative_frequency_ngrams(combined_trigrams)
    
    # Збереження топ-30 триграм у JSON
    top_trigrams = get_most_frequent_ngrams(combined_trigrams, n=30)
    top_trigrams_freq = {tg: freq for tg, freq in top_trigrams}
    save_frequencies_to_json(top_trigrams_freq, 'top30_trigrams.json')
    
    # Таблиця триграм, відсортована за спаданням частоти
    sorted_trigrams = sorted(freq_trigrams.items(), key=lambda item: item[1], reverse=True)
    df_trigrams = pd.DataFrame(sorted_trigrams, columns=['Триграм', 'Відносна частота'])
    print("\nТаблиця триграм (сортування за спаданням частоти):")
    print(df_trigrams.to_string(index=False))
    
    # Топ-30 триграм
    print_top_ngrams(freq_trigrams, top_n=30, ngram_type='триграм')
    
    # Діаграма топ-30 триграм
    plot_trigrams(freq_trigrams, 'Відносна частота 30 найбільш імовірних триграм')
    
    # Матриця частот триграм
    create_trigrams_matrix(freq_trigrams)

def get_most_frequent_ngrams(counter, n=30):
    """
    Повертає список з n найчастіших n-грам.
    """
    return counter.most_common(n)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python3 task3_trigram_frequency.py <file1> <file2> ...")
    else:
        main(sys.argv[1:])
