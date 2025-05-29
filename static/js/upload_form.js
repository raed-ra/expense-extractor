// static/js/upload_form.js

//block1: Run on page load
$(document).ready(function () {
    //block2: Hide loader and message if transactions table is present
    if ($('#transactionsTable').length > 0) {
        $('#statusLoader').addClass('d-none');
        $('#statusMessage').text('');
    }

    //block3: Handle form submission
    $('#uploadForm').submit(function (e) {
        e.preventDefault();

        //block4: Validate file input
        const fileInput = $('input[name="pdf_file"]')[0];
        if (!fileInput || fileInput.files.length === 0) {
            alert('Please select a PDF file.');
            return;
        }

        // Block5: Disable input + button and show loader
        $('#uploadForm').hide();
        $('#statusLoader').removeClass('d-none');
        $('#statusMessage').text('📤 Uploading file...');
        const formData = new FormData();
        formData.append('pdf_file', fileInput.files[0]);

        //block6: Send AJAX request to upload the file
        $.ajax({
            url: '/upload',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (html) {
                $('#statusMessage').text('📄 Extracting text from PDF...');
                setTimeout(() => $('#statusMessage').text('💬 Sending text to GPT...'), 1000);
                setTimeout(() => $('#statusMessage').text('✅ GPT response received. Preparing table...'), 2500);
                setTimeout(() => {
                    $('#statusLoader').addClass('d-none');
                    document.open();
                    document.write(html);
                    document.close();
                }, 4000);
            },
            error: function (xhr) {
                $('#statusMessage').text('❌ Upload failed: ' + xhr.responseText);
                $('#uploadForm').show(); // let user try again
            }
        });
    });

    // Block 7: Ensure the edit-submit button is properly initialized - I was using this because originally I wasn building editable tables in different places and this button was used to submit for other tables
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.setAttribute('data-submit-url', '/upload/edit-upload');
        submitBtn.setAttribute('data-mode', 'create');
    }
});
