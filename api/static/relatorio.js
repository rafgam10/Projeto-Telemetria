$(document).ready(function() {
    $('#selectMotorista').select2({
    placeholder: "Busque por nome ou placa...",
    });

    // Gráfico de Consumo
    const consumoCtx = document.getElementById('consumoChart').getContext('2d');
    const consumoChart = new Chart(consumoCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
            datasets: [{
                label: 'Consumo (km/L)',
                data: [2.6, 2.7, 2.8, 2.9, 3.0, 2.8, 2.9],
                borderColor: '#a8ba44',
                backgroundColor: 'rgba(168, 186, 68, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // necessário pra respeitar o tamanho do container
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


    const tempoCtx = document.getElementById('tempoChart').getContext('2d');
    const tempoChart = new Chart(tempoCtx, {
        type: 'bar',
        data: {
            labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
            datasets: [{
                label: 'Horas de Viagem',
                data: [5.2, 4.8, 6.1, 3.9, 4.5, 2.2],
                backgroundColor: 'rgba(168, 186, 68, 0.7)',
                borderColor: '#a8ba44',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // <- ESSENCIAL PRA RESPONSIVIDADE REAL
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
                        callback: function(value) {
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


    // Esconde os relatórios inicialmente e mostra apenas o placeholder
    $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').hide();
    $('#semSelecao').show();

    // Monitora seleção de motorista
    $('#selectMotorista').on('change', function() {
        const selectedText = $(this).find('option:selected').text();    
        if ($(this).val()) {
            $('#semSelecao').hide();
            $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').show();
            $('#infoMotoristaSelecionado, #infoTempoMotorista, #infoExportMotorista').text(selectedText);
        } else {
            $('#semSelecao').show();
            $('#relatorioSelecionado, #analiseTempo, #exportacaoRelatorios').hide();
        }
    });

});