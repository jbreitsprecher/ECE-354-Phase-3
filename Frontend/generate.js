window.onload = async () => {
    const container = document.getElementById("assignmentContainer");

    try {
        const response = await fetch("http://127.0.0.1:5000/api/assignments");
        const assignments = await response.json();

        if (assignments.length === 0) {
            container.innerHTML = "<p>No assignments found. Upload a syllabus first.</p>";
            return;
        }

        let html = "";
        assignments.forEach(a => {
            html += `
                <div class="assignment-card">
                    <h3>${a.title}</h3>
                    <p><strong>Due:</strong> ${a.dueDate}</p>
                </div>
            `;
        });

        container.innerHTML = html;

    } catch (err) {
        console.error(err);
        container.innerHTML = "<p>Error loading assignments.</p>";
    }
};


document.getElementById("makeScheduleBtn").addEventListener("click", () => {
    alert("Schedule generation coming soon!");
});
