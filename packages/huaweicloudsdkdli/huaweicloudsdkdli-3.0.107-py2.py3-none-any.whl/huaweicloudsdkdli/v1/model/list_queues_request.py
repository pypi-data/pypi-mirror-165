# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListQueuesRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'with_priv': 'bool',
        'with_charge_info': 'bool',
        'queue_type': 'str',
        'tags': 'str',
        'page_size': 'int',
        'current_page': 'int',
        'order': 'str'
    }

    attribute_map = {
        'with_priv': 'with-priv',
        'with_charge_info': 'with-charge-info',
        'queue_type': 'queue_type',
        'tags': 'tags',
        'page_size': 'page-size',
        'current_page': 'current-page',
        'order': 'order'
    }

    def __init__(self, with_priv=None, with_charge_info=None, queue_type=None, tags=None, page_size=None, current_page=None, order=None):
        """ListQueuesRequest

        The model defined in huaweicloud sdk

        :param with_priv: 是否返回权限信息。
        :type with_priv: bool
        :param with_charge_info: 是否返回收费信息
        :type with_charge_info: bool
        :param queue_type: 队列的类型,。有如下三种类型： sql general all 如果不指定，默认为sql。
        :type queue_type: str
        :param tags: 查询根据标签进行过滤
        :type tags: str
        :param page_size: 每页显示的最大结果行数，默认值Integer.MAX_VALUE（也即不分页）
        :type page_size: int
        :param current_page: 当前页码，默认为第一页。
        :type current_page: int
        :param order: 指定队列排序方式，默认为queue_name_asc（队列名称升序），支持queue_name_asc（队列名称升序）、queue_name_desc（队列名称降序）、cu_asc（CU数升序）、cu_desc（CU数降序）四种排序方式。
        :type order: str
        """
        
        

        self._with_priv = None
        self._with_charge_info = None
        self._queue_type = None
        self._tags = None
        self._page_size = None
        self._current_page = None
        self._order = None
        self.discriminator = None

        if with_priv is not None:
            self.with_priv = with_priv
        if with_charge_info is not None:
            self.with_charge_info = with_charge_info
        if queue_type is not None:
            self.queue_type = queue_type
        if tags is not None:
            self.tags = tags
        if page_size is not None:
            self.page_size = page_size
        if current_page is not None:
            self.current_page = current_page
        if order is not None:
            self.order = order

    @property
    def with_priv(self):
        """Gets the with_priv of this ListQueuesRequest.

        是否返回权限信息。

        :return: The with_priv of this ListQueuesRequest.
        :rtype: bool
        """
        return self._with_priv

    @with_priv.setter
    def with_priv(self, with_priv):
        """Sets the with_priv of this ListQueuesRequest.

        是否返回权限信息。

        :param with_priv: The with_priv of this ListQueuesRequest.
        :type with_priv: bool
        """
        self._with_priv = with_priv

    @property
    def with_charge_info(self):
        """Gets the with_charge_info of this ListQueuesRequest.

        是否返回收费信息

        :return: The with_charge_info of this ListQueuesRequest.
        :rtype: bool
        """
        return self._with_charge_info

    @with_charge_info.setter
    def with_charge_info(self, with_charge_info):
        """Sets the with_charge_info of this ListQueuesRequest.

        是否返回收费信息

        :param with_charge_info: The with_charge_info of this ListQueuesRequest.
        :type with_charge_info: bool
        """
        self._with_charge_info = with_charge_info

    @property
    def queue_type(self):
        """Gets the queue_type of this ListQueuesRequest.

        队列的类型,。有如下三种类型： sql general all 如果不指定，默认为sql。

        :return: The queue_type of this ListQueuesRequest.
        :rtype: str
        """
        return self._queue_type

    @queue_type.setter
    def queue_type(self, queue_type):
        """Sets the queue_type of this ListQueuesRequest.

        队列的类型,。有如下三种类型： sql general all 如果不指定，默认为sql。

        :param queue_type: The queue_type of this ListQueuesRequest.
        :type queue_type: str
        """
        self._queue_type = queue_type

    @property
    def tags(self):
        """Gets the tags of this ListQueuesRequest.

        查询根据标签进行过滤

        :return: The tags of this ListQueuesRequest.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ListQueuesRequest.

        查询根据标签进行过滤

        :param tags: The tags of this ListQueuesRequest.
        :type tags: str
        """
        self._tags = tags

    @property
    def page_size(self):
        """Gets the page_size of this ListQueuesRequest.

        每页显示的最大结果行数，默认值Integer.MAX_VALUE（也即不分页）

        :return: The page_size of this ListQueuesRequest.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this ListQueuesRequest.

        每页显示的最大结果行数，默认值Integer.MAX_VALUE（也即不分页）

        :param page_size: The page_size of this ListQueuesRequest.
        :type page_size: int
        """
        self._page_size = page_size

    @property
    def current_page(self):
        """Gets the current_page of this ListQueuesRequest.

        当前页码，默认为第一页。

        :return: The current_page of this ListQueuesRequest.
        :rtype: int
        """
        return self._current_page

    @current_page.setter
    def current_page(self, current_page):
        """Sets the current_page of this ListQueuesRequest.

        当前页码，默认为第一页。

        :param current_page: The current_page of this ListQueuesRequest.
        :type current_page: int
        """
        self._current_page = current_page

    @property
    def order(self):
        """Gets the order of this ListQueuesRequest.

        指定队列排序方式，默认为queue_name_asc（队列名称升序），支持queue_name_asc（队列名称升序）、queue_name_desc（队列名称降序）、cu_asc（CU数升序）、cu_desc（CU数降序）四种排序方式。

        :return: The order of this ListQueuesRequest.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this ListQueuesRequest.

        指定队列排序方式，默认为queue_name_asc（队列名称升序），支持queue_name_asc（队列名称升序）、queue_name_desc（队列名称降序）、cu_asc（CU数升序）、cu_desc（CU数降序）四种排序方式。

        :param order: The order of this ListQueuesRequest.
        :type order: str
        """
        self._order = order

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
        if not isinstance(other, ListQueuesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
