from datetime import datetime
import pytest
import inspect
import contactbook.model.contacts

# Verifying the existence of the Contact and ContactBook classes
module_members = [item[0] for item in inspect.getmembers(contactbook.model.contacts)]
contact_defined = "Contact" in module_members
contactbook_defined = "ContactBook" in module_members


if contact_defined:
    from contactbook.model.contacts import Contact

if contactbook_defined:
    from contactbook.model.contacts import ContactBook


@pytest.fixture()
def contact():
    return Contact(name="John Doe", phone="12345", email="john@work.com", tags=["work"])


@pytest.fixture()
def empty_contact_book():
    return ContactBook()


@pytest.fixture()
def contact_book_with_contacts():
    book = ContactBook()
    book.add_contact("John Doe", "12345", "john@work.com", ["work"])
    book.add_contact("Jane Doe", "67890", "jane@personal.com", ["friend"])
    book.add_contact("Alice Johnson", "12346", "alice@company.com", ["work"])
    return book


class TestContact:
    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    def test_contact_class_is_marked_as_dataclass(self, contact):
        """Test if the Contact class is marked with @dataclass."""
        assert hasattr(contact, "__dataclass_params__")

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("name", str), ("phone", str), ("email", str), ("tags", list), ("creation_date", datetime)]
    )
    def test_contact_class_has_correct_attributes(self, contact, attribute_name, attribute_type):
        """Test if the Contact class has all expected attributes and types."""
        assert hasattr(contact, attribute_name)
        assert isinstance(getattr(contact, attribute_name), attribute_type)

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    @pytest.mark.parametrize(
        "method_name, signature",
        [("add_tag", "(tag: str)"), ("__str__", "() -> str")]
    )
    def test_contact_class_has_required_methods_with_correct_signatures(self, contact, method_name, signature):
        """Test if the Contact class has the expected methods with correct signatures."""
        assert hasattr(contact, method_name)
        method = getattr(contact, method_name)
        assert callable(method)
        assert str(inspect.signature(method)) == signature

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    def test_contact_initialization_with_default_values(self):
        """Test the initialization of a Contact object with default values."""
        contact = Contact(name="Jane Doe", phone="67890", email="jane@personal.com")
        assert contact.name == "Jane Doe"
        assert contact.phone == "67890"
        assert contact.email == "jane@personal.com"
        assert contact.tags == []
        assert contact.creation_date

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    def test_add_tag_method_adds_new_tag_to_contact(self, contact):
        """Test if the add_tag method adds a new tag to a Contact."""
        contact.add_tag("new_tag")
        assert "new_tag" in contact.tags

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    def test_add_tag_method_does_not_add_duplicate_tags(self, contact):
        """Test if the add_tag method prevents adding duplicate tags to a Contact."""
        contact.add_tag("new_tag")
        contact.add_tag("new_tag")
        assert contact.tags.count("new_tag") == 1

    @pytest.mark.skipif(not contact_defined, reason="Contact class is not defined")
    def test_str_method_returns_correct_string_representation_of_contact(self, contact):
        """Test if the __str__ method returns the correct string representation of a Contact."""
        assert str(contact) == (
            f"Name: John Doe\nPhone: 12345\nEmail: john@work.com\nTags: work\nCreated on: {contact.creation_date}"
        )


class TestContactBook:
    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_contactbook_class_is_marked_as_dataclass(self, empty_contact_book):
        """Test if the ContactBook class is marked with @dataclass."""
        assert hasattr(empty_contact_book, "__dataclass_params__")

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_contactbook_has_contacts_dict_attribute(self, empty_contact_book):
        """Test if the ContactBook class has a 'contacts' attribute of type dict."""
        assert hasattr(empty_contact_book, "contacts")
        assert isinstance(empty_contact_book.contacts, dict)

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    @pytest.mark.parametrize(
        "method_name, signature",
        [("add_contact", "(name: str, phone: str, email: str, tags: list[str])"),
         ("delete_contact", "(phone: str)"),
         ("list_contacts", "() -> list[contactbook.model.contacts.Contact]"),
         ("contacts_by_tag", "(tag: str) -> list[contactbook.model.contacts.Contact]"),
         ("search_by_criteria", "(name: str = '', phone: str = '', email: str = '') -> list[contactbook.model.contacts.Contact]")]
    )
    def test_contactbook_has_required_methods_with_correct_signatures(self, empty_contact_book, method_name, signature):
        """Test if the ContactBook class has the required methods with correct signatures."""
        assert hasattr(empty_contact_book, method_name)
        method = getattr(empty_contact_book, method_name)
        assert callable(method)
        assert str(inspect.signature(method)) == signature

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_add_contact_method_adds_new_contact_to_contactbook(self, empty_contact_book):
        """Test if the add_contact method adds a new contact to the ContactBook."""
        empty_contact_book.add_contact("John Doe", "12345", "john@work.com", ["work"])
        assert len(empty_contact_book.contacts) == 1
        assert "12345" in empty_contact_book.contacts
        assert empty_contact_book.contacts["12345"].name == "John Doe"

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_delete_contact_method_removes_contact_from_contactbook(self, contact_book_with_contacts):
        """Test if the delete_contact method removes a contact from the ContactBook."""
        contact_book_with_contacts.delete_contact("12345")
        assert len(contact_book_with_contacts.contacts) == 2
        assert "12345" not in contact_book_with_contacts.contacts

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_list_contacts_method_returns_all_contacts(self, contact_book_with_contacts):
        """Test if the list_contacts method returns all contacts in the ContactBook."""
        contacts = contact_book_with_contacts.list_contacts()
        assert len(contacts) == 3
        assert contacts[0].name == "John Doe"

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    def test_contacts_by_tag_method_returns_contacts_with_specific_tag(self, contact_book_with_contacts):
        """Test if the contacts_by_tag method returns contacts with a specific tag."""
        contacts = contact_book_with_contacts.contacts_by_tag("work")
        assert len(contacts) == 2
        assert all("work" in contact.tags for contact in contacts)

    @pytest.mark.skipif(not contactbook_defined, reason="ContactBook class is not defined")
    @pytest.mark.parametrize(
        "criteria, expected_length",
        [({"name": "John"}, 2),
         ({"phone": "12345"}, 1),
         ({"email": "john@work.com"}, 1),
         ({"name": "Doe"}, 2),
         ({"name": "", "phone": "123"}, 2),
         ({"name": "Jane", "email": "jane@personal.com"}, 1)]
    )
    def test_search_by_criteria_method_returns_correct_contacts(self, contact_book_with_contacts, criteria, expected_length):
        """Test if the search_by_criteria method returns contacts matching the given criteria."""
        contacts = contact_book_with_contacts.search_by_criteria(**criteria)
        assert len(contacts) == expected_length
