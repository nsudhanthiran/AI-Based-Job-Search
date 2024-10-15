document.getElementById('resume').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.querySelector('.file-name').textContent = fileName;

    var uploadButton = document.querySelector('.custom-file-upload');
    uploadButton.style.backgroundColor = '#03e0d9';
    uploadButton.style.color = '#000';

    sessionStorage.setItem('uploadedFile', JSON.stringify({
        name: fileName,
        size: this.files[0].size
    }));
});

window.addEventListener('load', function() {
    var uploadedFile = sessionStorage.getItem('uploadedFile');
    if (uploadedFile) {
        uploadedFile = JSON.parse(uploadedFile);
        document.querySelector('.file-name').textContent = uploadedFile.name;
    }
});

document.getElementById('myForm').addEventListener('submit', function(event) {
    var jobType = document.getElementById('job_type');
    var workPreference = document.querySelectorAll('input[name="work_preference"]:checked');
    var resume = document.getElementById('resume');

    // Check if job type is selected
    if (!jobType.value) {
        alert('Please select a Type of Position.');
        event.preventDefault(); // Prevent form submission
        return;
    }

    // Check if work preference is selected
    if (workPreference.length === 0) {
        alert('Please select a Work Preference.');
        event.preventDefault(); // Prevent form submission
        return;
    }

    // Check if resume is uploaded
    if (!resume.files || resume.files.length === 0) {
        alert('Please upload a resume.');
        event.preventDefault(); // Prevent form submission
        return;
    }

    // Check if additional information is filled out
    
    
    
    // All fields are filled out, allow form submission
    // Optionally, you can remove the alerts and submit the form silently without alerts
});
