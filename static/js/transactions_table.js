// static/js/transactions_table.js

$(document).ready(function () {
    // Add new blank row
    $('#addRowBtn').click(function () {
        const newRow = `
            <tr>
                <td><input type="checkbox" class="delete-checkbox"></td>
                <td style="display:none"><input type="hidden" class="txn-id" value=""></td>
                <td><input type="date" class="form-control"></td>
                <td><input type="text" class="form-control"></td>
                <td><input type="number" step="0.01" class="form-control"></td>
                <td>
                    <select class="form-select">
                        <option value="debit">Debit</option>
                        <option value="credit">Credit</option>
                    </select>
                </td>
                <td>
                    <select class="form-select category-selector">
                        <option value="__custom__">Other...</option>
                    </select>
                    <input type="text" class="form-control category-input mt-2" style="display:none" placeholder="Enter new category">
                </td>
            </tr>
        `;
        $('#transactionsTable tbody').append(newRow);
    });

    // Delete selected rows
    $('#deleteSelectedBtn').click(function () {
        $('#transactionsTable tbody tr').each(function () {
            const checkbox = $(this).find('.delete-checkbox');
            if (checkbox.is(':checked')) {
                $(this).remove();
            }
        });
    });

    // Toggle custom category input
    $('#transactionsTable').on('change', '.category-selector', function () {
        const selected = $(this).val();
        const inputField = $(this).closest('td').find('.category-input');
        if (selected === '__custom__') {
            inputField.show();
        } else {
            inputField.hide();
        }
    });

    // Submit all changes
    $('#submitBtn').click(function () {
        const url = $(this).data('submit-url');
        const mode = $(this).data('mode');

        let newRows = [];
        let updatedRows = [];
        let deletedIds = [];

        $('#transactionsTable tbody tr').each(function () {
            const row = $(this);
            const id = row.find('.txn-id').val();
            const isDeleted = row.find('.delete-checkbox').is(':checked');

            let category;
            const selectedCategory = row.find('.category-selector').val();
            if (selectedCategory === '__custom__') {
                category = row.find('.category-input').val();
            } else {
                category = selectedCategory;
            }

            const txn = {
                date: row.find('input[type="date"]').val(),
                description: row.find('input[type="text"]').eq(0).val(),
                amount: parseFloat(row.find('input[type="number"]').val()),
                type: row.find('select').eq(0).val(),
                category: category
            };

            if (!txn.description || isNaN(txn.amount)) return; // basic validation

            if (id && isDeleted) {
                deletedIds.push(id);
            } else if (!id) {
                newRows.push(txn);
            } else {
                txn.id = id;
                updatedRows.push(txn);
            }
        });

        const payload = mode === 'create'
            ? { new: newRows }  // only new entries allowed
            : { new: newRows, updated: updatedRows, deleted: deletedIds };

        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(payload),
            success: function (response) {
                alert('✅ ' + response.message);
                window.location.href = '/'; // redirect home after save
            },
            error: function (xhr) {
                alert('❌ Error saving: ' + xhr.responseText);
            }
        });
    });
});
