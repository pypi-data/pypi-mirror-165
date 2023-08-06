from ..base import ShopLineResource

from ..collection import Collection, PaginatedCollection


class Customers(ShopLineResource):
    # 弃单
    CUSTOMER_COUNT = "/v2/count"

    def __init__(self):
        super().__init__()

    @classmethod
    def customer_count(cls, prefix_options=None, **kwargs):
        url = cls.get_base_url(cls.CUSTOMER_COUNT)
        return cls.count(form_=url)
