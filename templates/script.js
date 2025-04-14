const BASE_URL = "http://127.0.0.1:5000";

// === Search by Title ===
async function searchByTitle() {
  const title = document.getElementById("titleInput").value;
  const resultsList = document.getElementById("titleResults");
  resultsList.innerHTML = "";

  if (!title) return;

  try {
    const res = await fetch(`${BASE_URL}/recommend?title=${encodeURIComponent(title)}`);
    const data = await res.json();

    const messageItem = document.createElement("li");
    messageItem.textContent = data.message;
    resultsList.appendChild(messageItem);

    if (data.recommendations && data.recommendations.length > 0) {
      data.recommendations.forEach(movie => {
        const li = document.createElement("li");
        li.textContent = movie;
        resultsList.appendChild(li);
      });
    }
  } catch (err) {
    console.error("Error fetching title recommendations:", err);
    resultsList.innerHTML = "<li>Failed to fetch recommendations.</li>";
  }
}

// === Search by Preferences ===
async function searchByPreferences() {
  const genres = document.getElementById("genresInput").value.split(",").map(s => s.trim()).filter(Boolean);
  const actors = document.getElementById("actorsInput").value.split(",").map(s => s.trim()).filter(Boolean);
  const directors = document.getElementById("directorsInput").value.split(",").map(s => s.trim()).filter(Boolean);
  const resultsList = document.getElementById("prefResults");
  resultsList.innerHTML = "";

  try {
    const res = await fetch(`${BASE_URL}/recommend/preferences`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ genres, actors, directors })
    });

    const data = await res.json();

    const messageItem = document.createElement("li");
    messageItem.textContent = data.message;
    resultsList.appendChild(messageItem);

    if (data.recommendations && data.recommendations.length > 0) {
      data.recommendations.forEach(movie => {
        const li = document.createElement("li");
        li.textContent = movie;
        resultsList.appendChild(li);
      });
    }
  } catch (err) {
    console.error("Error fetching preference recommendations:", err);
    resultsList.innerHTML = "<li>Failed to fetch recommendations.</li>";
  }
}

// === Search by Category ===
async function searchByCategory() {
  const category = document.getElementById("categorySelect").value;
  const keyword = document.getElementById("keywordInput").value;
  const resultsList = document.getElementById("catResults");
  resultsList.innerHTML = "";

  if (!keyword) return;

  try {
    const res = await fetch(`${BASE_URL}/search?category=${encodeURIComponent(category)}&keyword=${encodeURIComponent(keyword)}`);
    const data = await res.json();

    const messageItem = document.createElement("li");
    messageItem.textContent = data.message;
    resultsList.appendChild(messageItem);

    const items = data.recommendations || data.results || [];
    if (items.length > 0) {
      items.forEach(movie => {
        const li = document.createElement("li");
        li.textContent = movie;
        resultsList.appendChild(li);
      });
    }
  } catch (err) {
    console.error("Error fetching category search:", err);
    resultsList.innerHTML = "<li>Failed to fetch results.</li>";
  }
}
