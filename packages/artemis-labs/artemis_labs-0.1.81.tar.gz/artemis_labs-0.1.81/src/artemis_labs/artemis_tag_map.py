'''
This module is used to set, unset, and query flag properties associated
with tags
'''

#pylint: disable=line-too-long

from typing import List

class TagMap():
    '''
    This class is a TagMap, which is used to set, unset, and query flag properties
    associated with tags
    '''
    def __init__(self):
        self.tags = {}

    def enable_tag(self, tag : str, prop : str) -> None:
        '''
        This sets the boolean status for the prop property of tag to true
        :param tag: Tag to manipulate
        :param prop: Property of tag to manipulate
        :return: None
        '''
        tag = tag.strip()
        if tag not in self.tags:
            self.tags[tag] = {}
        self.tags[tag][prop] = True

    def disable_tag(self, tag : str, prop : str) -> None:
        '''
        This sets the boolean status for the prop property of tag to false
        :param tag: Tag to manipulate
        :param prop: Property of tag to manipulate
        :return: None
        '''
        tag = tag.strip()
        if tag not in self.tags:
            self.tags[tag] = {}
        self.tags[tag][prop] = False


    def get_prop_value(self, tag_list : List[str], prop : str):
        '''
        Check the boolean status for the prop property associated with the tag_list.
        This chronologically works through the tags to return the prop value
        of the last tag in the list to have the prop. Otherwise it returns None
        if the prop is not stored for any of the tags
        :param tag_list: List of tags to check
        :param prop: Property of tag to check
        :return: Whether or not the prop property is set for the tag list
        '''
        val = None
        for tag in tag_list:
            tag = tag.strip()
            if tag in self.tags and prop in self.tags[tag]:
                val = self.tags[tag][prop]
        return val
