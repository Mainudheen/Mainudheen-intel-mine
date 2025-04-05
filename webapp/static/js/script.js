let editor;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror
    editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        mode: 'python',
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        extraKeys: {
            "Tab": "indentMore",
            "Shift-Tab": "indentLess"
        }
    });

    // Set initial size
    editor.setSize('100%', '300px');
});

function detectBugs() {
    const code = editor.getValue();
    const errorList = document.getElementById('error-list');
    errorList.innerHTML = '';

    // Reset error counts
    document.getElementById('syntax-count').textContent = '0';
    document.getElementById('runtime-count').textContent = '0';
    document.getElementById('potential-count').textContent = '0';

    if (!code.trim()) {
        const errorItem = document.createElement('div');
        errorItem.className = 'error-item syntax';
        errorItem.textContent = 'Please enter some code to analyze.';
        errorList.appendChild(errorItem);
        return;
    }

    fetch('/api/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            let syntaxCount = 0;
            let runtimeCount = 0;
            let potentialCount = 0;

            // Sort errors by line number
            data.errors.sort((a, b) => a.line - b.line);

            // Display all errors
            data.errors.forEach(error => {
                const errorItem = document.createElement('div');
                errorItem.className = `error-item ${error.error_type.replace(' ', '-')}`;
                
                // Format the error message
                let message = error.message;
                if (error.line > 0) {
                    message = `Line ${error.line}: ${message}`;
                }
                errorItem.textContent = message;
                
                errorList.appendChild(errorItem);

                // Update error counts
                switch(error.error_type) {
                    case 'syntax error':
                        syntaxCount++;
                        break;
                    case 'runtime error':
                        runtimeCount++;
                        break;
                    case 'potential error':
                        potentialCount++;
                        break;
                }
            });

            // Update error counts in the UI
            document.getElementById('syntax-count').textContent = syntaxCount;
            document.getElementById('runtime-count').textContent = runtimeCount;
            document.getElementById('potential-count').textContent = potentialCount;

            // Check if code is bug-free
            const isBugFree = data.errors.length === 1 && data.errors[0].error_type === 'bug-free';
            
            if (isBugFree || (syntaxCount === 0 && runtimeCount === 0 && potentialCount === 0)) {
                // Clear any existing error messages
                errorList.innerHTML = '';
                
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.className = 'error-item bug-free';
                successMessage.textContent = 'No errors found in your code! 🎉';
                errorList.appendChild(successMessage);
                
                // Show firework effect
                const fireworkContainer = document.querySelector('.firework-container');
                if (fireworkContainer) {
                    // Reset any existing animations
                    fireworkContainer.classList.remove('show');
                    void fireworkContainer.offsetWidth; // Trigger reflow
                    
                    // Show the fireworks
                    fireworkContainer.classList.add('show');
                    
                    // Hide after 5 seconds
                    setTimeout(() => {
                        fireworkContainer.classList.remove('show');
                    }, 5000);
                }
            }
        }
    })
    .catch(error => {
        const errorItem = document.createElement('div');
        errorItem.className = 'error-item runtime';
        errorItem.textContent = 'An error occurred while analyzing the code.';
        errorList.appendChild(errorItem);
    });
}

function clearEditor() {
    editor.setValue('');
    document.getElementById('error-list').innerHTML = '';
    document.getElementById('syntax-count').textContent = '0';
    document.getElementById('runtime-count').textContent = '0';
    document.getElementById('potential-count').textContent = '0';
} 