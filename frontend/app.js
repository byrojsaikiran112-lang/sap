let selectedMode = "study_plan";
let lastGenerationId = null;
let selectedRating = 0;

const $ = (id) => document.getElementById(id);
const modeButtons = document.querySelectorAll("[data-mode]");

modeButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    selectedMode = btn.dataset.mode;
    modeButtons.forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
  });
});

$("learnForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("resultStatus").innerHTML = '<span class="sparkle">✦</span><div><b>Creating your personalized result...</b><small>LearnSphere is thinking.</small></div>';
  $("output").classList.add("loading");
  $("output").textContent = "Generating your learning content...";
  $("generateBtn").disabled = true;
  $("feedback").classList.add("hidden");

  const payload = {
    student_name: $("student_name").value,
    course: $("course").value,
    topic: $("topic").value,
    level: $("level").value,
    goal: $("goal").value,
    study_time: $("study_time").value,
    mode: selectedMode
  };

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Generation failed");
    lastGenerationId = data.generation_id;
    $("output").textContent = data.output;
    $("resultStatus").innerHTML = '<span class="sparkle">✓</span><div><b>Your learning content is ready!</b><small>Generated and personalized for your topic.</small></div>';
    $("feedback").classList.remove("hidden");
    loadHistory();
  } catch (err) {
    $("output").innerHTML = `<p class="error">${escapeHtml(err.message)}</p>`;
    $("resultStatus").innerHTML = '<span class="sparkle">!</span><div><b>Something went wrong</b><small>Check your API configuration and try again.</small></div>';
  } finally {
    $("output").classList.remove("loading");
    $("generateBtn").disabled = false;
  }
});

$("copyBtn").addEventListener("click", async () => {
  await navigator.clipboard.writeText($("output").innerText);
  $("copyBtn").textContent = "✓";
  setTimeout(() => $("copyBtn").textContent = "⧉", 1200);
});

document.querySelectorAll("#stars button").forEach(btn => {
  btn.addEventListener("click", () => {
    selectedRating = Number(btn.dataset.rating);
    document.querySelectorAll("#stars button").forEach(b =>
      b.classList.toggle("active", Number(b.dataset.rating) <= selectedRating)
    );
  });
});

$("sendFeedback").addEventListener("click", async () => {
  if (!lastGenerationId || !selectedRating) return alert("Please select a rating.");
  const res = await fetch("/api/feedback", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      generation_id: lastGenerationId,
      rating: selectedRating,
      comment: $("feedbackComment").value
    })
  });
  if (res.ok) {
    $("sendFeedback").textContent = "Saved ✓";
    setTimeout(() => $("sendFeedback").textContent = "Submit", 1200);
  }
});

$("refreshHistory").addEventListener("click", loadHistory);

async function loadHistory() {
  try {
    const res = await fetch("/api/history");
    const data = await res.json();
    if (!data.items.length) {
      $("history").innerHTML = '<p class="muted">No learning sessions yet. Your generated content will appear here.</p>';
      return;
    }
    $("history").innerHTML = data.items.map(item => `
      <div class="history-item">
        <div class="history-title">${escapeHtml(item.topic)} · ${escapeHtml(item.mode)}</div>
        <div class="history-meta">${escapeHtml(item.student_name)} · ${escapeHtml(item.course)} · ${escapeHtml(item.created_at)}</div>
        <div class="history-output">${escapeHtml(item.output)}</div>
      </div>
    `).join("");
  } catch {
    $("history").innerHTML = '<p class="error">Could not load history.</p>';
  }
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
  }[c]));
}

loadHistory();
