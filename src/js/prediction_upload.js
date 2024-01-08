document.addEventListener("DOMContentLoaded", function() {
    setTitleWithCurrentDate();
    fetch('src/predictions.json')
        .then(response => response.json())
        .then(data => {
            const uniqueData = removeDuplicates(data);
            displayPredictions(uniqueData);
        })
        .catch(error => console.error('Error:', error));
});

function setTitleWithCurrentDate() {
    const titleElement = document.getElementById('title');
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    titleElement.textContent = `NHL Game Predictions for ${formattedDate}`;
}

function removeDuplicates(data) {
    const unique = [];
    const seenVenues = new Set();

    data.forEach(item => {
        if (!seenVenues.has(item.venue)) {
            seenVenues.add(item.venue);
            unique.push(item);
        }
    });

    return unique;
}

function displayPredictions(predictions) {
    const container = document.getElementById('predictions');
    predictions.forEach(prediction => {
        const homeTeamChance = prediction['home team percentage chance of winning'] || 'N/A';
        const awayTeamChance = prediction['away team percentage chance of winning'] || 'N/A';
        const predictedHomeGoals = prediction['predicted home team goals'] !== undefined 
            ? prediction['predicted home team goals']
            : 'N/A';
        const predictedAwayGoals = prediction['predicted away team goals'] !== undefined 
            ? prediction['predicted away team goals']
            : 'N/A';
        const confidenceRating = prediction['confidence rating']
            ? prediction['confidence rating'].charAt(0).toUpperCase() + prediction['confidence rating'].slice(1)
            : 'Unknown';
        const confidenceClass = getConfidenceClass(prediction['confidence rating']);
        const confidenceElement = `<span class="confidence ${confidenceClass}">Confidence: ${confidenceRating}</span>`;

        const predictionElement = document.createElement('div');
        predictionElement.className = 'prediction';
        predictionElement.innerHTML = `
            <h2>${prediction.venue} (${prediction['home team name']} vs ${prediction['away team name']})</h2>
            <div class="detail-section">
                <p><strong>Home Team:</strong> ${prediction['home team name']} - Chance of Winning: ${homeTeamChance}</p>
                <p><strong>Away Team:</strong> ${prediction['away team name']} - Chance of Winning: ${awayTeamChance}</p>
            </div>
            <div class="detail-section">
                <p><strong>Predicted Score:</strong> ${prediction['home team name']} ${predictedHomeGoals} - ${prediction['away team name']} ${predictedAwayGoals}</p>
            </div>
            <div class="reason-section">
                <p class="reason"><strong>Key Factors:</strong> ${prediction['key factors'] ? prediction['key factors'] : 'N/A'}</p>
            </div>
            <div class="reason-section">
                <p class="reason"><strong>Opposition:</strong> ${prediction['opposition'] ? prediction['opposition'] : 'N/A'}</p>
            </div>
            <div class="reason-section">
                <p class="reason"><strong>Simulation Results:</strong> ${prediction['simulation results'] ? prediction['simulation results'] : 'N/A'}</p>
            </div>
            <div class="reason-section">
                <p class="reason"><strong>Other Factors:</strong> ${prediction['other factors'] ? prediction['other factors'] : 'N/A'}</p>
            </div>
            ${confidenceElement}
        `;
        container.appendChild(predictionElement);
    });
}

function getConfidenceClass(confidenceRating) {
    switch (confidenceRating.toLowerCase()) {
        case 'high':
            return 'high-confidence';
        case 'medium':
            return 'medium-confidence';
        case 'low':
            return 'low-confidence';
        default:
            return '';
    }
}
