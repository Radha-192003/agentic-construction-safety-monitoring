export default function UploadSection({
  file,
  setFile,
  preview,
  setPreview,
  detectSafety,
}) {
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) return;

    setFile(selectedFile);

    // Create a reliable preview
    const reader = new FileReader();

    reader.onload = () => {
      setPreview(reader.result);
    };

    reader.readAsDataURL(selectedFile);
  };

  return (
    <div className="card shadow p-4">

      <h3 className="mb-4 text-center">
        Upload Construction Image / Video
      </h3>

      <div className="d-flex justify-content-center gap-3">

        <input
          type="file"
          className="form-control"
          accept="image/*,video/*"
          style={{ maxWidth: "350px" }}
          onChange={handleFileChange}
        />

        <button
          className="btn btn-primary"
          onClick={detectSafety}
          disabled={!file}
        >
          Detect Safety
        </button>

      </div>

      {file && (
        <p className="text-center mt-3 mb-0">
          Selected: <strong>{file.name}</strong>
        </p>
      )}

    </div>
  );
}