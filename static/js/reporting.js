$(document).ready(function () {
    if (typeof availableTransactionDates !== 'undefined') {
        flatpickr("#fromDate", {
            enable: availableTransactionDates,
            dateFormat: "Y-m-d"
        });
        flatpickr("#toDate", {
            enable: availableTransactionDates,
            dateFormat: "Y-m-d"
        });
    }

    if (typeof reportData !== 'undefined' && reportData.length > 0) {
        const ctx = document.getElementById('reportChart').getContext('2d');
        const labels = reportData.map(r => r.date);
        const amounts = reportData.map(r => r.amount);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Amount Over Time',
                    data: amounts,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: 'Spending Trend' }
                }
            }
        });
    }
});
