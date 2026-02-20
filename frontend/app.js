const apiUrlInput = document.getElementById("api-url");
const textInput = document.getElementById("text-input");
const validateBtn = document.getElementById("validate-btn");
const statusEl = document.getElementById("status");
const resultsSummaryEl = document.getElementById("results-summary");
const resultsListEl = document.getElementById("results-list");

function setStatus(message, type = "") {
  statusEl.textContent = message || "";
  statusEl.className = "status" + (type ? " " + type : "");
}

function createConfidencePill(confidence) {
  const span = document.createElement("span");
  span.classList.add("pill");

  const level = (confidence || "").toLowerCase();
  if (level === "high") {
    span.classList.add("pill-high");
  } else if (level === "medium") {
    span.classList.add("pill-medium");
  } else {
    span.classList.add("pill-low");
  }

  span.textContent = confidence || "Unknown";
  return span;
}

function renderResults(data) {
  const { validated, claims = [], message } = data || {};

  if (!claims.length) {
    resultsSummaryEl.textContent =
      message || "No claims returned. Try a different input.";
    resultsListEl.innerHTML = "";
    return;
  }

  const strongCount = claims.filter((c) =>
    ["High", "Medium"].includes(c.confidence)
  ).length;

  const summaryParts = [];
  summaryParts.push(
    `Overall validated: ${validated ? "true ✅" : "false ⚠️"}`
  );
  summaryParts.push(`Claims found: ${claims.length}`);
  summaryParts.push(`Strong evidence (High/Medium): ${strongCount}`);

  resultsSummaryEl.textContent =
    (message ? message + " • " : "") + summaryParts.join(" • ");

  resultsListEl.innerHTML = "";

  claims.forEach((claimObj, index) => {
    const item = document.createElement("div");
    item.className = "result-item";

    const header = document.createElement("div");
    header.className = "result-header";

    const claimText = document.createElement("div");
    claimText.className = "claim-text";
    claimText.textContent = `${index + 1}. ${claimObj.claim || ""}`;

    const pill = createConfidencePill(claimObj.confidence);

    header.appendChild(claimText);
    header.appendChild(pill);

    const metaRow = document.createElement("div");
    metaRow.className = "meta-row";
    const score = document.createElement("span");
    score.textContent = `Similarity: ${
      typeof claimObj.similarity_score === "number"
        ? claimObj.similarity_score.toFixed(3)
        : "0.000"
    }`;
    metaRow.appendChild(score);

    const snippet = document.createElement("div");
    snippet.className = "snippet";
    if (claimObj.best_match_snippet) {
      snippet.textContent = `Evidence: ${claimObj.best_match_snippet}`;
    } else {
      snippet.textContent = "Evidence: (no strong snippet found)";
    }

    const urlDiv = document.createElement("div");
    urlDiv.className = "url";
    if (claimObj.best_match_url) {
      const a = document.createElement("a");
      a.href = claimObj.best_match_url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = "Open source";
      urlDiv.appendChild(a);
    }

    item.appendChild(header);
    item.appendChild(metaRow);
    item.appendChild(snippet);
    if (claimObj.best_match_url) {
      item.appendChild(urlDiv);
    }

    resultsListEl.appendChild(item);
  });
}

async function handleValidate() {
  const apiUrl = apiUrlInput.value.trim();
  const text = textInput.value.trim();

  if (!apiUrl) {
    setStatus("Please provide the API URL.", "error");
    return;
  }

  if (!text) {
    setStatus("Please enter some text to validate.", "error");
    return;
  }

  validateBtn.disabled = true;
  setStatus("Validating claims...", "success");

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `API error (${response.status}): ${errorText || response.statusText}`
      );
    }

    const data = await response.json();
    renderResults(data);
    setStatus("Validation complete.", "success");
  } catch (err) {
    console.error(err);
    setStatus(
      `Failed to validate: ${err.message}. Is the backend running at the API URL?`,
      "error"
    );
    resultsSummaryEl.textContent = "";
    resultsListEl.innerHTML = "";
  } finally {
    validateBtn.disabled = false;
  }
}

validateBtn.addEventListener("click", handleValidate);

// Allow Ctrl+Enter to submit
textInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
    handleValidate();
  }
});

