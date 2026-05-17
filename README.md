# CSE5IDP
project
# CampusMate AI

CampusMate AI is an intelligent accessibility analysis prototype designed to support smart campus transportation environments.

The system uses YOLOv8 computer vision technology to analyse uploaded bus stop images, detect surrounding objects, estimate relative object distance, and identify accessibility risks for students and public transport users.

---

# Features

- User Login System
- Modern AI Dashboard UI
- Bus Stop Image Upload
- YOLOv8 Object Detection
- Accessibility Risk Analysis
- Person-to-Object Distance Estimation
- AI Analysis Report
- Student Profile Page

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web application framework |
| YOLOv8 | AI object detection |
| OpenCV | Image processing |
| HTML/CSS | Frontend interface |
| GitHub | Version control and collaboration |

---

# System Workflow

1. User logs into the CampusMate system
2. User uploads a bus stop image
3. YOLOv8 detects objects from the image
4. The system generates:
   - detected objects
   - confidence score
   - distance estimation
   - accessibility risk report
5. Results are displayed on the dashboard

---

# Accessibility Analysis

The system evaluates accessibility conditions using detected visual objects.

Examples:
- No bench/chair detected → medium accessibility risk
- Person detected without bus-related objects → high accessibility risk

The system estimates relative distance using pixel distance between object centre points.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/coraljin22/CampusMate.git
```

---

## Navigate to the Project Folder

```bash
cd CampusMate
```

---

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

---

# Project Structure

```text
CampusMate/
│
├── app.py
├── yolov8n.pt
├── README.md
├── requirements.txt
│
├── static/
│   ├── uploads/
│   └── results/
```

---

# Future Improvements

- Real-time video detection
- GPS-based bus stop mapping
- Database integration
- User authentication system
- Accessibility scoring model
- Notification system
- Mobile application version

---

# Team Members

- Coral Jin
- Shreya Shrestha
- Riya
- Rishabh Chaudhary
- Sumit Khanal
- Yaman

---

# Project Purpose

This project was developed as part of an AI and software engineering assessment to demonstrate how computer vision can support smart campus accessibility and public transport analysis.

---

# GitHub Repository

https://github.com/coraljin22/CampusMate