import json

from university.app.bll import BLL

class StudentsByClass:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, class_id):

        data = self.bll.list_of_students_by_class(int(class_id))
        response.body = json.dumps(data)
        return response
