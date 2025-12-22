let moodHistory = [];
const ctx = document.getElementById('moodChart').getContext('2d');
let moodChart;

// Initialize Chart
function initChart() {
    moodChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Dates or Entry numbers
            datasets: [{
                label: 'Mood Level (1:Sad, 2:Stressed, 3:Neutral, 4:Happy)',
                data: [],
                borderColor: '#3498db',
                tension: 0.3,
                fill: true,
                backgroundColor: 'rgba(52, 152, 219, 0.1)'
            }]
        },
        options: { scales: { y: { min: 1, max: 4, ticks: { stepSize: 1 } } } }
    });
}

const moodMap = { 'Sad': 1, 'Stressed': 2, 'Neutral': 3, 'Happy': 4 };

document.getElementById('moodForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        sleep: document.getElementById('sleep').value,
        screen: document.getElementById('screen').value,
        exercise: document.getElementById('exercise').value,
        work: document.getElementById('work').value,
        social: document.getElementById('social').value,
        caffeine: document.getElementById('caffeine').value
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        
        // Update UI Text
        document.getElementById('moodResult').innerText = result.mood;
        
        // Update Chart Data
        const timestamp = new Date().toLocaleTimeString();
        moodChart.data.labels.push(timestamp);
        moodChart.data.datasets[0].data.push(moodMap[result.mood]);
        
        // Keep only last 7 entries for clarity
        if (moodChart.data.labels.length > 7) {
            moodChart.data.labels.shift();
            moodChart.data.datasets[0].data.shift();
        }
        
        moodChart.update();

    } catch (error) {
        console.error("Error:", error);
    }
});

initChart();