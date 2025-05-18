const map = L.map('map').setView([20.5937, 78.9629], 5); // Default India coordinates

// Add Tile Layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Routing Control
const routingControl = L.Routing.control({
    waypoints: [],
    routeWhileDragging: true,
    show: false,
    lineOptions: {
        styles: [{
            color: 'green',
            weight: 10,
            opacity: 0.6
        }]
    }
}).addTo(map);

// Traffic Icons
const trafficIcons = {
    'कम': L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    }),
    'मध्यम': L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    }),
    'अधिक': L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    }),
    'बहुत अधिक': L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    }),
    'default': L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
    })
};

// 🔽 Get time from form
function getUserSelectedTime() {
    const timeInput = document.querySelector('input[name="time"]');
    return timeInput ? timeInput.value : null;
}

// 🔄 Map Click Handler
function sendMapClickToBackend(lat, lng) {
    const userTime = getUserSelectedTime();  // 🔸 Get user time if provided

    const clickData = {
        latitude: lat,
        longitude: lng,
        timestamp: new Date().toISOString(),
        time: userTime  
    };

    const loadingPopup = L.popup()
        .setLatLng([lat, lng])
        .setContent('<div class="loading-spinner">Data Loading ...</div>')
        .openOn(map);

    fetch('/api/map-click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(clickData)
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        map.closePopup(loadingPopup);

        if (data.success && data.prediction) {
            const trafficDensity = data.prediction.traffic_density || 'कम';
            const travelTime = data.prediction.estimated_travel_time || 'अज्ञात';

            const icon = trafficIcons[trafficDensity] || trafficIcons.default;

            const marker = L.marker([lat, lng], { icon: icon }).addTo(map);

            const popupContent = `
                <div class="prediction-popup">
                    <h3>यातायात जानकारी</h3>
                    <div class="prediction-info">
                        <p><strong>Traffic Condition</strong> ${trafficDensity}</p>
                        <p><strong>Lat/Lon:</strong> ${lat.toFixed(4)}, ${lng.toFixed(4)}</p>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent).openPopup();
        } else {
            L.marker([lat, lng]).addTo(map)
                .bindPopup(`<b>त्रुटि:</b> ${data.error || 'कोई पूर्वानुमान उपलब्ध नहीं'}`)
                .openPopup();
        }
    })
    .catch(error => {
        map.closePopup(loadingPopup);
        L.popup()
            .setLatLng([lat, lng])
            .setContent(`<b>त्रुटि:</b> ${error.message}`)
            .openOn(map);
    });
}

// Map click listener
map.on('click', function(e) {
    const clickedLat = e.latlng.lat;
    const clickedLng = e.latlng.lng;
    sendMapClickToBackend(clickedLat, clickedLng);
});

// 🔁 Form Submit Handler
document.getElementById('routeForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    navigator.geolocation.getCurrentPosition(async (position) => {
        const currentLat = position.coords.latitude;
        const currentLng = position.coords.longitude;

        const destination = document.querySelector('input[name="destination"]').value;

        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(destination)}`);
        const data = await response.json();

        if (data.length > 0) {
            const destLat = parseFloat(data[0].lat);
            const destLng = parseFloat(data[0].lon);

            routingControl.setWaypoints([
                L.latLng(currentLat, currentLng),
                L.latLng(destLat, destLng)
            ]);

            routingControl.on('routesfound', function(e) {
                const routes = e.routes;
                const summary = routes[0].summary;
                // Optional: Show summary info
            });
        } else {
            alert('Destination not found!');
        }
    }, (error) => {
        alert('Error getting your location: ' + error.message);
    });
});



