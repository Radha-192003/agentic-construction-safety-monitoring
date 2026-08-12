export default function ImageComparison({
  preview,
  result,
}) {
  if (!preview || !result) return null;

  const downloadImage = async () => {
    try {
      const response = await fetch(result.output_image);

      if (!response.ok) {
        throw new Error("Failed to fetch detection image");
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = "AI_Detection_Result.jpg";

      document.body.appendChild(a);

      a.click();

      document.body.removeChild(a);

      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error("Download failed:", error);
      alert("Unable to download image.");
    }
  };

  return (
    <div className="row mt-4">

      {/* Original Image */}
      <div className="col-md-6 text-center">

        <div className="card shadow p-3">

          <h4 className="mb-3">
            Original Image
          </h4>

          <img
            src={preview}
            alt="Original Construction"
            className="img-fluid rounded"
            style={{
              maxHeight: "500px",
              objectFit: "contain",
            }}
          />

        </div>

      </div>


      {/* AI Detection */}
      <div className="col-md-6 text-center">

        <div className="card shadow p-3">

          <h4 className="mb-3">
            AI Detection
          </h4>

          <img
            src={result.output_image}
            alt="AI Detection"
            className="img-fluid rounded"
            style={{
              maxHeight: "500px",
              objectFit: "contain",
            }}
          />

          <button
            className="btn btn-primary mt-3"
            onClick={downloadImage}
          >
            📥 Download Detection Image
          </button>

        </div>

      </div>

    </div>
  );
}