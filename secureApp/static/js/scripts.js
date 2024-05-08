window.onload = function () {
    setTimeout(function () {
        var exclamationMarks = document.getElementsByClassName('exclamation-mark');
        for (var i = 0; i < exclamationMarks.length; i++) {
            exclamationMarks[i].style.opacity = '0';
        }
    }, 1500);
};



document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.getElementById('password');
    const strengthDiv = document.getElementById('password-strength');
    const requirementsDiv = document.getElementById('password-requirements');

    passwordField.addEventListener('input', function () {
        const password = passwordField.value;
        const entropy = calculate_entropy(password);
        categorize_strength(entropy);
        const requirements = check_requirements(password);       
        update_requirements_ui(requirements);
    });

    function calculate_entropy(password) {
        const character_set_size = 95;
        const entropy = password.length * Math.log2(character_set_size);
        return entropy;
    }

    function categorize_strength(entropy) {
        const strong_entropy_threshold = 70;
        const medium_entropy_threshold = 50;
        if (entropy >= strong_entropy_threshold) {
            strengthDiv.innerHTML = `<p class='text-green-600'>Strong</p>`;
        } else if (entropy >= medium_entropy_threshold) {
            strengthDiv.innerHTML = `<p class='text-orange-600'>Medium</p>`;
        } else {
            strengthDiv.innerHTML = `<p class='text-red-600'>Weak</p>`;
        }
    }

    function check_requirements(password) {
        return {
            digit: /\d/.test(password),
            letter: /[a-zA-Z]/.test(password),
            specialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
            length: password.length >= 8
        };
    }

    function update_requirements_ui(requirements) {
        requirementsDiv.innerHTML = `
            <ul>
                <li class="${requirements.digit ? 'text-green-600' : 'text-red-600'}">At least one digit</li>
                <li class="${requirements.letter ? 'text-green-600' : 'text-red-600'}">At least one letter</li>
                <li class="${requirements.specialChar ? 'text-green-600' : 'text-red-600'}">At least one special character</li>
                <li class="${requirements.length ? 'text-green-600' : 'text-red-600'}">At least 8 characters long</li>
            </ul>
        `;
    }
    
    var form = document.querySelector('form');

    form.addEventListener('submit', function() {
        var submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
    });

});
