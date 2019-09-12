""" Starts a gunicorn server to serve the requests
"""

import falcon
from wsgiref import simple_server

from university.university.urls import ROUTES
from university.app.controller import students_by_class_service, students_list_service, \
    performance_by_student_service, class_list_service, class_by_student_service, \
    performance_by_class_service, performance_by_student_class_service, performance_by_class_student_service, \
    grade_sheet_service


def get_app():
    global app
    """Creates an instance of falcon app"""
    app = falcon.API()

    obj_students_list_service = students_list_service.StudentList()
    obj_class_by_student_service = class_by_student_service.ClassByStudent()
    obj_students_by_class_service = students_by_class_service.StudentsByClass()
    obj_class_list_service = class_list_service.ClassList()
    obj_performance_by_student_service = performance_by_student_service.PerformanceByStudent()
    obj_performance_by_class_service = performance_by_class_service.PerformanceByClass()
    obj_performance_by_student_class_service = performance_by_student_class_service.PerformanceByStudentClass()
    obj_performance_by_class_student_service = performance_by_class_student_service.PerformanceByClassStudent()
    obj_grade_sheet_service = grade_sheet_service.GradeSheetClass()

    # registering each api to app
    app.add_route(ROUTES["students_list"], obj_students_list_service)
    app.add_route(ROUTES["class_by_student"], obj_class_by_student_service)
    app.add_route(ROUTES["student_by_class"], obj_students_by_class_service)
    app.add_route(ROUTES["class_list"], obj_class_list_service)
    app.add_route(ROUTES["performance_by_student"], obj_performance_by_student_service)
    app.add_route(ROUTES["performance_by_class"], obj_performance_by_class_service)
    app.add_route(ROUTES["performance_by_student_for_class"], obj_performance_by_student_class_service)
    app.add_route(ROUTES["performance_by_class_for_student"], obj_performance_by_class_student_service)
    app.add_route(ROUTES["grade_sheet"], obj_grade_sheet_service)

    return app

app = get_app()

if __name__ == "__main__":
    # this is for testing only, gunicorn is used in actual environment
    httpd = simple_server.make_server('localhost', 8000, get_app())
    httpd.serve_forever()

