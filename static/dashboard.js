function formatUptime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return `${hours}h ${minutes}m ${secs}s`;
}


async function updateDashboard() {

    try {

        const response = await fetch("/api/status");

        if (!response.ok) {
            throw new Error("AegisOps API is unavailable");
        }

        const data = await response.json();


        document.getElementById("cpu-value").textContent =
            `${data.cpu_percent}%`;

        document.getElementById("memory-value").textContent =
            `${data.memory_percent}%`;

        document.getElementById("uptime-value").textContent =
            formatUptime(data.uptime_seconds);

        document.getElementById("requests-value").textContent =
            data.requests;

        document.getElementById("environment-value").textContent =
            data.environment;

        document.getElementById("version-value").textContent =
            data.version;

        document.getElementById("process-memory-value").textContent =
            `${data.process_memory_mb} MB`;

        document.getElementById("system-status").textContent =
            "● Operational";

    }

    catch (error) {

        document.getElementById("system-status").textContent =
            "● System Unavailable";

        console.error("AegisOps monitoring error:", error);
    }
}


updateDashboard();

setInterval(updateDashboard, 3000);