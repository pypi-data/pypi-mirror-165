from MSApi.MSLowApi import MSLowApi, caching
from MSApi.CustomTemplate import CustomTemplate


class GenCustomTemplatesMixin:

    @classmethod
    @caching
    def gen_customtemplates(cls, **kwargs):
        return MSLowApi.gen_objects('entity/{}/metadata/{}'.format(cls.get_typename(), CustomTemplate.get_typename())
                                    , CustomTemplate, **kwargs)
