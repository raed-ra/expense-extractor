// flow.js
// This script handles the dynamic behavior of the flow table, including editing and saving rows.

async function saveRow(id) {
    const row = document.querySelector(`tr[data-id='${id}']`);
    const data = {
        date: row.querySelector('input[type="date"]').value,
        type: row.querySelector('select').value,
        category: row.querySelectorAll('input')[1].value,
        description: row.querySelectorAll('input')[2].value,
        amount: row.querySelector('input[type="number"]').value
    };

    const response = await fetch(`/flow/${id}/edit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams(data)
    });

    const result = await response.json();
    if (result.success) {
        showToast("✅ Changes saved!");
    } else {
        alert('Error: ' + result.message);
    }
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.remove('hidden', 'animate-slide-fade-out');
    toast.classList.add('animate-slide-fade-in');

    setTimeout(() => {
        toast.classList.remove('animate-slide-fade-in');
        toast.classList.add('animate-slide-fade-out');
        setTimeout(() => toast.classList.add('hidden'), 400);
    }, 2000);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('tbody tr').forEach(row => {
        row.querySelectorAll('input, select').forEach(el => {
            el.addEventListener('keydown', event => {
                if (event.key === 'Enter') {
                    const id = row.getAttribute('data-id');
                    saveRow(id);
                }
            });
        });
    });
});
