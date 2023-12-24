#!/usr/bin/python3
"""This module contains a console which will interact with
    the ContactBook class to perform several operations like:

    Display contact, add contact, delete contact, update contact
    and search contact.
    """
import cmd
from models.Contact_Book import ContactBook
from models import storage

class contactConsole(cmd.Cmd):
    """A console for the ContactBook class"""

    prompt = "Phone-->$ "

    def do_quit(self, line):
        """a method to quit the console"""
        return True

    def do_EOF(self, line):
        """a method to quit the console when end of file is
        passed
        """
        print()
        return True

    def emptyline(self):
        """do not nothing when the user press just enter"""
        pass

    def do_add(self, line):
        """add new contact
            Here is the the guide on how to use this method:
                add <phone_number> <name>"""
        details = line.split()
        if len(details) < 1:
            print("***phone-number is missing***")
            return
        if len(details) < 2:
            print("***name is missing***")
            return
        obj = ContactBook()
        obj.phone_number = details[0]
        obj.name = details[1]
        isExists = obj.save()
        if isExists:
            print("{} created!".format(obj.phone_number))

    def do_display(self, line):
        """display the list of all contacts
            To use this method just type <display>
        """
        for contact in storage.all().values():
            print(str(contact))

    def do_search(self, line):
        """search for a particular contact details through phone
            name.

            Here is the guide on how to use this method:
            search <name>
        """
        for contact in storage.all().values():
            if contact.name == line.split()[0] or contact.phone_number == line.split()[0]:
                print(str(contact))

    def do_update(self, line):
        """update any attribute in the contact details"""

if __name__ == "__main__":
    contactConsole().cmdloop()
