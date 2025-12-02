const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");

uploadBox.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    let formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:5000/upload-file", {
        method: "POST",
        body: formData
    });

    addFileToList(file.name);
});

document.getElementById("uploadUrlBtn").addEventListener("click", async () => {
    const url = document.getElementById("urlInput").value;

    await fetch("http://127.0.0.1:5000/upload-url", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ url })
    });

    addFileToList(url);
});

function addFileToList(name) {
    const li = document.createElement("li");
    li.innerHTML = `
        ${name}
        <div>
            <button class="keep-btn">Keep</button>
            <button class="delete-btn">Delete</button>
        </div>
    `;
    fileList.appendChild(li);
}

document.getElementById("startBtn").addEventListener("click", async () => {
    const response = await fetch("http://127.0.0.1:5000/process-files");
    const data = await response.json();
    alert("Calendar generated! Check backend console.");
});

document.getElementById("cancelBtn").addEventListener("click", () => {
    fileList.innerHTML = "";
});
