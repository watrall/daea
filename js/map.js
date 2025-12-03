document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map', {
        attributionControl: false
    }).setView([27.295574, 31.026373], 6);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    L.control.attribution().setPrefix(
        '<a alt="A JS library for interactive maps" href="http://leafletjs.com" target="_blank">Leaflet</a>'
    ).addAttribution(
        'Map data &copy; <a target="_blank" href="http://openstreetmap.org">OpenStreetMap</a> contributors | <a target="_blank" href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a> | Imagery © <a target="_blank" href="http://mapbox.com">Mapbox</a>'
    ).addTo(map);

    // Load CSV data
    omnivore.csv('sites-popup.csv')
        .on('ready', function (layer) {
            this.eachLayer(function (marker) {
                const props = marker.toGeoJSON().properties;
                const popupContent = `
                    ${props.timePeriod}${props.siteName}<br><br>
                    ${props.info}<br><br>
                    ${props.link}
                `;
                marker.bindPopup(popupContent, { autoPanPadding: [5, 55] });
            });
        })
        .addTo(map);
});
