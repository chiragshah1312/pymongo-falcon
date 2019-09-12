import pymongo
from bson.son import SON

from university.university.config import *


class DAL:
    db_client = pymongo.MongoClient(DATABASE_CONNECTION)[DATABASE_NAME]

    def __init__(self):
        pass

    def get_all_students(self):
        return list(self.db_client[COLLECTION_STUDENTS].find({}))
        # return grades_coll.estimated_document_count()

    def get_each_collection_sample(self):
        for collection_name in ['posts', 'trips', 'tweets', 'grades', 'stories', 'zips', 'routes', 'students']:
            c = 0
            cursor = self.db_client[collection_name].find({})

            for document in cursor:

                print(collection_name)
                print(document)
                c += 1
                if c >= 1:
                    break

    def get_class_by_student_id(self, student_id):
        return list(self.db_client[COLLECTION_GRADES].find({'student_id': student_id}))

    def get_student_by_student_id(self, list_student_id):
        return list(self.db_client[COLLECTION_STUDENTS].find({"_id": {"$in": list_student_id}}))

    def get_student_by_class_id(self, class_id):
        return list(self.db_client[COLLECTION_GRADES].find({'class_id': class_id}))

    def get_classes(self):
        return list(self.db_client[COLLECTION_GRADES].find({}).distinct("class_id"))

    def get_performance_by_student_id(self, student_id):
         pipeline = [
             {'$match': {'student_id': student_id}
             },
             {'$project': {
                        "score": "$scores.score",
                        "class_id": "$class_id"}
             },
             {"$unwind": "$score"
             },
             {'$group': {
                        '_id': {"class_id": "$class_id"},
                        'sum': {'$sum': '$score'}}
             },
             {'$project': {
                        "class_id": "$_id.class_id",
                        "total_marks": "$sum",
                        "_id":0}
             }
         ]
         return list(self.db_client[COLLECTION_GRADES].aggregate(pipeline))

    def get_performance_by_class_id(self, class_id):
        pipeline = [
            {"$match": {"class_id": class_id}
            },
            {"$project": {
                    "student_id": "$student_id",
                    "score": "$scores.score"}
            },
            {"$unwind": "$score"
            },
            {'$group': {'_id': {"student_id": "$student_id"},
                        'sum': {'$sum': '$score'}}
            },
            {'$project': {
                        "student_id": "$_id.student_id",
                        "total_marks": "$sum",
                        "_id": 0
                        }
            },
            {"$lookup": {
                        "from": COLLECTION_STUDENTS,
                        "localField": "student_id",
                        "foreignField": "_id",
                        "as": "student_details"}
            },
            {"$project": {
                "student_id": "$student_id",
                "total_marks": "$total_marks",
                "student_name": "$student_details.name"},
            },
            {"$unwind": "$student_name"}
        ]
        return list(self.db_client[COLLECTION_GRADES].aggregate(pipeline))

    def get_performace_class_student(self, student_id, class_id):
        return list(self.db_client[COLLECTION_GRADES].find({'student_id': student_id, 'class_id': class_id}))

    def def_get_grade_sheet(self, class_id):
        pipeline = [
            {"$match": {"class_id": class_id}
             },
            {"$project": {
                "student_id": "$student_id",
                "total": {"$sum": "$scores.score"},
                "scores": "$scores"}
            },
            {'$project': {
                "student_id": "$student_id",
                "details":  {"$concatArrays": ["$scores", [{"type": "total", "marks": "$total"}]]} ,
                "total": "$total",
                "_id": 0
            }},
            {"$lookup": {
                        "from": COLLECTION_STUDENTS,
                        "localField": "student_id",
                        "foreignField": "_id",
                        "as": "student_details"}
            },
            {"$project": {
                "student_id": "$student_id",
                "details": "$details",
                "student_name": "$student_details.name",
                "total": "$total"},
            },
            {"$unwind": "$student_name"},
            {"$sort": {"total": -1}},
            {"$project": {
                "student_id": "$student_id",
                "details": "$details",
                "student_name": "$student_name"},
            },
        ]
        return list(self.db_client[COLLECTION_GRADES].aggregate(pipeline))