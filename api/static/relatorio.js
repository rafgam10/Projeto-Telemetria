// Variáveis globais dos gráficos
let consumoChart;
let tempoChart;

$(document).ready(function () {
    // Inicia select2
    $('#selectMotorista').select2({
        placeholder: "Busque por nome ou placa...",
    });

    // Gráfico de Consumo
    const consumoCtx = document.getElementById('consumoChart').getContext('2d');
    consumoChart = new Chart(consumoCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Consumo (km/L)',
                data: [],
                borderColor: '#a8ba44',
                backgroundColor: 'rgba(168, 186, 68, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#2d3748'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#2d3748'
                    }
                }
            }
        }
    });

    // Gráfico de Tempo
    const tempoCtx = document.getElementById('tempoChart').getContext('2d');
    tempoChart = new Chart(tempoCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Horas de Viagem',
                data: [],
                backgroundColor: 'rgba(168, 186, 68, 0.7)',
                borderColor: '#a8ba44',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#94a3b8',
                        callback: function (value) {
                            return value + 'h';
                        }
                    },
                    grid: {
                        color: '#2d3748'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#2d3748'
                    }
                }
            }
        }
    });

    // Esconde relatórios até selecionar motorista
    $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').hide();
    $('#semSelecao').show();

    // Ao selecionar um motorista
    $('#selectMotorista').on('change', function () {
        const idMotorista = $(this).val();
        const nomeCompleto = $(this).find('option:selected').text();

        if (idMotorista) {
            $('#semSelecao').hide();
            $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').show();

            fetch(`/admin/api/motorista-id/${encodeURIComponent(idMotorista)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.erro) {
                        alert(data.erro);
                        return;
                    }

                    $('#infoMotoristaSelecionado').text(nomeCompleto);
                    $('#infoTempoMotorista').text(nomeCompleto);
                    $('#infoExportMotorista').text(nomeCompleto);

                    atualizarGraficoConsumo(data.labels, data.consumos);
                    atualizarGraficoTempo(data.labels, data.tempos);
                });
        } else {
            $('#semSelecao').show();
            $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').hide();
        }
    });


});

// Funções auxiliares

function atualizarGraficoConsumo(labels, dados) {
    const media = mediaArray(dados);
    const melhor = Math.max(...dados).toFixed(2);
    const pior = Math.min(...dados).toFixed(2);

    document.querySelector("#relatorioSelecionado .grid div:nth-child(1) p.text-2xl").textContent = `${media} km/L`;
    document.querySelector("#relatorioSelecionado .grid div:nth-child(2) p.text-2xl").textContent = `${melhor} km/L`;
    document.querySelector("#relatorioSelecionado .grid div:nth-child(3) p.text-2xl").textContent = `${pior} km/L`;

    consumoChart.data.labels = labels;
    consumoChart.data.datasets[0].data = dados;
    consumoChart.update();
}

function atualizarGraficoTempo(labels, dados) {
    const media = mediaArray(dados);
    const maior = Math.max(...dados).toFixed(2);
    const menor = Math.min(...dados).toFixed(2);

    document.querySelector("#analiseTempo .grid div:nth-child(1) p.text-2xl").textContent = `${media} h`;
    document.querySelector("#analiseTempo .grid div:nth-child(2) p.text-2xl").textContent = `${maior} h`;
    document.querySelector("#analiseTempo .grid div:nth-child(3) p.text-2xl").textContent = `${menor} h`;

    tempoChart.data.labels = labels;
    tempoChart.data.datasets[0].data = dados;
    tempoChart.update();
}

function mediaArray(arr) {
    if (!arr.length) return 0;
    return (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2);
}



document.getElementById("btnExportarPDF").addEventListener("click", async function () {
    const area = document.getElementById("areaRelatorioPDF");
    const consumoChart = document.getElementById("consumoChart");
    const areagrafico = document.getElementById("areagrafico");
    const areagrafico2 = document.getElementById("areagrafico2");

    // Limita a largura total da área
    consumoChart.style.maxWidth = "794px";
    areagrafico.style.height = "200px";
    areagrafico2.style.height = "200px";
    consumoChart.style.height = "100%";
    area.style.boxSizing = "border-box";

    // Corrige cores incompatíveis (oklch)
    Array.from(area.querySelectorAll("*")).forEach(el => {
        const style = getComputedStyle(el);
        if (style.backgroundColor.includes("oklch")) {
            el.style.backgroundColor = "#1a2236";
        }
        if (style.color.includes("oklch")) {
            el.style.color = "#ffffff";
        }
    });

    // Redimensiona canvas
    const canvases = area.querySelectorAll("canvas");
    canvases.forEach(canvas => {
        canvas.style.maxWidth = "100%";
        canvas.style.height = "auto";
    });


    const opt = {
        margin: 5,
        filename: 'relatorio_motorista.pdf',
        image: { type: 'jpeg', quality: 0.95 },
        html2canvas: { scale: 1.5, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    try {
        await html2pdf().set(opt).from(area).save();
    } catch (error) {
        alert("Erro ao gerar PDF. Veja o console.");
        console.error(error);
    }

    consumoChart.style.maxWidth = "100%";
    areagrafico.style.height = "300px";
    areagrafico2.style.height = "300px";
});


document.getElementById("btnExportarExcel").addEventListener("click", function () {
    const nomePlaca = document.getElementById("infoExportMotorista").textContent;

    const [placa, ...nomeArr] = nomePlaca.split(" - ");
    const nomeCompleto = nomeArr.join(" - ").trim();
    const nomeMotorista = nomeCompleto;

    const datas = consumoChart.data.labels;
    const consumos = consumoChart.data.datasets[0].data;
    const tempos = tempoChart.data.datasets[0].data;

    // Cabeçalho + dados
    const sheetData = [["Motorista", "Placa", "Data", "Consumo (km/L)", "Tempo (h)"]];
    for (let i = 0; i < datas.length; i++) {
        sheetData.push([
            nomeMotorista,
            placa,
            datas[i],
            consumos[i] ?? "",
            tempos[i] ?? ""
        ]);
    }

    // Cria planilha
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(sheetData);

    // Aplica largura personalizada nas colunas
    ws['!cols'] = [
        { wch: 40 }, // Motorista
        { wch: 15 }, // Placa
        { wch: 20 }, // Data
        { wch: 20 }, // Consumo
        { wch: 20 }  // Tempo
    ];

    // Estiliza o cabeçalho com cor e negrito (hack via XLSX-style compatível)
    const headerStyle = {
        fill: { fgColor: { rgb: "A8BA44" } },
        font: { bold: true, color: { rgb: "FFFFFF" } }
    };

    const headerRange = ["A1", "B1", "C1", "D1", "E1"];
    headerRange.forEach(cell => {
        if (!ws[cell]) return;
        ws[cell].s = headerStyle;
    });

    // Anexa e exporta
    XLSX.utils.book_append_sheet(wb, ws, "Relatório");
    // Gera nome do arquivo com base no nome do motorista
    const nomeArquivo = "relatorio_motorista_" + nomeMotorista.replace(/[^\w]/g, "_") + ".xlsx";
    XLSX.writeFile(wb, nomeArquivo);

});
