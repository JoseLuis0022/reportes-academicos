const API = "http://localhost:8000";
let profiles = {};

async function loadProfiles() {
  const res = await fetch(`${API}/profiles`);
  profiles = await res.json();
  const select = document.getElementById("profile");
  select.innerHTML = "";
  for (const [key, p] of Object.entries(profiles)) {
    const opt = document.createElement("option");
    opt.value = key;
    opt.textContent = p.label;
    select.appendChild(opt);
  }
  document.getElementById("systemPrompt").value = profiles[select.value].system_prompt;
}

document.getElementById("loadTemplate").addEventListener("click", () => {
  const key = document.getElementById("profile").value;
  document.getElementById("systemPrompt").value = profiles[key].system_prompt;
});

document.getElementById("profile").addEventListener("change", (e) => {
  document.getElementById("systemPrompt").value = profiles[e.target.value].system_prompt;
});

document.getElementById("send").addEventListener("click", async () => {
  const body = {
    message: document.getElementById("message").value,
    copilot_profile: document.getElementById("profile").value,
    system_prompt: document.getElementById("systemPrompt").value,
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

loadProfiles();
