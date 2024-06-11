document.querySelectorAll('.contactBtn').forEach(function(button) {
    button.addEventListener('click', function() {
        document.getElementById('contactFormContainer').style.display = 'block';
    });
});

function hideContactForm() {
    document.getElementById('contactFormContainer').style.display = 'none';
}