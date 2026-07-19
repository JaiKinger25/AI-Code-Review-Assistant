import { useState } from "react";
import API from "../services/api";
import Navbar from "../components/Navbar";

function Dashboard() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);

  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");

  const uploadAndReview = async () => {
    if (!file) {
      alert("Please select a Python (.py) file.");
      return;
    }

    setLoading(true);
    setMessage("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const upload = await API.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const filename = upload.data.filename;

      const review = await API.get(`/review/${filename}`);

      setResult(review.data);

      setHistory((prev) => [
        {
          filename,
          date: new Date().toLocaleString(),
        },
        ...prev,
      ]);

      setMessage("Review Completed Successfully!");
    } catch (err) {
      setMessage(
        err.response?.data?.message ||
          err.response?.data?.error ||
          "Something went wrong."
      );
    }

    setLoading(false);
  };

  const getPylintScore = () => {
    if (!result?.pylint) return "--";

    const report =
      typeof result.pylint === "string"
        ? result.pylint
        : result.pylint.report;

    const match = report.match(/rated at ([0-9.]+)\/10/);

    return match ? match[1] : "--";
  };

  const getSecurityCount = () => {
    if (!result?.bandit) return 0;

    if (typeof result.bandit === "string") return 0;

    return result.bandit.results?.length || 0;
  };

  const getComplexity = () => {
    try {
      const report =
        typeof result.radon === "string"
          ? JSON.parse(result.radon)
          : JSON.parse(result.radon.report);

      const key = Object.keys(report)[0];

      return report[key][0]?.rank || "--";
    } catch {
      return "--";
    }
  };

  const copyReview = () => {
    navigator.clipboard.writeText(
      result?.ai_review?.review || ""
    );

    alert("Copied!");
  };

  const downloadReview = () => {
    const blob = new Blob(
      [result?.ai_review?.review || ""],
      {
        type: "text/plain",
      }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = "AI_Review.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  const filteredHistory = history.filter((item) =>
    item.filename
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <>
      <Navbar />

      <div
        style={{
          maxWidth: "1100px",
          margin: "30px auto",
          padding: "20px",
          fontFamily: "Arial",
        }}
      >
        <h1>AI Code Review Dashboard</h1>

        <p>Upload a Python (.py) file for analysis.</p>

        <input
          type="text"
          placeholder="Search Upload History..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "20px",
          }}
        />

        <input
          type="file"
          accept=".py"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <button
          onClick={uploadAndReview}
          disabled={loading}
          style={{
            marginLeft: "15px",
            padding: "10px 20px",
          }}
        >
          {loading
            ? "Reviewing..."
            : "Upload & Review"}
        </button>
                {message && (
          <h3 style={{ color: "green", marginTop: "20px" }}>
            {message}
          </h3>
        )}

        {filteredHistory.length > 0 && (
          <div
            style={{
              marginTop: "30px",
              padding: "15px",
              border: "1px solid #ddd",
              borderRadius: "10px",
            }}
          >
            <h2>📂 Upload History</h2>

            {filteredHistory.map((item, index) => (
              <div
                key={index}
                style={{
                  padding: "8px 0",
                  borderBottom: "1px solid #eee",
                }}
              >
                📄 {item.filename} — {item.date}
              </div>
            ))}
          </div>
        )}

        {result && (
          <>
            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(200px,1fr))",
                gap: "20px",
                marginTop: "30px",
              }}
            >
              <div
                style={{
                  background: "#f5f5f5",
                  padding: "20px",
                  borderRadius: "10px",
                }}
              >
                <h4>📄 File</h4>
                <h2>{result.filename}</h2>
              </div>

              <div
                style={{
                  background: "#f5f5f5",
                  padding: "20px",
                  borderRadius: "10px",
                }}
              >
                <h4>Pylint Score</h4>
                <h2>{getPylintScore()} / 10</h2>
              </div>

              <div
                style={{
                  background: "#f5f5f5",
                  padding: "20px",
                  borderRadius: "10px",
                }}
              >
                <h4>Security Issues</h4>
                <h2>{getSecurityCount()}</h2>
              </div>

              <div
                style={{
                  background: "#f5f5f5",
                  padding: "20px",
                  borderRadius: "10px",
                }}
              >
                <h4>Complexity</h4>
                <h2>{getComplexity()}</h2>
              </div>
            </div>

            <div style={{ marginTop: "20px" }}>
              <button
                onClick={copyReview}
                style={{
                  padding: "10px 20px",
                  marginRight: "10px",
                }}
              >
                📋 Copy AI Review
              </button>

              <button
                onClick={downloadReview}
                style={{
                  padding: "10px 20px",
                }}
              >
                📥 Download AI Review
              </button>
            </div>

            <div
              style={{
                marginTop: "30px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                padding: "20px",
              }}
            >
              <h2>✅ Pylint Report</h2>

              <pre style={{ whiteSpace: "pre-wrap" }}>
                {typeof result.pylint === "string"
                  ? result.pylint
                  : result.pylint.report}
              </pre>

              <hr />

              <h2>🔒 Bandit Report</h2>

              <pre style={{ whiteSpace: "pre-wrap" }}>
                {typeof result.bandit === "string"
                  ? result.bandit
                  : JSON.stringify(result.bandit, null, 2)}
              </pre>

              <hr />

              <h2>📊 Radon Report</h2>

              <pre style={{ whiteSpace: "pre-wrap" }}>
                {typeof result.radon === "string"
                  ? result.radon
                  : result.radon.report}
              </pre>

              <hr />

              <h2>🤖 AI Review</h2>

              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  background: "#fafafa",
                  padding: "20px",
                  borderRadius: "8px",
                }}
              >
                {result.ai_review?.review}
              </pre>
                            <p
                style={{
                  marginTop: "15px",
                  color: "#666",
                }}
              >
                Source: {result.ai_review?.source}
              </p>

            </div>
          </>
        )}
      </div>
    </>
  );
}

export default Dashboard;