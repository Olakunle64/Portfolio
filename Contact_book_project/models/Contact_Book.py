#!/usr/bin/python3
"""This module contains a class named <ContactBook> which is use
    to store individual contact details.
    """
import datetime
import models

class ContactBook():
    """This class contains a both instance attribute and
        methods

        instance attribute:
            name, phone number, email and address.
        Note: name must be unique for all contacts

        instance method:
            display_contacts - display all contacts
            search_contact - search for a contact either with
                                name or phone number
            update_contact - update the contact details
            delete_contact - delete a contact.
    """
    def __init__(self, *args, **kwargs):
        """initializing the instance variables"""
        if kwargs:
            self.__dict__ = kwargs.copy()
            self.__dict__["created_at"] = datetime.datetime.fromisoformat(kwargs["created_at"])
            self.__dict__["updated_at"] = datetime.datetime.fromisoformat(kwargs["updated_at"])
        else:
            self.name = ""
            self.phone_number = ""
            self.email = ""
            self.address = ""
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """string implementation of an instance"""
        return ("[{}]----{}".format(self.phone_number, self.__dict__))

    def to_dict(self):
        """return the dictionary attribute of an instance"""
        obj_dict = self.__dict__.copy()
        obj_dict["created_at"] = datetime.datetime.isoformat(self.created_at)
        obj_dict["updated_at"] = datetime.datetime.isoformat(obj_dict["updated_at"])
        return obj_dict

    def save(self):
        """save an instance to the json file"""
        self.updated_at = datetime.datetime.now()
        key = self.phone_number
        if key:
            models.storage._FileStorage__contacts[key] = self
            models.storage.save()
