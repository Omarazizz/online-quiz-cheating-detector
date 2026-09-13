import { useEffect, useState } from "react";
import "./App.css";
import SubmissionCard from "./components/SubmissionCard";
import SubmissionForm from "./components/SubmissionForm";

function App() {
  const [submissions, setSubmissions] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("connecting");

  useEffect(() => {
    async function loadHistory() {
      const response = await fetch(
        "http://127.0.0.1:8000/api/submissions/recent"
      );

      if (response.ok) {
        const data = await response.json();
        setSubmissions(data);
      }
    }

    loadHistory();

    const socket = new WebSocket(
      "ws://127.0.0.1:8000/ws/submissions"
    );

    socket.onopen = () => {
      setConnectionStatus("live");
    };

    socket.onclose = () => {
      setConnectionStatus("disconnected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "new_submission") {
        setSubmissions((current) => [
          data,
          ...current,
        ]);
      }
    };

    return () => {
      socket.close();
    };
  }, []);

  return (
    <main className="dashboard">
      <header>
        <h1>Online Quiz Cheating Detector</h1>

        <p>
          Connection:
          <strong> {connectionStatus}</strong>
        </p>
      </header>

      <SubmissionForm />

      <section>
        <h2>Recent Quiz Submissions</h2>

        {submissions.length === 0 ? (
          <p>No submissions yet.</p>
        ) : (
          submissions.map((event) => (
            <SubmissionCard
              key={event.submission.id}
              event={event}
            />
          ))
        )}
      </section>
    </main>
  );
}

export default App;