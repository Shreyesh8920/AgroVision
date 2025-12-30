// lang.js
const translations = {
  en: {
    //crop.html
    crop_heading: "Crop Recommendation",
    crop_input_soil: "Soil Type",
    crop_input_nitrogen: "Nitrogen (N)",
    crop_input_phosphorus: "Phosphorus (P)",
    crop_input_potassium: "Potassium (K)",
    crop_input_temp: "Temperature (°C)",
    crop_input_rainfall: "Rainfall (mm)",
    crop_submit_btn: "Get Recommendation",
    crop_result_label: "Recommended Crop:",

    //fertiliser.html
    fert_heading: "Fertilizer Recommendation",
    fert_input_crop: "Crop Name",
    fert_input_soil: "Soil Type",
    fert_input_nitrogen: "Nitrogen (N)",
    fert_input_phosphorus: "Phosphorus (P)",
    fert_input_potassium: "Potassium (K)",
    fert_input_ph: "Soil pH",
    fert_submit_btn: "Get Fertilizer Recommendation",
    fert_result_label: "Recommended Fertilizer:",

    //yield.html
    yield_heading: "Yield Prediction",
    yield_input_crop: "Crop Name",
    yield_input_area: "Area (hectares)",
    yield_input_soil: "Soil Type",
    yield_input_nitrogen: "Nitrogen (N)",
    yield_input_phosphorus: "Phosphorus (P)",
    yield_input_potassium: "Potassium (K)",
    yield_input_temp: "Temperature (°C)",
    yield_input_rainfall: "Rainfall (mm)",
    yield_submit_btn: "Predict Yield",
    yield_result_label: "Expected Yield (kg/ha):"
  },

  hi: {
    //crop.html
    crop_heading: "फसल सिफारिश",
    crop_input_soil: "मृदा प्रकार",
    crop_input_nitrogen: "नाइट्रोजन (N)",
    crop_input_phosphorus: "फास्फोरस (P)",
    crop_input_potassium: "पोटैशियम (K)",
    crop_input_temp: "तापमान (°C)",
    crop_input_rainfall: "वर्षा (मिमी)",
    crop_submit_btn: "सिफारिश प्राप्त करें",
    crop_result_label: "सिफारिश की गई फसल:",

    //fertiliser.html
    fert_heading: "उर्वरक सिफारिश",
    fert_input_crop: "फसल का नाम",
    fert_input_soil: "मृदा प्रकार",
    fert_input_nitrogen: "नाइट्रोजन (N)",
    fert_input_phosphorus: "फास्फोरस (P)",
    fert_input_potassium: "पोटैशियम (K)",
    fert_input_ph: "मृदा pH",
    fert_submit_btn: "उर्वरक सिफारिश प्राप्त करें",
    fert_result_label: "सिफारिश किया गया उर्वरक:",

    //yield.html
    yield_heading: "उत्पादन पूर्वानुमान",
    yield_input_crop: "फसल का नाम",
    yield_input_area: "क्षेत्रफल (हेक्टेयर में)",
    yield_input_soil: "मृदा प्रकार",
    yield_input_nitrogen: "नाइट्रोजन (N)",
    yield_input_phosphorus: "फास्फोरस (P)",
    yield_input_potassium: "पोटैशियम (K)",
    yield_input_temp: "तापमान (°C)",
    yield_input_rainfall: "वर्षा (मिमी)",
    yield_submit_btn: "उत्पादन पूर्वानुमान करें",
    yield_result_label: "अपेक्षित उत्पादन (किग्रा/हेक्टेयर):"
  }
};


function translatePage(lang) {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (translations[lang][key]) {
      el.textContent = translations[lang][key];
    }
  });
}


function setLanguage(lang) {
  translatePage(lang);
  localStorage.setItem("language", lang);
}

document.addEventListener("DOMContentLoaded", () => {
  const savedLang = localStorage.getItem("language") || "en";
  translatePage(savedLang);
});