# ==================================================
# CONTACT MANAGEMENT SYSTEM
# Week 3 Project - Functions & Dictionaries
# ==================================================

import json
import re
import csv
from datetime import datetime
import os

DATA_FILE = "contacts_data.json"
BACKUP_FILE = "contacts_backup.json"

# ---------------- VALIDATION FUNCTIONS ----------------

def validate_phone(phone):
    """Validate and clean phone number"""
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None


def validate_email(email):
    """Validate email format"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# ---------------- FILE OPERATIONS ----------------

def load_contacts():
    """Load contacts from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            print("✅ Contacts loaded successfully.")
            return json.load(file)
    print("✅ No existing contacts file found. Starting fresh.")
    return {}


def save_contacts(contacts):
    """Save contacts to file"""
    with open(DATA_FILE, "w") as file:
        json.dump(contacts, file, indent=4)
    with open(BACKUP_FILE, "w") as backup:
        json.dump(contacts, backup, indent=4)
    print("✅ Contacts saved successfully.")


# ---------------- CRUD OPERATIONS ----------------

def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")

    name = input("Enter contact name: ").strip().title()
    if not name:
        print("❌ Name cannot be empty.")
        return

    if name in contacts:
        print("❌ Contact already exists.")
        return

    phone = input("Enter phone number: ").strip()
    valid, phone = validate_phone(phone)
    if not valid:
        print("❌ Invalid phone number.")
        return

    email = input("Enter email (optional): ").strip()
    if not validate_email(email):
        print("❌ Invalid email format.")
        return

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip().title() or "Other"

    contacts[name] = {
        "phone": phone,
        "email": email or None,
        "address": address or None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✅ Contact '{name}' added successfully!")


def search_contacts(contacts):
    term = input("Enter name or phone to search: ").lower()
    results = {}

    for name, info in contacts.items():
        if term in name.lower() or term in info["phone"]:
            results[name] = info

    if not results:
        print("❌ No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 50)
    for name, info in results.items():
        display_contact(name, info)


def update_contact(contacts):
    name = input("Enter contact name to update: ").strip().title()
    if name not in contacts:
        print("❌ Contact not found.")
        return

    print("Leave blank to keep existing value.")

    phone = input("New phone: ").strip()
    if phone:
        valid, phone = validate_phone(phone)
        if valid:
            contacts[name]["phone"] = phone

    email = input("New email: ").strip()
    if email and validate_email(email):
        contacts[name]["email"] = email

    address = input("New address: ").strip()
    if address:
        contacts[name]["address"] = address

    group = input("New group: ").strip()
    if group:
        contacts[name]["group"] = group

    contacts[name]["updated_at"] = datetime.now().isoformat()
    print("✅ Contact updated successfully.")


def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip().title()
    if name not in contacts:
        print("❌ Contact not found.")
        return

    confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        print("✅ Contact deleted successfully.")


def display_all_contacts(contacts):
    if not contacts:
        print("❌ No contacts available.")
        return

    print(f"\n--- ALL CONTACTS ({len(contacts)}) ---")
    print("=" * 60)
    for name, info in contacts.items():
        display_contact(name, info)


def display_contact(name, info):
    print(f"👤 {name}")
    print(f"   📞 {info['phone']}")
    if info["email"]:
        print(f"   📧 {info['email']}")
    if info["address"]:
        print(f"   📍 {info['address']}")
    print(f"   👥 {info['group']}")
    print("-" * 40)


# ---------------- ADVANCED FEATURES ----------------

def export_to_csv(contacts):
    with open("contacts_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["address"], info["group"]])
    print("✅ Contacts exported to CSV.")


def show_statistics(contacts):
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {len(contacts)}")

    groups = {}
    for info in contacts.values():
        groups[info["group"]] = groups.get(info["group"], 0) + 1

    print("Contacts by Group:")
    for g, count in groups.items():
        print(f"  {g}: {count}")


# ---------------- MENU SYSTEM ----------------

def main_menu():
    contacts = load_contacts()

    while True:
        print("\n" + "=" * 50)
        print("CONTACT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contacts(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            display_all_contacts(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            show_statistics(contacts)
        elif choice == "8":
            save_contacts(contacts)
            print("👋 Thank you for using Contact Management System!")
            break
        else:
            print("❌ Invalid choice. Try again.")


# ---------------- PROGRAM START ----------------

if __name__ == "__main__":
    main_menu()
