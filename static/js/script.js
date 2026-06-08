// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');

        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(section => section.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
    });
});

function detectDataType(value) {
    const trimmed = String(value).trim();
    if (trimmed.length === 0) {
        return { type: 'Empty', value: '' };
    }

    const lower = trimmed.toLowerCase();
    if (['true', 'false', 'yes', 'no'].includes(lower)) {
        return { type: 'Boolean', value: ['true', 'yes'].includes(lower) };
    }

    if (/^[+-]?\d+$/.test(trimmed)) {
        return { type: 'Integer', value: parseInt(trimmed, 10) };
    }

    if (/^[+-]?(\d*\.\d+|\d+\.\d*)$/.test(trimmed) && !Number.isNaN(Number(trimmed))) {
        return { type: 'Float/Decimal', value: parseFloat(trimmed) };
    }

    const dateFormats = [
        { regex: /^\d{4}-\d{2}-\d{2}$/, order: ['year', 'month', 'day'] },
        { regex: /^\d{2}-\d{2}-\d{4}$/, order: ['day', 'month', 'year'] },
        { regex: /^\d{2}\/\d{2}\/\d{4}$/, order: ['month', 'day', 'year'] },
        { regex: /^\d{4}\/\d{2}\/\d{2}$/, order: ['year', 'month', 'day'] }
    ];

    for (const format of dateFormats) {
        if (format.regex.test(trimmed)) {
            const parts = trimmed.includes('/') ? trimmed.split('/') : trimmed.split('-');
            const dateParts = {};
            format.order.forEach((key, index) => {
                dateParts[key] = Number(parts[index]);
            });
            const date = new Date(`${dateParts.year}-${String(dateParts.month).padStart(2, '0')}-${String(dateParts.day).padStart(2, '0')}`);
            if (!Number.isNaN(date.getTime())) {
                return { type: 'Date', value: trimmed };
            }
        }
    }

    return { type: 'String/Text', value: trimmed };
}

function detectType() {
    const input = document.getElementById('typeInput').value;
    const result = detectDataType(input);

    if (!input.trim()) {
        alert('Please enter a value');
        return;
    }

    document.getElementById('detectedType').textContent = result.type;
    document.getElementById('detectedValue').textContent = result.value;
    document.getElementById('typeResult').classList.remove('hidden');
}

function predictPrice(engineSize, horsepower, age, mileage, brandValue) {
    const values = [engineSize, horsepower, age, mileage, brandValue].map(v => Number(v));
    if (values.some(v => Number.isNaN(v))) {
        return { error: 'All values must be valid numbers.', success: false };
    }

    const [es, hp, ag, mi, bv] = values;
    const predictedPrice = es * 500000 + hp * 10000 - ag * 80000 - mi * 5 + bv * 300000;
    return { predicted_price: Number(predictedPrice.toFixed(2)), success: true };
}

function showPriceResult(data) {
    if (data.success) {
        document.getElementById('predictedPrice').textContent = data.predicted_price.toLocaleString();
        document.getElementById('priceResult').classList.remove('hidden');
    } else {
        alert('Error: ' + data.error);
    }
}

if (document.getElementById('priceForm')) {
    document.getElementById('priceForm').addEventListener('submit', (e) => {
        e.preventDefault();

        const engineSize = document.getElementById('engineSize').value;
        const horsepower = document.getElementById('horsepower').value;
        const age = document.getElementById('age').value;
        const mileage = document.getElementById('mileage').value;
        const brandValue = document.getElementById('brandValue').value;

        const result = predictPrice(engineSize, horsepower, age, mileage, brandValue);
        showPriceResult(result);
    });
}

function analyzeValues() {
    const input = document.getElementById('batchInput').value.trim();
    const predict = document.getElementById('predictCheckbox').checked;

    if (!input) {
        alert('Please enter values');
        return;
    }

    const values = input.split(/[,\n]+/).map(v => v.trim()).filter(v => v.length > 0);
    const detected = values.map(value => detectDataType(value));

    let html = '<strong>Data Type Detection Results:</strong><br>';
    detected.forEach((result, index) => {
        html += `<div class="type-item"><strong>Value ${index + 1}:</strong> "${values[index]}" → <strong>${result.type}</strong></div>`;
    });
    document.getElementById('typesList').innerHTML = html;

    if (predict && values.length >= 5) {
        const prediction = predictPrice(values[0], values[1], values[2], values[3], values[4]);
        if (prediction.success) {
            document.getElementById('priceInfo').innerHTML = `<div style="margin-top: 20px; padding: 15px; background: #f1f8f4; border-left: 4px solid #4caf50; border-radius: 5px;"><strong>Predicted Car Price:</strong> <span style="font-size: 1.5em; color: #4caf50; font-weight: bold;">$${prediction.predicted_price.toLocaleString()}</span></div>`;
        } else {
            document.getElementById('priceInfo').innerHTML = `<div style="margin-top: 20px; padding: 15px; background: #ffe6e6; border-left: 4px solid #f44336; border-radius: 5px;"><strong>Error:</strong> ${prediction.error}</div>`;
        }
    } else {
        document.getElementById('priceInfo').innerHTML = predict ? '<div style="margin-top: 20px; padding: 15px; background: #ffe6e6; border-left: 4px solid #f44336; border-radius: 5px;"><strong>Error:</strong> Enter at least 5 numeric values to predict price.</div>' : '';
    }

    document.getElementById('batchResult').classList.remove('hidden');
}

if (document.getElementById('typeInput')) {
    document.getElementById('typeInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            detectType();
        }
    });
}
