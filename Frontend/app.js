// === Handle File Upload ===
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

    const formData = new FormData();
    formData.append("file", selectedFile);

    uploadStatus.innerText = "Uploading...";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            uploadStatus.innerText = "Upload complete!";
        } else {
            uploadStatus.innerText = "Upload failed.";
        }
    } catch (err) {
        uploadStatus.innerText = "Server error.";
        console.error(err);
    }
});

// === START BUTTON — REQUEST CALENDAR GENERATION ===
document.getElementById("startBtn").addEventListener("click", async () => {
    startStatus.innerText = "Working...";

    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST"
        });

        const result = await response.json();

        if (result.success) {
            startStatus.innerHTML =
                `<a href="http://127.0.0.1:5000/download/${result.file}" target="_blank">
                    Download Calendar
                </a>`;
        } else {
            startStatus.innerText = "Error generating calendar.";
        }
    } catch (err) {
        startStatus.innerText = "Server error.";
        console.error(err);
    }
});
