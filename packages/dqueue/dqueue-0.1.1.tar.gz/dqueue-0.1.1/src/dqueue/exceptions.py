# -*- coding: utf-8 -*-
class ItemExistError(Exception):
    """数据已存在"""

    def __init__(self, item_id):
        super(ItemExistError, self).__init__(u'item %s was exist' % item_id)


class ItemKeyError(KeyError):
    def __init__(self, item_id):
        super(ItemKeyError, self).__init__(u'item %s not found' % item_id)

