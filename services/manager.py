from models.student import Student
from services.storage import load_data, save_data

class StudentManager:
    def __init__(self):
        self.students = load_data()

    def add_student(self, student: Student):
        self.students.append(student.to_dict())
        save_data(self.students)

    def list_students(self):
        return self.students

    def delete_student(self, student_id):
        # Ensure ID matches even if numeric/string mismatch
        self.students = [s for s in self.students if str(s["id"]) != str(student_id)]
        save_data(self.students)

    def delete_student_by_name(self, name):
        # Delete ignoring uppercase/lowercase
        self.students = [s for s in self.students if s["name"].lower() != name.lower()]
        save_data(self.students)

    def update_student(self, student_id, new_data):
        updated = False
        for s in self.students:
            if str(s["id"]) == str(student_id):
                s.update(new_data)
                updated = True
                break
        if updated:
            save_data(self.students)
        return updated

    # 🔥 CHECK DUPLICATE IDs
    def is_duplicate_id(self, student_id):
        return any(str(student["id"]) == str(student_id) for student in self.students)

    # (Optional – If you want duplicate name check in future)
    def is_duplicate_name(self, name):
        return any(student["name"].lower() == name.lower() for student in self.students)
