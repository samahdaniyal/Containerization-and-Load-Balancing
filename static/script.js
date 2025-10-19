// Fetch instance information
async function fetchInstanceInfo() {
    try {
        const response = await fetch('/instance');
        const data = await response.json();
        document.getElementById('instance-info').textContent = `Served by: ${data.instance}`;
    } catch (error) {
        console.error('Error fetching instance info:', error);
        document.getElementById('instance-info').textContent = 'Error loading instance info';
    }
}

// Fetch instance info when page loads
fetchInstanceInfo();

async function shortenUrl() {
    const longUrl = document.getElementById('longUrl').value;
    const resultDiv = document.getElementById('shortenResult');
    
    if (!longUrl) {
        showError(resultDiv, 'Please enter a URL');
        return;
    }

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: longUrl })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(resultDiv, `Short URL: ${window.location.origin}/${data.short_url}`);
        } else {
            showError(resultDiv, data.error || 'Failed to shorten URL');
        }
    } catch (error) {
        showError(resultDiv, 'An error occurred');
    }
}

async function expandUrl() {
    const shortUrl = document.getElementById('shortUrl').value;
    const resultDiv = document.getElementById('expandResult');
    
    if (!shortUrl) {
        showError(resultDiv, 'Please enter a short code');
        return;
    }

    try {
        const response = await fetch(`/expand?url=${encodeURIComponent(shortUrl)}`);
        const data = await response.json();
        
        if (response.ok) {
            showSuccess(resultDiv, `Long URL: ${data.long_url}`);
        } else {
            showError(resultDiv, data.error || 'Failed to expand URL');
        }
    } catch (error) {
        showError(resultDiv, 'An error occurred');
    }
}

function showSuccess(element, message) {
    element.className = 'result success';
    element.textContent = message;
}

function showError(element, message) {
    element.className = 'result error';
    element.textContent = message;
}
