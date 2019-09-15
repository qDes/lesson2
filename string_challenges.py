# Вывести последнюю букву в слове
word = 'Архангельск'
print(f"Последняя буква в {word} - {word[-1]}")


# Вывести количество букв "а" в слове
word = 'Архангельск'
print(f"Количество гласных в {word} - {word.lower().count('а')}")


# Вывести количество гласных букв в слове
vowels = {'а', 'о', 'и', 'е', 'ё', 'э','ы', 'у', 'ю', 'я'}
word = 'Архангельск'
value_vowels = 0
for char in word.lower():
    if char in vowels:
        value_vowels += 1
print(f'Количество гласных в "{word}" - {value_vowels}.')


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(f"Количество слов в предложении - {len(sentence.split())}")


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
for word in sentence.split():
    print(word[0])


# Вывести усреднённую длину слова.
sentence = 'Мы приехали в гости'

words = len(sentence.split())
chars = len(sentence.replace(' ',""))
print(chars/words)

