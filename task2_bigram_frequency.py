import sys
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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

def print_top_ngrams(freq_dict, top_n=30, ngram_type='Біграм'):
    """
    Виводить топ-N найбільш імовірних n-грам.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)[:top_n]
    print(f"\nТоп {top_n} {ngram_type}:")
    for ngram, freq in sorted_items:
        print(f"{ngram}: {freq:.4f}")

def plot_bigrams(freq_dict, title):
    """
    Будує діаграму відносної частоти 30 найбільш імовірних біграм.
    """
    sorted_items = sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)[:30]
    bigrams, frequencies = zip(*sorted_items)
    
    plt.figure(figsize=(16,8))
    sns.barplot(x=bigrams, y=frequencies, palette='coolwarm')
    plt.title(title)
    plt.xlabel('Біграми')
    plt.ylabel('Відносна частота')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_bigrams_matrix(freq_dict):
    """
    Створює теплову карту частот появи біграм.
    """
    letters = UKRAINIAN_ALPHABET
    matrix = pd.DataFrame(0, index=letters, columns=letters)
    
    for bigram, freq in freq_dict.items():
        if len(bigram) == 2:
            first, second = bigram
            if first in letters and second in letters:
                matrix.at[first, second] = freq
    
    plt.figure(figsize=(12,10))
    sns.heatmap(matrix, annot=False, cmap='Blues')
    plt.title('Матриця частот біграм')
    plt.xlabel('Друга літера')
    plt.ylabel('Перша літера')
    plt.tight_layout()
    plt.show()

def main(file_paths):
    """
    Основна функція для підрахунку та виводу частотних характеристик біграм.
    """
    combined_bigrams = Counter()
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned = clean_text(text)
                bigrams = count_ngrams(cleaned.replace(' ', ''), 2)
                combined_bigrams.update(bigrams)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
            continue
    
    freq_bigrams = relative_frequency_ngrams(combined_bigrams)
    
    # Таблиця біграм, відсортована за спаданням частоти
    sorted_bigrams = sorted(freq_bigrams.items(), key=lambda item: item[1], reverse=True)
    df_bigrams = pd.DataFrame(sorted_bigrams, columns=['Біграм', 'Відносна частота'])
    print("\nТаблиця біграм (сортування за спаданням частоти):")
    print(df_bigrams.to_string(index=False))
    
    # Топ-30 біграм
    print_top_ngrams(freq_bigrams, top_n=30, ngram_type='біграм')
    
    # Діаграма топ-30 біграм
    plot_bigrams(freq_bigrams, 'Відносна частота 30 найбільш імовірних біграм')
    
    # Матриця частот біграм
    create_bigrams_matrix(freq_bigrams)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python3 task2_bigram_frequency.py <file1> <file2> ...")
    else:
        main(sys.argv[1:])
