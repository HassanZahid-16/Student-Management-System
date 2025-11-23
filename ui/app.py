import streamlit as st
from services.manager import StudentManager
from models.student import Student
import pandas as pd


# -------------------------------------------------------------------
# 🌗 THEME TOGGLE (Fully Working)
# -------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Toggle button
if st.sidebar.button("🌙 Dark Mode" if st.session_state.theme == "light" else "☀ Light Mode"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

# CSS Themes
dark_css = """
<style>
body, .stApp { background-color: #0e1117 !important; color: white !important; }
[data-testid="stHeader"] { background-color: #0e1117 !important; }
[data-testid="stSidebar"] { background-color: #161a23 !important; }
table, th, td { color: white !important; }
.stButton>button {
    background-color: #262730 !important;
    color: white !important;
    border-radius: 6px;
}
</style>
"""

light_css = """
<style>
body, .stApp { background-color: white !important; color: black !important; }
[data-testid="stHeader"] { background-color: white !important; }
[data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
.stButton>button {
    background-color: #e0e0e0 !important;
    color: black !important;
    border-radius: 6px;
}
</style>
"""

if st.session_state.theme == "dark":
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)


# -------------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------------
def main():
    manager = StudentManager()
    st.title("🎓 Student Management System")

    # -------------------------------------------------------
    # 📊 DASHBOARD SECTION
    # -------------------------------------------------------
    students = manager.list_students()
    if students:
        df = pd.DataFrame(students)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total Students", len(df))
        col2.metric("🎓 Total Grades", len(df["grade"].unique()))
        col3.metric("⭐ Performance Categories", len(df["performance"].unique()))
        col4.metric("📅 Average Age", round(df["age"].mean(), 1))

        st.subheader("📌 Breakdown Overview")
        c1, c2 = st.columns(2)

        with c1:
            st.write("**Grade-wise Count**")
            grade_count = df["grade"].value_counts().reset_index()
            grade_count.columns = ["Grade", "Count"]
            st.table(grade_count)

        with c2:
            st.write("**Performance-wise Count**")
            performance_count = df["performance"].value_counts().reset_index()
            performance_count.columns = ["Performance", "Count"]
            st.table(performance_count)

    else:
        st.info("📊 Dashboard will appear here once you add students.")

    # -------------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------------
    choice = st.sidebar.radio(
        "Select Option",
        ["Add Student", "View Students", "Update Student", "Delete Student"]
    )

    # -------------------------------------------------------
    # ADD STUDENT
    # -------------------------------------------------------
    if choice == "Add Student":
        st.header("➕ Add Student")
        id = st.text_input("Student ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"])
        performance = st.selectbox("Performance", ["Excellent", "Good", "Average", "Poor"])

        if st.button("Save"):
            if id.strip() == "" or name.strip() == "":
                st.error("⚠ Student ID and Name are required!")
            elif manager.is_duplicate_id(id):
                st.error("⚠ Student ID already exists!")
            else:
                student = Student(id, name, age, grade, performance)
                manager.add_student(student)
                st.success("✔ Student added successfully!")

    # -------------------------------------------------------
    # VIEW STUDENTS
    # -------------------------------------------------------
    elif choice == "View Students":
        st.header("📋 All Students")
        students = manager.list_students()

        if not students:
            st.warning("⚠ No students found.")
        else:
            search = st.text_input("🔍 Search by Student Name")
            grade_filter = st.selectbox("🎓 Filter by Grade", ["All"] + sorted(list(set([s["grade"] for s in students]))))
            performance_filter = st.selectbox("📌 Filter by Performance", ["All", "Excellent", "Good", "Average", "Poor"])
            age_range = st.slider("📅 Filter by Age", min_value=1, max_value=100, value=(1, 100))

            filtered = students

            if search:
                filtered = [s for s in filtered if search.lower() in s["name"].lower()]
            if grade_filter != "All":
                filtered = [s for s in filtered if s["grade"] == grade_filter]
            if performance_filter != "All":
                filtered = [s for s in filtered if s["performance"] == performance_filter]
            filtered = [s for s in filtered if age_range[0] <= s["age"] <= age_range[1]]

            st.subheader("🔎 Search & Filter Results")
            st.table(filtered)

    # -------------------------------------------------------
    # UPDATE STUDENT
    # -------------------------------------------------------
    elif choice == "Update Student":
        st.header("✏ Update Student")
        students = manager.list_students()

        if not students:
            st.warning("⚠ No students found for update.")
        else:
            ids = [s["id"] for s in students]
            selected = st.selectbox("Choose Student ID", ids)
            student = next((s for s in students if s["id"] == selected), None)

            name = st.text_input("Name", student["name"])
            age = st.number_input("Age", min_value=1, value=student["age"])
            grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], index=["A","B","C","D","E","F"].index(student["grade"]))
            performance = st.selectbox("Performance", ["Excellent", "Good", "Average", "Poor"], index=["Excellent","Good","Average","Poor"].index(student["performance"]))

            if st.button("Update"):
                manager.update_student(selected, {
                    "name": name,
                    "age": age,
                    "grade": grade,
                    "performance": performance
                })
                st.success("✔ Student updated successfully!")

    # -------------------------------------------------------
    # DELETE STUDENT  🔥 UPDATED WITH YES / NO CONFIRMATION
    # -------------------------------------------------------
    elif choice == "Delete Student":
        st.header("🗑 Delete Student")
        students = manager.list_students()

        if not students:
            st.warning("⚠ No students to delete.")
        else:
            delete_method = st.radio("Delete Method:", ["Delete by ID", "Delete by Name"])

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
                st.session_state.student_to_delete = None
                st.session_state.delete_by = None

            if delete_method == "Delete by ID":
                ids = [s["id"] for s in students]
                selected = st.selectbox("Choose Student ID", ids)

                if st.button("Delete"):
                    st.session_state.confirm_delete = True
                    st.session_state.student_to_delete = selected
                    st.session_state.delete_by = "id"

            else:
                names = [s["name"] for s in students]
                selected_name = st.selectbox("Choose Student Name", names)

                if st.button("Delete"):
                    st.session_state.confirm_delete = True
                    st.session_state.student_to_delete = selected_name
                    st.session_state.delete_by = "name"

            if st.session_state.confirm_delete:
                st.warning("⚠ Are you sure you want to delete this student?")
                colA, colB = st.columns(2)

                with colA:
                    if st.button("✔ YES"):
                        if st.session_state.delete_by == "id":
                            manager.delete_student(st.session_state.student_to_delete)
                        else:
                            manager.delete_student_by_name(st.session_state.student_to_delete)
                        st.session_state.confirm_delete = False
                        st.error("🗑 Student deleted successfully!")
                        st.rerun()

                with colB:
                    if st.button("❌ NO"):
                        st.session_state.confirm_delete = False
                        st.info("❎ Deletion cancelled.")
                        st.rerun()


if __name__ == "__main__":
    main()
