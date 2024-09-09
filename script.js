document.getElementById('test-instructions-form').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent the form from submitting traditionally

    // Get the context and screenshots
    const context = document.getElementById('context').value;
    const screenshots = document.getElementById('screenshots').files;

    // Check if at least one screenshot is uploaded
    if (screenshots.length === 0) {
        alert('Please upload at least one screenshot!');
        return;
    }

    // Prepare the data to send to the server
    const formData = new FormData();
    formData.append('context', context);  // Optional text context
    for (let i = 0; i < screenshots.length; i++) {
        formData.append('screenshots', screenshots[i]);  // Append each screenshot
    }

    // Send the request to the server
    try {
        const response = await fetch('/describe-testing-instructions', {
            method: 'POST',
            body: formData
        });

        // Handle the response from the server
        const result = await response.json();
        if (response.ok) {
            // Display the output
            document.getElementById('output').innerText = JSON.stringify(result, null, 2);
        } else {
            document.getElementById('output').innerText = 'Error: ' + result.error;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').innerText = 'Failed to generate instructions.';
    }
});
