// ----------------------------
// State
// ----------------------------
let userScore = 0;
let modelScore = 0;
let currentTrueLabel = null;
let currentModelPrediction = null;

// DOM
const imageEl = document.getElementById("mushroomImage");
const resultEl = document.getElementById("resultArea");
const userScoreEl = document.getElementById("userScore");
const modelScoreEl = document.getElementById("modelScore");

// ----------------------------
// Fetch new mushroom from backend
// ----------------------------
async function loadRandomMushroom() {

    try {
        const response = await fetch("/get_image");
        const data = await response.json();

        console.log(data);

        // Save truth + model prediction
        currentTrueLabel = data.true_label;
        currentModelPrediction = data.model_prediction;

        // Show image
        imageEl.src = data.image_path;

        resultEl.innerHTML = "<p>Make your guess!</p>";

    } catch (error) {
        console.error("Error loading mushroom:", error);
    }
}

// ----------------------------
// Handle user guess
// ----------------------------
function handleGuess(userGuess) {

    if (!currentTrueLabel) return;

    // Update user score
    if (userGuess === currentTrueLabel) {
        userScore++;
    }

    // Update model score
    if (currentModelPrediction === currentTrueLabel) {
        modelScore++;
    }

    // Update UI
    userScoreEl.textContent = userScore;
    modelScoreEl.textContent = modelScore;

    resultEl.innerHTML = `
        <p><strong>Correct:</strong> ${currentTrueLabel}</p>
        <p><strong>You guessed:</strong> ${userGuess}</p>
        <p><strong>Model guessed:</strong> ${currentModelPrediction}</p>
    `;
}

// ----------------------------
// Button Events
// ----------------------------
document.querySelector(".edible").onclick = () => handleGuess("edible");
document.querySelector(".poisonous").onclick = () => handleGuess("poisonous");
document.querySelector(".next").onclick = loadRandomMushroom;

// Load first mushroom on page load
loadRandomMushroom();
