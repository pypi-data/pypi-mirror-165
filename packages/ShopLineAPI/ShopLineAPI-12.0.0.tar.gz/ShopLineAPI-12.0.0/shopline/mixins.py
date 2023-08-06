import shopline.resources


class CountMixins:

    @classmethod
    def count(cls, form_=None, **kwargs):
        if not form_:
            url = cls.get_base_url("/count")
        else:
            url = form_
        response = cls.connect.get(url, cls.get_headers())
        objs = cls.format.decode(response.body)
        return objs
