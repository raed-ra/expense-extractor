// static/js/upload_form.js

$(document).ready(function () {
    // If the table is already shown (e.g., after a reload), hide the loader just in case
    if ($('#transactionsTable').length > 0) {
        $('#statusLoader').addClass('d-none');
        $('#statusMessage').text('');
    }

    $('#uploadForm').submit(function (e) {
        e.preventDefault();

        const fileInput = $('input[name="pdf_file"]')[0];
        if (!fileInput || fileInput.files.length === 0) {
            alert('Please select a PDF file.');
            return;
        }

        // Disable input + button and show loader
        $('#uploadForm').hide();
        $('#statusLoader').removeClass('d-none');
        $('#statusMessage').text('📤 Uploading file...');

        const formData = new FormData();
        formData.append('pdf_file', fileInput.files[0]);

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

    // Ensure the edit-submit button is properly initialized
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.setAttribute('data-submit-url', '/upload/edit-upload');
        submitBtn.setAttribute('data-mode', 'create');
    }
});
