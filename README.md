# 🎯 AI Interview Simulator

An AI-powered interview simulation platform built with Django that conducts category-based interviews, evaluates answers using semantic similarity, calculates scores automatically, and detects malpractice through real-time face monitoring using OpenCV.

---

## 🚀 Features

### 👤 User Module
- User Registration and Login
- Category-wise Interview Selection
- Interview Request System
- AI-Based Answer Evaluation
- Automatic Score Calculation
- View Interview Results
- Prevention of Multiple Attempts

### 👨‍💼 Admin Module
- Add and Manage Interview Questions
- Approve or Reject Interview Requests
- View User Requests
- View Interview Results

### 🤖 AI Evaluation
- Semantic similarity-based answer evaluation
- Automatic mark calculation
- Final score generation

### 🎥 Malpractice Detection
- Real-time face monitoring using OpenCV
- Detects:
  - No face detected
  - Multiple faces detected
- Prevents re-attempts after malpractice detection

---

## 🛠️ Tech Stack

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite / MySQL
- **AI:** Semantic Similarity Algorithm
- **Computer Vision:** OpenCV
- **Authentication:** Django Authentication System

---



## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/akshaykv03/Ai_Interview_Simulator.git
cd Ai_Interview_Simulator
```

### Create Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r req.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

### Home Page

<img width="1890" height="833" alt="Screenshot 2026-06-23 151932" src="https://github.com/user-attachments/assets/8fe7e3a4-51f9-45c0-8952-ae230eb49615" />

---

### User Registration

<img width="1580" height="826" alt="Screenshot 2026-06-23 152000" src="https://github.com/user-attachments/assets/892fe73e-25da-42b2-832e-21ca7c564bd1" />

---

### Login Page

<img width="1892" height="827" alt="Screenshot 2026-06-23 152059" src="https://github.com/user-attachments/assets/f2911fad-bf86-479b-9642-784d68414755" />

---

### Face Detection / Malpractice Monitoring

<img width="1890" height="830" alt="Screenshot 2026-06-23 152515" src="https://github.com/user-attachments/assets/44140f97-69d3-409f-a5fa-4a000dddab3a" />

---

### Result Page

<img width="1889" height="696" alt="Screenshot 2026-06-23 152137" src="https://github.com/user-attachments/assets/31abdc61-609f-46bb-a3d8-3d3de1d1c24e" />

---


## 🔄 Workflow

1. User registers and logs in.
2. User requests an interview category.
3. Admin approves the request.
4. User attends the interview.
5. AI evaluates answers automatically.
6. Face detection continuously monitors the candidate.
7. Results are stored and displayed.
8. User can view scores and interview status.

---

## 🎥 Malpractice Detection

The system uses OpenCV Haar Cascade to monitor candidates during interviews.

### Conditions

✅ One face detected → Normal

❌ No face detected → Suspicious

❌ Multiple faces detected → Malpractice

---

## 🔮 Future Enhancements

- Voice-based interviews
- Speech-to-text answer evaluation
- Webcam recording
- Timer-based interviews
- Question randomization
- PDF report generation
- Email notifications
- Analytics dashboard

---

## 👨‍💻 Author

**Akshay K V**

Python Full Stack Developer | Django Developer

---

⭐ If you found this project useful, consider giving it a star!
