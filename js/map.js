document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map', {
        attributionControl: false
    }).setView([27.295574, 31.026373], 6);

    // Expose map for testing
    window.map = map;

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    L.control.attribution().setPrefix(
        '<a alt="A JS library for interactive maps" href="http://leafletjs.com" target="_blank">Leaflet</a>'
    ).addAttribution(
        'Map data &copy; <a target="_blank" href="http://openstreetmap.org">OpenStreetMap</a> contributors | <a target="_blank" href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a> | Imagery © <a target="_blank" href="http://mapbox.com">Mapbox</a>'
    ).addTo(map);

    // Initialize Marker Cluster Group
    const markers = L.markerClusterGroup();
    window.markers = markers;

    // Side Panel Logic
    const sidePanel = document.getElementById('side-panel');
    const panelTitle = document.getElementById('panel-title');
    const panelInfo = document.getElementById('panel-info');
    const panelLink = document.getElementById('panel-link');
    const closePanelBtn = document.getElementById('close-panel');

    const closePanel = () => {
        sidePanel.classList.remove('open');
    };

    if (closePanelBtn) {
        closePanelBtn.addEventListener('click', closePanel);
    }

    const showSidePanel = (props) => {
        console.log("Showing side panel for:", props.siteName);
        if (!sidePanel) {
            console.error("Side panel element not found!");
            return;
        }
        // Parse title from HTML (props.siteName is <h3>Name</h3>)
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = props.siteName;
        panelTitle.textContent = tempDiv.textContent || tempDiv.innerText || "Site Details";

        // Info
        panelInfo.innerHTML = `
            <div class="mb-3 text-muted">${props.timePeriod}</div>
            <div>${props.info}</div>
        `;

        // Link (props.link is <a href="...">MORE DETAILS</a>)
        tempDiv.innerHTML = props.link;
        const link = tempDiv.querySelector('a');
        if (link) {
            panelLink.href = link.getAttribute('href');
            panelLink.style.display = 'block';
        } else {
            panelLink.style.display = 'none';
        }

        sidePanel.classList.add('open');
        console.log("Side panel class added. Classes:", sidePanel.className);
    };

    // Load CSV data
    omnivore.csv('sites-popup.csv')
        .on('ready', function (layer) {
            this.eachLayer(function (marker) {
                const props = marker.toGeoJSON().properties;

                // Instead of binding popup, add click listener
                marker.on('click', () => {
                    console.log("Marker clicked!", props);
                    showSidePanel(props);
                });

                // Add to cluster group
                markers.addLayer(marker);
            });

            // Add cluster group to map
            map.addLayer(markers);
        });
});
