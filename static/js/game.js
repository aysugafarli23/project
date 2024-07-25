const timer = document.getElementById('timer');
const cardsLength = document.querySelectorAll('.words .card').length;

let selectedCards = [];
let matchedCards = 0;
let timerInterval;
let elapsedTime = 0;


function selectCard(e) {
    const clickedCard = e.target;

    if (clickedCard.dataset.type === 'voice') {
        playVoice(clickedCard.dataset.content);
    }

    if (selectedCards.length < 2 && !selectedCards.includes(clickedCard)) {
        selectedCards.push(clickedCard);
        clickedCard.classList.add('selected');

        if (selectedCards.length === 2) {
            checkForMatch();
        }
    }
}

function checkForMatch() {
    const [card1, card2] = selectedCards;
    const isMatch = card1.dataset.id === card2.dataset.id;
    isMatch ? removeCards(card1, card2) : unmatchCards(card1, card2);
    selectedCards = [];
}

function removeCards(card1, card2) {
    card1.classList.add('matched');
    card2.classList.add('matched');
    matchedCards += 1;

    if (matchedCards === cardsLength) {
        stopTimer();
        gameOver();
    }   
}

function unmatchCards(card1, card2) {
    card1.classList.add('unmatched');
    card2.classList.add('unmatched');

    setTimeout(() => {
        card1.classList.remove('unmatched', 'selected');
        card2.classList.remove('unmatched', 'selected');
    }, 300);
}

function playVoice(text) {
    var msg = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(msg);
}


function startTimer() {
    timerInterval = setInterval(() => {
        elapsedTime++;
        timer.textContent = formatTime(elapsedTime);
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

function resetTimer() {
    clearInterval(timerInterval);
    elapsedTime = 0;
    timer.textContent = '00:00';
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function playMusic() {
    const music = document.getElementById('music');
    const iconPlay = document.getElementById('icon-play');
    const iconMute = document.getElementById('icon-mute');

    if (music.paused) {
        music.play();
        iconPlay.classList.remove('hidden');
        iconMute.classList.add('hidden');
    } else {
        music.pause();
        iconPlay.classList.add('hidden');
        iconMute.classList.remove('hidden');
    }

    music.addEventListener('ended', () => music.play());
}

function gameOver(){
    localStorage.setItem('timerValue', timer.textContent);
    const csrftoken = getCookie('csrftoken');
    const formData = new FormData();
    formData.append('new_score', elapsedTime);

    fetch('/game/gameover/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrftoken }})
    .then(() => {
        window.location.href = '/game/gameover/';
    });
}

if (document.getElementById('game-board')){
    resetTimer();
    startTimer();
}

if (document.getElementById('gameover')){
    displayTimerValue();
}

function displayTimerValue() {
    let timerValue = localStorage.getItem('timerValue');
    timer.textContent = timerValue;
}

function copyScore() {
    var gameUrl = window.location.origin + '/game';
    var score = localStorage.getItem('timerValue');
    var message = "I scored " + score + " in the match voice game. Try it out here: " + gameUrl;

    var tempInput = document.createElement("input");
    tempInput.value = message;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    CopyAlert();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function OptionsAlert(){
    Swal.fire({
        position: "top",
        title: "Options",
        html: `
            <p>Try to finish the game as fast as possible</p>
        `,
        showCloseButton: true,
        showConfirmButton: false,
    });
}

function CopyAlert(){
    Swal.fire({
        position: "center",
        icon: "success",
        title: "Link copied to clipboard!",
        showConfirmButton: false,
        timer: 1500
    });
}