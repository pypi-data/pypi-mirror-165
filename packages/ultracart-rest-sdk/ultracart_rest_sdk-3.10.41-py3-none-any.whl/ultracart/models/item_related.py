# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ItemRelated(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'no_system_calculated_related_items': 'bool',
        'not_relatable': 'bool',
        'related_items': 'list[ItemRelatedItem]'
    }

    attribute_map = {
        'no_system_calculated_related_items': 'no_system_calculated_related_items',
        'not_relatable': 'not_relatable',
        'related_items': 'related_items'
    }

    def __init__(self, no_system_calculated_related_items=None, not_relatable=None, related_items=None):  # noqa: E501
        """ItemRelated - a model defined in Swagger"""  # noqa: E501

        self._no_system_calculated_related_items = None
        self._not_relatable = None
        self._related_items = None
        self.discriminator = None

        if no_system_calculated_related_items is not None:
            self.no_system_calculated_related_items = no_system_calculated_related_items
        if not_relatable is not None:
            self.not_relatable = not_relatable
        if related_items is not None:
            self.related_items = related_items

    @property
    def no_system_calculated_related_items(self):
        """Gets the no_system_calculated_related_items of this ItemRelated.  # noqa: E501

        True to suppress system calculated relationships  # noqa: E501

        :return: The no_system_calculated_related_items of this ItemRelated.  # noqa: E501
        :rtype: bool
        """
        return self._no_system_calculated_related_items

    @no_system_calculated_related_items.setter
    def no_system_calculated_related_items(self, no_system_calculated_related_items):
        """Sets the no_system_calculated_related_items of this ItemRelated.

        True to suppress system calculated relationships  # noqa: E501

        :param no_system_calculated_related_items: The no_system_calculated_related_items of this ItemRelated.  # noqa: E501
        :type: bool
        """

        self._no_system_calculated_related_items = no_system_calculated_related_items

    @property
    def not_relatable(self):
        """Gets the not_relatable of this ItemRelated.  # noqa: E501

        Not relatable  # noqa: E501

        :return: The not_relatable of this ItemRelated.  # noqa: E501
        :rtype: bool
        """
        return self._not_relatable

    @not_relatable.setter
    def not_relatable(self, not_relatable):
        """Sets the not_relatable of this ItemRelated.

        Not relatable  # noqa: E501

        :param not_relatable: The not_relatable of this ItemRelated.  # noqa: E501
        :type: bool
        """

        self._not_relatable = not_relatable

    @property
    def related_items(self):
        """Gets the related_items of this ItemRelated.  # noqa: E501

        Related items  # noqa: E501

        :return: The related_items of this ItemRelated.  # noqa: E501
        :rtype: list[ItemRelatedItem]
        """
        return self._related_items

    @related_items.setter
    def related_items(self, related_items):
        """Sets the related_items of this ItemRelated.

        Related items  # noqa: E501

        :param related_items: The related_items of this ItemRelated.  # noqa: E501
        :type: list[ItemRelatedItem]
        """

        self._related_items = related_items

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ItemRelated, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ItemRelated):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
