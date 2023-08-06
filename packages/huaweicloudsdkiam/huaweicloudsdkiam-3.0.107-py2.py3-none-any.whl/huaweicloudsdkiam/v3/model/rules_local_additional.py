# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RulesLocalAdditional:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str'
    }

    attribute_map = {
        'name': 'name'
    }

    def __init__(self, name=None):
        """RulesLocalAdditional

        The model defined in huaweicloud sdk

        :param name: user：联邦用户在本系统中的用户名称。 &#x60;&#x60;&#x60; \&quot;user\&quot;:{\&quot;name\&quot;:\&quot;{0}\&quot;} &#x60;&#x60;&#x60;  group：联邦用户在本系统中所属用户组。 &#x60;&#x60;&#x60; \&quot;group\&quot;:{\&quot;name\&quot;:\&quot;0cd5e9\&quot;} &#x60;&#x60;&#x60;
        :type name: str
        """
        
        

        self._name = None
        self.discriminator = None

        if name is not None:
            self.name = name

    @property
    def name(self):
        """Gets the name of this RulesLocalAdditional.

        user：联邦用户在本系统中的用户名称。 ``` \"user\":{\"name\":\"{0}\"} ```  group：联邦用户在本系统中所属用户组。 ``` \"group\":{\"name\":\"0cd5e9\"} ```

        :return: The name of this RulesLocalAdditional.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RulesLocalAdditional.

        user：联邦用户在本系统中的用户名称。 ``` \"user\":{\"name\":\"{0}\"} ```  group：联邦用户在本系统中所属用户组。 ``` \"group\":{\"name\":\"0cd5e9\"} ```

        :param name: The name of this RulesLocalAdditional.
        :type name: str
        """
        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RulesLocalAdditional):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
