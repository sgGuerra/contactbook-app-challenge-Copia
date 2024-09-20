from rich.console import Console as RichConsole
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

from contactbook.model.contacts import ContactBook, Contact


class Console:

    def __init__(self, contact_book: ContactBook):
        self.contact_book = contact_book
        self.console = RichConsole()
        self.populate_initial_contacts()

    def show_menu(self):
        menu_panel = Panel(
            """[bold cyan]Menu:[/bold cyan]
1. Add new contact
2. List all contacts
3. Search contact
4. Delete contact
5. Search by tag
0. Exit""",
            title="Contact Book",
            border_style="green"
        )
        self.console.print(menu_panel)
        return Prompt.ask("Choose an option", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")

    def run(self):
        while True:
            option = self.show_menu()
            if option == "1":
                self.add_contact()
            elif option == "2":
                self.list_contacts()
            elif option == "3":
                self.search_contact_by_criteria()
            elif option == "4":
                self.delete_contact()
            elif option == "5":
                self.search_by_tag()
            elif option == "0":
                self.console.print(Panel("[bold red]Goodbye![/bold red]", border_style="red"))
                break

    def add_contact(self):
        name = Prompt.ask("Enter name")
        phone = Prompt.ask("Enter phone")
        email = Prompt.ask("Enter email")
        tags = Prompt.ask("Enter tags (comma-separated)").split(",")
        self.contact_book.add_contact(name, phone, email, tags)
        self.console.print(Panel(f"[green]Contact '{name}' added successfully![/green]", border_style="green"))

    def list_contacts(self):
        contacts = self.contact_book.list_contacts()
        if contacts:
            table = Table(title="Contacts", title_style="bold magenta", box=None, border_style="blue")
            table.add_column("Name", style="cyan")
            table.add_column("Phone", style="yellow")
            table.add_column("Email", style="green")
            table.add_column("Tags", style="magenta")
            table.add_column("Created", style="white")

            for contact in contacts:
                table.add_row(contact.name, contact.phone, contact.email, ", ".join(contact.tags), str(contact.creation_date))

            self.console.print(table)
        else:
            self.console.print(Panel("[bold red]No contacts available.[/bold red]", border_style="red"))

    def search_contact_by_criteria(self):
        name = Prompt.ask("Enter name (leave empty to skip)")
        phone = Prompt.ask("Enter phone (leave empty to skip)")
        email = Prompt.ask("Enter email (leave empty to skip)")
        contacts = self.contact_book.search_by_criteria(name, phone, email)
        if contacts:
            self.display_contacts_table(contacts)
        else:
            self.console.print(Panel("[bold red]No contacts found with the given criteria.[/bold red]", border_style="red"))

    def delete_contact(self):
        phone = Prompt.ask("Enter phone number of the contact to delete")
        self.contact_book.delete_contact(phone)
        self.console.print(Panel(f"[bold red]Contact with phone '{phone}' deleted.[/bold red]", border_style="red"))

    def search_by_tag(self):
        tag = Prompt.ask("Enter tag to search by")
        results = self.contact_book.contacts_by_tag(tag)
        if results:
            self.console.print(f"[bold green]{len(results)}[/bold green] [bold cyan]contact(s) found with tag:[/bold cyan] '{tag}'")
            self.display_contacts_table(results)
        else:
            self.console.print(Panel(f"[bold red]No contacts found with tag '{tag}'.[/bold red]", border_style="red"))

    def display_contacts_table(self, contacts: list[Contact]):
        table = Table(title="Contacts", title_style="bold magenta", box=None, border_style="blue")
        table.add_column("Name", style="cyan")
        table.add_column("Phone", style="yellow")
        table.add_column("Email", style="green")
        table.add_column("Tags", style="magenta")
        table.add_column("Created", style="white")

        for contact in contacts:
            table.add_row(contact.name, contact.phone, contact.email, ", ".join(contact.tags), str(contact.creation_date))

        self.console.print(table)

    def populate_initial_contacts(self):
        """Populate the contact book with 10 unique contacts, but with shared data for common searches."""
        contacts_data = [
            ("John Doe", "12345", "john@work.com", ["work"]),
            ("Jane Doe", "67890", "jane@personal.com", ["friend"]),
            ("John Smith", "12346", "john.smith@work.com", ["work"]),
            ("Michael Smith", "67891", "michael.smith@work.com", ["coworker"]),
            ("Alice Johnson", "12347", "alice@company.com", ["work"]),
            ("Bob Brown", "67892", "bob@company.com", ["coworker"]),
            ("Carol White", "12348", "carol@work.com", ["work"]),
            ("David Black", "67893", "david@personal.com", ["friend"]),
            ("Emily Clark", "12349", "emily@work.com", ["work"]),
            ("Frank Miller", "67894", "frank@company.com", ["coworker"])
        ]

        for name, phone, email, tags in contacts_data:
            self.contact_book.add_contact(name, phone, email, tags)

        self.console.print(
            Panel("[green]10 contacts have been pre-loaded into the contact book.[/green]",
                  border_style="green"))

