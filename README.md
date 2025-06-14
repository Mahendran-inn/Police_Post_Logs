# Police_Post_Logs 🚔

## 🔹 Project Title
**Police_Post_Logs** — A Streamlit application designed to visualize and analyze police post logs.  
It lets you:
- Perform **CRUD operations**
- Push cleaned CSV data directly into a **Postgres database**
- Retrieve and view this data through a **user-friendly Streamlit UI**

---

## 🔹 Installed Libraries

- 🐍 **Python**
- 🐼 **Pandas**
- 🔹 **SQLAlchemy**
- 🐘 **Psycopg2**
- 🌐 **Streamlit**

---

## 🔹 Installation and Setup

### 1️⃣ Create and Activate a Virtual Environment:

```bash
python -m venv .venv
````

To activate:

```bash
.venv/Scripts/activate  # Windows
```

---

### 2️⃣ Install Required Packages:

```bash
pip install pandas
pip install sqlalchemy
pip install psycopg2
pip install streamlit
```

---

## 🔹 Why Pandas?

🚀 **Pandas** is a powerful library for:

* Loading CSV files
* Viewing, cleaning, and transforming data
* Handling duplicates, null values, and changing data types

### Example:

```python
import pandas as pd
data = pd.read_csv("path/to/file.csv")
```

### Basic structure checks:

```python
data.isnull().sum()
data.duplicated().sum()
df.info()
df = data.copy()
```

---

## 🔹 Why SQLAlchemy?

🚀 **SQLAlchemy** lets you:

* Push large amounts of data directly into a Postgres database.
* Handle table schema, connection, and transactions gracefully.

### Example:

```python
from sqlalchemy import create_engine

username = "yourUsername"
password = "yourPass"
host = "yourHost"
port = 5432
database = "yourDatabase"

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
connection = engine.connect()

df.to_sql("your_table_name", connection, if_exists='replace', index=False)
```

---

## 🔹 Why Psycopg2?

🚀 **Psycopg2** lets you:

* Perform low-level operations directly on your Postgres database.
* Query, execute, and fetch results manually.

### Example:

```python
import psycopg2

connection = psycopg2.connect(
    host='yourHost',
    port='yourPort',
    database='yourDatabase',
    user='yourUsername',
    password='yourPass'
)

mediator = connection.cursor()
mediator.execute("SELECT * FROM your_table")
result = mediator.fetchall()
```

---

## 🔹 Why Streamlit?

🚀 **Streamlit** lets you:

* Display your cleaned data directly in a web UI.
* Provide interactive components for a better User Experience.

---

## 🔹 Run Streamlit Application:

```bash
streamlit run policelog.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔹 Summary

✅ The **Police\_Post\_Logs** application efficiently:

* Initializes a **virtual environment**
* Loads CSV files with **pandas**
* Pushes cleaned data to **Postgres** with **SQLAlchemy**
* Performs raw **query operations** with **Psycopg2**
* Displays results through **Streamlit**

