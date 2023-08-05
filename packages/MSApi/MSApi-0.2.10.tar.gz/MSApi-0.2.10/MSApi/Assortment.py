from MSApi.MSLowApi import caching, MSLowApi
from MSApi.Template import Template
from MSApi.ObjectMS import ObjectMS

from MSApi.mixin.GenCustomTemplatesMixin import GenCustomTemplatesMixin
from MSApi.mixin.RequestLabelMixin import RequestLabelMixin
from MSApi.mixin.GenListMixin import GenerateListMixin


class Assortment(ObjectMS,
                 GenerateListMixin,
                 RequestLabelMixin,
                 GenCustomTemplatesMixin):
    _type_name = 'assortment'

