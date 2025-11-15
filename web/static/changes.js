document.addEventListener("DOMContentLoaded", () => {
    loadChanges();
});

function loadChanges() {
    document.getElementById("loading_changes").style.display = "block";

    fetch("/api/changes")
        .then(res => res.json())
        .then(data => {
            document.getElementById("loading_changes").style.display = "none";
            document.getElementById("changes_content").style.display = "block";

            loadNewDevices(data.new_devices);
            loadRemovedDevices(data.removed_devices);
            loadPortChanges(data.port_changes);
        });
}

function loadNewDevices(list) {
    const ul = document.getElementById("new_devices");
    ul.innerHTML = "";

    if (list.length === 0) {
        ul.innerHTML = `<li class="list-group-item">No new devices</li>`;
        return;
    }

    list.forEach(ip => {
        ul.innerHTML += `
            <li class="list-group-item list-group-item-success">
                + ${ip}
            </li>
        `;
    });
}

function loadRemovedDevices(list) {
    const ul = document.getElementById("removed_devices");
    ul.innerHTML = "";

    if (list.length === 0) {
        ul.innerHTML = `<li class="list-group-item">No removed devices</li>`;
        return;
    }

    list.forEach(ip => {
        ul.innerHTML += `
            <li class="list-group-item list-group-item-danger">
                - ${ip}
            </li>
        `;
    });
}

function loadPortChanges(list) {
    const ul = document.getElementById("port_changes");
    ul.innerHTML = "";

    if (list.length === 0) {
        ul.innerHTML = `<li class="list-group-item">No port changes</li>`;
        return;
    }

    list.forEach(change => {
        ul.innerHTML += `
            <li class="list-group-item list-group-item-warning">
                <strong>${change.ip}</strong><br>
                Opened: ${change.opened.join(", ") || "None"}<br>
                Closed: ${change.closed.join(", ") || "None"}
            </li>
        `;
    });
}
