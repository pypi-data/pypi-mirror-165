from ..base import ShopLineResource


class Merchants(ShopLineResource):
    """get shop info"""

    SHOP = "/shop"

    def __init__(self):
        super().__init__()

    @classmethod
    def shop(cls):
        url = cls.get_base_url(cls.SHOP)
        return cls.find(from_=url)