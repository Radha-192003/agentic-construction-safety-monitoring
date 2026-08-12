export default function LoadingSpinner() {
  return (
    <div className="text-center my-5">

      <div
        className="spinner-border text-primary"
        style={{ width: "4rem", height: "4rem" }}
      ></div>

      <h4 className="mt-3">
        AI is analyzing image...
      </h4>

    </div>
  );
}