from ..base import ShopLineResource

from ..collection import Collection, PaginatedCollection


class Customers(ShopLineResource):
    """customer"""

    # 弃单
    CUSTOMER_COUNT = "/v2/count"
    CUSTOMER = "/v2/customers"

    def __init__(self):
        super().__init__()

    @classmethod
    def customer_count(cls, prefix_options=None, **kwargs):
        url = cls.get_base_url(cls.CUSTOMER_COUNT)
        return cls.count(from_=url)

    @classmethod
    def customer(cls, id_=None):
        url = cls.get_base_url(cls.CUSTOMER if not id_ else "/v2/{}".format(id_), item="" if not id_ else None)
        return cls.find(from_=url)