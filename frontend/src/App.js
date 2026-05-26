import React, { useState } from "react";
import "./App.css";

function App() {
  const [started, setStarted] = useState(false);
  const [mode, setMode] = useState("");
  const [pincode, setPincode] = useState("");
  const [stores, setStores] = useState([]);

  const searchByPincodeWithValue = async (pin) => {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const userLat = position.coords.latitude;
      const userLon = position.coords.longitude;

      const response = await fetch("http://127.0.0.1:8000/search-by-pincode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pincode: pin,
          user_lat: userLat,
          user_lon: userLon,
        }),
      });

      const data = await response.json();
      setStores(data.stores || []);
    });
  };

  const searchByPincode = async () => {
    searchByPincodeWithValue(pincode);
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported. Please use Chrome.");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      const detectedPincode = spokenText.replace(/\D/g, "");

      if (detectedPincode.length === 6) {
        setPincode(detectedPincode);
        searchByPincodeWithValue(detectedPincode);
      } else {
        alert("Could not detect valid pincode");
      }
    };

    recognition.onerror = () => {
      alert("Voice recognition failed");
    };
  };

  return (
    <div className="app">
      {!started ? (
        <div className="landing-page">
          <div className="landing-shape1">+</div>
          <div className="landing-shape2">○</div>
          <div className="landing-shape3">+</div>
          <div className="landing-shape4">○</div>
          <div className="landing-shape5">○</div>
          <div className="landing-shape6">+</div>

          <img src="/images/bee.jpg" alt="Bee" className="bee-img" />

          <h1 className="landing-title">MediBee</h1>

          <p className="landing-tagline">
            Find medical stores near you,
            <br />
            fast, easy & reliable.
          </p>

          <img
            src="/images/illustration.jpg"
            alt="Medical Illustration"
            className="landing-illustration"
          />

          <button
            className="get-started-btn"
            onClick={() => setStarted(true)}
          >
            Find Stores Near Me
          </button>
        </div>
      ) : (
        <div className="main-page">

          <div className="main-shape1">💉</div>
          <div className="main-shape2">💊</div>
          <div className="main-shape3">🏥</div>

          <h1 className="main-title">MediBee</h1>

          <p className="subtitle">
            Find nearby medical stores using text or voice
          </p>

          <button
            className="back-btn"
            onClick={() => {
              setStarted(false);
              setMode("");
              setStores([]);
              setPincode("");
            }}
          >
            ← Back to Home
          </button>

          <div className="buttons">
            <button onClick={() => setMode("type")}>
              Type Pincode
            </button>

            <button onClick={() => setMode("speak")}>
              Speak Pincode
            </button>
          </div>

          {mode === "type" && (
            <div className="search-box">
              <input
                type="text"
                placeholder="Enter pincode"
                value={pincode}
                onChange={(e) => setPincode(e.target.value)}
              />

              <button onClick={searchByPincode}>
                Search
              </button>
            </div>
          )}

          {mode === "speak" && (
            <div className="voice-box">
              <p>Click below and say your pincode</p>

              <button onClick={startListening}>
                🎤 Start Speaking
              </button>

              {pincode && (
                <p>
                  Detected Pincode:
                  <strong> {pincode}</strong>
                </p>
              )}
            </div>
          )}

          <div className="results">
            {stores.map((store, index) => (
              <div className="card" key={index}>
                <h3>{store.name}</h3>

                <p>{store.address}</p>

                <p>
                  <strong>Distance:</strong> {store.distance_km} km away
                </p>

                <a
                  href={store.map_link}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open in Google Maps
                </a>
              </div>
            ))}
          </div>

        </div>
      )}
    </div>
  );
}

export default App;