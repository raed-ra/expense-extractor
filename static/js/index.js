function uploadFile() {
    const file = document.getElementById('fileElem').files[0];
    const formData = new FormData();
    formData.append('pdf', file);
}