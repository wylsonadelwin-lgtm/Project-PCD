const button1 = document.getElementById('Mulai');
const uploadbutton = document.getElementById('Upload');
const uploadForm = document.getElementById('uploadForm');

button1.addEventListener('click', () => {
    window.location.href = 'traffic/';
});

uploadbutton.addEventListener('click', () => {
    on();
});

document.getElementById("overlay").addEventListener('click', (e) => {
    if (e.target.id === 'overlay') off();
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const statusDiv = document.getElementById('uploadStatus');
    const file = fileInput.files[0];
    
    // 1. Get the CSRF token from the hidden input Django generated
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // 2. Point to the relative URL or the variable we discussed
        const response = await fetch('/upload_and_detect/', { 
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken // REQUIRED for Django POST requests
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 3. Update the image in the table
            document.getElementById('resultImage').src = data.image;
            statusDiv.innerHTML = `<p>Detected ${data.objects_detected} objects</p>`;
        } else {
            statusDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        console.error(error);
    }
});

function on(){
    document.getElementById("overlay").style.display = "flex";
}

function off(){
    document.getElementById("overlay").style.display = "none";
    document.getElementById('uploadForm').reset();
}