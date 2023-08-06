from ..base import ShopLineResource


class Sales(ShopLineResource):

    DISCOUNT_CODES_COUNT = "/discount_codes/count"

    def __init__(self):
        super().__init__()

    @classmethod
    def discount_codes_count(cls):
        url = cls.get_base_url(cls.DISCOUNT_CODES_COUNT)
        return cls.count(from_=url)