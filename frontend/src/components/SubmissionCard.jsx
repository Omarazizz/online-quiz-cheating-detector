function SubmissionCard({ event }) {
  const { submission, flags, risk_score } = event;

  return (
    <article>
      <h3>Student {submission.student_id}</h3>

      <p>Question: {submission.question_id}</p>

      <p>Answer: {submission.answer}</p>

      <p>Time taken: {submission.time_taken} seconds</p>

      <p>
        Risk score: <strong>{risk_score}/100</strong>
      </p>

      {flags.length > 0 ? (
        <div>
          <strong>Cheating flags:</strong>

          {flags.map((flag) => (
            <p key={flag.id}>
              {flag.reason} — Rule score: {flag.score}
            </p>
          ))}
        </div>
      ) : (
        <p>No suspicious behavior detected.</p>
      )}
    </article>
  );
}

export default SubmissionCard;