export default function RiskBadge({ risk }) {

  if (!risk) return null;

  let color = "success";
  let message = "SAFE TO CONTINUE";

  if (risk === "MEDIUM") {

    color = "warning";
    message = "NEEDS ATTENTION";

  }

  if (risk === "HIGH") {

    color = "danger";
    message = "STOP WORK IMMEDIATELY";

  }

  return (

    <div className="card shadow mt-4">

      <div className="card-body text-center">

        <h3>Overall Risk</h3>

        <span
          className={`badge bg-${color} fs-3 px-4 py-3`}
        >
          {risk}
        </span>

        <h5 className="mt-3">

          {message}

        </h5>

      </div>

    </div>

  );

}