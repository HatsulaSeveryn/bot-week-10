from collections import UserDict


def input_error(message: str = ''):
    """
    Decorator function for handling input errors
    :param message: optional parameter to specify the input error
    """

    def inner(handler):
        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception as error_:
                print(error_, '\n', message)

        return wrapper

    return inner


class Field:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:

    def __init__(self, name: str, *args):
        self.name = Name(name)
        self.phones = []

    @input_error()
    def add_phone(self, phone: str, *args):
        print(f'{phone} has been added to the {self.name} record')
        return self.phones.append(Phone(phone))

    @input_error('Phone not found!')
    def delete_phone(self, phone: str, *args):
        print(f'{phone} has been deleted from the {self.name} record')
        return self.phones.remove(Phone(phone))

    @input_error('Incorrect phone number when trying to update!')
    def change_phone(self, old_phone: str, new_phone: str, *args):
        print(f'{old_phone} has been changed to {new_phone} in the {self.name} record')
        self.phones.remove(Phone(old_phone))
        return self.phones.append(Phone(new_phone))

    def __repr__(self):
        return f'{self.name}: {self.phones}'


class AddressBook(UserDict):

    @input_error()
    def add_record(self, record: Record, *args):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
            print(f'{record} has been added')
        else:
            print(f'User with name {record.name.value} already exist')

    @input_error('Update record: update {name} add/delete/change {phone} {new phone}(optional)')
    def update_record(self, record: Record, option: str, *phones):
        if record.name.value in self.data:
            match option:
                case 'add':
                    self.data[record.name.value].add_phone(phones[0])
                case 'delete':
                    self.data[record.name.value].delete_phone(phones[0])
                case 'change':
                    self.data[record.name.value].change_phone(phones[0], phones[1])
        else:
            print(f"Record with name {record.name} doesn't exist!")
            raise NameError

    @input_error('Unable to delete. Record not found!')
    def delete_record(self, record: Record, *args):
        print(f'Record {record} has been deleted!')
        del self.data[record.name.value]

    @input_error()
    def show_phones(self, name: str):
        print(self.data[name])

    @input_error()
    def show_all(self):
        print(self.__repr__())

    def __repr__(self):
        return self.data


def main():
    book = AddressBook()

    while True:
        user_command = (input('...').lower()).split()
        match user_command[0]:
            case 'add':
                book.add_record(Record(*user_command[1:]))
            case 'update':
                book.update_record(Record(user_command[1]), user_command[2], *user_command[3:])
            case 'delete':
                book.delete_record(Record(*user_command[1:]))
            case 'phone':
                book.show_phones(Record(*user_command[1:]))
            case 'show':
                book.show_all()
            case 'close' | 'exit' | 'quit':
                quit()
            case _:
                print('Wrong command!')


if __name__ == '__main__':
    main()
