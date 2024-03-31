document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('recommendForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var movieInput = document.getElementById('movieInput');
            if (movieInput) {
                var movie = movieInput.value;
                fetch('/recommend', {
                    method: 'POST',
                    body: new URLSearchParams({ movie: movie }),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    var recommendations = data.recommendations;
                    var recommendationsHTML = '<h2>Recommendations</h2>';
                    recommendations.forEach(function(title) {
                        recommendationsHTML += '<p>' + title + '</p>';
                    });
                    var recommendationsContainer = document.getElementById('recommendations');
                    if (recommendationsContainer) {
                        recommendationsContainer.innerHTML = recommendationsHTML;
                    } else {
                        console.error("Element with ID 'recommendations' not found.");
                    }
                })
                .catch(error => {
                    console.error("Error fetching recommendations:", error);
                });
            } else {
                console.error("Element with ID 'movieInput' not found.");
            }
        });
    } else {
        console.error("Form element with ID 'recommendForm' not found.");
    }
});
