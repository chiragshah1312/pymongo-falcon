import json

from university.app.bll import BLL


class GradeSheetClass:
    def __init__(self):
        self.bll = BLL()

    def on_get(self, request, response, class_id):
        data = self.bll.grade_sheet(int(class_id))

        response.body = json.dumps(data)
        return response
