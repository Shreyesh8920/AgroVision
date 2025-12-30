document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('fertiliserForm');
    const formInputs = document.querySelectorAll('input, select');
    const submitBtn = document.getElementById('submitBtn');
    const loader = document.getElementById('loader');
    const resultBox = document.getElementById('resultBox');
    const resultText = document.getElementById('resultText');
    const btnText = document.getElementById('btnText');
    // Live validation
    formInputs.forEach(input => {
        input.addEventListener('input', () => {
            const errorMsg = input.nextElementSibling?.nextElementSibling || input.nextElementSibling;
            let valid = true;

            if (input.tagName.toLowerCase() === 'select' && (input.value === 'Select…' || input.value === '')) {
                valid = false;
            } else if (input.tagName.toLowerCase() === 'input' && !input.value.trim()) {
                valid = false;
            } else if (!input.checkValidity()) {
                valid = false;
            }

            if (valid) {
                input.classList.remove('border-red-500');
                input.classList.add('border-green-500');
                if (errorMsg) errorMsg.classList.add('hidden');
            } else {
                input.classList.remove('border-green-500');
            }
        });
    });

    // Submit handler
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        let isValid = true;

        // validation
        formInputs.forEach(input => {
            const errorMsg = input.nextElementSibling?.nextElementSibling || input.nextElementSibling;
            let valid = true;

            if (input.tagName.toLowerCase() === 'select' && (input.value === 'Select…' || input.value === '')) {
                valid = false;
                if (errorMsg) {
                    errorMsg.textContent = 'This field cannot be empty';
                    errorMsg.classList.remove('hidden');
                }
                input.classList.add('border-red-500');
                input.classList.remove('border-green-500');
            } else if (input.tagName.toLowerCase() === 'input' && !input.value.trim()) {
                valid = false;
                if (errorMsg) {
                    errorMsg.textContent = 'This field cannot be empty';
                    errorMsg.classList.remove('hidden');
                }
                input.classList.add('border-red-500');
                input.classList.remove('border-green-500');
            } else if (!input.checkValidity()) {
                valid = false;
                input.classList.add('border-red-500');
                input.classList.remove('border-green-500');
                if (errorMsg) {
                    errorMsg.classList.remove('hidden');
                    if (input.validity.valueMissing) {
                        errorMsg.textContent = 'This field cannot be empty';
                    } else if (input.validity.rangeOverflow || input.validity.rangeUnderflow) {
                        errorMsg.textContent = `Value must be between ${input.min} and ${input.max}`;
                    } else if (input.validity.stepMismatch) {
                        errorMsg.textContent = 'Please enter a valid decimal value';
                    }
                }
            } else {
                input.classList.remove('border-red-500');
                input.classList.add('border-green-500');
                if (errorMsg) errorMsg.classList.add('hidden');
            }

            if (!valid) isValid = false;
        });

        if (!isValid) return;
        loader.classList.remove('hidden');
        resultBox.classList.add('hidden');
        btnText.textContent = 'Processing...';
        submitBtn.disabled = true;

        const data = {};
        formInputs.forEach(input => {
            if (!input.name) return; 

            if (input.type === 'number') {
                data[input.name] = Number(input.value);
            } else {
                data[input.name] = input.value;
            }
        });

        try {
            const response = await fetch(
                '/recommend_fertilizer',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                }
            );

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            submitBtn.disabled = false;
            btnText.textContent = 'Get Fertilizer Recommendation';
            loader.classList.add('hidden');
            if (result.recommended_fertilizer) {
                resultText.textContent = result.recommended_fertilizer;
                resultBox.classList.remove('hidden');
            } else {
                resultText.textContent = 'No recommendation received';
                resultBox.classList.remove('hidden');
            }

        } catch (error) {
            loader.classList.add('hidden');
            submitBtn.disabled = false;
            btnText.textContent = 'Get Fertilizer Recommendation';

            resultText.textContent = 'Error while fetching recommendation';
            resultBox.classList.remove('hidden');

        }
    });
});
