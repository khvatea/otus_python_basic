import json
import sys
import os

from prettytable import PrettyTable
import difflib


def handbook_open(handbook_file: str) -> list:
    """
    Open phone book directory from file
    :param handbook_file: JSON file containing phone book contact entries
    :return: List object, with contacts in dict format
    """
    # Create a temporary buffer file
    handbook_buffer_file = "buff.{}".format(handbook_file)

    with open(handbook_file, "r", encoding='utf8') as handbook_json:
        handbook_buffer = json.load(handbook_json)

    with open(handbook_buffer_file, "w", encoding='utf8') as handbook_buffer_json:
        json.dump(handbook_buffer, handbook_buffer_json, ensure_ascii=False, indent=4)

    return handbook_buffer


def save_handbook(handbook_file: str, handbook: list):
    """
    Save the handbook in JSON format
    :param handbook_file: path to the handbook JSON file
    :param handbook: list of handbook entries
    :return:
    """
    with open(handbook_file, "w", encoding='utf8') as handbook_json:
        json.dump(handbook, handbook_json, ensure_ascii=False, indent=4)


def handbook_show_all_rows(handbook: list, sort_by_field="name") -> str:
    """
    Get all handbook entries sorted by the selected field (by default, sorting will be done by the 'name' field)
    :param handbook: list of handbook entries
    :param sort_by_field: Table sort field
    :return: Return string representation of table in current state
    """
    pretty_table = PrettyTable()

    # set table field names
    pretty_table.field_names = ["name", "phone", "email", "address"]
    pretty_table.align["name"] = "l"
    pretty_table.align["address"] = "l"

    # place all lines from the dictionary into a table
    for contact in handbook:
        pretty_table.add_row(list(contact.values()))

    return pretty_table.get_string(sortby=sort_by_field)


def add_raw(handbook: list, new_contact: dict):
    """
    Add an entry to the handbook
    :param handbook: list of handbook entries
    :param new_contact: New contact in dict format
    :return:
    """
    expected_field_names = {"name", "phone", "email", "address"}

    if isinstance(new_contact, dict):
        missing_keys = expected_field_names - new_contact.keys()
        extra_keys = new_contact.keys() - expected_field_names

        if missing_keys:
            print(f"Ошибка при записи контакта. Отсутствуют ключи: {missing_keys}")
        elif extra_keys:
            print(f"Ошибка при записи контакта. Лишние ключи: {extra_keys}")
        else:
            handbook.append(new_contact)
    else:
        print(f"""
        В функции передан: {type(new_contact)}
        Требуется dict
        """)


def find_raws(handbook: list, search_string: str, find_by_field="name") -> list:
    """
    Searching for contacts in the handbook
    :param handbook: list of handbook entries
    :param search_string: Search string
    :param find_by_field: Field to search for
    :return: Search result
    """
    result = [contact for contact in handbook if search_string in contact[find_by_field]]
    return result


def update_raw(handbook: list, name: str, update_contact: dict) -> dict:
    """
    Update a handbook entry
    :param handbook: list of handbook entries
    :param name: Name of the record that is being updated
    :param update_contact: Data according to handbook fields in dict format
    :return: Updated contact
    """
    for contact in handbook:
        if contact["name"] == name:
            contact.update(update_contact)
            return contact


def delete_raw(handbook: list, name: str):
    """
    Removing an entry from the handbook
    :param handbook: list of handbook entries
    :param name: Name of the entry to be deleted
    :return: Remove contact in dict format
    """
    for contact in handbook:
        if contact["name"] == name:
            handbook.remove(contact)
            return contact
    return None

def handbooks_compare(handbook_source: str, handbook_buffer: str) -> list:
    """
    Comparison of the handbook before and after the change
    :param handbook_source: Main handbook file
    :param handbook_buffer: Handbook buffer file
    :return: List of changes
    """
    with open(handbook_source, "r", encoding='utf8') as source:
        source_json = json.load(source)

    with open(handbook_buffer, "r", encoding='utf8') as buffer:
        source_buffer = json.load(buffer)

    ret = []
    before = [str(raw) for raw in source_json]
    after = [str(raw) for raw in source_buffer]
    difflist = difflib.ndiff(before, after)

    for line in difflist:
        if line.startswith(u'+'):
            ret.append("\033[3m\033[32m{}\033[0m\n".format(line))
        elif line.startswith(u'-'):
            ret.append("\033[3m\033[31m{}\033[0m\n".format(line))
        elif line.startswith(u'?'):
            ret.append("{}".format(line))
    return ret

