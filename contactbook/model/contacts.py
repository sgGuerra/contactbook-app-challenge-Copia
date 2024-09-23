from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Contact:
    name: str
    phone: str
    email: str
    tags: list[str] = field(default_factory=list)
    creation_date: datetime = field(init=False, default_factory=datetime.now)

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def __str__(self) -> str:
        return (f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nTags: {", ".join(self.tags)}\n"
                f"Created on: {self.creation_date}")


@dataclass
class ContactBook:
    contacts: dict[str, Contact] = field(init=False, default_factory=dict)

    def add_contact(self, name: str, phone: str, email: str, tags: list[str]):
        new_contact = Contact(name, phone, email, tags)
        self.contacts[phone] = new_contact

    def delete_contact(self, phone: str):
        del self.contacts[phone]

    def list_contacts(self) -> list[Contact]:
        return [c for c in self.contacts.values()]

    def contacts_by_tag(self, tag: str) -> list[Contact]:
        return [c for c in self.contacts.values() if tag in c.tags]

    def search_by_criteria(self, name: str, phone: str, email: str) -> list[Contact]:
        pass