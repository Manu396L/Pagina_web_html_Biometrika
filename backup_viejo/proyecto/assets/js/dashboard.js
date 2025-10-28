// dashboard-charts.js
// Inicializar gráficos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Gráfico de Asistencia (Doughnut)
    const asistenciaCtx = document.getElementById('asistenciaChart').getContext('2d');
    const asistenciaChart = new Chart(asistenciaCtx, {
        type: 'doughnut',
        data: {
            labels: ['Ausencia', 'Asistencia'],
            datasets: [{
                data: [0, 21],
                backgroundColor: ['#e74c3c', '#2ecc71'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Estado de Dispositivos (Doughnut)
    const dispositivosCtx = document.getElementById('dispositivosChart').getContext('2d');
    const dispositivosChart = new Chart(dispositivosCtx, {
        type: 'doughnut',
        data: {
            labels: ['Online', 'Offline', 'No Autorizado'],
            datasets: [{
                data: [2, 1, 0],
                backgroundColor: ['#2ecc71', '#e74c3c', '#f39c12'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Programación (Doughnut)
    const programacionCtx = document.getElementById('programacionChart').getContext('2d');
    const programacionChart = new Chart(programacionCtx, {
        type: 'doughnut',
        data: {
            labels: ['No Programado', 'Programado'],
            datasets: [{
                data: [2, 19],
                backgroundColor: ['#3498db', '#9b59b6'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Gráfico de Excepciones de Asistencia (Bar)
    const excepcionesCtx = document.getElementById('excepcionesChart').getContext('2d');
    const excepcionesChart = new Chart(excepcionesCtx, {
        type: 'bar',
        data: {
            labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            datasets: [
                {
                    label: 'Llegadas tarde',
                    data: [1, 2, 1, 3, 2, 0, 0],
                    backgroundColor: '#3498db',
                    borderRadius: 4
                },
                {
                    label: 'Salidas temprano',
                    data: [0, 1, 2, 1, 1, 0, 0],
                    backgroundColor: '#e74c3c',
                    borderRadius: 4
                },
                {
                    label: 'Ausencia',
                    data: [0, 0, 1, 0, 1, 0, 0],
                    backgroundColor: '#f39c12',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
});