from collections import Counter

def get_most_frequent_name(names):
    return max(set(names), key = names.count)

def get_name_list(students):
    return list(student.get('first_name') for student in students)


# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика.
students = [
  {'first_name': 'Вася'},
  {'first_name': 'Петя'},
  {'first_name': 'Маша'},
  {'first_name': 'Маша'},
  {'first_name': 'Петя'},
]
# ???

print('#'*10)
print("Problem 1.")
names = get_name_list(students)
for name, value in Counter(names).items():
    print(f"{name}: {value}")

print('#'*10)

# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2


# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя.
students = [
        {'first_name': 'Вася'},
  {'first_name': 'Петя'},
  {'first_name': 'Маша'},
  {'first_name': 'Маша'},
  {'first_name': 'Оля'},
]
print('#'*10)
print('Problem 2.')
# ???
names = get_name_list(students)
print('Самое частое имя:',get_most_frequent_name(names)) 
print('#' * 10)
# Пример вывода
# Самое частое имя среди учеников: Маша

# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
school_students = [
  [  # это – первый класс
    {'first_name': 'Вася'},
    {'first_name': 'Вася'},
  ],
  [  # это – второй класс
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
  ]
]

print('#'*10)
print('Problem 3.')

for num, group in enumerate(school_students):
    names = get_name_list(group)
    frq_name = get_most_frequent_name(names)
    print(f"Самое частое имя в классе {num+1}: {frq_name}")
print('#'*10)
# ???


# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша


# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
school = [
  {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
  {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
  'Маша': False,
  'Оля': False,
  'Олег': True,
  'Миша': True,
}
# ???
print('#'*10)
print('Problem 4.')

for group in school:
    names = get_name_list(group.get('students'))
    boys, girls = 0, 0
    for name in names:
        if is_male[name]:
            boys += 1
        else:
            girls += 1
    group_name = group.get('class')
    print(f"В классе {group_name} {girls} девочки и {boys} мальчика")
print('#'*10)
# Пример вывода:
# В классе 2a 2 девочки и 0 мальчика.
# В классе 3c 0 девочки и 2 мальчика.

# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков.
school = [
  {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
  {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
  'Маша': False,
  'Оля': False,
  'Олег': True,
  'Миша': True,
}
# ???
print('Problem 5.')
max_dict = {
        'boys':{'class':'','value': 0 },
        'girls':{'class':'', 'value': 0}
        }


for group in school:
    names = get_name_list(group.get('students'))
    boys, girls = 0, 0
    for name in names:
        if is_male[name]:
            boys += 1
        else:
            girls += 1
    group_name = group.get('class')
    
    if max_dict['boys']['value'] < boys:
        max_dict['boys']['value'] = boys
        max_dict['boys']['class'] = group_name
    
    if max_dict['girls']['value'] < girls:
        max_dict['girls']['value'] = girls
        max_dict['girls']['class'] = group_name

print('Больше всего мальчиков в классе',max_dict['boys']['class'])
print('Больше всего девочек в классе',max_dict['girls']['class'])


# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

