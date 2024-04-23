document.getElementById('market-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const unit = document.getElementById('unit').value;
    const pam = parseFloat(document.getElementById('pam').value);
    const tamPercent = parseFloat(document.getElementById('tam-percent').value);
    const samPercent = parseFloat(document.getElementById('sam-percent').value);
    const somPercent = parseFloat(document.getElementById('som-percent').value);
    const conversionRate = parseFloat(document.getElementById('conversion-rate').value);
    const growthRate = parseFloat(document.getElementById('growth-rate').value);
    const cost = parseFloat(document.getElementById('cost').value);

    const tam = pam * (tamPercent / 100);
    const sam = tam * (samPercent / 100);
    const som = sam * (somPercent / 100);

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ unit, pam, tam, sam, som, conversionRate, growthRate, cost, year: 2024 })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <h2>Диаграмма размера рынка</h2>
            <img src="data:image/png;base64,${data.chart}" alt="Диаграмма размера рынка">
        `;

        const forecastDiv = document.getElementById('forecast');
        forecastDiv.innerHTML = `
            <h2>Прогноз финансовых результатов</h2>
            <img src="data:image/png;base64,${data.forecastChart}" alt="Прогноз финансовых результатов">
        `;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте еще раз позже.');
    });
});
