document.addEventListener("DOMContentLoaded", function () {
    const statusContainer = document.getElementById("status-container");
    const uptimePercentage = document.getElementById("uptime-percentage");

    // Remplacez par votre clé API et l'ID du moniteur
    const apiKey = process.env["UPTIME_API_KEY"];
    const monitorID = process.env["MONITOR_ID"];
    const apiUrl = `https://api.uptimerobot.com/v2/getMonitors`;

    // Requête à l'API UptimeRobot
    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `api_key=${apiKey}&monitors=${monitorID}&format=json&response_times=1&response_times_limit=24`,
    })
        .then((response) => response.json())
        .then((data) => {
            const statusData = data.monitors[0].response_times.map((rt) => {
                return { uptime: rt.value < 3000 }; // Exemple: considérer uptime si le temps de réponse est inférieur à 3000ms
            });

            let uptimeCount = 0;

            statusData.forEach((data) => {
                const segment = document.createElement("div");
                segment.classList.add("status-segment");
                if (!data.uptime) {
                    segment.classList.add("down");
                } else {
                    uptimeCount++;
                }
                statusContainer.appendChild(segment);
            });

            // Calculer et afficher le pourcentage de disponibilité
            const uptimePercentageValue = (
                (uptimeCount / statusData.length) *
                100
            ).toFixed(3);
            uptimePercentage.textContent = `${uptimePercentageValue}%`;
        })
        .catch((error) =>
            console.error(
                "Erreur lors de la récupération des données UptimeRobot:",
                error,
            ),
        );
});

let selectedFile = null;
setInterval(autoRefreshLogs, 5000);

function loadLog(filename) {
    selectedFile = filename;
    const logUrl = `/logs/${filename}`;
    document.getElementById("log-content").innerHTML = `
        <!doctype html>
        <html lang="">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Loading...</title>
        </head>
        <body>
            <div class="container">
                <div class="cube"><div class="cube__inner"></div></div>
                <div class="cube"><div class="cube__inner"></div></div>
                <div class="cube"><div class="cube__inner"></div></div>
            </div>
        </body>
        </html>
        <style>
        .body {
            height: 100%;
            width: 100%;
        }
        .container {
            margin: auto;
            margin-top: 25%;
            --uib-size: 90px;
            --uib-color: white;
            --uib-speed: 1.75s;
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            width: var(--uib-size);
            height: calc(var(--uib-size) * 0.6);
        }
        .cube {
            flex-shrink: 0;
            width: calc(var(--uib-size) * 0.2);
            height: calc(var(--uib-size) * 0.2);
            animation: jump var(--uib-speed) ease-in-out infinite;
        }
        .cube__inner {
            display: block;
            height: 100%;
            width: 100%;
            border-radius: 25%;
            background-color: var(--uib-color);
            transform-origin: center bottom;
            animation: morph var(--uib-speed) ease-in-out infinite;
            transition: background-color 0.3s ease;
        }
        .cube:nth-child(2) {
            animation-delay: calc(var(--uib-speed) * -0.36);
            .cube__inner {
            animation-delay: calc(var(--uib-speed) * -0.36);
            }
        }
        .cube:nth-child(3) {
            animation-delay: calc(var(--uib-speed) * -0.2);
            .cube__inner {
            animation-delay: calc(var(--uib-speed) * -0.2);
            }
        }
        @keyframes jump {
            0% {
            transform: translateY(0px);
            }
            30% {
            transform: translateY(0px);
            animation-timing-function: ease-out;
            }
            50% {
            transform: translateY(-200%);
            animation-timing-function: ease-in;
            }
            75% {
            transform: translateY(0px);
            animation-timing-function: ease-in;
            }
        }
        @keyframes morph {
            0% {
            transform: scaleY(1);
            }
            10% {
            transform: scaleY(1);
            }
            20%,
            25% {
            transform: scaleY(0.6) scaleX(1.3);
            animation-timing-function: ease-in-out;
            }
            30% {
            transform: scaleY(1.15) scaleX(0.9);
            animation-timing-function: ease-in-out;
            }
            40% {
            transform: scaleY(1);
            }
            70%,
            85%,
            100% {
            transform: scaleY(1);
            }
            75% {
            transform: scaleY(0.8) scaleX(1.2);
            }
        }
        </style>
    `;
    setTimeout(() => {
        fetch(logUrl)
            .then((response) => response.text())
            .then((data) => {
                const lines = data.split("\n");
                const logContent = lines
                    .map((line) => `<p style="margin: 0;">${line}</p>`)
                    .join("");
                document.getElementById("log-title").innerHTML =
                    `<h2>${filename}</h2>`;
                document.getElementById("log-content").innerHTML = logContent;
                const log_content = document.getElementById("log-content");
                log_content.scrollTop = log_content.scrollHeight;
            })
            .catch((error) => {
                console.error("Error fetching log file:", error);
            });
    }, 1200);
}

