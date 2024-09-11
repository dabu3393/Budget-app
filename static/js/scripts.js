window.onload = function() {
    // Data passed from Flask to JavaScript
    const categories = JSON.parse(document.getElementById('donutChart').dataset.categories);
    const spentAmounts = JSON.parse(document.getElementById('donutChart').dataset.spentAmounts);

    // Chart.js code to render the donut chart
    const ctx = document.getElementById('donutChart').getContext('2d');
    const donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories,  // Categories as labels
            datasets: [{
                label: 'Spending',
                data: spentAmounts,  // Spending amounts as data
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(199, 199, 199, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,  // Ensure responsiveness
            maintainAspectRatio: false,  // Allow chart to adapt to container size
            animation: false,  // Disable animation for better performance
            plugins: {
                legend: {
                    position: 'right',  // Position the legend on the right side
                },
                title: {
                    display: true,
                    text: 'Spending Distribution by Category'
                }
            }
        }
    });
};
