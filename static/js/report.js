// --- static/js/report.js ---
document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#fromDate", {
        enable: availableTransactionDates,
        dateFormat: "Y-m-d"
    });
    flatpickr("#toDate", {
        enable: availableTransactionDates,
        dateFormat: "Y-m-d"
    });

    document.getElementById('filterForm').addEventListener('submit', async (e) => {
        // Prevent the default form submission
        e.preventDefault();
        // get the form data and create a URL with query parameters
        const params = new URLSearchParams(new FormData(e.target));
        document.getElementById('exportBtn').href = `/report/export?${params.toString()}`;

        const url = `/report/data?${params.toString()}`;
        const res = await fetch(url);
        const data = await res.json();

        updateTable(data);
        updateChart(data);
        updatePieChart(data);
    });

    function updateTable(data) {
        const tbody = document.querySelector("#reportTable tbody");
        tbody.innerHTML = "";
    
        if (data.length > 0) {
            document.getElementById('tableContainer').style.display = "block";
            document.getElementById('exportBtn').classList.remove("hidden");
    
            for (let txn of data) {
                const row = `<tr class="border-b hover:bg-gray-50">
                    <td class="px-4 py-2">${txn.date}</td>
                    <td class="px-4 py-2">${txn.description}</td>
                    <td class="px-4 py-2">${txn.amount}</td>
                    <td class="px-4 py-2">${txn.type}</td>
                    <td class="px-4 py-2">${txn.category}</td>
                </tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            }
        } else {
            document.getElementById('tableContainer').style.display = "none";
            document.getElementById('exportBtn').classList.add("hidden");
        }
    }
    

    // stores a 2D chart instance against the chart context
    const chartCtx = document.getElementById('reportChart').getContext('2d');
    let chartInstance = null;

    function updateChart(data) {

        document.getElementById('lineChartContainer').classList.toggle('hidden', data.length === 0);

        const labels = data.map(d => d.date);
        const amounts = data.map(d => d.amount);

        if (chartInstance) chartInstance.destroy();
        chartInstance = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Amount',
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
    let pieChartInstance = null;

    function updatePieChart(data) {
        const totalsByCategory = {};
    
        for (let txn of data) {
            if (txn.type === 'debit') {  // optional: only visualize spending
                const cat = txn.category || 'Uncategorized';
                totalsByCategory[cat] = (totalsByCategory[cat] || 0) + txn.amount;
            }
        }
    
        const hasPieData = Object.keys(totalsByCategory).length > 0;
        document.getElementById('pieChartContainer').classList.toggle('hidden', !hasPieData);
    
        const labels = Object.keys(totalsByCategory);
        const values = Object.values(totalsByCategory);
    
        if (pieChartInstance) pieChartInstance.destroy();
    
        const pieCtx = document.getElementById('pieChart').getContext('2d');
        pieChartInstance = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56',
                        '#4BC0C0', '#9966FF', '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' },
                    title: { display: true, text: 'Spending by Category' }
                }
            }
        });
    }
    
});
