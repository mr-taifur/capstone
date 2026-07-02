# 🛡️ AgriGuardian AI
### Smart Crop Health Guard for Bangladeshi Farmers using Multi-Agent AI

AgriGuardian AI is an intelligent multi-agent decision support system that helps farmers and agricultural extension workers diagnose crop diseases, receive treatment recommendations, analyze weather-related disease risks, and generate professional PDF reports.

Built using **Python**, **Streamlit**, and **Google Gemini AI**, the system combines AI reasoning with agricultural knowledge to provide practical, explainable recommendations.

---

## 🌟 Features

- 🌱 AI-powered crop disease diagnosis
- 🤖 Multi-Agent AI workflow
- 📷 Image-based crop analysis
- 📝 Symptom text analysis
- 🌦️ Weather-aware disease risk prediction
- 💊 Organic, biological, and BARC-approved chemical recommendations
- 📚 Built-in Bangladesh crop disease knowledge base
- 📄 Professional PDF report generation
- 🛡️ Prompt injection & unsafe input protection
- 🔒 Security logging and validation
- ⚡ Demo Mode (works without API key)
- 🚀 Live Mode using Google Gemini 2.5 Flash

---

## 🏗️ Multi-Agent Architecture

The application consists of five specialized AI agents:

### 🔍 Disease Detection Agent
- Extracts crop information
- Identifies symptoms
- Performs initial diagnosis

### 🩺 Diagnosis Agent
- Matches symptoms against disease knowledge
- Determines likely disease
- Estimates confidence level

### 💊 Treatment Agent
Provides:
- Organic treatments
- Biological control methods
- BARC-approved pesticides
- Safety recommendations

### 🌦️ Weather Analysis Agent
Analyzes:

- Temperature
- Humidity
- Rain probability

Then predicts disease outbreak risks and farming advisories.

### 📄 Report Agent
Generates a professional downloadable PDF report containing:

- Disease diagnosis
- Weather analysis
- Treatment plan
- Safety recommendations

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | Web Interface |
| Google Gemini 2.5 Flash | AI Reasoning |
| ReportLab | PDF Generation |
| Pillow | Image Processing |
| Requests | Weather API |
| Python-dotenv | Environment Variables |

---

# Project Structure

```
AgriGuardianAI/
│
├── app.py
├── orchestrator.py
├── agents.py
├── tools.py
├── security.py
├── pdf_generator.py
├── requirements.txt
├── .env.example
├── README.md
│
├── skills/
│   ├── disease_knowledge.py
│   ├── treatment_knowledge.py
│   └── weather_analysis.py
│
├── reports/
│
└── logs/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AgriGuardian-AI.git
```

Move into the project

```bash
cd AgriGuardian-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Get your Gemini API key from:

https://aistudio.google.com/app/apikey

---

# Run the Project

```bash
streamlit run app.py
```

The application will open automatically at

```
http://localhost:8501
```

---

# Demo Mode

If no Gemini API key is available, AgriGuardian AI automatically switches to **Demo Mode**, allowing users to explore the application using the built-in agricultural knowledge base without making external API calls.

---

# Security Features

The application includes multiple guardrails:

- Prompt Injection Detection
- Input Validation
- Image File Validation
- Security Event Logging
- Safe Agent Execution
- Restricted Chemical Recommendations

---

# Supported Crops

Examples include:

- 🌾 Rice
- 🥔 Potato
- 🍅 Tomato
- 🥬 Vegetables
- 🌽 Maize

---

# Outputs

The system generates:

- Disease diagnosis
- Disease confidence
- Treatment recommendations
- Weather analysis
- Disease outbreak risk
- Farmer safety instructions
- Professional PDF report

---

# Future Improvements

- Mobile Application
- Bengali Voice Assistant
- Satellite Image Integration
- Drone Image Analysis
- IoT Sensor Support
- Real-time Weather APIs
- Farmer Chatbot
- Disease Prediction Dashboard

---

# Requirements

Major dependencies:

```
streamlit
google-adk
mcp
reportlab
python-dotenv
requests
pillow
pytest
```

Install all dependencies using

```bash
pip install -r requirements.txt
```

---

# Screenshots

<img width="1907" height="332" alt="Screenshot 2026-07-02 234843" src="https://github.com/user-attachments/assets/160ffbc7-02c5-4253-bd4d-c4cfbd96171c" />
<img width="1915" height="908" alt="Screenshot 2026-07-02 234940" src="https://github.com/user-attachments/assets/6d0d1527-0028-4516-ad7a-d40676bbd666" />
<img width="1507" height="903" alt="image" src="https://github.com/user-attachments/assets/cb1b7c89-8529-4234-b270-0ba465e224a5" />
<img width="1411" height="834" alt="Screenshot 2026-07-02 235104" src="https://github.com/user-attachments/assets/c17cf320-b5ea-4386-a88c-f6e00bce4d18" />
<img width="1443" height="789" alt="Screenshot 2026-07-02 235203" src="https://github.com/user-attachments/assets/893a91e1-eaec-4271-876e-cc4f194d87ba" />

# Demo Video

https://github.com/user-attachments/assets/66417c20-0813-4823-bba4-5d84b706b2cf


# Author

**Taifur Rahman**

B.Sc. in Computer Science & Engineering

Daffodil International University

Bangladesh

GitHub:
https://github.com/mr-taifur

---

# Acknowledgements

- Google Gemini AI
- Streamlit
- Bangladesh Agricultural Research Council (BARC)
- Python Open Source Community

---

# License

This project is intended for educational and research purposes.

MIT License

---

⭐ If you found this project useful, please consider giving it a star!
