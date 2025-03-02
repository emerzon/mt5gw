// Function to load instruments from localStorage
function loadInstruments() {
    console.log('Loading instruments from /symbols');
    fetch('/symbols')
        .then(response => response.json())
        .then(symbols => {
            console.log('Symbols received:', symbols);

            const datalist = document.getElementById('instrument-list');

            // Clear existing options
            datalist.innerHTML = '';

            // Add options to datalist
            symbols.forEach(symbol => {
                const option = document.createElement('option');
                option.value = symbol;
                datalist.appendChild(option);
                console.log('Added option:', symbol);
            });

            // Load the last used instrument, timeframe, and number of candles from localStorage
            const storedInstrument = localStorage.getItem('lastUsedInstrument');
            const storedTimeframe = localStorage.getItem('lastUsedTimeframe');
            const storedNumCandles = localStorage.getItem('lastUsedNumCandles');

            if (storedInstrument) {
                console.log('Loading last used instrument from localStorage:', storedInstrument);
                document.getElementById('instrument').value = storedInstrument;
            } else if (symbols.length > 0) {
                // Set the first symbol as the default value if no instrument is stored
                const firstSymbol = symbols[0];
                console.log('Setting default instrument to:', firstSymbol);
                document.getElementById('instrument').value = firstSymbol;
            }

            if (storedTimeframe) {
                console.log('Loading last used timeframe from localStorage:', storedTimeframe);
                document.getElementById('timeframe').value = storedTimeframe;
            }

            if (storedNumCandles) {
                console.log('Loading last used numCandles from localStorage:', storedNumCandles);
                document.getElementById('num_candles').value = storedNumCandles;
            }
        })
        .catch(error => {
            console.error('Error fetching symbols:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // Log Chart.js loading status
    console.log('Chart.js loaded:', typeof Chart !== 'undefined');
    
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded correctly.');
    }
    
    // Load instruments from localStorage
    loadInstruments();
    
    // Add click event listener to instrument input to select all text when clicked
    const instrumentInput = document.getElementById('instrument');

    instrumentInput.addEventListener('focus', function() {
        this.select();
    });

    instrumentInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const datalist = document.getElementById('instrument-list');
            if (datalist.options.length > 0) {
                this.value = datalist.options[0].value;
                event.preventDefault(); // Prevent form submission
            }
        }
    });

    // Add event listeners for denoising method checkboxes
    const denoiseCheckboxes = document.querySelectorAll('.denoise-method');
    denoiseCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDenoiseSettings);
    });
    
    // Initialize range input displays
    document.getElementById('kalman-q').addEventListener('input', function() {
        document.getElementById('kalman-q-value').textContent = this.value;
    });
    
    document.getElementById('kalman-r').addEventListener('input', function() {
        document.getElementById('kalman-r-value').textContent = this.value;
    });
    
    // Initialize number of candles slider display
    document.getElementById('num_candles').addEventListener('input', function() {
        document.getElementById('num_candles_value').textContent = this.value;
    });
    
    // Initialize denoising settings visibility
    updateDenoiseSettings();
});

let ohlcChart, volumeChart;

// Function to update denoising settings visibility
function updateDenoiseSettings() {
    const denoiseSettings = document.getElementById('denoising-settings');
    const waveletSettings = document.getElementById('wavelet-settings');
    const kalmanSettings = document.getElementById('kalman-settings');
    const ssaSettings = document.getElementById('ssa-settings');
    const emdSettings = document.getElementById('emd-settings');
    
    // Check if any denoising method is selected
    const waveletChecked = document.getElementById('wavelet').checked;
    const kalmanChecked = document.getElementById('kalman').checked;
    const ssaChecked = document.getElementById('ssa').checked;
    const emdChecked = document.getElementById('emd').checked;
    
    // Show/hide the main denoising settings container
    if (waveletChecked || kalmanChecked || ssaChecked || emdChecked) {
        denoiseSettings.style.display = 'block';
    } else {
        denoiseSettings.style.display = 'none';
    }
    
    // Show/hide specific method settings
    waveletSettings.style.display = waveletChecked ? 'block' : 'none';
    kalmanSettings.style.display = kalmanChecked ? 'block' : 'none';
    ssaSettings.style.display = ssaChecked ? 'block' : 'none';
    emdSettings.style.display = emdChecked ? 'block' : 'none';
}

