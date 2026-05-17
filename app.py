from flask import Flask, render_template_string, request, redirect, url_for, session
from ultralytics import YOLO
import os
import math
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "campusmate_secret_key"

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")

style = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #eef4ff, #f8fbff);
    color: #0f172a;
}

.navbar {
    height: 72px;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid #e5e7eb;
    padding: 0 55px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 10;
}

.logo {
    font-size: 24px;
    font-weight: 800;
    color: #2563eb;
}

.navbar a {
    color: #334155;
    text-decoration: none;
    margin-left: 28px;
    font-weight: 600;
}

.navbar a:hover {
    color: #2563eb;
}

.container {
    max-width: 1150px;
    margin: 45px auto;
    padding: 0 24px;
}

.hero {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border-radius: 30px;
    padding: 52px;
    box-shadow: 0 25px 60px rgba(37,99,235,0.28);
}

.hero h1 {
    font-size: 42px;
    margin: 0 0 14px;
}

.hero p {
    font-size: 18px;
    opacity: 0.92;
    max-width: 760px;
    line-height: 1.7;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    margin-top: 28px;
}

.card {
    background: rgba(255,255,255,0.94);
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.08);
    margin-bottom: 24px;
}

.card h2 {
    margin-top: 0;
    font-size: 24px;
}

.subtitle {
    color: #64748b;
    line-height: 1.7;
}

.upload-box {
    border: 2px dashed #93c5fd;
    border-radius: 22px;
    padding: 32px;
    text-align: center;
    background: #f8fbff;
}

input {
    padding: 14px;
    width: 100%;
    margin: 12px 0;
    border: 1px solid #cbd5e1;
    border-radius: 14px;
    font-size: 15px;
}

input[type="file"] {
    background: white;
}

button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    padding: 14px 26px;
    border-radius: 14px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 12px 24px rgba(37,99,235,0.25);
}

button:hover {
    transform: translateY(-1px);
}

.badge {
    display: inline-block;
    background: #eef2ff;
    color: #3730a3;
    padding: 10px 15px;
    border-radius: 999px;
    margin: 6px;
    font-weight: 600;
}

.profile-row {
    display: flex;
    justify-content: space-between;
    padding: 14px 0;
    border-bottom: 1px solid #e5e7eb;
}

.low {
    color: #16a34a;
    font-size: 22px;
    font-weight: 800;
}

.medium {
    color: #f59e0b;
    font-size: 22px;
    font-weight: 800;
}

.high {
    color: #dc2626;
    font-size: 22px;
    font-weight: 800;
}

img {
    width: 100%;
    border-radius: 22px;
    box-shadow: 0 18px 45px rgba(15,23,42,0.12);
}

.login-card {
    max-width: 460px;
    margin: 90px auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    overflow: hidden;
    border-radius: 14px;
}

th {
    background: #eef2ff;
    color: #3730a3;
    padding: 13px;
    text-align: left;
}

td {
    padding: 13px;
    border-bottom: 1px solid #e5e7eb;
}

tr:hover {
    background: #f8fafc;
}

.report-note {
    background: #fefce8;
    color: #854d0e;
    padding: 14px;
    border-radius: 14px;
    margin-top: 18px;
    line-height: 1.6;
}

@media (max-width: 760px) {
    .navbar {
        padding: 0 22px;
    }

    .grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 32px;
    }

    .hero h1 {
        font-size: 32px;
    }
}
</style>
"""

login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusMate Login</title>
    """ + style + """
</head>
<body>
    <div class="navbar">
        <div class="logo">CampusMate AI</div>
    </div>

    <div class="container">
        <div class="card login-card">
            <h1>Welcome Back</h1>
            <p class="subtitle">Login to access the CampusMate AI accessibility analysis system.</p>

            <form method="POST">
                <input type="text" name="username" placeholder="Enter username" required>
                <input type="password" name="password" placeholder="Enter password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusMate Dashboard</title>
    """ + style + """
</head>
<body>
    <div class="navbar">
        <div class="logo">CampusMate AI</div>
        <div>
            <a href="/dashboard">Dashboard</a>
            <a href="/profile">Profile</a>
            <a href="/logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>Hello, {{ username }} 👋</h1>
            <p>
                CampusMate uses AI vision to analyse bus stop images, detect objects,
                estimate person-to-object distance, and identify accessibility risks.
            </p>
        </div>

        <div class="grid">
            <div class="card">
                <h2>AI Bus Stop Analysis</h2>
                <p class="subtitle">
                    Upload a bus stop image. The system will use YOLOv8 to detect objects
                    such as people, buses, benches and chairs.
                </p>

                <form action="/detect" method="POST" enctype="multipart/form-data">
                    <div class="upload-box">
                        <p><strong>Upload bus stop image</strong></p>
                        <input type="file" name="image" accept="image/*" required>
                        <button type="submit">Run AI Analysis</button>
                    </div>
                </form>
            </div>

            <div class="card">
                <h2>System Features</h2>
                <span class="badge">YOLOv8 Detection</span>
                <span class="badge">Object Confidence</span>
                <span class="badge">Distance Report</span>
                <span class="badge">Accessibility Risk</span>
                <span class="badge">Student Profile</span>
                <span class="badge">Smart Campus</span>

                <p class="subtitle" style="margin-top: 20px;">
                    This prototype supports smart campus accessibility monitoring by analysing
                    visual conditions around bus stops.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""

profile_page = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusMate Profile</title>
    """ + style + """
</head>
<body>
    <div class="navbar">
        <div class="logo">CampusMate AI</div>
        <div>
            <a href="/dashboard">Dashboard</a>
            <a href="/profile">Profile</a>
            <a href="/logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>User Profile</h1>
            <p>Personalised student accessibility support profile.</p>
        </div>

        <div class="card">
            <div class="profile-row">
                <strong>Username</strong>
                <span>{{ username }}</span>
            </div>
            <div class="profile-row">
                <strong>Role</strong>
                <span>Student</span>
            </div>
            <div class="profile-row">
                <strong>Campus</strong>
                <span>Melbourne</span>
            </div>
            <div class="profile-row">
                <strong>Accessibility Preference</strong>
                <span>Bus stop accessibility support</span>
            </div>
        </div>

        <div class="card">
            <h2>Prototype Features</h2>
            <span class="badge">AI Detection</span>
            <span class="badge">Bus Stop Analysis</span>
            <span class="badge">Distance Estimation</span>
            <span class="badge">Accessibility Risk</span>
            <span class="badge">Student Dashboard</span>
        </div>
    </div>
</body>
</html>
"""

