from contactbook.model.contacts import ContactBook
from contactbook.view.ui_console import Console


def main():
    contactbook = ContactBook()
    console = Console(contactbook)
    console.run()


if __name__ == "__main__":
    main()
