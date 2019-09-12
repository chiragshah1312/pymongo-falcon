import json

from university.app.bll import BLL


class ClassList:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response):
        data = self.bll.list_of_classes()

        response.body = json.dumps(data)
        return response
