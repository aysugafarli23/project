var tag = document.createElement('script');

		tag.src = "https://youglish.com/public/emb/widget.js";
		var firstScriptTag = document.getElementsByTagName('script')[0];
		firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

		// 3. This function creates a widget after the API code downloads.
		var widget;
		function onYouglishAPIReady() {
			widget = new YG.Widget("widget-1", {
				components : 8408 //search box & caption 
			});
		}

		
	    function handleKeyPress(event) {
            if (event.key === 'Enter') {
                handleSearch();
            }
        }
	    
	    function handleSearch() {
			var inputText = document.getElementById('searchInput').value;
			widget.fetch(inputText, "english"); // Fetch the results for the initial search term
		}