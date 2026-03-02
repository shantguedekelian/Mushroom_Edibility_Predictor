// ----------------------------
// Fake dataset (for now)
// ----------------------------
const mushrooms = [
    {img: "data/mushrooms/train/edible/Agaricus/000_ePQknW8cTp8.jpg", label: "edible"},
    {img: "data/mushrooms/train/poisonous/Amanita_abrupta/Amanita_abrupta4.png", label: "poisonous"},
    {img: "data/mushrooms/train/edible/blue_roundhead/3.png", label: "edible"},
    {img: "data/mushrooms/train/poisonous/Cortinarius_cinnabarinus/Cortinarius_cinnabarinus2.png", label: "poisonous"},
];

// ----------------------------
// State
// ----------------------------
let userScore = 0;
let modelScore = 0;
let currentMushroom = null;

// DOM
const imageEl = document.getElementById("mushroomImage");
const resultEl = document.getElementById("resultArea");
const userScoreEl = document.getElementById("userScore");
const modelScoreEl = document.getElementById("modelScore");

// ----------------------------
// Load random mushroom
// ----------------------------
function loadRandomMushroom() {
    const index = Math.floor(Math.random() * mushrooms.length);
    currentMushroom = mushrooms[index];

    imageEl.src = currentMushroom.img;
    resultEl.innerHTML = "<p>Make your guess!</p>";
}

loadRandomMushroom();

function handleGuess(userGuess) {

    // Ground truth
    const correct = currentMushroom.label;

    // Simulated model guess
    const modelGuess = Math.random() > 0.5 ? "edible" : "poisonous";

    // Update user score
    if (userGuess === correct) {
        userScore++;
    }

    // Update model score
    if (modelGuess === correct) {
        modelScore++;
    }

    // Update UI
    userScoreEl.textContent = userScore;
    modelScoreEl.textContent = modelScore;

    resultEl.innerHTML = `
        <p><strong>Correct:</strong> ${correct}</p>
        <p><strong>You guessed:</strong> ${userGuess}</p>
        <p><strong>Model guessed:</strong> ${modelGuess}</p>
    `;
}
document.querySelector(".edible").onclick = () => handleGuess("edible");
document.querySelector(".poisonous").onclick = () => handleGuess("poisonous");

document.querySelector(".next").onclick = loadRandomMushroom;
