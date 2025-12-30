window.lang = window.lang || 'en';

function translatePage() {
  document.querySelectorAll('[data-key]').forEach(el => {
    const key = el.getAttribute('data-key');
    if (
      window.lang &&
      window.langData &&
      window.langData[window.lang] &&
      window.langData[window.lang][key]
    ) {
      el.textContent = window.langData[window.lang][key];
    }
  });
}

// main
document.addEventListener('DOMContentLoaded', () => {

  translatePage();

  const form = document.getElementById('cropForm');
  if (!form) return;
  const spinner = document.getElementById('spinner');
  const inputs = {
    N: document.getElementById('nitrogen'),
    P: document.getElementById('phosphorous'),
    K: document.getElementById('potassium'),
    temperature: document.getElementById('temperature'),
    humidity: document.getElementById('humidity'),
    ph: document.getElementById('ph'),
    rainfall: document.getElementById('rainfall')
    
  };

  const ranges = {
    nitrogen: [0, 140],
    phosphorous: [5, 145],
    potassium: [5, 205],
    temperature: [-10, 50],
    humidity: [0, 100],
    ph: [0, 14],
    rainfall: [0, 4000],
  };

  form.addEventListener('submit', function (event) {
    event.preventDefault(); // 

    let valid = true;

    Object.keys(ranges).forEach(id => {
      const input = document.getElementById(id);
      const error = document.getElementById(id + 'Error');
      const value = input.value.trim();
      const [min, max] = ranges[id];

      if (value === '' || isNaN(value) || value < min || value > max) {
        error.textContent = `Value must be between ${min} and ${max}`;
        error.classList.remove('hidden');
        input.classList.add('error');
        valid = false;
      } else {
        error.textContent = '';
        error.classList.add('hidden');
        input.classList.remove('error');
      }
    });

    if (!valid) return; 
    spinner.classList.remove('hidden');
    const payload = {
      N: Number(inputs.N.value),
      P: Number(inputs.P.value),
      K: Number(inputs.K.value),
      temperature: Number(inputs.temperature.value),
      humidity: Number(inputs.humidity.value),
      ph: Number(inputs.ph.value),
      rainfall: Number(inputs.rainfall.value)

      
    };

    console.log('CROP PAYLOAD:', payload);

    fetch('/recommend_crop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(r => r.json())
      .then(data => {
        spinner.classList.add('hidden');
        const resultDiv = document.getElementById('crop-result');
        if (data.recommended_crop && resultDiv) {
          resultDiv.textContent = 'Recommended Crop: ' + data.recommended_crop;
          resultDiv.classList.add('visible');
        }
      })
      .catch(err => {
        spinner.classList.add('hidden');
        console.error('Crop error:', err);
      });
  });
});
