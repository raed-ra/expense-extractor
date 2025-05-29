// static/js/upload.js

// Block1: Run on page load
$(document).ready(function () {
    const hasTable = $('#transactionsTable').length > 0;

    // Block2: Disable form fields if the table is shown - we are going this by hard coding but the js code is for a fallback for cases where we don't have a full page reload
    if (hasTable) {
        $('#uploadForm input[type="file"]').prop('disabled', true);
        $('#uploadForm button[type="submit"]').prop('disabled', true);
    }

    // Block 3: Add new row
    $('#addRowBtn').click(function () {
        let categoryOptions = categories.map(cat =>
            `<option value="${cat}">${cat}</option>`
        ).join('');
        categoryOptions += `<option value="__custom__">Other...</option>`;
    
        const newRow = `
            <tr>
                <td><input type="checkbox" class="delete-checkbox w-100"></td>
                <td style="display:none"><input type="hidden" class="txn-id" value=""></td>
                <td><input type="date" class="form-control w-100"></td>
                <td><input type="text" class="form-control w-100"></td>
                <td><input type="number" step="0.01" class="form-control w-100"></td>
                <td>
                    <select class="form-select w-100">
                        <option value="debit">Debit</option>
                        <option value="credit">Credit</option>
                    </select>
                </td>
                <td>
                    <div class="d-flex flex-column">
                        <select class="form-select category-selector w-100">
                            ${categoryOptions}
                        </select>
                        <input type="text" class="form-control category-input mt-2 w-100" style="display:none" placeholder="Enter new category">
                    </div>
                </td>
            </tr>
        `;
        $('#transactionsTable tbody').append(newRow);
    });
    

    // Block 4: Delete selected rows
    $('#deleteSelectedBtn').click(function () {
        $('#transactionsTable tbody tr').each(function () {
            const checkbox = $(this).find('.delete-checkbox');
            if (checkbox.is(':checked')) {
                $(this).remove();
            }
        });
    });

    // Block 5: Toggle custom category field  -If the user selects “Other...” (which has the value "__custom__"),
    $('#transactionsTable').on('change', '.category-selector', function () {
        const selected = $(this).val(); // Get the selected value
        const input = $(this).closest('td').find('.category-input'); // Find the input field in the same column
        if (selected === '__custom__') {
            input.show().focus();
        } else {
            input.hide();
            input.val(selected); // optional: sync value
        }
    });

    // Block 6: Submit the table to the attributed URL given by the button set in the upload_form.js
    $('#submitBtn').click(function () {
        const url = $(this).data('submit-url');
        const mode = $(this).data('mode');

        // each means that we are going to iterate over each row in the table
        let newRows = [];
        $('#transactionsTable tbody tr').each(function () {
            //wraps it as a jQuery object so we can use jQuery functions like .find()
            const row = $(this);

            let category;
            const selected = row.find('.category-selector').val();
            if (selected === '__custom__') {
                category = row.find('.category-input').val();
            } else {
                category = selected;
            }

            const txn = {
                date: row.find('input[type="date"]').val(),
                description: row.find('input[type="text"]').eq(0).val(),
                amount: parseFloat(row.find('input[type="number"]').val()),
                // use .eq(0) because later in the same row you also have a second <input type="text"> — for custom category input — and you don’t want that one here.
                credit_type: row.find('select').eq(0).val(), //.eq(0) ensures we’re not accidentally getting the category dropdown.
                category: category,
                //filename: $('strong').text()  // filename shown in alert div
            };
            //skips the row if any of the required fields are empty or invalid
            if (!txn.description || isNaN(txn.amount)) return;

            newRows.push(txn);
        });

        // Sends the new rows to the server
        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ new: newRows, filename: $('strong').text() }),
            // Block 8: Display a success message and remove the current table from the page
            success: function (response) {
                const messageHtml = `
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                            ${response.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;

                $('#transactionsTable tbody').remove();
                $('#messageArea').html(messageHtml);
            
                // Optional: Re-enable form if you want them to upload again
                $('#uploadForm input[type="file"]').prop('disabled', false);
                $('#uploadForm button[type="submit"]').prop('disabled', false);
            },
            error: function (xhr) {
                alert('❌ Error: ' + xhr.responseText);
            }
        });
    });
});
