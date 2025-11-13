// State management
let currentData = null;
let currentCharts = [];

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileStats = document.getElementById('fileStats');
const btnRemove = document.getElementById('btnRemove');
const controls = document.getElementById('controls');
const chartType = document.getElementById('chartType');
const dataColumn = document.getElementById('dataColumn');
const statsGrid = document.getElementById('statsGrid');
const chartsContainer = document.getElementById('chartsContainer');
const dataTableContainer = document.getElementById('dataTableContainer');
const dataTable = document.getElementById('dataTable');
const btnExport = document.getElementById('btnExport');

// Color palettes for charts
const colorPalettes = {
    vibrant: [
        'rgba(99, 102, 241, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(59, 130, 246, 0.8)',
        'rgba(236, 153, 75, 0.8)',
        'rgba(147, 51, 234, 0.8)',
        'rgba(34, 197, 94, 0.8)'
    ],
    gradient: [
        'rgba(168, 85, 247, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(251, 146, 60, 0.8)',
        'rgba(252, 211, 77, 0.8)',
        'rgba(134, 239, 172, 0.8)',
        'rgba(96, 165, 250, 0.8)',
        'rgba(196, 181, 253, 0.8)',
        'rgba(253, 164, 175, 0.8)',
        'rgba(165, 243, 252, 0.8)',
        'rgba(254, 215, 170, 0.8)'
    ]
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    });

    // Remove file
    btnRemove.addEventListener('click', (e) => {
        e.stopPropagation();
        resetApp();
    });

    // Chart type change
    chartType.addEventListener('change', () => {
        if (currentData) {
            renderVisualizations(currentData);
        }
    });

    // Data column change
    dataColumn.addEventListener('change', () => {
        if (currentData) {
            renderVisualizations(currentData);
        }
    });

    // Export button
    btnExport.addEventListener('click', exportInsights);
}

function handleFile(file) {
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!['csv', 'xlsx', 'xls'].includes(fileExtension)) {
        alert('Please upload a CSV or Excel file');
        return;
    }

    const reader = new FileReader();

    if (fileExtension === 'csv') {
        reader.onload = (e) => {
            parseCSV(e.target.result, file);
        };
        reader.readAsText(file);
    } else {
        reader.onload = (e) => {
            parseExcel(e.target.result, file);
        };
        reader.readAsArrayBuffer(file);
    }
}

function parseCSV(content, file) {
    Papa.parse(content, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
            currentData = {
                headers: results.meta.fields,
                rows: results.data,
                fileName: file.name,
                fileSize: file.size
            };
            displayFileInfo(file, results.data.length);
            processData();
        },
        error: (error) => {
            alert('Error parsing CSV: ' + error.message);
        }
    });
}

function parseExcel(arrayBuffer, file) {
    try {
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (jsonData.length === 0) {
            alert('The Excel file appears to be empty');
            return;
        }

        const headers = jsonData[0];
        const rows = jsonData.slice(1).map(row => {
            const obj = {};
            headers.forEach((header, index) => {
                obj[header] = row[index];
            });
            return obj;
        });

        currentData = {
            headers: headers,
            rows: rows,
            fileName: file.name,
            fileSize: file.size
        };

        displayFileInfo(file, rows.length);
        processData();
    } catch (error) {
        alert('Error parsing Excel file: ' + error.message);
    }
}

