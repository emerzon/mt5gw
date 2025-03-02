document.addEventListener('DOMContentLoaded', function() {
    // Log Chart.js loading status
    console.log('Chart.js loaded:', typeof Chart !== 'undefined');
    
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded correctly.');
    }
});

let ohlcChart, volumeChart;

document.getElementById('date_range').addEventListener('change', function() {
    const customDateRange = document.getElementById('custom_date_range');
    if (this.value === 'custom') {
        customDateRange.style.display = 'block';
    } else {
        customDateRange.style.display = 'none';
    }
});

function fetchAndPlot() {
    // Destroy existing charts if they exist and have a destroy method
    if (ohlcChart && typeof ohlcChart.destroy === 'function') ohlcChart.destroy();
    if (volumeChart && typeof volumeChart.destroy === 'function') volumeChart.destroy();

    const instrument = document.getElementById('instrument').value;
    const timeframe = document.getElementById('timeframe').value;
    const dateRange = document.getElementById('date_range').value;
    let dateFrom = null;
    let dateTo = null;

    if (dateRange === 'custom') {
        dateFrom = document.getElementById('date_from').value;
        dateTo = document.getElementById('date_to').value;
    } else {
        const now = new Date();
        dateTo = now.toISOString().slice(0, 19);
        let days = 1;
        if (dateRange === '7d') days = 7;
        if (dateRange === '30d') days = 30;
        const past = new Date(now.setDate(now.getDate() - days));
        dateFrom = past.toISOString().slice(0, 19);
    }

    const sma = document.getElementById('sma').checked;
    const rsi = document.getElementById('rsi').checked;
    
    // Get all selected denoising methods
    const denoiseMethods = [];
    if (document.getElementById('wavelet').checked) denoiseMethods.push('wavelet');
    if (document.getElementById('kalman').checked) denoiseMethods.push('kalman');
    if (document.getElementById('ssa').checked) denoiseMethods.push('ssa');
    if (document.getElementById('emd').checked) denoiseMethods.push('emd');

    const indicators = [];
    if (sma) indicators.push('sma');
    if (rsi) indicators.push('rsi');

    const requestData = {
        instrument,
        timeframe,
        date_from: dateFrom || null,
        date_to: dateTo || null,
        indicators,
        denoise_methods: denoiseMethods
    };

    fetch('/fetch_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data received:', data);
        console.log('Data keys:', Object.keys(data));
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        if (!data.open || !data.high || !data.low || !data.close) {
            console.error('OHLC data missing:', data);
            alert('OHLC data is missing from the response.');
            return;
        }

        let timeUnit;
        switch (timeframe) {
            case '1min': timeUnit = 'minute'; break;
            case '1h': timeUnit = 'hour'; break;
            case '1d': timeUnit = 'day'; break;
            default: timeUnit = 'minute';
        }

        const ohlcCtx = document.getElementById('ohlcChart').getContext('2d');
        const ohlcData = data.time.map((t, i) => ({
            x: new Date(t),
            o: data.open[i],
            h: data.high[i],
            l: data.low[i],
            c: data.close[i]
        }));
        console.log('OHLC data:', ohlcData);

        // Create a multi-line chart for OHLC data
        const chartData = {
            datasets: [
                {
                    label: 'Close',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.close[i] })),
                    borderColor: 'blue',
                    borderWidth: 2,
                    fill: false,
                    tension: 0,
                    pointRadius: 0
                },
                {
                    label: 'Open',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.open[i] })),
                    borderColor: 'green',
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    hidden: true
                },
                {
                    label: 'High',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.high[i] })),
                    borderColor: 'rgba(0, 255, 0, 0.5)',
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    hidden: true
                },
                {
                    label: 'Low',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.low[i] })),
                    borderColor: 'rgba(255, 0, 0, 0.5)',
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    hidden: true
                }
            ]
        };
        
        ohlcChart = new Chart(ohlcCtx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: timeUnit,
                            tooltipFormat: 'yyyy-MM-dd HH:mm:ss',
                            displayFormats: {
                                minute: 'HH:mm',
                                hour: 'HH:mm',
                                day: 'MMM dd'
                            }
                        },
                        title: { display: true, text: 'Time' }
                    },
                    y: {
                        title: { display: true, text: 'Price' },
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: { display: true },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                },
                elements: {
                    point: {
                        radius: 0
                    },
                    line: {
                        tension: 0
                    }
                }
            }
        });

        if (data.sma) {
            ohlcChart.data.datasets.push({
                label: 'SMA',
                type: 'line',
                data: data.time.map((t, i) => ({ x: new Date(t), y: data.sma[i] })),
                borderColor: '#ff0000',
                fill: false
            });
        }
        if (data.rsi) {
            ohlcChart.data.datasets.push({
                label: 'RSI',
                type: 'line',
                data: data.time.map((t, i) => ({ x: new Date(t), y: data.rsi[i] })),
                borderColor: '#0000ff',
                fill: false,
                yAxisID: 'rsi-y'
            });
            ohlcChart.options.scales['rsi-y'] = {
                type: 'linear',
                position: 'right',
                title: { display: true, text: 'RSI' },
                min: 0,
                max: 100
            };
        }
        // Define a set of colors for denoised series
        const denoiseColors = {
            'wavelet': '#00ffff', // Cyan
            'kalman': '#ff00ff',  // Magenta
            'ssa': '#ffff00',     // Yellow
            'emd': '#ff8000'      // Orange
        };
        
        // Add all denoised series to the chart
        console.log("Looking for denoised data in:", data);
        
        // First, handle the default denoised_close if present
        if (data.denoised_close) {
            console.log("Found default denoised_close data");
            ohlcChart.data.datasets.push({
                label: 'Default Denoised',
                type: 'line',
                data: data.time.map((t, i) => ({ x: new Date(t), y: data.denoised_close[i] })),
                borderColor: '#00ffff',
                fill: false,
                borderWidth: 1.5
            });
        }
        
        // Then handle method-specific denoised data
        const denoiseMethods = ['wavelet', 'kalman', 'ssa', 'emd'];
        
        for (const key in data) {
            console.log("Checking key:", key);
            
            // Check if the key contains any of the denoising method names
            const matchingMethod = denoiseMethods.find(method => 
                key.startsWith(method + '_') && key.includes('denoised_')
            );
            
            if (matchingMethod) {
                console.log(`Found denoised data for method ${matchingMethod}, key: ${key}`);
                const color = denoiseColors[matchingMethod] || '#' + Math.floor(Math.random()*16777215).toString(16);
                
                const timeKey = key.replace('_close', '_time'); // Construct the time key
                if (data[timeKey]) {
                    ohlcChart.data.datasets.push({
                        label: `${matchingMethod.charAt(0).toUpperCase() + matchingMethod.slice(1)} Denoised`,
                        type: 'line',
                        data: data[timeKey].map((t, i) => ({ x: new Date(t), y: data[key][i] })),
                        borderColor: color,
                        fill: false,
                        borderWidth: 1.5
                    });
                } else {
                    console.error(`Time data not found for ${key}`);
                }
            }
        }
        ohlcChart.update();

        const volumeCtx = document.getElementById('volumeChart').getContext('2d');
        // Format volume data for time-based chart
        const volumeData = data.time.map((t, i) => ({
            x: new Date(t),
            y: data.volume[i]
        }));
        
        volumeChart = new Chart(volumeCtx, {
            type: 'bar',
            data: {
                datasets: [{
                    label: 'Volume',
                    data: volumeData,
                    backgroundColor: '#888888'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: { unit: timeUnit },
                        title: { display: true, text: 'Time' }
                    },
                    y: {
                        title: { display: true, text: 'Volume' }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error:', error));
}