function fetchAndPlot() {
    // Destroy existing charts if they exist and have a destroy method
    if (ohlcChart && typeof ohlcChart.destroy === 'function') ohlcChart.destroy();
    if (volumeChart && typeof volumeChart.destroy === 'function') volumeChart.destroy();

    const instrument = document.getElementById('instrument').value;
    const timeframe = document.getElementById('timeframe').value;
    const numCandles = parseInt(document.getElementById('num_candles').value);

    // Save the instrument, timeframe, and number of candles to localStorage
    localStorage.setItem('lastUsedInstrument', instrument);
    localStorage.setItem('lastUsedTimeframe', timeframe);
    localStorage.setItem('lastUsedNumCandles', numCandles);
    
    // Show loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    }
    
    // Get all selected denoising methods and their settings
    const denoiseMethods = [];
    const denoiseSettings = {};
    
    // Wavelet settings
    if (document.getElementById('wavelet').checked) {
        denoiseMethods.push('wavelet');
        denoiseSettings.wavelet = {
            level: document.getElementById('wavelet-level').value,
            type: document.getElementById('wavelet-type').value
        };
    }
    
    // Kalman settings
    if (document.getElementById('kalman').checked) {
        denoiseMethods.push('kalman');
        denoiseSettings.kalman = {
            q: document.getElementById('kalman-q').value,
            r: document.getElementById('kalman-r').value
        };
    }
    
    // SSA settings
    if (document.getElementById('ssa').checked) {
        denoiseMethods.push('ssa');
        denoiseSettings.ssa = {
            window: document.getElementById('ssa-window').value,
            groups: document.getElementById('ssa-groups').value
        };
    }
    
    // EMD settings
    if (document.getElementById('emd').checked) {
        denoiseMethods.push('emd');
        denoiseSettings.emd = {
            imfs: document.getElementById('emd-imfs').value
        };
    }

    const requestData = {
        instrument,
        timeframe,
        bars: numCandles,
        denoise_methods: denoiseMethods,
        denoise_settings: denoiseSettings
    };

    fetch('/fetch_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading overlay
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
        
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
                    borderWidth: 3,
                    fill: false,
                    tension: 0,
                    pointRadius: 0
                },
                {
                    label: 'Open',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.open[i] })),
                    borderColor: 'green',
                    borderWidth: 3,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    hidden: true
                },
                {
                    label: 'High',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.high[i] })),
                    borderColor: 'rgba(0, 255, 0, 0.5)',
                    borderWidth: 3,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    hidden: true
                },
                {
                    label: 'Low',
                    data: data.time.map((t, i) => ({ x: new Date(t), y: data.low[i] })),
                    borderColor: 'red',
                    borderWidth: 3,
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

        // Define a set of colors for denoised series
        const denoiseColors = {
            'wavelet': '#00ffff', // Cyan
            'kalman': '#ff00ff',  // Magenta
            'ssa': '#ffff00',     // Yellow
            'emd': '#ff8000'      // Orange
        };
        
        // Add all denoised series to the chart
        console.log("Looking for denoised data in:", data);
        
        // Handle denoised data - only process method-specific denoised data
        const denoiseMethods = ['wavelet', 'kalman', 'ssa', 'emd'];
        const processedMethods = new Set(); // Keep track of processed methods
        
        for (const key in data) {
            console.log("Checking key:", key);
            
            // Check if the key contains any of the denoising method names
            const matchingMethod = denoiseMethods.find(method => 
                key.startsWith(method + '_') && key.includes('denoised_')
            );
            
            if (matchingMethod && !processedMethods.has(matchingMethod)) {
                console.log(`Found denoised data for method ${matchingMethod}, key: ${key}`);
                const color = denoiseColors[matchingMethod] || '#' + Math.floor(Math.random()*16777215).toString(16);
                
                const timeKey = key.replace('_close', '_time'); // Construct the time key
                if (data[timeKey]) {
                    ohlcChart.data.datasets.push({
                        label: `${matchingMethod.charAt(0).toUpperCase() + matchingMethod.slice(1)}`,
                        type: 'line',
                        data: data[timeKey].map((t, i) => ({ x: new Date(t), y: data[key][i] })),
                        borderColor: color,
                        fill: false,
                        borderWidth: 2,
                        borderDash: [5, 5]
                    });
                    processedMethods.add(matchingMethod); // Mark the method as processed
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
    .catch(error => {
        // Hide loading overlay
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
        console.error('Error:', error);
        alert('Error fetching data: ' + error.message);
    });
}
