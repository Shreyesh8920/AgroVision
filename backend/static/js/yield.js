document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("yieldForm");
  if (!form) return;
  const loadingEl = document.getElementById("yield-loading");
  const resultBox = document.getElementById("yield-result-box");
  const resultValue = document.getElementById("yield-result-value");


  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const fields = [
      { id: "crop_name", type: "select" },     
      { id: "region", type: "select" },
      { id: "soil_type", type: "select" },
      { id: "fertilizer_used", type: "select" },
      { id: "irrigation_used", type: "select" },
      { id: "rainfall", type: "number", min: 0, max: 5000 },
      { id: "temperature", type: "number", min: -10, max: 60 },
      { id: "n", type: "number", min: 0, max: 300 },
      { id: "p", type: "number", min: 0, max: 300 },
      { id: "k", type: "number", min: 0, max: 300 },
      { id: "ph", type: "number", min: 0, max: 14 }
    ];

    let valid = true;
    const rawData = {};

    fields.forEach(f => {
      const el = document.getElementById(f.id);
      if (!el) return;

      let value = el.value.trim();
      let isFieldValid = true;

      if (f.type === "select" && (!value || value.startsWith("Select"))) {
        isFieldValid = false;
        valid = false;
      }

      if (f.type === "number") {
        let numValue = parseFloat(value);
        if (!value || isNaN(numValue) || numValue < f.min || numValue > f.max) {
          isFieldValid = false;
          valid = false;
        } else {
          value = numValue;
        }
      }

      el.classList.toggle("is-invalid", !isFieldValid);
      rawData[f.id] = value;
    });

    if (!valid) return;
    loadingEl.classList.remove("d-none");
    resultBox.classList.add("d-none");

    const payload = {
      crop_name: rawData.crop_name,               
      Region: [rawData.region],
      Soil_Type: [rawData.soil_type],
      Rainfall_mm: [rawData.rainfall],
      Temperature_Celsius: [rawData.temperature],
      Fertilizer_Used: [rawData.fertilizer_used === "true"],
      Irrigation_Used: [rawData.irrigation_used === "true"],
      N: [rawData.n],
      P: [rawData.p],
      K: [rawData.k],
      ph: [rawData.ph]
    };

    try {
      const response = await fetch("/predict_yield", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      const yieldValue = Number(result.predicted_yield).toFixed(2);

      loadingEl.classList.add("d-none");
      resultBox.classList.remove("d-none");
      resultValue.style.color = "#047857";
      resultValue.textContent = `${yieldValue} quintals/acre`;
    } catch (error) {
      console.error("Yield prediction failed:", error);
      loadingEl.classList.add("d-none");
      resultBox.classList.remove("d-none");
      resultValue.style.color = "red";
      resultValue.textContent = "Prediction failed. Please try again.";
    }
  });
});