function refreshLogs() {
    document.getElementById("log-title").innerHTML = "";
    document.getElementById("log-content").innerHTML = `
        <!doctype html>
        <html lang="">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>Loading...</title>
        </head>
        <body>
            <div class="container">
                <div class="cube"><div class="cube__inner"></div></div>
                <div class="cube"><div class="cube__inner"></div></div>
                <div class="cube"><div class="cube__inner"></div></div>
            </div>
        </body>
        </html>
        <style>
        .body {
            height: 100%;
            width: 100%;
        }
        .container {
            margin: auto;
            margin-top: 25%;
            --uib-size: 90px;
            --uib-color: white;
            --uib-speed: 1.75s;
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            width: var(--uib-size);
            height: calc(var(--uib-size) * 0.6);
        }
        .cube {
            flex-shrink: 0;
            width: calc(var(--uib-size) * 0.2);
            height: calc(var(--uib-size) * 0.2);
            animation: jump var(--uib-speed) ease-in-out infinite;
        }
        .cube__inner {
            display: block;
            height: 100%;
            width: 100%;
            border-radius: 25%;
            background-color: var(--uib-color);
            transform-origin: center bottom;
            animation: morph var(--uib-speed) ease-in-out infinite;
            transition: background-color 0.3s ease;
        }
        .cube:nth-child(2) {
            animation-delay: calc(var(--uib-speed) * -0.36);
            .cube__inner {
            animation-delay: calc(var(--uib-speed) * -0.36);
            }
        }
        .cube:nth-child(3) {
            animation-delay: calc(var(--uib-speed) * -0.2);
            .cube__inner {
            animation-delay: calc(var(--uib-speed) * -0.2);
            }
        }
        @keyframes jump {
            0% {
            transform: translateY(0px);
            }
            30% {
            transform: translateY(0px);
            animation-timing-function: ease-out;
            }
            50% {
            transform: translateY(-200%);
            animation-timing-function: ease-in;
            }
            75% {
            transform: translateY(0px);
            animation-timing-function: ease-in;
            }
        }
        @keyframes morph {
            0% {
            transform: scaleY(1);
            }
            10% {
            transform: scaleY(1);
            }
            20%,
            25% {
            transform: scaleY(0.6) scaleX(1.3);
            animation-timing-function: ease-in-out;
            }
            30% {
            transform: scaleY(1.15) scaleX(0.9);
            animation-timing-function: ease-in-out;
            }
            40% {
            transform: scaleY(1);
            }
            70%,
            85%,
            100% {
            transform: scaleY(1);
            }
            75% {
            transform: scaleY(0.8) scaleX(1.2);
            }
        }
        </style>
    `;
    setTimeout(() => {
        if (selectedFile) {
            loadLog(selectedFile);
        } else {
            document.getElementById("log-title").innerHTML = "";
            document.getElementById("log-content").innerHTML =
                "Aucun fichier de logs à rechargé n'a été trouvé.";
        }
    }, 1200);
}

function closeLogs() {
    document.getElementById("log-title").innerHTML = "";
    document.getElementById("log-content").innerHTML =
        "Ici s'afficheront les logs du fichier sélectionné.";
    selectedFile = null;
}

function autoRefreshLogs() {
    if (selectedFile) {
        const logUrl = `/logs/${selectedFile}`;
        fetch(logUrl)
            .then((response) => response.text())
            .then((data) => {
                const lines = data.split("\n");
                const logContent = lines
                    .map((line) => `<p style="margin: 0;">${line}</p>`)
                    .join("");
                document.getElementById("log-title").innerHTML =
                    `<h2>${selectedFile}</h2>`;
                document.getElementById("log-content").innerHTML = logContent;
                const log_content = document.getElementById("log-content");
                log_content.scrollTop = log_content.scrollHeight;
            })
            .catch((error) => {
                console.error("Error fetching log file:", error);
            });
    }
}

function printLogs() {
    if (selectedFile) {
        var content = document.getElementById("log-content").innerHTML;
        var printWindow = window.open("", "", "height=500,width=800");

        printWindow.document.write(`
            <head>
                <title>FC-Tryhard BOT - ${selectedFile}</title>
            </head>
            <body>
                <div id="log-title">${document.getElementById("log-title").innerHTML}</div>
                <div id="log-content">${content}</div>
            </body>
        `);

        printWindow.document.close();
        printWindow.focus();

        printWindow.print();
        printWindow.close();
    }
}
