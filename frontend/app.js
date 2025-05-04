let selectedRatio = 1.33;
const dropArea = document.getElementById("drop-area");
const fileList = document.getElementById("file-list");

let filesToUpload = [];

// Ratio selector
document.querySelectorAll(".capsule").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".capsule").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedRatio = parseFloat(btn.getAttribute("data-ratio"));
  });
});

// Handle drop
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.classList.add("highlight");
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.classList.remove("highlight");

  const files = e.dataTransfer.files;
  for (const file of files) {
    addFileRow(file);
    filesToUpload.push(file);
  }
});

// Display file info
function addFileRow(file) {
  const row = fileList.insertRow();
  row.insertCell(0).innerText = file.name;
  row.insertCell(1).innerText = (file.size / (1024 * 1024)).toFixed(1) + "Mo";
  row.insertCell(2).innerText = "—"; // will be updated later with real date
  row.insertCell(3).innerText = "4:3"; // placeholder for ratio
  const statusCell = row.insertCell(4);
  statusCell.innerText = "⬜️"; // unchecked initially
}

// Stretch action
document.getElementById("stretch-btn").addEventListener("click", async () => {
  for (let i = 0; i < filesToUpload.length; i++) {
    const formData = new FormData();
    formData.append("file", filesToUpload[i]);
    formData.append("ratio", selectedRatio);

    try {
      const response = await fetch("http://localhost:8000/stretch", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (response.ok) {
        fileList.rows[i].cells[2].innerText = result.date;
        fileList.rows[i].cells[4].innerText = "✅";
      } else {
        fileList.rows[i].cells[4].innerText = "❌";
      }

    } catch (error) {
      console.error("Stretch error:", error);
      fileList.rows[i].cells[4].innerText = "❌";
    }
  }
});
