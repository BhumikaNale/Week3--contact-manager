"""
Test file for Contact Management System
Run this file to verify basic functionality manually.
"""

from contacts_manager import (
    add_contact,
    search_contact,
    update_contact,
    delete_contact,
    load_contacts
)

def run_tests():
    print("Running Contact Management System Tests...\n")

    # Test Add Contact
    add_contact("Test User", "9999999999")
    print("✔ Add Contact Test Passed")

    # Test Search Contact
    search_contact("Test User")
    print("✔ Search Contact Test Passed")

    # Test Update Contact
    update_contact("Test User", "8888888888")
    print("✔ Update Contact Test Passed")

    # Test Delete Contact
    delete_contact("Test User")
    print("✔ Delete Contact Test Passed")

    # Final Data Check
    contacts = load_contacts()
    print("\nFinal Contacts Data:", contacts)

if __name__ == "__main__":
    run_tests()
