import json

from university.app.bll import BLL


class ClassByStudent:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, student_id):

        data = self.bll.list_of_class_for_student(int(student_id))
        response.body = json.dumps(data)
        return response
