document.addEventListener('DOMContentLoaded', function() {
    const statusContainer = document.getElementById('status-container');
    const uptimePercentage = document.getElementById('uptime-percentage');

    // Remplacez par votre clé API et l'ID du moniteur
    const apiKey = process.env['UPTIME_API_KEY']
    const monitorID = process.env['MONITOR_ID']
    const apiUrl = `https://api.uptimerobot.com/v2/getMonitors`;

    // Requête à l'API UptimeRobot
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `api_key=${apiKey}&monitors=${monitorID}&format=json&response_times=1&response_times_limit=24`
    })
    .then(response => response.json())
    .then(data => {
        const statusData = data.monitors[0].response_times.map(rt => {
            return { uptime: rt.value < 3000 }; // Exemple: considérer uptime si le temps de réponse est inférieur à 3000ms
        });

        let uptimeCount = 0;

        statusData.forEach(data => {
            const segment = document.createElement('div');
            segment.classList.add('status-segment');
            if (!data.uptime) {
                segment.classList.add('down');
            } else {
                uptimeCount++;
            }
            statusContainer.appendChild(segment);
        });

        // Calculer et afficher le pourcentage de disponibilité
        const uptimePercentageValue = (uptimeCount / statusData.length * 100).toFixed(3);
        uptimePercentage.textContent = `${uptimePercentageValue}%`;
    })
    .catch(error => console.error('Erreur lors de la récupération des données UptimeRobot:', error));
});
