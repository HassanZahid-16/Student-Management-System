class Student:
    def __init__(self, student_id, name, age, grade, performance):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.performance = performance

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "performance": self.performance
        }
