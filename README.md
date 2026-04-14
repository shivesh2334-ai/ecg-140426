# 🫀 Systematic ECG Interpretation Tool (AI-Enhanced)

A guided, step-by-step ECG analysis web application built with **Python** and **Flask**, powered by **Google MedGemma** — a medical-domain specialized AI model from Google.

This tool digitizes the "Final Checklist for ECG Interpretation" workflow, allowing medical professionals and students to upload ECG images, calculate parameters (Rate, Axis, QTc) using standard clinical rules, and receive an AI-generated cardiologist consultation.

---

## 🚀 Features

- **Image Upload:** Support for JPG and PNG ECG images.
- **Smart Rate Calculation:**
  - *Regular Rhythm:* 1500 / small squares method.
  - *Irregular Rhythm:* 6-second strip method (QRS count × 10).
- **Axis Determination:** Automated logic based on Leads I and aVF (detects Normal, LAD, RAD, and Extreme deviation).
- **Interval Converter:** Input measurements in "small squares" and automatically convert to milliseconds (25 mm/s paper speed).
- **QTc Calculator:** Automatic calculation of Corrected QT using Bazett's Formula ($QTc = QT / \sqrt{RR}$).
- **AI Cardiologist Consultation:** Sends the ECG image and your manual findings to Google MedGemma (a medical-domain specialized AI model) for visual verification, formal diagnosis, clinical relevance, and next steps.
- **Real-time calculations** in the browser as you enter values.

---

## ☁️ Vercel Deployment

### One-click deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/shivesh2334-ai/ecg-140426)

### CLI deploy

```bash
npm install -g vercel
vercel
```

Follow the prompts. No build step is required — Vercel picks up `vercel.json` automatically.

### Environment Variables (optional)

You can pre-configure the MedGemma API key as an environment variable so it is available server-side, but the UI also accepts it directly from the user.

| Variable | Description |
|---|---|
| `MEDGEMMA_API_KEY` | Your Google MedGemma API key (optional — users can enter it in the UI) |

Set it in the Vercel dashboard under **Project → Settings → Environment Variables**.

---

## 🛠️ Local Development

### Prerequisites

- Python 3.9 or higher
- A [Google MedGemma API key](https://aistudio.google.com/app/apikey) (free tier available)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Flask app

```bash
python api/index.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📋 Usage

1. Enter your **Google MedGemma API Key** in the sidebar.
2. **Upload** a PNG or JPG ECG image.
3. (Optional) Add **patient clinical context** (e.g., age, symptoms, history).
4. Work through the **Manual Findings Checklist** (Steps 0–8):
   - Calibration
   - Rate & Rhythm
   - P Waves
   - PR Interval
   - QRS Duration
   - Axis
   - ST/T Changes
   - QT Interval (QTc is calculated automatically)
5. Click **"Generate Diagnosis with MedGemma 🩺"** to get the AI report.

---

## ⚠️ Disclaimer

AI models can hallucinate. This tool is for **educational purposes only**. Always verify findings with a qualified human cardiologist.
