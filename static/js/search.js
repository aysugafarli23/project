// Load the Youglish widget API asynchronously
var tag = document.createElement('script');
tag.src = "https://youglish.com/public/emb/widget.js";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// Function to get query parameter from URL
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

// Function to create a widget after the API code downloads
var widget;
function onYouglishAPIReady() {
  const searchTerm = getQueryParam('q') || 'courage'; // Default to 'courage' if no query parameter
  widget = new YG.Widget("widget-1", {
    width: 640,
    border: 'none',
    components: 8265, // search box & caption & All captions
    events: {
      'onFetchDone': onFetchDone,
      'onVideoChange': onVideoChange,
      'onCaptionConsumed': onCaptionConsumed
    },
    controls: true,
    captionColor: '#212529',
    captionSize: 20,
    markerColor: 'transparent',
    linkColor: 'white',
    keywordColor: 'orange',
    initialSearchTerm: searchTerm // Set the initial search term from the query parameter
  });
  widget.fetch(searchTerm, "english"); // Fetch the results for the initial search term
}

// Debugging helper function to ensure the widget API is loaded
function checkYouglishAPI() {
  if (typeof YG === 'undefined') {
    console.error('Youglish API not loaded.');
  } else {
    console.log('Youglish API loaded successfully.');
    onYouglishAPIReady();
  }
}

// Ensure the Youglish API is ready before executing
window.onload = function() {
  setTimeout(checkYouglishAPI, 1000);
};

var views = 0, curTrack = 0, totalTracks = 0;

// The API will call this method when the search is done
function onFetchDone(event) {
  if (event.totalResult === 0) alert("No result found");
  else totalTracks = event.totalResult;
}

// The API will call this method when switching to a new video.
function onVideoChange(event) {
  curTrack = event.trackNumber;
  views = 0;
}

// The API will call this method when a caption is consumed.
function onCaptionConsumed(event) {
  if (++views < 3)
    widget.replay();
  else if (curTrack < totalTracks)
    widget.next();
}

// Function to handle search input
function handleSearch(query) {
  if (query) {
    window.location.href = `search/?q=${encodeURIComponent(query)}`;
  } else {
    alert("Please enter a word to search.");
  }
}


// Initialize event listeners for the dictionary page
function initializeDictPage() {
  document.querySelector('.searchBtn').addEventListener('click', function() {
    const query = document.getElementById('dictInput').value.trim();
    handleSearch(query);
  });

  document.querySelector('#helloBtn').addEventListener('click', function() {
    handleSearch('hello');
  });

  document.querySelector('#worldBtn').addEventListener('click', function() {
    handleSearch('world');
  });
}

// Initialize event listeners for the search page
function initializeSearchPage() {
  const searchTerm = getQueryParam('q') || 'courage'; // Default to 'courage' if no query parameter
  const searchInput = document.querySelector('#widget-1 input'); // Adjust the selector based on the widget's search input

  if (searchInput) {
    searchInput.value = searchTerm;
  }
}

document.addEventListener("DOMContentLoaded", function() {
  if (document.querySelector('.dict__content')) {
    initializeDictPage();
  } else if (document.querySelector('#widget-1')) {
    initializeSearchPage();
  }
});