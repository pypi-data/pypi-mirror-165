from ..base import ShopLineResource

from ..collection import Collection, PaginatedCollection


class Products(ShopLineResource):
    """products """
    DETAIL = "/products"

    def __init__(self):
        super().__init__()

    @classmethod
    def products(cls, _id=None, prefix_options=None, **kwargs):
        url = cls.get_base_url(cls.DETAIL if not _id else "/{}".format(_id), page=cls.page_size if not _id else None)
        return cls.find(from_=url, **kwargs)

