from math import ceil

from university.app.dal import DAL


class BLL:
    def __init__(self):
        self.dal = DAL()

    def list_of_students(self):
        data = self.dal.get_all_students()
        output = []
        for student in data:
            output.append({
                'student_id': student['_id'],
                'student_name': student['name']
            })
        return output

    def list_of_class_for_student(self, student_id):
        classes = [{'class_id': x['class_id']} for x in self.dal.get_class_by_student_id(student_id)]
        student_details = self.dal.get_student_by_student_id([student_id])[0]
        data = {
            'classes': classes,
            'student_id': student_details['_id'],
            'student_name': student_details['name']
        }
        return data

    def list_of_students_by_class(self, class_id):
        student_ids = list(set([student['student_id'] for student in self.dal.get_student_by_class_id(class_id)]))
        students = [{
                'student_id': student['_id'],
                'student_name': student['name']
            } for student in self.dal.get_student_by_student_id(student_ids)]

        return {"class_id": class_id,
                "students": students}

    def list_of_classes(self):
        classes = self.dal.get_classes()
        return [{'class_id': id} for id in classes]

    def performance_by_student_id(self, student_id):
        student_details = self.dal.get_student_by_student_id([student_id])[0]
        classes = self.dal.get_performance_by_student_id(student_id)
        return {
            "student_id": student_id,
            "student_name": student_details['name'],
            "classes": classes
        }

    def performance_by_class_id(self, class_id):
        return {"class_id": class_id,
                "students": self.dal.get_performance_by_class_id(class_id)}

    def performance_by_student_id_class_id(self, student_id, class_id):
        student_details = self.dal.get_student_by_student_id([student_id])[0]
        score_details = self.dal.get_performace_class_student(student_id, class_id)[0]
        return {
            "class_id": score_details['class_id'],
            "student_id": student_details['_id'],
            "marks": score_details['scores'],
            "student_name": student_details['name'],
        }

    def grade_sheet(self, class_id):
        scores = self.dal.def_get_grade_sheet(class_id)
        total_records = float(len(scores))

        grade_a = int(ceil(total_records/12.0))
        range_grade_a = [x for x in range(0, grade_a)]

        grade_b = int(ceil(total_records/6.0))
        range_grade_b = [x for x in range(grade_a, grade_b)]

        grade_c = int(ceil(total_records/4.0))
        range_grade_c = [x for x in range(grade_b, grade_c)]

        grade_d = int(ceil(total_records))
        range_grade_d = [x for x in range(grade_c, grade_d)]

        for index, row in enumerate(scores):
            if index in range_grade_a:
                row['grade'] = 'A'
            elif index in range_grade_b:
                row['grade'] = 'B'
            elif index in range_grade_c:
                row['grade'] = 'C'
            elif index in range_grade_d:
                row['grade'] = 'D'

        return scores
