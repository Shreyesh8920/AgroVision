// document.addEventListener('DOMContentLoaded', function() {
//     // Form validation
//     const formInputs = document.querySelectorAll('input, select');
//     const submitBtn = document.getElementById('submitBtn');
//     const resultContainer = document.getElementById('fertilizer-result');
    
//     // Add input/change event listeners for live validation feedback
//     formInputs.forEach(input => {
//         input.addEventListener('input', () => {
//             const errorMsg = input.nextElementSibling?.nextElementSibling || input.nextElementSibling;
//             let valid = true;

//             if (input.tagName.toLowerCase() === 'select' && (input.value === 'Select…' || input.value === '')) {
//                 valid = false;
//             } else if (input.tagName.toLowerCase() === 'input' && !input.value.trim()) {
//                 valid = false;
//             } else if (!input.checkValidity()) {
//                 valid = false;
//             }

//             if (valid) {
//                 input.classList.remove('border-red-500');
//                 input.classList.add('border-green-500');
//                 if (errorMsg) errorMsg.classList.add('hidden');
//             } else {
//                 input.classList.remove('border-green-500');
//             }
//         });
//     });
    
//     // Submit button handler
//     submitBtn.addEventListener('click', async function(e) {
//         e.preventDefault();
        
//         let isValid = true;
//         formInputs.forEach(input => {
//             const errorMsg = input.nextElementSibling?.nextElementSibling || input.nextElementSibling;
//             let valid = true;

//             if (input.tagName.toLowerCase() === 'select' && (input.value === 'Select…' || input.value === '')) {
//                 valid = false;
//                 if (errorMsg) {
//                     errorMsg.textContent = 'This field cannot be empty';
//                     errorMsg.classList.remove('hidden');
//                 }
//                 input.classList.add('border-red-500');
//                 input.classList.remove('border-green-500');
//             } else if (input.tagName.toLowerCase() === 'input' && !input.value.trim()) {
//                 valid = false;
//                 if (errorMsg) {
//                     errorMsg.textContent = 'This field cannot be empty';
//                     errorMsg.classList.remove('hidden');
//                 }
//                 input.classList.add('border-red-500');
//                 input.classList.remove('border-green-500');
//             } else if (!input.checkValidity()) {
//                 valid = false;
//                 input.classList.add('border-red-500');
//                 input.classList.remove('border-green-500');
//                 if (errorMsg) {
//                     errorMsg.classList.remove('hidden');
//                     if (input.validity.valueMissing) {
//                         errorMsg.textContent = 'This field cannot be empty';
//                     } else if (input.validity.rangeOverflow || input.validity.rangeUnderflow) {
//                         if (input.step === '0.1') {
//                             errorMsg.textContent = `Value must be between ${parseFloat(input.min).toFixed(1)} and ${parseFloat(input.max).toFixed(1)}`;
//                         } else {
//                             errorMsg.textContent = `Value must be between ${input.min} and ${input.max}`;
//                         }
//                     } else if (input.validity.stepMismatch) {
//                         errorMsg.textContent = 'Please enter a valid decimal value';
//                     }
//                 }
//             } else {
//                 input.classList.remove('border-red-500');
//                 input.classList.add('border-green-500');
//                 if (errorMsg) errorMsg.classList.add('hidden');
//             }

//             if (!valid) {
//                 isValid = false;
//             }
//         });
        
//         if (isValid) {
//             // Gather input data
//             const data = {};
//             formInputs.forEach(input => {
//                 data[input.name] = input.value;
//             });

//             try {
//                 const response = await fetch('/recommend_fertilizer', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                     body: JSON.stringify(data)
//                 });

//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }

//                 const result = await response.json();

//                 if (result.recommended_fertilizer) {
//                     if (resultContainer) {
//                         resultContainer.textContent = `Recommended Fertilizer: ${result.recommended_fertilizer}`;
//                     }
//                 } else {
//                     if (resultContainer) {
//                         resultContainer.textContent = 'No recommendation received from the server.';
//                     }
//                 }
//             } catch (error) {
//                 if (resultContainer) {
//                     resultContainer.textContent = 'Error occurred while fetching recommendation: ' + error.message;
//                 }
//             }
//         }
//     });
    
//     // Remove validateInput function and input/change event listeners
// });



document.addEventListener('DOMContentLoaded', function () {

    const formInputs = document.querySelectorAll('input, select');
    const submitBtn = document.getElementById('submitBtn');
    const resultContainer = document.getElementById('fertilizer-result');

    // Live validation (UNCHANGED)
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
    submitBtn.addEventListener('click', async function (e) {
        e.preventDefault();

        let isValid = true;

        // Validation (UNCHANGED)
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

        // ================= FIXED PART START =================

        const data = {};
        formInputs.forEach(input => {
            if (!input.name) return; // safety

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

            if (result.recommended_fertilizer) {
                resultContainer.textContent =
                    `Recommended Fertilizer: ${result.recommended_fertilizer}`;
            } else {
                resultContainer.textContent =
                    'No recommendation received from the server.';
            }

        } catch (error) {
            resultContainer.textContent =
                'Error occurred while fetching recommendation: ' + error.message;
        }

        // ================= FIXED PART END =================
    });
});
