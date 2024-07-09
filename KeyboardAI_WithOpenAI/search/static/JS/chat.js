$(document).ready(function() {
        let typingTimer; // Timer identifier
        let doneTypingInterval = 1000; // Attendre 1000ms (1 seconde) après la frappe pour déclencher la requête

        $("#text").on("input", function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(sendRequest, doneTypingInterval);
        });

        function sendRequest() {
            let context = $("#text").val();
            $.ajax({
                headers: { "X-CSRFToken": "{{ csrf_token }}" },
                data: {
                    context: context,
                },
                type: "POST",
                url: "{% url 'search:get_suggestions' %}",
                dataType: 'json',
            }).done(function(data) {
                updateSuggestions(data.suggestions);
            });
        }

        $("#messageArea").on("submit", function(event) {
            const date = new Date();
            const hour = date.getHours();
            const minute = date.getMinutes();
            const str_time = hour + ":" + minute;
            var rawText = $("#text").val();

            var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

            $("#text").val("");
            $("#messageFormeight").append(userHtml);

            $.ajax({
                headers: { "X-CSRFToken": "{{ csrf_token }}" },
                data: {
                    msg: rawText,
                },
                type: "POST",
                url: "{% url 'search:get_response' %}",
                dataType: 'json',
            }).done(function(data) {
                var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + data.response + '<span class="msg_time">' + str_time + '</span></div></div>';
                $("#messageFormeight").append($.parseHTML(botHtml));
            });
            event.preventDefault();
        });
    });

    function updateSuggestions(suggestions) {
        // Récupérer le conteneur des suggestions
        let suggestionsContainer = document.getElementById('suggestionsContainer');

        // Vider le contenu actuel du conteneur
        suggestionsContainer.innerHTML = '';

        // Générer les divs de suggestion pour chaque suggestion reçue
        for (let i = 0; i < suggestions.length; i++) {
            let suggestionDiv = document.createElement('div');
            suggestionDiv.classList.add('suggestion');
            suggestionDiv.textContent = suggestions[i];
            suggestionDiv.onclick = function() {
                addToInput(suggestions[i]);
            };
            suggestionsContainer.appendChild(suggestionDiv);
        }
    }

    function addToInput(text) {
        var input = document.getElementById('text');
        input.value += ' ' + text;
    }