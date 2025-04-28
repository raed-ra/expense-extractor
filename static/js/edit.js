// static/js/edit.js

$(document).ready(function() {
    // Delete a row
    $('#transactionsTable').on('click', '.delete-row', function() {
        $(this).closest('tr').remove();
    });

    // Add a new blank row
    $('#addRowBtn').click(function() {
        const newRow = `
            <tr>
                <td><input type="date" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="number" step="0.01" class="form-control"></td>
                <td>
                    <select class="form-select">
                        <option value="debit">Debit</option>
                        <option value="credit">Credit</option>
                    </select>
                </td>
                <td><input type="text" class="form-control" value="Uncategorized"></td>
                <td>
                    <button class="btn btn-danger btn-sm delete-row">🗑️ Delete</button>
                </td>
            </tr>
        `;
        $('#transactionsTable tbody').append(newRow);
    });

    // Submit all rows
    $('#submitBtn').click(function() {
        const transactions = [];

        $('#transactionsTable tbody tr').each(function() {
            const date = $(this).find('input[type="date"]').val();
            const description = $(this).find('input[type="text"]').eq(0).val();
            const amount = parseFloat($(this).find('input[type="number"]').val());
            const type = $(this).find('select').val();
            const category = $(this).find('input[type="text"]').eq(1).val();

            // Basic validation
            if (description && !isNaN(amount)) {
                transactions.push({
                    date,
                    description,
                    amount,
                    type,
                    category
                });
            }
        });

        // Send to server
        $.ajax({
            url: '/edit-upload',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(transactions),
            success: function(response) {
                alert('✅ ' + response.message);
                window.location.href = '/'; // Redirect back to homepage
            },
            error: function(xhr) {
                alert('Error saving: ' + xhr.responseText);
            }
        });

    });
});
