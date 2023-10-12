// dashboard.js
document.addEventListener("DOMContentLoaded", function () {
    // Code for fetching data from your Django views or API
    // Example:
    fetch('/api/data/')  // Replace with your data endpoint
        .then(response => response.json())
        .then(data => {
            createBarChart(data);
            createPieChart(data);
        })
        .catch(error => console.error(error));

    function createBarChart(data) {
        // Bar chart creation code here using Chart.js
    }

    function createPieChart(data) {
        // Pie chart creation code here using Chart.js
    }
});