######################
def menu(handbook: list, level="0") -> str:
    """
    Main menu of the handbook
    :param handbook: list of handbook entries
    :param level: Menu level
    :return: The string received when entering from the console
    """
    if level == "0":
        print("\nВыберите действие:")
        print("1. Открыть справочник")
        if handbook:
            print("2. Показать все контакты")
            print("3. Показать изменения")
            print("4. Создать контакт")
            print("5. Найти контакт")
            print("6. Обновить контакт")
            print("7. Удалить контакт")
        print("8. Выйти и сохранить")

    elif level == "2":
        print("\t1. Сортировать по имени")
        print("\t1. Сортировать по адресу")
        print("\t3. Сортировать по телефону")

    return input("Введите номер действия: ")


def main():
    """
    Interactive processing of the handbook
    :return:
    """
    hndbook = []
    hndbook_file = "handbook.json"
    hndbook_buffer_file = "buff.{}".format(hndbook_file)

    while True:
        choice = menu(hndbook)

        if choice == '1':
            hndbook = handbook_open(hndbook_file)

        elif choice == '2':
            choice = menu(hndbook, choice)
            field_names = {"1": "name", "2": "address", "3": "phone"}
            if choice in field_names:
                print(handbook_show_all_rows(hndbook, field_names[choice]))
            else:
                sys.stdout.writelines("\033[31mНеправильный ввод. Пожалуйста, попробуйте снова.\033[0m\n")

        elif choice == '3':
            save_handbook(hndbook_buffer_file, hndbook)
            hndbook_changes = handbooks_compare(hndbook_file, hndbook_buffer_file)
            if not hndbook_changes:
                sys.stdout.writelines("\033[34mИзменений в справочнике нет.\033[0m\n")
            else:
                sys.stdout.writelines(hndbook_changes)

        elif choice == '4':
            new_contact = {"name": "undefined", "phone": "undefined", "email": "undefined", "address": "undefined"}

            print("\nЗаполните поля нового контакта")
            for key, value in new_contact.items():
                new_contact[key] = input(f"{key}: ")

            add_raw(hndbook, new_contact)

        elif choice == '5':
            find_contacts = find_raws(hndbook, input("\nКого ищем?: "))
            print(handbook_show_all_rows(find_contacts))

        elif choice == '6':
            contact = input("\nВведите полное имя контакта: ")
            if contact == "":
                continue
            find_contacts = find_raws(hndbook, contact)

            if find_contacts:
                update_contact = find_contacts[0]
                print(f"\nОбновите поля контакта {update_contact['name']}")
                for key, value in update_contact.items():
                    item = input(f"{key} (сейчас ==> {value}): ")
                    if item != "":
                        update_contact[key] = item
                print(update_raw(hndbook, contact, update_contact))
            else:
                sys.stdout.writelines("\033[34mЗапрошенный контакт не найден.\033[0m\n")


        elif choice == '7':
            contact = input("\nВведите полное имя контакта для удаления: ")

            status_operation = delete_raw(hndbook, contact)
            if status_operation:
                print(f"Запись {status_operation} успешно удалена.")
            else:
                print("""
                Контакт не удален, т.к. не был найден.
                Убедитесь в правильности и полноте указанного имени.
                Воспользуйтесь поиском по контактам (п. 6).
                """)

        elif choice == '8':
            if hndbook:
                save_handbook(hndbook_buffer_file, hndbook)
                hndbook_changes = handbooks_compare(hndbook_file, hndbook_buffer_file)
                if not hndbook_changes:
                    sys.stdout.writelines("\033[34mИзменений в справочнике нет.\033[0m\n")
                else:
                    sys.stdout.writelines(hndbook_changes)
                    if input("Сохранить изменения (y/n)?") == 'y':
                        save_handbook(hndbook_file, hndbook)

            if os.path.exists(hndbook_buffer_file):
                os.remove(hndbook_buffer_file)
            print("Выход...")

            break

        else:
            sys.stdout.writelines("\033[31mНеправильный ввод. Пожалуйста, попробуйте снова.\033[0m\n")

if __name__ == "__main__":
    main()