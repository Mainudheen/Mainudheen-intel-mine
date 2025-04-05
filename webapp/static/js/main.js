document.addEventListener('DOMContentLoaded', function () {
    const codeInput = document.getElementById('code-input');
    const lineNumbers = document.getElementById('line-numbers');
    const runButton = document.getElementById('run-button');
    const errorDisplay = document.getElementById('error-display');

    function updateLineNumbers() {
        const lines = codeInput.value.split('\n');
        const lineCount = lines.length;
        
        // Create line numbers for all lines
        const lineNumbersHtml = Array.from({ length: lineCount }, (_, i) => 
            `<div class="line-number" data-line="${i + 1}">${i + 1}</div>`).join('');
        
        // Update the line numbers display
        lineNumbers.innerHTML = lineNumbersHtml;
        
        // Ensure the line numbers container matches the height of the textarea
        lineNumbers.style.height = `${codeInput.scrollHeight}px`;
    }

    function highlightErrorLines(errorLines) {
        document.querySelectorAll('.line-number').forEach(line => 
            line.classList.remove('error-line'));
        
        errorLines.forEach(lineNumber => {
            const line = lineNumbers.querySelector(`[data-line="${lineNumber}"]`);
            if (line) {
                line.classList.add('error-line');
            }
        });
    }

    async function detectErrors() {
        try {
            const code = codeInput.value.trim();
            if (!code) {
                errorDisplay.innerHTML = '<div class="error">Please enter some code!</div>';
                return;
            }

            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });

            const result = await response.json();
            highlightErrorLines([]);

            if (result.errors && result.errors.length > 0) {
                let errorHtml = '<div class="error-list">';
                const errorLines = new Set();

                result.errors.forEach(error => {
                    errorHtml += `<div class="error-item">`;
                    errorHtml += `<span class="error-type">${error.error_type}</span>: `;
                    errorHtml += `<span class="error-message">${error.message} (Line ${error.line})</span>`;
                    errorHtml += `</div>`;
                    
                    if (error.line > 0) {
                        errorLines.add(error.line);
                    }
                });

                errorHtml += '</div>';
                errorDisplay.innerHTML = errorHtml;
                highlightErrorLines(Array.from(errorLines));
            } else {
                errorDisplay.innerHTML = '<div class="success">No errors found!</div>';
            }

        } catch (error) {
            errorDisplay.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        }
    }

    runButton.addEventListener('click', detectErrors);
    codeInput.addEventListener('input', updateLineNumbers);
    codeInput.addEventListener('scroll', () => {
        lineNumbers.scrollTop = codeInput.scrollTop;
    });
    
    // Initial update
    updateLineNumbers();
});
