const dateElement = document.getElementById("date");
const today = new Date();
// base for flask backend
const API_BASE = "http://127.0.0.1:5000";

// this displays the date
dateElement.textContent = today.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric"
});


//file upload constructor 
const fileInput = document.getElementById("fileInput");
const uploadBox = document.getElementById("upload-box");
const fileList = document.getElementById("fileList");
const extractResults = document.getElementById("extract-results");
//page splitting into 2
const pageUpload = document.getElementById("page-upload");
const pageAssignments = document.getElementById("page-assignments");
//first screen buttons
const startBtn = document.getElementById("startBtn");
const backBtn = document.getElementById("backBtn");
const generateBtn = document.getElementById("generateBtn");

let extractedAssignments = [];


//file BOX UPload
uploadBox.addEventListener("click", () => fileInput.click());


// file upload and extract
fileInput.addEventListener("change", () => {
    fileList.innerHTML = "";
    extractResults.innerHTML = "";

    const file = fileInput.files[0];
    if (!file) return;

    //display file name
    const li = document.createElement("li");
    li.textContent = file.name;
    fileList.appendChild(li);

    // prepares to send the file to backend 
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/api/upload-syllabus", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            extractResults.innerHTML = `<p style="color:green;">✓ File processed successfully!</p>`;

            extractedAssignments = data.assignments || [];

            if (extractedAssignments.length === 0) {
                extractResults.innerHTML += `<p>No assignments found.</p>`;
                return;
            }

            
            extractedAssignments.forEach(a => {
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

    
    if (!fileInput.files[0]) {
        alert("Upload a file first!");
        return;
    }

    
    pageUpload.classList.add("hidden");
    pageAssignments.classList.remove("hidden");

    const container = document.getElementById("assignmentList");
    container.innerHTML = "";

    
    if (extractedAssignments.length === 0) {
        container.innerHTML = "<p>No assignments found in this document.</p>";
        return;
    }

    
    extractedAssignments.forEach(a => {
        container.innerHTML += `
            <div class="assignment-card">
                <h3>${a.title}</h3>
                <p>Due: ${a.due}</p>
            </div>
        `;
    });
});


// start button
backBtn.addEventListener("click", () => {
    pageAssignments.classList.add("hidden");
    pageUpload.classList.remove("hidden");
});

// Simple Calendar (WIP)

let calCurrentMonth = new Date().getMonth();
let calCurrentYear = new Date().getFullYear();

function renderSimpleCalendar(year, month) {
  const monthLabel = document.getElementById("calendar-month-label");
  const body = document.getElementById("calendar-body");

  if (!monthLabel || !body) {
    return;
  }

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  monthLabel.textContent = `${monthNames[month]} ${year}`;

  body.innerHTML = "";

  const firstDay = new Date(year, month, 1);
  const startingWeekday = firstDay.getDay(); // 0 = Sunday
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  let currentDay = 1;
  let row = document.createElement("tr");

  // Empty cells before the first day
  for (let i = 0; i < startingWeekday; i++) {
    row.appendChild(document.createElement("td"));
  }

  // Fill the days
  while (currentDay <= daysInMonth) {
    if (row.children.length === 7) {
      body.appendChild(row);
      row = document.createElement("tr");
    }

    const cell = document.createElement("td");

    const dayNumber = document.createElement("div");
    dayNumber.className = "calendar-day-number";
    dayNumber.textContent = currentDay;
    cell.appendChild(dayNumber);

    row.appendChild(cell);
    currentDay++;
  }

  // Fill trailing empty cells
  while (row.children.length < 7) {
    row.appendChild(document.createElement("td"));
  }

  body.appendChild(row);
}

function initSimpleCalendarControls() {
  const prevBtn = document.getElementById("prev-month");
  const nextBtn = document.getElementById("next-month");

  if (!prevBtn || !nextBtn) {
    return;
  }

  prevBtn.addEventListener("click", () => {
    calCurrentMonth--;
    if (calCurrentMonth < 0) {
      calCurrentMonth = 11;
      calCurrentYear--;
    }
    renderSimpleCalendar(calCurrentYear, calCurrentMonth);
  });

  nextBtn.addEventListener("click", () => {
    calCurrentMonth++;
    if (calCurrentMonth > 11) {
      calCurrentMonth = 0;
      calCurrentYear++;
    }
    renderSimpleCalendar(calCurrentYear, calCurrentMonth);
  });
}

// Initialize the simple calendar on page load
window.addEventListener("DOMContentLoaded", () => {
  initSimpleCalendarControls();
  renderSimpleCalendar(calCurrentYear, calCurrentMonth);
});
