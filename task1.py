from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday already exists")

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                days_to_birthday = (birthday_this_year - today).days

                if 0 <= days_to_birthday <= days:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays


if __name__ == "__main__":
    book = AddressBook()

    # Creating a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.05.1990")

    # Adding John's record to the address book
    book.add_record(john_record)

    # Creating and adding a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("20.05.1985")
    book.add_record(jane_record)

    # Printing all records in the book
    for name, record in book.data.items():
        print(record)

    # Finding and editing John's phone
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")

    print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

    # Searching for a specific phone in John's record
    if john:
        found_phone = john.find_phone("5555555555")
        print(f"{john.name.value}: {found_phone}")  # Output: 5555555555

    # Deleting Jane's record
    book.delete("Jane")

    # Printing all records in the book after deletion
    for name, record in book.data.items():
        print(record)

    # Getting upcoming birthdays within the next 7 days
    upcoming_birthdays = book.get_upcoming_birthdays()
    for record in upcoming_birthdays:
        print(f"Upcoming birthday: {record.name.value} on {record.birthday.value.strftime('%d.%m.%Y')}")
