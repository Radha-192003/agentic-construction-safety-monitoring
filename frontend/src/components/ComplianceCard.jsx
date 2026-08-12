export default function ComplianceCard({ detections }) {

  if (!detections) return null;

  const persons = detections.Person || 0;

  const helmet = detections.Hardhat || 0;

  const vest = detections["Safety Vest"] || 0;

  const mask = detections.Mask || 0;

  let score = 100;

  if (persons > 0) {

    score =
      (
        (helmet + vest + mask) /
        (persons * 3)
      ) * 100;

    score = Math.round(score);

  }

  return (

    <div className="card shadow mt-4">

      <div className="card-body text-center">

        <h4>Compliance Score</h4>

        <h1 className="text-success">

          {score}%

        </h1>

      </div>

    </div>

  );

}