import { useState } from "react";

function SubmissionForm() {
  const [studentId, setStudentId] = useState("");
  const [questionId, setQuestionId] = useState("");
  const [answer, setAnswer] = useState("");
  const [timeTaken, setTimeTaken] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const response = await fetch(
      "http://127.0.0.1:8000/api/submissions",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: studentId,
          question_id: questionId,
          answer,
          time_taken: Number(timeTaken),
        }),
      }
    );

    if (!response.ok) {
      alert("Submission failed");
      return;
    }

    setStudentId("");
    setQuestionId("");
    setAnswer("");
    setTimeTaken("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Simulate Quiz Submission</h2>

      <input
        type="text"
        placeholder="Student ID"
        value={studentId}
        onChange={(event) => setStudentId(event.target.value)}
        required
      />

      <input
        type="text"
        placeholder="Question ID"
        value={questionId}
        onChange={(event) => setQuestionId(event.target.value)}
        required
      />

      <input
        type="text"
        placeholder="Answer"
        value={answer}
        onChange={(event) => setAnswer(event.target.value)}
        required
      />

      <input
        type="number"
        step="0.1"
        placeholder="Time taken (seconds)"
        value={timeTaken}
        onChange={(event) => setTimeTaken(event.target.value)}
        required
      />

      <button type="submit">
        Submit Answer
      </button>
    </form>
  );
}

export default SubmissionForm;