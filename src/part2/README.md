# 🎯 Judge Dashboard - Flask Web App (Part2)

This is the **Flask-based web application** used for **judging research posters**.  
It reads judges' assignments from an **Excel file**, retrieves additional data from a **MySQL database**, and allows **judges to submit scores**.

💡 **For Public Access**: The app is exposed to the internet via **ngrok**, allowing remote users to log in and access the dashboard.

---

## 🚀 **1. Installation & Setup (Run Locally)**

### ✅ **Step 1: Clone the Repository**
First, **clone the project** and navigate into the `part2/` directory:
```sh
git clone https://github.com/rohitanil/Otto.git
cd src/part2
```

### ✅ **Step 2: Create a Virtual Environment**
To avoid dependency conflicts, create and activate a Python virtual environment:
```sh
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR (For Windows)
.venv\Scripts\activate
```

### ✅ **Step 3: Install Dependencies**
Ensure you have all required packages installed:
```sh
pip install -r requirements.txt
```

---

## 🎯 **2. Configuring the Database**
This app retrieves judge and poster details from MySQL. Update the database connection in `db_connection.py`:

```python
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="your-database-host",
        user="your-database-user",
        password="your-database-password",
        database="your-database-name"
    )
```

## 🔥 **3. Running the Backend**
Start the Flask backend:
```sh
python backend_api.py
```
Once the server starts, it will be available at:
```
http://127.0.0.1:5001/
```

---

## 🌍 **4. Exposing the App Publicly with ngrok**
To make your Flask app accessible to external users, use ngrok.

### ✅ **Step 1: Install ngrok**
If you haven’t installed ngrok, download it from: [ngrok Download](https://ngrok.com/downloads/mac-os)

Then, extract and install it:
```sh
unzip ngrok.zip
chmod +x ngrok
```

### ✅ **Step 2: Start Flask Locally**
Ensure the Flask server is running:
```sh
python backend_api.py
```

### ✅ **Step 3: Start ngrok to Expose Flask**
Run:
```sh
ngrok http 5001
```
This will generate a public URL like:
```
Forwarding   https://random-name.ngrok.io -> http://127.0.0.1:5001
```
Copy this ngrok URL and share it with users to access the login page remotely.

---

## 🔑 **5. Accessing the Login Page**
**Locally:** Open in your browser:
```
http://127.0.0.1:5001/login_page.html
```

**Publicly (via ngrok):**
```
https://b646-67-249-96-145.ngrok-free.app
```

---

## 🛠 **6. Testing API Endpoints (Optional)**
You can test API endpoints using Postman or cURL.

### ✅ **Login (POST Request)**
```sh
curl -X POST http://127.0.0.1:5001/login -H "Content-Type: application/json" -d '{"judge_id": "14"}'
```

### ✅ **Get Assigned Posters**
```sh
curl "http://127.0.0.1:5001/dashboard?judge_id=14"
```

### ✅ **Submit a Score (POST Request)**
```sh
curl -X POST http://127.0.0.1:5001/submit_score -H "Content-Type: application/json" -d '{"judge_id": "14", "poster_id": "2", "score": "8.5"}'
```

---

## ❓ **7. Troubleshooting**

❌ **Error: "ModuleNotFoundError: No module named 'Flask'"?**  
✔ Run: `pip install -r requirements.txt`

❌ **Error: "MySQL connection refused"?**  
✔ Ensure MySQL is running and credentials in `db_connection.py` are correct.

❌ **ngrok shows "ERR_NGROK_6023"?**  
✔ Run: `ngrok authtoken YOUR_AUTH_TOKEN` (Get it from [ngrok.com](https://ngrok.com))