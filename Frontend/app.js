//File Upload 
const fileInput = document.getElementById("fileInput");
const uploadedList = document.getElementById("uploadedList");
const uploadStatus = document.getElementById("uploadStatus");
const startStatus = document.getElementById("startStatus");
let selectedFile = null;

// Click upload box to open file selector
document.getElementById("upload-box").addEventListener("click", () => {
    fileInput.click();
});

// When a file is chosen
fileInput.addEventListener("change", async () => {
    selectedFile = fileInput.files[0];
    if (!selectedFile) return;

    uploadedList.innerHTML = `<li>${selectedFile.name}</li>`;

    uploadStatus.innerText = "Ready to Upload.";
});

// Start Button 
document.getElementById("startButton").addEventListener("click", async () => {
    if (!selectedFile) {
        uploadStatus.innerHTML = `<span style="color:red;">❌ No file selected.</span>`;
        return;
    }

    uploadStatus.innerText = "Uploading…";

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("http://127.0.0.1:5000/api/upload-syllabus", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            uploadStatus.innerHTML = `<span style="color:red;">❌ Upload failed.</span>`;
            return;
        }

        const result = await response.json();

        uploadStatus.innerHTML = `<span style="color:lime;">✔️ File processed successfully!</span>`;

        // Show extracted assignments
        if (result.assignmentsExtracted && result.assignmentsExtracted.length > 0) {
            let html = "<h3>Extracted Assignments:</h3><ul>";
            result.assignmentsExtracted.forEach(a => {
                html += `<li><strong>${a.title}</strong> — Due: ${a.dueDate}</li>`;
            });
            html += "</ul>";

            startStatus.innerHTML = html;
        } else {
            startStatus.innerHTML = "<p>No assignments found in this file.</p>";
        }

    } catch (err) {
        console.error(err);
        uploadStatus.innerHTML = `<span style="color:red;">❌ Error: ${err.message}</span>`;
    }
});
