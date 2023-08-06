import shopline.resources


class CountMixins:

    @classmethod
    def count(cls, from_=None, **kwargs):
        if not from_:
            url = cls.get_base_url("/count")
        else:
            url = from_
        response = cls.connect.get(url, cls.get_headers())
        objs = cls.format.decode(response.body)
        return objs
