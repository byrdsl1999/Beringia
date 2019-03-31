# -*- coding: utf-8 -*-
"""feature.py

.. _Docstring example here:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""


class Feature(object):
    def __init__(self, location=None):
        """This is a generic class that defines features of locale.

        Args:
            location (beringia.locale.Locale):

        """
        self.location = location

    def has_location(self):
        """has_location docs

        Returns:
            bool:

        """
        if self.location is None:
            return False
        else:
            return True

    def delete_self(self):
        """delete_self docs

        """
        del self
