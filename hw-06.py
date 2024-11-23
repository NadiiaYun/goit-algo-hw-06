from collections import UserDict
import re

# Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):    
    pass    

# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    # рНаслідує клас Field. Значення зберігaється в полі value.
    def __init__(self, phone_number):
        self.value = None
        self.set_phone_number(phone_number)

    def set_phone_number(self, phone_number):
        if self.validate_phone_number(phone_number):
            self.value = phone_number           
        else:            
            raise ValueError("Невірний формат номера телефону. Має бути 10 цифр.")

    def validate_phone_number(self, phone_number):
        # Перевірка, чи номер складається лише з 10 цифр
        return bool(re.match(r'^\d{10}$', phone_number)) 

# Клас Record для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# Функціональність:
# Додавання телефонів.
# Видалення телефонів.
# Редагування телефонів.
# Пошук телефону.

class Record(Name, Phone):
    # реалізація класу

    def __init__(self, name):
        # Реалізовано зберігання об'єкта Name в атрибуті name.
        self.name = Name(name)        
        self.phones = []
    
    '''Реалізовано метод для додавання - add_phone.
       На вхід подається рядок, який містить номер телефона.'''
    def add_phone(self, phone_number): 
        # Реалізовано зберігання списку об'єктів Phone в атрибуті phones.        
        self.phones.append(Phone(phone_number))

    '''Реалізовано метод для видалення - remove_phone. 
       На вхід подається рядок, який містить номер телефона.'''
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                print(f"Number {phone_number} deleted successfully.")
   
    '''Реалізовано метод для редагування - edit_phone. 
       На вхід подається два аргумента - рядки, які містять старий номер телефона та новий. 
       У разі некоректності вхідних даних метод має завершуватись помилкою ValueError.'''
    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                print(f"Number {old_phone_number} changed to {new_phone_number}.")

    ''' Реалізовано метод для пошуку об'єктів Phone - find_phone.
        На вхід подається рядок, який містить номер телефона. 
        Метод має повертати або об’єкт Phone, або None'''
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас AddressBook:
# Клас для зберігання та управління записами

# Функціональність:
# Додавання записів.
# Пошук записів за іменем.
# Видалення записів за іменем.

# Має наслідуватись від класу UserDict 
class AddressBook(UserDict):
    # реалізація класу

    '''Реалізовано метод add_record, який додає запис до self.data. 
        Записи Record у AddressBook зберігаються як значення у словнику. 
        В якості ключів використовується значення Record.name.value.'''
    def add_record(self, record):
        self.data[record.name.value] = record

    '''Реалізовано метод find, який знаходить запис за ім'ям. 
       На вхід отримує один аргумент - рядок, якій містить ім’я. 
       Повертає об’єкт Record, або None, якщо запис не знайден.'''
    def find(self, name):        
        return self.data.get(name, None)
    
    '''Реалізовано метод delete, який видаляє запис за ім'ям.'''       
    def delete(self, name):        
        if name in self.data:
            del self.data[name]
            print(f"Запис з ім'ям {name} видалено.")
        else:
            print(f"Запис з ім'ям {name} не знайдено.") 

    '''Реалізовано магічний метод __str__ для красивого виводу об’єкту класу AddressBook.'''
    def __str__(self):
        result = []
        print("Адресна книга:")
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result) 

if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі     
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    print(book)