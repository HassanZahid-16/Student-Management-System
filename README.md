# 🎓 Student Management System (Streamlit + Python OOP)

A simple Student Management System built using Python, Streamlit, and Object-Oriented Programming (OOP).  
It allows you to add, update, delete, search, and manage student records using a JSON file as storage.

---

## 🚀 Quick Start

### 1. Clone / Download Project
Open the project folder in VS Code.

---

### 2. Create Virtual Environment
```bash
python -m venv venv
````

Activate it:

* Windows CMD:

```bash
venv\Scripts\activate
```

* PowerShell:

```bash
venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

```bash
streamlit run ui/app.py
```

Open the browser link shown (usually):

```
http://localhost:8501
```

---

## 📁 Project Structure

```
models/              # Student class (OOP model)
services/
    storage.py       # JSON read/write operations
    manager.py       # CRUD, validation, search logic
ui/
    app.py           # Streamlit frontend
data/
    students.json    # Data storage file
```

---

## ✨ Features

* ➕ Add new students
* 📋 View all students
* ✏ Update student details
* 🗑 Delete students
* 🔍 Search and filter students
* 📊 Dashboard with statistics
* 🎨 Dark/Light mode UI

---

## 🛠 Technologies Used

* Python
* Streamlit
* Pandas
* JSON (file storage)
* Object-Oriented Programming (OOP)

---

## 📌 Notes

* Make sure `data/students.json` exists before running
* If not present, create it with:

```json
[]
```

