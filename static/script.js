document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    const cityInput = document.getElementById('cityInput');
    const searchButton = document.getElementById('searchButton');
    const resultsSection = document.getElementById('results');

    darkModeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
    });

    searchButton.addEventListener('click', async () => {
        const city = cityInput.value.trim();
        if (city) {
            try {
                const response = await fetch(`/air-quality/${city}`);
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                console.error('Error fetching data:', error);
                resultsSection.innerHTML = '<p>Error fetching data. Please try again.</p>';
            }
        }
    });

    function displayResults(data) {
        resultsSection.innerHTML = `
            <div id="averageAQI">Average AQI: ${data.average_aqi.toFixed(2)}</div>
            <div id="maxAQI">Max AQI: ${data.max_aqi}</div>
            <div id="latestData">
                <h3>Latest Data for ${data.city}</h3>
                <p>AQI: ${data.latest_data.aqi}</p>
                <p>PM2.5: ${data.latest_data.pm25}</p>
                <p>PM10: ${data.latest_data.pm10}</p>
                <p>NO2: ${data.latest_data.no2}</p>
                <p>SO2: ${data.latest_data.so2}</p>
                <p>CO: ${data.latest_data.co}</p>
                <p>Timestamp: ${new Date(data.latest_data.timestamp).toLocaleString()}</p>
            </div>
        `;
    }
});