// Initialize Map
const map = L.map('map').setView([20.5937, 78.9629], 5); // India default

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Place marker if coordinates passed from backend
if (typeof DEST_COORDS !== 'undefined' && DEST_COORDS !== null) {
    const { lat, lng, name } = DEST_COORDS;
    window.destinationMarker = L.marker([lat, lng])
        .addTo(map)
        .bindPopup(`Destination: ${name}`).openPopup();
    map.setView([lat, lng], 13);
}

// Allow form to submit normally for Flask processing
document.getElementById('routeForm').addEventListener('submit', function (e) {
    // Let the form post - no preventDefault
});
