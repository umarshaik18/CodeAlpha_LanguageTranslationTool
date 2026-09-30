# 🌐 Language Translation Tool
Live Demo : code-alpha-language-translation-too-lovat.vercel.app
<p>
backend : https://codealpha-languagetranslationtool-yc9h.onrender.com
<p>
A full-stack web application that translates text between multiple languages and provides audio pronunciation for translated text.

## 🚀 Features

- 🌍 Translate text between multiple languages
- 🇬🇧 English
- 🇮🇳 Telugu
- 🇮🇳 Hindi
- 🇮🇳 Tamil
- 🇪🇸 Spanish
- 🔄 Swap source and target languages
- 📋 Copy translated text
- 🔊 Listen to translated text using Text-to-Speech
- 📱 Responsive and mobile-friendly UI
- ⚡ FastAPI backend
- ⚛️ React frontend
- 🛡️ Input validation and error handling

## 🛠️ Technologies Used

### Frontend
- React
- Vite
- JavaScript
- HTML
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- HTTPX

### Translation
- Google Translate through `deep-translator`
- MyMemory as a fallback translation service

### Text-to-Speech
- Google Text-to-Speech (`gTTS`)

## 📂 Project Structure

```text
LanguageTranslationTool/
│
├── backend/
│   ├── models/
│   │   └── translation.py
│   │
│   ├── services/
│   │   └── translator.py
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── .gitignore
└── README.md
