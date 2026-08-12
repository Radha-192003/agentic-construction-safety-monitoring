export default function SummaryCards({ detections }) {

  if (!detections) return null;

  return (

    <div className="card shadow mt-5 p-4">

      <h3 className="text-center mb-4">
        Detection Summary
      </h3>

      <div className="row">

        {Object.entries(detections).map(([name, count]) => (

          <div className="col-md-3 mb-3" key={name}>

            <div
              className="card text-center border-0 shadow-sm"
            >

              <div className="card-body">

                <h5>{name}</h5>

                <h2
                  className="text-primary"
                >
                  {count}
                </h2>

              </div>

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}