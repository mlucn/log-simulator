// Log Simulator Web UI - Main JavaScript
const API_BASE = '/api/v1';

// State
let schemas = {};
let currentSchemaInfo = null;
let generatedLogs = null;

// DOM Elements
const schemaSelect = document.getElementById('schema');
const scenarioSelect = document.getElementById('scenario');
const generateForm = document.getElementById('generateForm');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const resultsCard = document.getElementById('resultsCard');
const errorCard = document.getElementById('errorCard');
const schemaInfoCard = document.getElementById('schemaInfoCard');
const output = document.getElementById('output');
const resultCount = document.getElementById('resultCount');
const executionTime = document.getElementById('executionTime');
const errorMessage = document.getElementById('errorMessage');
const schemaInfo = document.getElementById('schemaInfo');

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    await loadSchemas();
    setupEventListeners();
});

// Load available schemas from API
async function loadSchemas() {
    try {
        const response = await fetch(`${API_BASE}/schemas`);
        if (!response.ok) throw new Error('Failed to load schemas');

        const data = await response.json();
        schemas = data.schemas;

        // Populate schema dropdown
        schemaSelect.innerHTML = '<option value="">Select a schema...</option>';
        Object.keys(schemas).forEach(category => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = category.replace('_', ' ').toUpperCase();

            schemas[category].forEach(schemaPath => {
                const option = document.createElement('option');
                option.value = schemaPath;
                // Extract readable name from path (e.g., "cloud_identity/google_workspace" -> "Google Workspace")
                const namePart = schemaPath.split('/')[1] || schemaPath;
                option.textContent = namePart
                    .split('_')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');
                option.dataset.category = category;
                optgroup.appendChild(option);
            });

            schemaSelect.appendChild(optgroup);
        });
    } catch (error) {
        showError(`Failed to load schemas: ${error.message}`);
    }
}

// Load schema details and scenarios
async function loadSchemaDetails(schemaPath) {
    try {
        const response = await fetch(`${API_BASE}/schemas/${encodeURIComponent(schemaPath)}`);
        if (!response.ok) throw new Error('Failed to load schema details');

        currentSchemaInfo = await response.json();

        // Update scenario dropdown
        scenarioSelect.innerHTML = '<option value="">Default (random)</option>';
        if (currentSchemaInfo.available_scenarios && currentSchemaInfo.available_scenarios.length > 0) {
            currentSchemaInfo.available_scenarios.forEach(scenario => {
                const option = document.createElement('option');
                option.value = scenario;
                option.textContent = scenario.replace(/_/g, ' ');
                scenarioSelect.appendChild(option);
            });
        }

        // Show schema info
        displaySchemaInfo();
    } catch (error) {
        console.error('Failed to load schema details:', error);
    }
}

// Display schema information
function displaySchemaInfo() {
    if (!currentSchemaInfo) {
        schemaInfoCard.style.display = 'none';
        return;
    }

    let infoHTML = '';
    if (currentSchemaInfo.description) {
        infoHTML += `<p><strong>Description:</strong> ${currentSchemaInfo.description}</p>`;
    }
    if (currentSchemaInfo.log_type) {
        infoHTML += `<p><strong>Log Type:</strong> ${currentSchemaInfo.log_type}</p>`;
    }
    if (currentSchemaInfo.output_format) {
        infoHTML += `<p><strong>Output Format:</strong> ${currentSchemaInfo.output_format}</p>`;
    }
    if (currentSchemaInfo.available_scenarios && currentSchemaInfo.available_scenarios.length > 0) {
        infoHTML += `<p><strong>Available Scenarios:</strong> ${currentSchemaInfo.available_scenarios.length}</p>`;
    }

    schemaInfo.innerHTML = infoHTML;
    schemaInfoCard.style.display = 'block';
}

// Setup event listeners
function setupEventListeners() {
    // Schema selection change
    schemaSelect.addEventListener('change', (e) => {
        const schemaPath = e.target.value;
        if (schemaPath) {
            loadSchemaDetails(schemaPath);
        } else {
            schemaInfoCard.style.display = 'none';
            scenarioSelect.innerHTML = '<option value="">Default (random)</option>';
        }
    });

    // Form submission
    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await generateLogs();
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        if (generatedLogs) {
            const jsonText = JSON.stringify(generatedLogs.logs, null, 2);
            navigator.clipboard.writeText(jsonText)
                .then(() => {
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = '📋 Copy to Clipboard';
                    }, 2000);
                })
                .catch(err => showError('Failed to copy to clipboard'));
        }
    });

    // Download JSON
    downloadBtn.addEventListener('click', () => {
        if (generatedLogs) {
            const jsonText = JSON.stringify(generatedLogs.logs, null, 2);
            const blob = new Blob([jsonText], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `logs_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    });
}

// Generate logs via API
async function generateLogs() {
    const formData = new FormData(generateForm);
    const schemaPath = formData.get('schema');
    const count = parseInt(formData.get('count'));
    const timeSpread = parseInt(formData.get('timeSpread'));
    const scenario = formData.get('scenario');

    if (!schemaPath) {
        showError('Please select a schema');
        return;
    }

    // Show loading state
    setLoadingState(true);
    hideError();
    resultsCard.style.display = 'none';

    try {
        const requestBody = {
            schema_name: schemaPath,
            count: count
        };

        if (timeSpread > 0) {
            requestBody.time_spread_seconds = timeSpread;
        }

        if (scenario) {
            requestBody.scenario = scenario;
        }

        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate logs');
        }

        generatedLogs = await response.json();
        displayResults();
    } catch (error) {
        showError(`Error generating logs: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

// Display generated logs
function displayResults() {
    if (!generatedLogs) return;

    // Format JSON with syntax highlighting
    const jsonText = JSON.stringify(generatedLogs.logs, null, 2);
    output.textContent = jsonText;

    // Update metadata
    resultCount.textContent = `${generatedLogs.count} logs`;
    executionTime.textContent = `Generated in ${generatedLogs.execution_time.toFixed(3)}s`;

    // Show results
    resultsCard.style.display = 'block';
    copyBtn.disabled = false;
    downloadBtn.disabled = false;

    // Scroll to results
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide error message
function hideError() {
    errorCard.style.display = 'none';
}

// Set loading state
function setLoadingState(loading) {
    generateBtn.disabled = loading;
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');

    if (loading) {
        btnText.style.display = 'none';
        spinner.style.display = 'inline-block';
    } else {
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}
