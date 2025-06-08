let consumoChart, distanciaChart;

$(document).ready(() => {
    $('#selectMotorista').select2({
        placeholder: "Busque por nome ou placa..."
    });

    $('#selectMotorista').on('change', async function () {
        const id = $(this).val();
        const nome = $(this).find('option:selected').text();

        if (!id) {
            $('#semSelecao').show();
            $('#areaRelatorioPDF').addClass('hidden');
            return;
        }

        try {
            const res = await fetch(`/admin/api/motorista-id/${id}`);
            const dados = await res.json();

            if (dados.erro) {
                alert(dados.erro);
                return;
            }

            $('#semSelecao').hide();
            $('#areaRelatorioPDF').removeClass('hidden');

            $('.motorista-nome').text(nome);

            atualizarGraficoConsumo(dados.labels, dados.consumos, dados);
            atualizarGraficoDistancia(dados.labels, dados.distancias);
        } catch (e) {
            console.error("Erro ao buscar dados do motorista:", e);
        }
    });

    inicializarGraficos();
});

function inicializarGraficos() {
    const consumoCtx = document.getElementById("consumoChart").getContext("2d");
    const distanciaCtx = document.getElementById("distanciaChart").getContext("2d");

    consumoChart = new Chart(consumoCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Consumo médio (km/L)',
                data: [],
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: gerarOpcoes("Consumo médio (km/L)")
    });

    distanciaChart = new Chart(distanciaCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Quilometragem semanal (km)',
                data: [],
                backgroundColor: '#818cf8',
                borderColor: '#6366f1',
                borderWidth: 1
            }]
        },
        options: gerarOpcoes("Quilometragem semanal (km)")
    });
}

function gerarOpcoes(titulo) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#e2e8f0' } },
            tooltip: {
                callbacks: {
                    label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}`
                }
            }
        },
        scales: {
            x: {
                ticks: { color: '#cbd5e1' },
                grid: { color: '#334155' }
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#cbd5e1' },
                grid: { color: '#334155' }
            }
        }
    };
}

function atualizarGraficoConsumo(labels, dados, resumo) {
    consumoChart.data.labels = labels;
    consumoChart.data.datasets[0].data = dados;
    consumoChart.update();

    atualizarCard("#relatorioSelecionado", [
        resumo.media_consumo.toFixed(2),
        resumo.melhor_consumo.toFixed(2),
        resumo.pior_consumo.toFixed(2)
    ], "km/L");
}

function atualizarGraficoDistancia(labels, dados) {
    distanciaChart.data.labels = labels;
    distanciaChart.data.datasets[0].data = dados;
    distanciaChart.update();

    const media = mediaArray(dados).toFixed(1);
    const max = Math.max(...dados).toFixed(1);
    const min = Math.min(...dados).toFixed(1);

    atualizarCard("#graficoDistancia", [media, max, min], "km");
}

function atualizarCard(selector, valores, unidade = "") {
    const cards = document.querySelectorAll(`${selector} .grid div p.text-2xl`);
    if (cards.length >= 3) {
        cards[0].textContent = `${valores[0]} ${unidade}`;
        cards[1].textContent = `${valores[1]} ${unidade}`;
        cards[2].textContent = `${valores[2]} ${unidade}`;
    }
}

function mediaArray(arr) {
    return arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
}





// ---------- EXPORTAÇÃO PDF ----------

document.getElementById("btnExportarPDF").addEventListener("click", async function () {
    const area = document.getElementById("areaRelatorioPDF");

    // Define altura fixa nos gráficos
    const consumoChartCanvasDiv = document.getElementById("consumoChartDiv");
    const distanciaChartCanvasDiv = document.getElementById("distanciaChartDiv");
    const consumoChartCanvas = document.getElementById("consumoChart");
    const distanciaChartCanvas = document.getElementById("distanciaChart");

    consumoChartCanvasDiv.style.width = "100%";
    consumoChartCanvasDiv.style.height = "170px";

    distanciaChartCanvasDiv.style.width = "100%";
    distanciaChartCanvasDiv.style.height = "170px";

    consumoChartCanvas.style.width = "100%";
    consumoChartCanvas.style.height = "auto";

    distanciaChartCanvas.style.width = "100%";
    distanciaChartCanvas.style.height = "auto";

    // Corrige cores incompatíveis
    area.querySelectorAll("*").forEach(el => {
        const style = getComputedStyle(el);
        if (style.backgroundColor.includes("oklch")) el.style.backgroundColor = "#1a2236";
        if (style.color.includes("oklch")) el.style.color = "#ffffff";
    });

    const opt = {
        margin: 5,
        filename: 'relatorio_motorista.pdf',
        image: { type: 'jpeg', quality: 0.95 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    try {
        await html2pdf().set(opt).from(area).save();
    } catch (error) {
        alert("Erro ao gerar PDF. Veja o console.");
        console.error(error);
    }

    // Restaurar se necessário (opcional)
    consumoChartCanvas.style.height = "";
    distanciaChartCanvas.style.height = "";
    consumoChartCanvasDiv.style.height = "";
    distanciaChartCanvasDiv.style.height = "";
});


// ---------- EXPORTAÇÃO EXCEL ----------
document.getElementById("btnExportarExcel").addEventListener("click", function () {
    const nomePlaca = document.getElementById("infoExportMotorista").textContent;
    const [placa, ...nomeArr] = nomePlaca.split(" - ");
    const nomeMotorista = nomeArr.join(" - ").trim();

    const datas = consumoChart.data.labels;
    const consumos = consumoChart.data.datasets[0].data;
    const distancias = distanciaChart.data.datasets[0].data;

    const sheetData = [["Motorista", "Placa", "Data", "Consumo (km/L)", "Quilometragem (km)"]];
    for (let i = 0; i < datas.length; i++) {
        sheetData.push([
            nomeMotorista,
            placa,
            datas[i],
            consumos[i] ?? "",
            distancias[i] ?? ""
        ]);
    }

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(sheetData);

    ws['!cols'] = [
        { wch: 40 }, { wch: 15 }, { wch: 20 },
        { wch: 20 }, { wch: 20 }
    ];

    const headerStyle = {
        fill: { fgColor: { rgb: "A8BA44" } },
        font: { bold: true, color: { rgb: "FFFFFF" } }
    };

    ["A1", "B1", "C1", "D1", "E1"].forEach(cell => {
        if (ws[cell]) ws[cell].s = headerStyle;
    });

    XLSX.utils.book_append_sheet(wb, ws, "Relatório");
    const nomeArquivo = "relatorio_motorista_" + nomeMotorista.replace(/[^\w]/g, "_") + ".xlsx";
    XLSX.writeFile(wb, nomeArquivo);
});
