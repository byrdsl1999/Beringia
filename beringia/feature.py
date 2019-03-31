# -*- coding: utf-8 -*-
"""Example Google style docstrings.
"""


class Feature(object):
    """This is a generic class that defines features of locale."""

    def __init__(self, location=None):
        self.location = location

    def has_location(self):
        if self.location == None:
            return False
        else:
            return True

    def delete_self(self):
        del self