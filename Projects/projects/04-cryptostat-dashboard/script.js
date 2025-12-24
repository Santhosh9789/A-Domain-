const ctx = document.getElementById('marketChart').getContext('2d');

const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(13, 138, 188, 0.5)');
gradient.addColorStop(1, 'rgba(13, 138, 188, 0)');

const marketChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
            label: 'Portfolio Value',
            data: [12000, 19000, 15000, 25000, 22000, 30000, 42000],
            borderColor: '#0d8abc',
            backgroundColor: gradient,
            borderWidth: 2,
            pointBackgroundColor: '#121212',
            pointBorderColor: '#0d8abc',
            pointRadius: 6,
            pointHoverRadius: 8,
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#a0a0a0' }
            },
            y: {
                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                ticks: { color: '#a0a0a0' }
            }
        }
    }
});
