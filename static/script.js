document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('code');
    const detectButton = document.getElementById('detect');
    const clearButton = document.getElementById('clear');
    const resultsContainer = document.getElementById('results');
    const errorCount = document.getElementById('error-count');
    const lineCount = document.getElementById('line-count');

    // Update line count
    function updateLineCount() {
        const lines = codeInput.value.split('\n').length;
        lineCount.textContent = `Lines: ${lines}`;
    }

    // Create error item
    function createErrorItem(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = `error-item ${error.error_type === 'bug-free' ? 'bug-free' : ''}`;
        
        const errorType = document.createElement('div');
        errorType.className = 'error-type';
        errorType.textContent = error.error_type.charAt(0).toUpperCase() + error.error_type.slice(1);
        
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = error.message;
        
        errorDiv.appendChild(errorType);
        errorDiv.appendChild(errorMessage);
        
        if (error.fix_suggestion) {
            const fixSuggestion = document.createElement('div');
            fixSuggestion.className = 'fix-suggestion';
            fixSuggestion.textContent = error.fix_suggestion;
            errorDiv.appendChild(fixSuggestion);
        }
        
        return errorDiv;
    }

    // Handle detect button click
    detectButton.addEventListener('click', async function() {
        const code = codeInput.value;
        if (!code.trim()) {
            resultsContainer.innerHTML = `
                <div class="error-item">
                    <div class="error-type">Input Error</div>
                    <div class="error-message">Please enter some code to analyze</div>
                </div>
            `;
            return;
        }

        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            const data = await response.json();
            
            // Clear previous results
            resultsContainer.innerHTML = '';
            
            // Update error count
            const errorCount = data.errors.filter(error => error.error_type !== 'bug-free').length;
            document.getElementById('error-count').textContent = `Errors: ${errorCount}`;
            
            // Show results
            if (data.errors.length === 0) {
                resultsContainer.innerHTML = `
                    <div class="error-item bug-free">
                        <div class="error-type">Success</div>
                        <div class="error-message">No errors found in your code!</div>
                    </div>
                `;
            } else {
                data.errors.forEach(error => {
                    resultsContainer.appendChild(createErrorItem(error));
                });
            }

        } catch (error) {
            resultsContainer.innerHTML = `
                <div class="error-item">
                    <div class="error-type">Error</div>
                    <div class="error-message">An error occurred while analyzing your code</div>
                </div>
            `;
        }
    });

    // Handle clear button click
    clearButton.addEventListener('click', function() {
        codeInput.value = '';
        resultsContainer.innerHTML = `
            <div class="welcome-message">
                <i class="fas fa-robot"></i>
                <p>Enter your Python code and click "Detect Bugs" to start!</p>
            </div>
        `;
        errorCount.textContent = 'Errors: 0';
        lineCount.textContent = 'Lines: 0';
    });

    // Update line count as user types
    codeInput.addEventListener('input', updateLineCount);

    // Initial line count
    updateLineCount();
}); 