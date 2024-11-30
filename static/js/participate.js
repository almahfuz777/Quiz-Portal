// participate.js

let duration = window.quizDuration; // Use the global variable set by Django for the quiz duration in seconds
let countdownElement = document.getElementById("countdown");
let timerContainer = document.getElementById("timerContainer"); // Timer container element
let confirmationModal = document.getElementById("confirmationModal");
let startQuizButton = document.getElementById("startQuizButton");
let cancelButton = document.getElementById("cancelButton");
let quizForm = document.getElementById("quizForm");

function updateTimer() {
    let minutes = Math.floor(duration / 60);
    let seconds = duration % 60;
    countdownElement.innerText = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    
    if (duration <= 0) {
        // Stop timer and submit the quiz when time runs out
        clearInterval(timerInterval);
        alert("Time's up! Submitting your answers.");
        quizForm.submit(); // Automatically submit the form
    } else {
        duration--;
    }
}

// Show the confirmation modal before starting the quiz
window.onload = function () {
    confirmationModal.style.display = "block"; // Show confirmation modal
}

// Start quiz when user confirms
startQuizButton.addEventListener('click', function() {
    confirmationModal.style.display = "none"; // Hide confirmation modal
    quizForm.style.display = "block"; // Show the quiz form (questions)
    timerContainer.style.display = "block"; // Show the timer container
    timerInterval = setInterval(updateTimer, 1000); // Start the timer
});

// Cancel the quiz start
cancelButton.addEventListener('click', function() {
    window.location.href = quizHomeUrl; // Redirect to quiz home if canceled
});

// submit button clicked
document.getElementById("quizForm").addEventListener("submit", function () {
    // Stop the timer when submitting
    clearInterval(window.timerInterval);
});
