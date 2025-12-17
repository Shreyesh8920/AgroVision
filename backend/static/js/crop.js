// document.addEventListener('DOMContentLoaded', function() {
//     const nInput = document.getElementById('N');
//     const pInput = document.getElementById('P');
//     const kInput = document.getElementById('K');
//     const tempInput = document.getElementById('temperature');
//     const humidityInput = document.getElementById('humidity');
//     const phInput = document.getElementById('pH');
//     const form = document.querySelector('form');
//     const resultDiv = document.getElementById('crop-result');

//     function parseAndValidate(input, name, min, max, isInteger) {
//         if (!input) return { valid: false, value: null, name };
//         const val = input.value.trim();
//         if (val === '') return { valid: false, value: null, name };
//         let num;
//         if (isInteger) {
//             if (!/^\d+$/.test(val)) return { valid: false, value: null, name };
//             num = Number(val);
//         } else {
//             if (!/^\d*\.?\d*$/.test(val)) return { valid: false, value: null, name };
//             num = Number(val);
//         }
//         if (isNaN(num)) return { valid: false, value: null, name };
//         if (num < min || num > max) return { valid: false, value: num, name };
//         return { valid: true, value: num, name };
//     }

//     function showError(input) {
//         let errorElem = input.nextElementSibling;
//         if (!errorElem || !errorElem.classList.contains('error-message')) {
//             errorElem = document.createElement('div');
//             errorElem.className = 'error-message';
//             errorElem.style.color = 'red';
//             errorElem.style.fontSize = '0.9em';
//             errorElem.style.marginTop = '2px';
//             input.parentNode.insertBefore(errorElem, input.nextSibling);
//         }
//         errorElem.textContent = 'Enter a valid value';
//     }

//     function clearError(input) {
//         const errorElem = input.nextElementSibling;
//         if (errorElem && errorElem.classList.contains('error-message')) {
//             errorElem.textContent = '';
//         }
//     }

//     function maskIntegerInput(event) {
//         const allowedKeys = ['Backspace', 'ArrowLeft', 'ArrowRight', 'Delete', 'Tab'];
//         if (allowedKeys.includes(event.key)) return;
//         if (!/^\d$/.test(event.key)) event.preventDefault();
//     }

//     function maskDecimalInput(event, input) {
//         const allowedKeys = ['Backspace', 'ArrowLeft', 'ArrowRight', 'Delete', 'Tab'];
//         if (allowedKeys.includes(event.key)) return;
//         if (event.key === '.' && input.value.includes('.')) event.preventDefault();
//         if (!/^\d$/.test(event.key) && event.key !== '.') event.preventDefault();
//     }

//     [nInput, pInput, kInput, humidityInput].forEach(i => i && i.addEventListener('keydown', maskIntegerInput));
//     [tempInput, phInput].forEach(i => i && i.addEventListener('keydown', e => maskDecimalInput(e, i)));

//     [nInput, pInput, kInput, tempInput, humidityInput, phInput].forEach(input => {
//         if (input) input.addEventListener('input', () => clearError(input));
//     });

//     if (form) {
//         form.addEventListener('submit', function(event) {
//             event.preventDefault();
//             const inputsToValidate = [
//                 {input: nInput, name: 'N', min: 0, max: 100, isInteger: true},
//                 {input: pInput, name: 'P', min: 0, max: 100, isInteger: true},
//                 {input: kInput, name: 'K', min: 0, max: 100, isInteger: true},
//                 {input: tempInput, name: 'Temperature', min: 0, max: 50, isInteger: false},
//                 {input: humidityInput, name: 'Humidity', min: 0, max: 100, isInteger: true},
//                 {input: phInput, name: 'pH', min: 0, max: 14, isInteger: false}
//             ];

//             let allValid = true;
//             const values = {};

//             for (const item of inputsToValidate) {
//                 const result = parseAndValidate(item.input, item.name, item.min, item.max, item.isInteger);
//                 if (!result.valid) {
//                     allValid = false;
//                     showError(item.input);
//                     item.input.focus();
//                     break;
//                 }
//                 values[item.name.toLowerCase()] = result.value;
//             }

//             if (allValid) {
//                 fetch('http://127.0.0.1:5500/recommend_crop', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify(values)
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.recommended_crop) {
//                         resultDiv.textContent = 'Recommended Crop: ' + data.recommended_crop;
//                     } else {
//                         resultDiv.textContent = 'Error: No recommendation received';
//                     }
//                 })
//                 .catch(err => {
//                     console.error('Error fetching crop recommendation:', err);
//                     resultDiv.textContent = 'Error fetching crop recommendation. Check console.';
//                 });
//             }
//         });
//     }
// });

console.log("CROP.JS LOADED");

document.addEventListener('DOMContentLoaded', function () {

  const form = document.getElementById('cropForm');

  // Correct input IDs (match crop.html exactly)
  const nitrogenInput     = document.getElementById('nitrogen');
  const phosphorousInput  = document.getElementById('phosphorous');
  const potassiumInput    = document.getElementById('potassium');
  const temperatureInput  = document.getElementById('temperature');
  const humidityInput     = document.getElementById('humidity');
  const rainfallInput     = document.getElementById('rainfall');
  const phInput           = document.getElementById('ph');

  if (!form) return;


  form.addEventListener('submit', function () {
    if (!window.isCropFormValid) {
        return;
    }
    // Do NOT preventDefault here (HTML already handles it)
    // We agreed to fix submit flow later

    // Safety check
    if (
      !nitrogenInput || !phosphorousInput || !potassiumInput ||
      !temperatureInput || !humidityInput || !rainfallInput || !phInput
    ) {
      console.error('One or more input elements not found');
      return;
    }

    // Build payload EXACTLY as backend expects
    const payload = {
      N: Number(nitrogenInput.value),
      P: Number(phosphorousInput.value),
      K: Number(potassiumInput.value),
      temperature: Number(temperatureInput.value),
      humidity: Number(humidityInput.value),
      ph: Number(phInput.value),
      rainfall: Number(rainfallInput.value)
    };

    // Optional: log to verify
    console.log('CROP PAYLOAD:', payload);

    fetch('/recommend_crop', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
      console.log('CROP RESPONSE:', data);

      // Result rendering (if you add a result div later)
      const resultDiv = document.getElementById('crop-result');
      if (resultDiv && data.recommended_crop) {
        resultDiv.textContent = 'Recommended Crop: ' + data.recommended_crop;
      }
    })
    .catch(error => {
      console.error('Crop recommendation error:', error);
    });

  });

});
