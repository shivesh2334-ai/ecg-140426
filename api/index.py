import math
import os
import io

from flask import Flask, request, render_template, jsonify
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)


def calculate_qtc(qt_interval, heart_rate):
    """Calculates QTc using Bazett's Formula"""
    if heart_rate <= 0:
        return 0
    rr_interval_sec = 60 / heart_rate
    return qt_interval / math.sqrt(rr_interval_sec)


def get_medgemma_response(api_key, image, prompt):
    """Sends image and text prompt to MedGemma"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('medgemma-1.5-4b-it')
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.form.get("api_key", "").strip()
    if not api_key:
        return jsonify({"error": "API key is required."}), 400

    uploaded_file = request.files.get("ecg_image")
    if not uploaded_file or uploaded_file.filename == "":
        return jsonify({"error": "ECG image is required."}), 400

    try:
        image = Image.open(uploaded_file.stream)
    except Exception:
        return jsonify({"error": "Could not read the uploaded image."}), 400

    # Collect manual findings from form
    clinical_context = request.form.get("clinical_context", "")
    calibration = request.form.get("calibration", "Standard")
    rhythm = request.form.get("rhythm", "Regular")

    try:
        heart_rate = float(request.form.get("heart_rate", 75))
    except ValueError:
        heart_rate = 75

    p_waves = request.form.get("p_waves", "Sinus (Upright I, II, aVF)")

    try:
        pr_ms = float(request.form.get("pr_ms", 160))
    except ValueError:
        pr_ms = 160

    try:
        qrs_ms = float(request.form.get("qrs_ms", 80))
    except ValueError:
        qrs_ms = 80

    axis = request.form.get("axis", "Normal Axis")
    st_changes = request.form.get("st_changes", "None/Normal")

    try:
        qt_ms = float(request.form.get("qt_ms", 360))
    except ValueError:
        qt_ms = 360

    qtc = calculate_qtc(qt_ms, heart_rate)

    findings = {
        "Clinical Context": clinical_context,
        "Calibration": calibration,
        "Rhythm": rhythm,
        "Heart Rate": f"{int(heart_rate)} bpm",
        "P Waves": p_waves,
        "PR Interval": f"{int(pr_ms)} ms",
        "QRS Duration": f"{int(qrs_ms)} ms",
        "Axis": axis,
        "ST-T Changes": st_changes,
        "QTc": f"{int(qtc)} ms",
    }

    prompt = f"""
You are MedGemma, a specialized medical AI model from Google with expertise in cardiology and ECG interpretation.
I have performed a manual analysis of the attached ECG image and recorded the following findings.

Patient Clinical Context: {findings['Clinical Context']}

My Manual Findings:
- Rate: {findings['Heart Rate']}
- Rhythm: {findings['Rhythm']}
- P Waves: {findings['P Waves']}
- PR Interval: {findings['PR Interval']}
- QRS Duration: {findings['QRS Duration']}
- Axis: {findings['Axis']}
- ST/T Changes: {findings['ST-T Changes']}
- QTc: {findings['QTc']}

Please perform the following:
1. VISUAL VERIFICATION: Look at the image. Do my manual findings (Rate, Axis, ST changes) look accurate? Correct me if I am wrong.
2. DIAGNOSIS: Based on the image and the confirmed metrics, provide a formal ECG diagnosis.
3. CLINICAL RELEVANCE: Explain the significance of these findings given the clinical context.
4. NEXT STEPS: Suggest immediate management or further tests.
"""

    result = get_medgemma_response(api_key, image, prompt)
    return jsonify({"result": result, "qtc": int(qtc), "heart_rate": int(heart_rate)})


if __name__ == "__main__":
    app.run(debug=True)
