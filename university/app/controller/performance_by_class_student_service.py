import json

from university.app.bll import BLL


class PerformanceByClassStudent:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, class_id, student_id):
        data = self.bll.performance_by_student_id_class_id(int(student_id), int(class_id))

        response.body = json.dumps(data)
        return response