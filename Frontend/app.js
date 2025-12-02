//file upload
const fileInput = document.getElementById("fileInput");
const startButton = document.getElementById("startBtn");
const uploadedList = document.getElementById("uploadedList");

// store uploaded 
let selectedFile = null;

// handle file 
fileInput.addEventListener("change", (e) => {
    selectedFile = e.target.files[0];

    uploadedList.innerHTML = `
        <p>1. ${selectedFile.name}</p>
    `;
});

// send file to backend 
startButton.addEventListener("click", async () => {
    if (!selectedFile) {
        alert("Please upload a file first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log(result);

        alert("Dates extracted! Check console for output.");

    } catch (error) {
        console.error("Upload failed:", error);
    }
});
