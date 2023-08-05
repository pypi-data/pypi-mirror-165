
from MSApi.Template import Template


class CustomTemplate(Template):
    _type_name = 'customtemplate'

    def __init__(self, json):
        super().__init__(json)
