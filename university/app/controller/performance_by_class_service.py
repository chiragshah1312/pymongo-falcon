import json

from university.app.bll import BLL


class PerformanceByClass:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, class_id):
        data = self.bll.performance_by_class_id(int(class_id))

        response.body = json.dumps(data)
        return response
