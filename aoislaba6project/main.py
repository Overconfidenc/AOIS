from hash_table import create_table_from_dict
from hash_utils import standardize_key, format_entry
from terms_med import terms_med

dictionary = create_table_from_dict(terms_med)

print("Добро пожаловать в медицинский словарь!")
while True:
    user_choice = input("""
1) Показать все термины
2) Найти определение
3) Добавить термин
4) Удалить термин
0) Выход
Выберите действие: """)

    match user_choice:
        case '1':
            print('\n', dictionary)

        case '2':
            search_key = standardize_key(input("Введите термин: "))
            definition = dictionary.retrieve(search_key)
            if definition is None:
                print("Термин не найден.")
            else:
                print(format_entry(dictionary, search_key))

        case '3':
            new_term = standardize_key(input("Введите новый термин: "))
            if dictionary.retrieve(new_term) is None:
                new_definition = input("Введите определение: ")
                dictionary.insert(new_term, new_definition)
                print("Термин добавлен!")
            else:
                print("Термин уже существует:")
                print(format_entry(dictionary, new_term))

        case '4':
            term_to_remove = standardize_key(input("Введите термин для удаления: "))
            if not dictionary.remove(term_to_remove):
                print("Термин не найден.")
            else:
                print("Термин удалён!")

        case '0':
            print("Работа завершена.")
            break

        case _:
            print("Неверный ввод!")