
const dateElement = document.getElementById("date");
const today = new Date();

dateElement.textContent = today.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric"
});


const fileInput = document.getElementById("fileInput");
const uploadBox = document.getElementById("upload-box");
const fileList = document.getElementById("fileList");
const extractResults = document.getElementById("extract-results");

const pageUpload = document.getElementById("page-upload");
const pageAssignments = document.getElementById("page-assignments");

const startBtn = document.getElementById("startBtn");
const backBtn = document.getElementById("backBtn");
const generateBtn = document.getElementById("generateBtn");


let extractedAssignments = [];


uploadBox.addEventListener("click", () => fileInput.click());


fileInput.addEventListener("change", () => {
    fileList.innerHTML = "";
    extractResults.innerHTML = "";

    const file = fileInput.files[0];
    if (!file) return;

    const li = document.createElement("li");
    li.textContent = file.name;
    fileList.appendChild(li);

    
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/upload", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            extractResults.innerHTML = `<p style="color:green;">✓ File processed successfully!</p>`;

            if (data.assignments.length === 0) {
                extractResults.innerHTML += `<p>No assignments found.</p>`;
            }

            extractedAssignments = data.assignments;

            data.assignments.forEach(a => {
                extractResults.innerHTML += `
                    <li><strong>${a.title}</strong> — Due: ${a.due}</li>
                `;
            });
        })
        .catch(err => {
            extractResults.innerHTML = `<p style="color:red;">Error processing file.</p>`;
            console.error(err);
        });
});


startBtn.addEventListener("click", () => {
    if (extractedAssignments.length === 0) {
        alert("Upload a file first!");
        return;
    }

    pageUpload.classList.add("hidden");
    pageAssignments.classList.remove("hidden");

    const container = document.getElementById("assignmentList");
    container.innerHTML = "";

    extractedAssignments.forEach(a => {
        container.innerHTML += `
            <div class="assignment-card">
                <h3>${a.title}</h3>
                <p>Due: ${a.due}</p>
            </div>
        `;
    });
});


backBtn.addEventListener("click", () => {
    pageAssignments.classList.add("hidden");
    pageUpload.classList.remove("hidden");
});


generateBtn.addEventListener("click", () => {
    alert("Schedule generation coming next! 📅");
});
