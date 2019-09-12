import json

from university.app.bll import BLL


class PerformanceByStudent:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, student_id):
        data = self.bll.performance_by_student_id(int(student_id))

        response.body = json.dumps(data)
        return response
