let cachedLat = null;
let cachedLon = null;
let weatherInterval = null;

async function fetchData(location) {
  function setValue(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? '';
  }

  try {
    let url = '';
    if (location && typeof location === 'string') {
      //url = `http://127.0.0.1:5100/collect?location=${encodeURIComponent(location)}`;
      url = `/collect?location=${encodeURIComponent(location)}`;

    } else if (location && location.lat != null && location.lon != null) {
      //url = `http://127.0.0.1:5100/collect?lat=${location.lat}&lon=${location.lon}`;
      url = `/collect?lat=${location.lat}&lon=${location.lon}`;

    } else {
      throw new Error('Invalid location parameter');
    }

    const response = await fetch(url);
    if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
    const data = await response.json();

    const todayStr = new Date().toLocaleDateString(undefined, { year:'numeric', month:'short', day:'numeric' });
    function getSeason(date){
      const m = date.getMonth() + 1;
      if (m === 12 || m <= 2) return 'Winter';
      else if (m <= 5) return 'Spring';
      else if (m <= 8) return 'Summer';
      else return 'Autumn';
    }
    const seasonStr = getSeason(new Date());

    let locationName = 'Unknown Location';
    if (location && typeof location === 'object' && location.lat != null && location.lon != null) {
      try {
        const geoResponse = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${location.lat}&lon=${location.lon}`);
        if (geoResponse.ok) {
          const geoData = await geoResponse.json();
          const addr = geoData.address || {};
          locationName = addr.city || addr.town || addr.village || addr.county || addr.state || addr.country || 'Unknown Location';
        }
      } catch (geoErr) {
        console.error('Error fetching location name:', geoErr);
      }
    } else if (typeof location === 'string') {
      locationName = location;
    }

    // Safely format values with units or fallback to 'N/A'
    setValue('temp-value', data.temperature != null ? `${data.temperature} °C` : 'N/A');
    setValue('humidity-value', data.humidity != null ? `${data.humidity} %` : 'N/A');
    setValue('rainfall-value', data.rainfall != null ? `${data.rainfall} mm` : 'N/A');
    setValue('wind-value', data.wind_speed != null ? `${data.wind_speed} km/h` : 'N/A');

    // Update other dashboard cards if any
    const cardMap = [
      {id:'card-today', value: todayStr},
      {id:'card-season', value: seasonStr},
      {id:'card-weather', value: data.weather ?? (data.rainfall > 0 ? 'Rainy' : 'Clear')},
      {id:'card-soil-moisture', value: data.soil_moisture != null ? data.soil_moisture : 'N/A'},
      {id:'card-field-location', value: locationName},
      {id:'card-uv-index', value: data.uv_index != null ? data.uv_index : 'N/A'},
      {id:'card-sunrise', value: data.sunrise ?? 'N/A'},
      {id:'card-sunset', value: data.sunset ?? 'N/A'},
      {id:'card-precipitation', value: data.rainfall != null ? data.rainfall : 'N/A'},
      {id:'card-location-name', value: locationName}
    ];
    cardMap.forEach(c => {
      const el = document.getElementById(c.id);
      if (el) {
        const valEl = el.querySelector('.card-value');
        if (valEl) valEl.textContent = c.value;
      }
    });

  } catch(e) {
    ['temp-value','humidity-value','rainfall-value','wind-value'].forEach(id => setValue(id, 'N/A'));
    console.error('Error fetching data:', e);
  }
}

window.addEventListener('load', () => {
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        cachedLat = pos.coords.latitude;
        cachedLon = pos.coords.longitude;

        // Initial fetch
        fetchData({ lat: cachedLat, lon: cachedLon });

        // Refresh weather every 10 minutes (OPTION 2)
        if (!weatherInterval) {
          weatherInterval = setInterval(() => {
            fetchData({ lat: cachedLat, lon: cachedLon });
          }, 10 * 60 * 1000); // 10 minutes
        }
      },
      err => {
        console.warn('Geolocation error or permission denied:', err);
        const manualLocation = prompt(
          'Location permission denied or unavailable. Please enter your city/location:'
        );
        if (manualLocation && manualLocation.trim()) {
          fetchData(manualLocation.trim());
        } else {
          ['temp-value','humidity-value','rainfall-value','wind-value'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.textContent = 'N/A';
          });
        }
      },
      { timeout: 10000 }
    );
  } else {
    ['temp-value','humidity-value','rainfall-value','wind-value'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.textContent = 'N/A';
    });
  }
});

// === Language Support ===
const translations = {
  en: {
    temperatureLabel: "Temperature",
    humidityLabel: "Humidity",
    rainfallLabel: "Rainfall",
    windLabel: "Wind Speed",
  },
  hi: {
    temperatureLabel: "तापमान",
    humidityLabel: "नमी",
    rainfallLabel: "वर्षा",
    windLabel: "पवन गति",
  }
};

function applyLanguage(lang) {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translations[lang] && translations[lang][key]) {
      el.textContent = translations[lang][key];
    }
  });
}

window.applyLanguage = applyLanguage;