const moodMap = { 'Sad': 1, 'Stressed': 2, 'Neutral': 3, 'Happy': 4 };
let moodChart;
let importanceChartInstance;

function initChart() {
    const ctx = document.getElementById('moodChart').getContext('2d');
    if (moodChart) moodChart.destroy(); // Prevent duplicate charts
    
    moodChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], 
            datasets: [{
                label: 'Mood History',
                data: [],
                borderColor: '#3b82f6',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(59, 130, 246, 0.1)'
            }]
        },
        options: {
            responsive: true,
            scales: { y: { min: 1, max: 4 } }
        }
    });
}

async function handleAuth(type) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch(`http://127.0.0.1:5000/${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
    });

    if (response.ok) {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('app-content').style.display = 'block';
        
        // TIMELINE FIX: Initialize chart first, then load data
        initChart(); 
        loadHistoryFromDB();
    } else {
        alert("Authentication Error");
    }
}

function initChart() {
    const ctx = document.getElementById('moodChart').getContext('2d');
    if (moodChart) moodChart.destroy();
    
    moodChart = new Chart(ctx, {
        type: 'line',
        data: { labels: [], datasets: [{
            label: 'Mood Level',
            data: [],
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.4
        }]},
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 1, max: 4,
                    ticks: {
                        stepSize: 1,
                        callback: (v) => Object.keys(moodMap).find(k => moodMap[k] === v)
                    },
                    grid: { color: 'rgba(255,255,255,0.05)' }
                }
            }
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

    const response = await fetch(`http://127.0.0.1:5000/predict${isSim ? '?sim=true' : ''}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
        credentials: 'include'
    });

    const result = await response.json();
    document.getElementById('moodResult').innerText = result.mood;
    
    // Advice logic
    if (result.advice) {
        document.getElementById('advice-container').style.display = 'block';
        document.getElementById('moodAdvice').innerText = result.advice;
    }

    // Update Timeline if not simulation
    if (!isSim) {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        moodChart.data.labels.push(time);
        moodChart.data.datasets[0].data.push(moodMap[result.mood]);
        moodChart.update();
    }
});

async function loadHistoryFromDB() {
    const response = await fetch('http://127.0.0.1:5000/history', { credentials: 'include' });
    const data = await response.json();
    moodChart.data.labels = data.map(e => e.date);
    moodChart.data.datasets[0].data = data.map(e => moodMap[e.mood]);
    moodChart.update();
}