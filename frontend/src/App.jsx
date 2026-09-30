import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const languages = [
  { code: "en", name: "English" },
  { code: "te", name: "Telugu" },
  { code: "hi", name: "Hindi" },
  { code: "ta", name: "Tamil" },
  { code: "es", name: "Spanish" },
];

function App() {
  const [text, setText] = useState("");
  const [translation, setTranslation] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [targetLanguage, setTargetLanguage] = useState("te");
  const [loading, setLoading] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const [error, setError] = useState("");

  const handleTranslate = async () => {
    if (!text.trim()) {
      setError("Please enter some text to translate.");
      setTranslation("");
      return;
    }

    setLoading(true);
    setError("");
    setTranslation("");

    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text.trim(),
          source_language: sourceLanguage,
          target_language: targetLanguage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Translation failed.");
      }

      setTranslation(data.translated_text);
    } catch (err) {
      setError(
        err.message || "Unable to connect to the translation service."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSwap = () => {
    setSourceLanguage(targetLanguage);
    setTargetLanguage(sourceLanguage);
    setText(translation);
    setTranslation("");
    setError("");
  };

  const handleCopy = async () => {
    if (!translation) return;

    try {
      await navigator.clipboard.writeText(translation);
      alert("Translation copied!");
    } catch {
      setError("Could not copy the translation.");
    }
  };

  const handleSpeak = async () => {
    if (!translation) return;

    setAudioLoading(true);
    setError("");

    try {
      const params = new URLSearchParams({
        text: translation,
        language: targetLanguage,
      });

      const response = await fetch(`${API_URL}/tts?${params.toString()}`, {
        method: "POST",
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail || "Unable to generate audio.");
      }

      const audioBlob = await response.blob();

      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
      };

      await audio.play();
    } catch (err) {
      setError(
        err.message ||
          "Unable to generate speech. Please try again."
      );
    } finally {
      setAudioLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Language Translation Tool</h1>
          <p>Translate text quickly and easily</p>
        </div>
      </header>

      <main className="container">
        <section className="translator-card">
          <div className="language-row">
            <div className="language-box">
              <label>From</label>

              <select
                value={sourceLanguage}
                onChange={(e) => setSourceLanguage(e.target.value)}
              >
                {languages.map((language) => (
                  <option
                    key={language.code}
                    value={language.code}
                  >
                    {language.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="swap-button"
              onClick={handleSwap}
              title="Swap languages"
            >
              ⇄
            </button>

            <div className="language-box">
              <label>To</label>

              <select
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
              >
                {languages.map((language) => (
                  <option
                    key={language.code}
                    value={language.code}
                  >
                    {language.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="translation-area">
            <div className="input-section">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to translate..."
                maxLength={5000}
              />

              <div className="character-count">
                {text.length}/5000
              </div>
            </div>

            <div className="output-section">
              {translation ? (
                <p className="translation-text">
                  {translation}
                </p>
              ) : (
                <p className="placeholder-text">
                  Your translation will appear here...
                </p>
              )}
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <div className="actions">
            <button
              className="translate-button"
              onClick={handleTranslate}
              disabled={loading}
            >
              {loading ? "Translating..." : "Translate"}
            </button>

            <button
              className="copy-button"
              onClick={handleCopy}
              disabled={!translation}
            >
              Copy
            </button>

            <button
              className="speak-button"
              onClick={handleSpeak}
              disabled={!translation || audioLoading}
            >
              {audioLoading ? "🔊 Loading..." : "🔊 Listen"}
            </button>
          </div>
        </section>

        <section className="info-section">
          <h2>Supported Languages</h2>

          <div className="language-list">
            {languages.map((language) => (
              <span
                key={language.code}
                className="language-tag"
              >
                {language.name}
              </span>
            ))}
          </div>
        </section>
      </main>

      <footer>
        <p>Language Translation Tool • React + FastAPI</p>
      </footer>
    </div>
  );
}

export default App;