from ..base import ShopLineResource

from ..collection import Collection, PaginatedCollection


class Orders(ShopLineResource):
    # 弃单
    ABANDONED_ORDERS = "/abandoned_orders"

    def __init__(self):
        super().__init__()

    @classmethod
    def abandoned_orders(cls, id_=None, prefix_options=None, **kwargs):
        url = cls.get_base_url(cls.ABANDONED_ORDERS, page=cls.page_size)
        return cls.find(from_=url, **kwargs)

    @classmethod
    def orders(cls, prefix_options=None, **kwargs):
        url = cls.get_base_url("", page=cls.page_size)
        return cls.find(from_=url, **kwargs)

