import ReactMarkdown from "react-markdown";

export default function Report({ report }) {

  if (!report) return null;

  const downloadReport = () => {

    const blob = new Blob(
      [report],
      { type: "text/plain" }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Safety_Report.txt";

    a.click();

    URL.revokeObjectURL(url);

  };

  return (

    <div className="card shadow mt-4 mb-5">

      <div className="card-body">

        <div className="d-flex justify-content-between">

          <h3>📄 AI Safety Report</h3>

          <button
            className="btn btn-success"
            onClick={downloadReport}
          >
            📥 Download Report
          </button>

        </div>

        <hr />

        <ReactMarkdown>

          {report}

        </ReactMarkdown>

      </div>

    </div>

  );

}