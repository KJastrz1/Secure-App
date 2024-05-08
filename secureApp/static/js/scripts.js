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
        const strengthCategory = categorize_strength(entropy);
        const requirements = check_requirements(password);

        strengthDiv.innerText = `Password Strength: ${strengthCategory}`;
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
            return 'Strong';
        } else if (entropy >= medium_entropy_threshold) {
            return 'Medium';
        } else {
            return 'Weak';
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
                <li style="color: ${requirements.digit ? 'green' : 'red'};">At least one digit</li>
                <li style="color: ${requirements.letter ? 'green' : 'red'};">At least one letter</li>
                <li style="color: ${requirements.specialChar ? 'green' : 'red'};">At least one special character</li>
                <li style="color: ${requirements.length ? 'green' : 'red'};">At least 8 characters long</li>
            </ul>
        `;
    }

    

});
