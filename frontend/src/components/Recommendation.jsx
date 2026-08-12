import ReactMarkdown from "react-markdown";

export default function Recommendation({ recommendation }) {
  if (!recommendation) return null;

  return (
    <div className="card shadow mt-5">
      <div className="card-body">
        <h3>🤖 AI Safety Recommendation</h3>

        <ReactMarkdown>
          {recommendation}
        </ReactMarkdown>
      </div>
    </div>
  );
}