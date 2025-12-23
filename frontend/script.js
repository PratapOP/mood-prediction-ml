const moodMap = { 'Sad': 1, 'Stressed': 2, 'Neutral': 3, 'Happy': 4 };
let moodChart;
let importanceChartInstance;

// --- AUTH LOGIC ---
async function handleAuth(type) {
    if (type === 'logout') {
        await fetch('http://127.0.0.1:5000/logout', { method: 'POST', credentials: 'include' });
        location.reload(); return;
    }
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch(`http://127.0.0.1:5000/${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
    });
    const result = await response.json();
    if (response.ok) {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('app-content').style.display = 'block';
        document.getElementById('display-user').innerText = username;
        initChart();
        loadHistoryFromDB();
    } else { alert(result.error || result.message); }
}

// --- APP LOGIC ---
function initChart() {
    const ctx = document.getElementById('moodChart').getContext('2d');
    Chart.defaults.color = '#94a3b8';
    moodChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Mood Level',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: { 
            responsive: true,
            scales: { y: { min: 1, max: 4, grid: { color: 'rgba(255,255,255,0.05)' } } } 
        }
    });
}

document.getElementById('moodForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const isSim = document.getElementById('simMode').checked;
    
    const formData = {
        sleep: document.getElementById('sleep').value,
        screen: document.getElementById('screen').value,
        exercise: document.getElementById('exercise').value,
        work: document.getElementById('work').value,
        social: document.getElementById('social').value,
        caffeine: document.getElementById('caffeine').value
    };

    // If simulation, we use a query param so the backend knows not to save
    const url = isSim ? 'http://127.0.0.1:5000/predict?sim=true' : 'http://127.0.0.1:5000/predict';

    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
        credentials: 'include'
    });

    const result = await response.json();
    const resultDisplay = document.getElementById('moodResult');
    resultDisplay.innerText = result.mood;
    
    // Animate mood change
    const colors = { 'Happy': '#10b981', 'Neutral': '#f59e0b', 'Stressed': '#f97316', 'Sad': '#ef4444' };
    resultDisplay.style.color = colors[result.mood];

    showImportance(result.importance);

    // Only update timeline if NOT in simulation mode
    if (!isSim) {
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        moodChart.data.labels.push(timestamp);
        moodChart.data.datasets[0].data.push(moodMap[result.mood]);
        if (moodChart.data.labels.length > 10) {
            moodChart.data.labels.shift();
            moodChart.data.datasets[0].data.shift();
        }
        moodChart.update();
    }
});

function showImportance(importance) {
    const impCtx = document.getElementById('importanceChart').getContext('2d');
    if (importanceChartInstance) importanceChartInstance.destroy();

    importanceChartInstance = new Chart(impCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(importance),
            datasets: [{ 
                data: Object.values(importance), 
                backgroundColor: '#3b82f6',
                borderRadius: 5
            }]
        },
        options: { 
            indexAxis: 'y', 
            plugins: { legend: { display: false } },
            scales: { x: { display: false }, y: { grid: { display: false } } }
        }
    });
}

async function loadHistoryFromDB() {
    const response = await fetch('http://127.0.0.1:5000/history', { credentials: 'include' });
    const data = await response.json();
    data.forEach(entry => {
        moodChart.data.labels.push(entry.date);
        moodChart.data.datasets[0].data.push(moodMap[entry.mood]);
    });
    moodChart.update();
}

// Show/Hide sim notice
document.getElementById('simMode').addEventListener('change', (e) => {
    document.getElementById('sim-notice').style.display = e.target.checked ? 'block' : 'none';
    document.getElementById('predictBtn').innerText = e.target.checked ? 'Run Simulation' : 'Analyze Mood';
});