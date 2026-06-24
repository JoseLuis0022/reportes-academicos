const API = "http://localhost:8001";

document.getElementById("provider").addEventListener("change", (e) => {
  document.getElementById("model").value =
    e.target.value === "ollama" ? "gemma3:4b" : "openai/gpt-4o-mini";
});

document.getElementById("send").addEventListener("click", async () => {
  const body = {
    message: document.getElementById("message").value,
    provider: document.getElementById("provider").value,
    model: document.getElementById("model").value,
  };
  document.getElementById("reply").textContent = "Generando...";
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  document.getElementById("reply").textContent = data.reply || data.error;
  document.getElementById("metrics").textContent = JSON.stringify(data.metrics, null, 2);
});
