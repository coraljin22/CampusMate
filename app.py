from flask import Flask, render_template_string, request, redirect, url_for, session
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "campusmate_secret_key"

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")


login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusMate Login</title>
</head>
<body>
    <h1>CampusMate Login</h1>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>

        <label>Password:</label>
        <input type="password" name="password" required><br><br>

        <button type="submit">Login</button>
    </form>
</body>
</html>
"""


dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>CampusMate Dashboard</title>
</head>
<body>
    <h1>Hello, {{ username }}</h1>
    <h2>Welcome to CampusMate</h2>

    <p>This prototype uses YOLOv8 AI detection to identify objects from uploaded images.</p>

    <form action="/detect" method="POST" enctype="multipart/form-data">
        <label>Upload an image:</label>
        <input type="file" name="image" accept="image/*" required>
        <button type="submit">Run AI Detection</button>
    </form>

    <br>
    <a href="/logout">Logout</a>
</body>
</html>
"""


result_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Detection Result</title>
</head>
<body>
    <h1>AI Detection Result</h1>

    <h2>Detected Objects:</h2>
    <ul>
        {% for item in objects %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>

    <h2>Result Image:</h2>
    <img src="{{ image_path }}" width="600">

    <br><br>
    <a href="/dashboard">Back to Dashboard</a>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
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


@app.route("/detect", methods=["POST"])
def detect():
    if "username" not in session:
        return redirect(url_for("login"))

    image = request.files["image"]
    filename = secure_filename(image.filename)

    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(upload_path)

    results = model(upload_path)

    detected_objects = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            detected_objects.append(class_name)

        result.save(filename=os.path.join(RESULT_FOLDER, filename))

    image_path = "/" + os.path.join(RESULT_FOLDER, filename).replace("\\", "/")

    return render_template_string(
        result_page,
        objects=detected_objects,
        image_path=image_path
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)