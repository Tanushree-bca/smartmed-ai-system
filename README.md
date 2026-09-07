# 💊 SmartMed AI System

An AI-powered, cloud-deployed medicine reminder and health companion web app.

**Domain:** Artificial Intelligence & Cloud Computing
**Type:** Internship Project (BCA)

🔗 **Live App:** https://tanushree-bca-smartmed-ai-system-app-dgzloy.streamlit.app

---

## 📌 About

SmartMed AI System helps users track their daily medicines, log how they're feeling, and get an AI-based prediction of their health status — all through a simple web interface, accessible from any device.

## ✨ Features

- **🏠 Medicine Reminder** — Log up to 3 daily medicines with reminder times, and mark each as taken or missed.
- **🩺 AI Health Check** — Enter temperature, feeling, and missed doses. A trained Decision Tree model predicts whether health status is "Normal" or "Needs Attention."
- **📋 Medicine History** — Browse a clean, tabbed view of all past medicine and health check records.

## 🧠 AI Model

- Built with **scikit-learn**'s `DecisionTreeClassifier`
- Trained on sample health data (temperature, feeling, missed doses → health status)
- Categorical inputs are label-encoded before training
- Model is saved as `.pkl` files and loaded at runtime for fast predictions

## ☁️ Cloud Deployment

- Code is version-controlled with **Git** and hosted on **GitHub**
- Deployed live using **Streamlit Community Cloud**
- Continuous deployment: pushing to GitHub automatically updates the live app

## 🛠️ Tech Stack

| Layer            | Technology         |
|-------------------|--------------------|
| Language          | Python              |
| Web Framework     | Streamlit           |
| Machine Learning  | scikit-learn, joblib|
| Data Handling     | pandas              |
| Storage           | JSON                |
| Version Control   | Git & GitHub        |
| Hosting           | Streamlit Cloud     |

## 📁 Project Structure

```
smartmed_project/
├── app.py                 # Main entry point, navigation, styling
├── medicine_reminder.py   # Medicine Reminder page
├── health_check.py        # AI-powered Health Check page
├── medicine_history.py    # Medicine History page
├── storage.py              # Save/load records (JSON)
├── train_model.py          # Trains and saves the AI model (run once)
├── health_model.pkl        # Trained AI model
├── feeling_encoder.pkl     # Label encoder for "feeling" input
├── requirements.txt        # Python dependencies
└── smartmed_data.json      # Saved user records
```

## ▶️ Running Locally

```bash
pip install -r requirements.txt
python train_model.py    # only needed once, to create the AI model files
streamlit run app.py
```

## 👩‍💻 Author

Tanushree — BCA, Internship Project