function displayFileInfo(file, rowCount) {
    uploadArea.style.display = 'none';
    fileInfo.style.display = 'block';
    fileName.textContent = file.name;
    fileStats.textContent = `${rowCount.toLocaleString()} rows • ${formatFileSize(file.size)}`;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function processData() {
    // Show controls
    controls.style.display = 'flex';

    // Populate column dropdown
    dataColumn.innerHTML = '<option value="auto">Auto Detect</option>';
    currentData.headers.forEach(header => {
        const option = document.createElement('option');
        option.value = header;
        option.textContent = header;
        dataColumn.appendChild(option);
    });

    // Analyze and visualize data
    analyzeData();
    renderVisualizations(currentData);
    renderDataTable(currentData);

    // Show all sections
    statsGrid.style.display = 'grid';
    chartsContainer.style.display = 'grid';
    dataTableContainer.style.display = 'block';
}

function analyzeData() {
    const data = currentData.rows;
    const totalRows = data.length;

    // Calculate statistics
    const stats = [
        {
            label: 'Total Records',
            value: totalRows.toLocaleString(),
            icon: '📊'
        },
        {
            label: 'Columns',
            value: currentData.headers.length,
            icon: '📑'
        }
    ];

    // Find categorical and numerical columns
    const categoricalColumns = [];
    const numericalColumns = [];

    currentData.headers.forEach(header => {
        const values = data.map(row => row[header]).filter(v => v !== null && v !== undefined && v !== '');
        const uniqueValues = new Set(values);

        if (uniqueValues.size < values.length * 0.5 && uniqueValues.size < 50) {
            categoricalColumns.push(header);
        }

        const numericValues = values.filter(v => !isNaN(parseFloat(v)));
        if (numericValues.length > values.length * 0.5) {
            numericalColumns.push(header);
        }
    });

    // Add more specific stats
    if (currentData.headers.includes('STATUS')) {
        const statusCount = {};
        data.forEach(row => {
            const status = row['STATUS'];
            statusCount[status] = (statusCount[status] || 0) + 1;
        });

        const mostCommonStatus = Object.keys(statusCount).reduce((a, b) =>
            statusCount[a] > statusCount[b] ? a : b
        );

        stats.push({
            label: 'Most Common Status',
            value: mostCommonStatus,
            icon: '📈'
        });
    }

    if (currentData.headers.includes('Source')) {
        const sourceCount = {};
        data.forEach(row => {
            const source = row['Source'];
            if (source) sourceCount[source] = (sourceCount[source] || 0) + 1;
        });

        stats.push({
            label: 'Unique Sources',
            value: Object.keys(sourceCount).length,
            icon: '🎯'
        });
    }

    // Render stats
    renderStats(stats);
}

function renderStats(stats) {
    statsGrid.innerHTML = stats.map(stat => `
        <div class="stat-card">
            <div class="stat-label">${stat.icon} ${stat.label}</div>
            <div class="stat-value">${stat.value}</div>
        </div>
    `).join('');
}

function renderVisualizations(data) {
    // Clear existing charts
    currentCharts.forEach(chart => chart.destroy());
    currentCharts = [];

    const selectedColumn = dataColumn.value;

    // Chart 1: Status distribution (Pie)
    if (data.headers.includes('STATUS')) {
        createPieChart('chart1', data, 'STATUS', 'Status Distribution');
    }

    // Chart 2: Source distribution (Bar)
    if (data.headers.includes('Source')) {
        createBarChart('chart2', data, 'Source', 'Leads by Source');
    }

    // Chart 3: Time trend (Line)
    if (data.headers.includes('Created')) {
        createTimelineChart('chart3', data, 'Created', 'Leads Over Time');
    }

    // Chart 4: Responsible person distribution (Doughnut)
    if (data.headers.includes('Responsible')) {
        createDoughnutChart('chart4', data, 'Responsible', 'Top Agents', 10);
    }
}

function createPieChart(canvasId, data, column, title) {
    const counts = getColumnCounts(data.rows, column);
    const labels = Object.keys(counts);
    const values = Object.values(counts);

    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // Update title
    const chartCard = canvas.closest('.chart-card');
    if (chartCard) {
        chartCard.querySelector('.chart-title').textContent = title;
    }

    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colorPalettes.vibrant,
                borderColor: 'rgba(255, 255, 255, 0.8)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'white',
                        padding: 15,
                        font: {
                            size: 12,
                            family: 'Inter'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        family: 'Inter'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter'
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });

    currentCharts.push(chart);
}

function createBarChart(canvasId, data, column, title) {
    const counts = getColumnCounts(data.rows, column);
    const sortedEntries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    const labels = sortedEntries.map(e => e[0]);
    const values = sortedEntries.map(e => e[1]);

    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // Update title
    const chartCard = canvas.closest('.chart-card');
    if (chartCard) {
        chartCard.querySelector('.chart-title').textContent = title;
    }

    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: values,
                backgroundColor: colorPalettes.gradient,
                borderColor: 'rgba(255, 255, 255, 0.5)',
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        family: 'Inter'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'white',
                        font: {
                            family: 'Inter'
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: 'white',
                        font: {
                            family: 'Inter'
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });

    currentCharts.push(chart);
}