result_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Analysis Result</title>
    """ + style + """
</head>
<body>
    <div class="navbar">
        <div class="logo">CampusMate AI</div>
        <div>
            <a href="/dashboard">Dashboard</a>
            <a href="/profile">Profile</a>
            <a href="/logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>AI Analysis Result</h1>
            <p>
                The system analysed the uploaded image and generated an object detection,
                distance and accessibility report.
            </p>
        </div>

        <div class="card">
            <h2>Detected Objects</h2>
            {% if objects %}
                {% for item in objects %}
                    <span class="badge">{{ item }}</span>
                {% endfor %}
            {% else %}
                <p class="subtitle">No objects detected.</p>
            {% endif %}
        </div>

        <div class="card">
            <h2>Accessibility Risk</h2>
            <p class="{{ risk_class }}">{{ risk }}</p>
            <p class="subtitle">{{ explanation }}</p>
        </div>

        <div class="card">
            <h2>AI Analysis Report</h2>

            <h3>Object Detection Details</h3>
            <table>
                <tr>
                    <th>Object</th>
                    <th>Confidence</th>
                    <th>Centre Point</th>
                    <th>Bounding Box</th>
                </tr>
                {% for item in object_details %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.confidence }}%</td>
                    <td>({{ item.center_x }}, {{ item.center_y }})</td>
                    <td>{{ item.bbox }}</td>
                </tr>
                {% endfor %}
            </table>

            <h3 style="margin-top: 28px;">Person-to-Object Distance</h3>
            {% if distance_report %}
            <table>
                <tr>
                    <th>Person</th>
                    <th>Object</th>
                    <th>Estimated Distance</th>
                </tr>
                {% for d in distance_report %}
                <tr>
                    <td>{{ d.person }}</td>
                    <td>{{ d.object }}</td>
                    <td>{{ d.distance }} pixels</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
                <p class="subtitle">
                    No person-to-object distance was calculated because either no person
                    or no other object was detected.
                </p>
            {% endif %}

            <div class="report-note">
                Note: This prototype estimates relative distance using pixel distance
                between detected bounding box centre points. It does not calculate real-world metres.
            </div>
        </div>

        <div class="card">
            <h2>Result Image</h2>
            <img src="{{ image_path }}">
        </div>

        <a href="/dashboard">
            <button>Back to Dashboard</button>
        </a>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("dashboard"))

    return render_template_string(login_page)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        dashboard_page,
        username=session["username"]
    )

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        profile_page,
        username=session["username"]
    )

@app.route("/detect", methods=["POST"])
def detect():
    if "username" not in session:
        return redirect(url_for("login"))

    image = request.files["image"]

    if image.filename == "":
        return redirect(url_for("dashboard"))

    filename = secure_filename(image.filename)

    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    result_path = os.path.join(RESULT_FOLDER, filename)

    image.save(upload_path)

    results = model(upload_path)

    detected_objects = []
    object_details = []
    person_centres = []
    other_objects = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            detail = {
                "name": class_name,
                "confidence": round(confidence * 100, 2),
                "center_x": round(center_x, 2),
                "center_y": round(center_y, 2),
                "bbox": f"({round(x1)}, {round(y1)}) to ({round(x2)}, {round(y2)})"
            }

            detected_objects.append(class_name)
            object_details.append(detail)

            if class_name == "person":
                person_centres.append(detail)
            else:
                other_objects.append(detail)

        result.save(filename=result_path)

    distance_report = []

    for person in person_centres:
        for obj in other_objects:
            distance = math.sqrt(
                (person["center_x"] - obj["center_x"]) ** 2 +
                (person["center_y"] - obj["center_y"]) ** 2
            )

            distance_report.append({
                "person": "person",
                "object": obj["name"],
                "distance": round(distance, 2)
            })

    detected_objects = list(set(detected_objects))

    risk = "Low Accessibility Risk"
    risk_class = "low"
    explanation = "The bus stop area appears to contain useful detected objects or facilities."

    if "bench" not in detected_objects and "chair" not in detected_objects:
        risk = "Medium Accessibility Risk"
        risk_class = "medium"
        explanation = "No seating object was detected. This may reduce comfort for elderly users, disabled users, or students waiting for buses."

    if "person" in detected_objects and "bus" not in detected_objects:
        risk = "High Accessibility Risk"
        risk_class = "high"
        explanation = "People were detected, but no bus-related object was detected. The system suggests reviewing the bus stop environment and service availability."

    image_path = "/" + result_path.replace("\\", "/")

    return render_template_string(
        result_page,
        objects=detected_objects,
        object_details=object_details,
        distance_report=distance_report,
        risk=risk,
        risk_class=risk_class,
        explanation=explanation,
        image_path=image_path
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)