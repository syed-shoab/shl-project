const apiBaseURL = "https://shl-assessment-api.onrender.com";
const searchBtn = document.getElementById("searchBtn");
const queryInput = document.getElementById("queryInput");
const resultSection = document.getElementById("resultSection");

searchBtn.addEventListener("click", async () => {
  const query = queryInput.value.trim();
  if (!query) {
    alert("Please enter a query");
    return;
  }

  const url = `${apiBaseURL}/recommend?q=${encodeURIComponent(query)}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to fetch recommendations");
    }
    const data = await response.json();
    displayResults(data);
  } catch (error) {
    console.error(error);
    alert("Error fetching recommendations");
  }
});

function displayResults(data) {
  const tableHTML = `
    <table>
      <tr>
        <th>Assessment Name</th>
        <th>Remote Support</th>
        <th>Adaptive Support</th>
        <th>Duration</th>
        <th>Test Type</th>
      </tr>
      ${data.map((item) => `
        <tr>
          <td><a href="${item.assessment_url}" target="_blank">${item.assessment_name}</a></td>
          <td>${item.remote_support}</td>
          <td>${item.adaptive_support}</td>
          <td>${item.duration}</td>
          <td>${item.test_type}</td>
        </tr>
      `).join("")}
    </table>
  `;
  resultSection.innerHTML = tableHTML;
}