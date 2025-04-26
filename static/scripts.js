function uploadFile() {
    const file = document.getElementById('fileElem').files[0];
    const formData = new FormData();
    formData.append('pdf', file);

    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            let html = '<h2>Categorized Expenses</h2>';
            html += '<table class="table table-bordered"><thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Debit/Credit</th><th>Category</th></tr></thead><tbody>';
            
            data.forEach(item => {
                html += `<tr>
                    <td>${item.date || '-'}</td>
                    <td>${item.description}</td>
                    <td>${item.amount}</td>
                    <td>${item.type || '-'}</td>
                    <td>${item.category}</td>
                </tr>`;
            });
        
            html += '</tbody></table>';
            $('#result').html(html);
        },
        error: function (xhr) {
            $('#result').html(`<p class="text-danger">Error: ${xhr.responseText}</p>`);
        }
    });
}
