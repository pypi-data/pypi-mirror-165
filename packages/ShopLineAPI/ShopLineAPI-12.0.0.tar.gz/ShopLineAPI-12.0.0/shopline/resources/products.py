from ..base import ShopLineResource

from ..collection import Collection, PaginatedCollection


class Products(ShopLineResource):
    DETAIL = "/products"

    def __init__(self):
        super().__init__()

    @classmethod
    def products(cls, _id=None, prefix_options=None, **kwargs):
        url = cls.get_base_url(cls.DETAIL, page=cls.page_size)
        return cls.find(from_=url, **kwargs)