function createTimelineChart(canvasId, data, column, title) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // Parse dates and count by date
    const dateCounts = {};
    data.rows.forEach(row => {
        const dateStr = row[column];
        if (dateStr) {
            // Try to parse the date
            let date;
            if (dateStr.includes('/')) {
                const parts = dateStr.split('/');
                // Assuming DD/MM/YYYY format
                date = new Date(parts[2], parts[1] - 1, parts[0]);
            } else {
                date = new Date(dateStr);
            }

            if (!isNaN(date.getTime())) {
                const dateKey = date.toISOString().split('T')[0];
                dateCounts[dateKey] = (dateCounts[dateKey] || 0) + 1;
            }
        }
    });

    const sortedDates = Object.keys(dateCounts).sort();
    const values = sortedDates.map(date => dateCounts[date]);

    // Update title
    const chartCard = canvas.closest('.chart-card');
    if (chartCard) {
        chartCard.querySelector('.chart-title').textContent = title;
    }

    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedDates.map(date => {
                const d = new Date(date);
                return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Leads Created',
                data: values,
                borderColor: 'rgba(99, 102, 241, 1)',
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(99, 102, 241, 1)',
                pointBorderColor: 'white',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        family: 'Inter'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'white',
                        font: {
                            family: 'Inter'
                        },
                        stepSize: 1
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: 'white',
                        font: {
                            family: 'Inter'
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });

    currentCharts.push(chart);
}

function createDoughnutChart(canvasId, data, column, title, limit = 10) {
    const counts = getColumnCounts(data.rows, column);
    const sortedEntries = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, limit);
    const labels = sortedEntries.map(e => e[0]);
    const values = sortedEntries.map(e => e[1]);

    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // Update title
    const chartCard = canvas.closest('.chart-card');
    if (chartCard) {
        chartCard.querySelector('.chart-title').textContent = title;
    }

    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colorPalettes.gradient,
                borderColor: 'rgba(255, 255, 255, 0.8)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'white',
                        padding: 10,
                        font: {
                            size: 11,
                            family: 'Inter'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        family: 'Inter'
                    },
                    bodyFont: {
                        size: 13,
                        family: 'Inter'
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });

    currentCharts.push(chart);
}

function getColumnCounts(rows, column) {
    const counts = {};
    rows.forEach(row => {
        const value = row[column];
        if (value !== null && value !== undefined && value !== '') {
            counts[value] = (counts[value] || 0) + 1;
        }
    });
    return counts;
}

function renderDataTable(data) {
    const maxRows = 50; // Show first 50 rows
    const displayRows = data.rows.slice(0, maxRows);

    let tableHTML = '<thead><tr>';
    data.headers.forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });
    tableHTML += '</tr></thead><tbody>';

    displayRows.forEach(row => {
        tableHTML += '<tr>';
        data.headers.forEach(header => {
            const value = row[header] !== null && row[header] !== undefined ? row[header] : '';
            tableHTML += `<td>${value}</td>`;
        });
        tableHTML += '</tr>';
    });

    tableHTML += '</tbody>';

    if (data.rows.length > maxRows) {
        tableHTML += `<caption style="caption-side: bottom; margin-top: 15px; color: rgba(255, 255, 255, 0.7);">
            Showing first ${maxRows} of ${data.rows.length} rows
        </caption>`;
    }

    dataTable.innerHTML = tableHTML;
}

function exportInsights() {
    if (!currentData) return;

    const insights = {
        fileName: currentData.fileName,
        totalRows: currentData.rows.length,
        totalColumns: currentData.headers.length,
        headers: currentData.headers,
        analysis: {}
    };

    // Add column analysis
    currentData.headers.forEach(header => {
        const values = currentData.rows.map(row => row[header]).filter(v => v !== null && v !== undefined && v !== '');
        const uniqueValues = new Set(values);

        insights.analysis[header] = {
            totalValues: values.length,
            uniqueValues: uniqueValues.size,
            topValues: Object.entries(getColumnCounts(currentData.rows, header))
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([value, count]) => ({ value, count }))
        };
    });

    const blob = new Blob([JSON.stringify(insights, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `insights_${currentData.fileName.replace(/\.[^/.]+$/, '')}_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function resetApp() {
    currentData = null;
    currentCharts.forEach(chart => chart.destroy());
    currentCharts = [];

    uploadArea.style.display = 'block';
    fileInfo.style.display = 'none';
    controls.style.display = 'none';
    statsGrid.style.display = 'none';
    chartsContainer.style.display = 'none';
    dataTableContainer.style.display = 'none';

    fileInput.value = '';
}
