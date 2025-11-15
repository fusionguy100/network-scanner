// -------------------------------
// OS ICON MAP
// -------------------------------
const osIcons = {
    "Windows": "/static/icons/windows.png",
    "Linux": "/static/icons/linux.png",
    "Unix": "/static/icons/linux.png",
    "MacOS": "/static/icons/apple.png",
    "Router": "/static/icons/router.png",
    "Unknown": "/static/icons/unknown.png"
};


// -------------------------------
// RUN SCAN BUTTON
// -------------------------------
document.getElementById("scan_btn").addEventListener("click", () => {
    runScan();
});


// -------------------------------
// SHOW / HIDE LOADING SPINNER
// -------------------------------
function showLoading() {
    document.getElementById("loading_screen").style.display = "block";
}

function hideLoading() {
    document.getElementById("loading_screen").style.display = "none";
}


// -------------------------------
// RUN FULL SCAN
// -------------------------------
async function runScan() {
    showLoading();

    const res = await fetch("/scan?subnet=192.168.0.0/24");
    const data = await res.json();

    hideLoading();
    loadDashboard(data.devices);
}


// -------------------------------
// LOAD DASHBOARD METRICS
// -------------------------------
function loadDashboard(devices) {
    // Count severity types
    let high = 0, medium = 0, low = 0;

    devices.forEach(d => {
        d.issues.forEach(issue => {
            if (issue.severity === "high") high++;
            else if (issue.severity === "medium") medium++;
            else low++;
        });
    });

    // Fill summary cards
    document.getElementById("total_devices").textContent = devices.length;
    document.getElementById("high_count").textContent = high;
    document.getElementById("medium_count").textContent = medium;
    document.getElementById("low_count").textContent = low;

    // Fill device table
    loadDeviceTable(devices);

    // Load charts
    loadSeverityChart(high, medium, low);
    loadPortsChart(devices);
}


// -------------------------------
// DEVICE TABLE
// -------------------------------
function loadDeviceTable(devices) {
    const tbody = document.getElementById("device_rows");
    tbody.innerHTML = "";

    devices.forEach(dev => {
        const tr = document.createElement("tr");

        const osIcon = osIcons[dev.os] || osIcons["Unknown"];

        tr.innerHTML = `
            <td>${dev.ip}</td>
            <td>${dev.vendor}</td>

            <td>
                <img src="${osIcon}" class="os-icon">
                ${dev.os}
            </td>

            <td>${dev.open_ports.join(", ")}</td>

            <td>
                ${dev.issues.length > 0
                    ? `<span class="badge bg-danger">${dev.issues.length} Risks</span>`
                    : `<span class="badge bg-success">OK</span>`}
            </td>
        `;

        tbody.appendChild(tr);
    });
}


// -------------------------------
// SEVERITY PIE CHART
// -------------------------------
let severityChartInstance;

function loadSeverityChart(high, medium, low) {
    const ctx = document.getElementById("severityChart").getContext("2d");

    if (severityChartInstance) severityChartInstance.destroy();

    severityChartInstance = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["High", "Medium", "Low"],
            datasets: [{
                data: [high, medium, low],
                backgroundColor: ["#dc3545", "#ffc107", "#28a745"]
            }]
        }
    });
}


// -------------------------------
// PORT DISTRIBUTION CHART
// -------------------------------
let portsChartInstance;

function loadPortsChart(devices) {
    let portCounts = {};

    devices.forEach(dev => {
        dev.open_ports.forEach(port => {
            portCounts[port] = (portCounts[port] || 0) + 1;
        });
    });

    const labels = Object.keys(portCounts);
    const values = Object.values(portCounts);

    const ctx = document.getElementById("portsChart").getContext("2d");

    if (portsChartInstance) portsChartInstance.destroy();

    portsChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Hosts with port open",
                data: values
            }]
        }
    });
}


// -------------------------------
// INITIAL LOAD (summary + devices)
// -------------------------------
async function initialLoad() {
    const resDevices = await fetch("/api/devices");
    const devBody = await resDevices.json();

    loadDashboard(devBody.devices || devBody);
}

initialLoad();
