// dashboard.js
// Funções e variáveis do dashboard extraídas do template

const CACHE_KEY = 'dashboard_data';
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

function getCachedData() {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        if (Date.now() - timestamp < CACHE_DURATION) {
            return data;
        }
    }
    return null;
}

function setCachedData(data) {
    localStorage.setItem(CACHE_KEY, JSON.stringify({
        data,
        timestamp: Date.now()
    }));
}

function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('d-none');
}

function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

function showConfirmation(message, callback) {
    const modal = document.getElementById('confirmationModal');
    document.getElementById('confirmationMessage').textContent = message;
    document.getElementById('confirmActionBtn').onclick = () => {
        callback();
        bootstrap.Modal.getInstance(modal).hide();
    };
    new bootstrap.Modal(modal).show();
}

function applyAdvancedFilters() {
    const formData = new FormData(document.getElementById('filterForm'));
    const params = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
        if (value) params.append(key, value);
    }
    filterDashboard(params.toString());
    bootstrap.Modal.getInstance(document.getElementById('filterModal')).hide();
}

async function refreshDashboard() {
    showLoading();
    try {
        const funcionarioStatus = document.querySelector('select[name="funcionario_status"]').value;
        let url = window.dashboardDataUrl || '/get-filtered-dashboard-data/';
        const params = new URLSearchParams();
        params.append('funcionario_status', funcionarioStatus);
        url += (url.includes('?') ? '&' : '?') + params.toString();
        const response = await fetch(url);
        const data = await response.json();
        updateCharts(data);
        updateDocumentTable(data.documentos);
        setCachedData(data);
        showToast('Dashboard atualizado com sucesso!');
    } catch (error) {
        showToast('Erro ao atualizar dashboard', 'danger');
        console.error('Erro:', error);
    } finally {
        hideLoading();
    }
}

function deleteDocument(id) {
    showConfirmation('Tem certeza que deseja excluir este documento?', async () => {
        showLoading();
        try {
            const response = await fetch(`/documento/delete/${id}`, { method: 'POST' });
            if (response.ok) {
                showToast('Documento excluído com sucesso!');
                refreshDashboard();
            } else {
                throw new Error('Erro ao excluir documento');
            }
        } catch (error) {
            showToast('Erro ao excluir documento', 'danger');
            console.error('Erro:', error);
        } finally {
            hideLoading();
        }
    });
}

const observerOptions = {
    root: null,
    rootMargin: '50px',
    threshold: 0.1
};

const chartObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const chartId = entry.target.id;
            if (chartId === 'statusChart') {
                createStatusChart();
            } else if (chartId === 'tipoChart') {
                createTipoChart(window.tiposDocumentos || [], window.quantidadePorTipo || []);
            }
            chartObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#statusChart, #tipoChart').forEach(chart => {
        chartObserver.observe(chart);
    });
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    refreshDashboard();
    setInterval(refreshDashboard, CACHE_DURATION);
});

function destroyCharts() {
    if (window.statusChart && typeof window.statusChart.destroy === 'function') {
        window.statusChart.destroy();
    }
    if (window.tipoChart && typeof window.tipoChart.destroy === 'function') {
        window.tipoChart.destroy();
    }
}

function createStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    window.statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Vencidos', 'Críticos', 'Vencendo', 'Em Dia'],
            datasets: [{
                data: (data && data.status_data) ? data.status_data : [0, 0, 0, 0],
                backgroundColor: ['#dc3545', '#6f42c1', '#ffc107', '#28a745'],
                hoverBackgroundColor: ['#c82333', '#5a2b9f', '#e0a800', '#218838']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: getComputedStyle(document.body).color,
                        font: { size: 14 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function createTipoChart(labels, data) {
    const ctx = document.getElementById('tipoChart').getContext('2d');
    window.tipoChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Quantidade',
                data: data,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
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
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: getComputedStyle(document.body).color,
                        font: { size: 13 }
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.body).color,
                        font: { size: 13 }
                    }
                }
            }
        }
    });
}

function createLocalChart(labels, data) {
    const container = document.getElementById('localChartContainer');
    if (!container) return;
    container.innerHTML = '<canvas id="localChart"></canvas>';
    const ctx = document.getElementById('localChart').getContext('2d');
    window.localChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Qtd. Documentos',
                data: data,
                backgroundColor: 'rgba(40, 167, 69, 0.6)',
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: getComputedStyle(document.body).color,
                        font: { size: 13 }
                    }
                },
                x: {
                    ticks: {
                        color: getComputedStyle(document.body).color,
                        font: { size: 13 }
                    }
                }
            }
        }
    });
}

function updateKPIs(kpis) {
    document.querySelector('[data-count][data-kpi="vencidos"]').textContent = kpis.vencidos;
    document.querySelector('[data-count][data-kpi="criticos"]').textContent = kpis.criticos;
    document.querySelector('[data-count][data-kpi="vencendo"]').textContent = kpis.vencendo;
    document.querySelector('[data-count][data-kpi="em_dia"]').textContent = kpis.em_dia;
    document.querySelector('[data-count][data-kpi="total"]').textContent = kpis.total;
}

function updateCharts(data) {
    destroyCharts();
    createStatusChart(data);
    createTipoChart(data.tipos_documentos, data.quantidade_por_tipo);
    if (data.kpis) updateKPIs(data.kpis);
    if (data.locais_labels && data.locais_data) createLocalChart(data.locais_labels, data.locais_data);
}

function filterDashboard(status) {
    const funcionarioStatus = document.querySelector('select[name="funcionario_status"]').value;
    const url = new URL(window.dashboardDataUrl || '/get-filtered-dashboard-data/', window.location.origin);
    if (status !== 'Todos') {
        url.searchParams.append('status', status);
    }
    url.searchParams.append('funcionario_status', funcionarioStatus);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
            updateDocumentTable(data.documentos);
        })
        .catch(error => console.error('Erro ao buscar dados filtrados:', error));
}

let currentPage = 1;
const itemsPerPage = 10;
let allDocuments = [];

function updateDocumentTable(documentos) {
    allDocuments = documentos;
    renderDocumentTablePage(1);
    renderPaginationControls();
}

function renderDocumentTablePage(page) {
    currentPage = page;
    const tableBody = document.querySelector('#documentTableBody');
    if (!tableBody) return;
    tableBody.innerHTML = '';
    if (!allDocuments.length) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum documento encontrado com este filtro.</td></tr>';
        renderPaginationControls();
        return;
    }
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageDocs = allDocuments.slice(start, end);
    pageDocs.forEach(doc => {
        const statusClass = getStatusClass(doc.dias_restantes);
        const row = createTableRow(doc, statusClass);
        tableBody.appendChild(row);
    });
    renderPaginationControls();
}

function renderPaginationControls() {
    let paginationContainer = document.getElementById('dashboardPagination');
    if (!paginationContainer) {
        paginationContainer = document.createElement('div');
        paginationContainer.id = 'dashboardPagination';
        paginationContainer.className = 'd-flex justify-content-center mt-3';
        const table = document.querySelector('#documentTableBody');
        if (table && table.parentElement && table.parentElement.parentElement) {
            table.parentElement.parentElement.appendChild(paginationContainer);
        } else {
            document.body.appendChild(paginationContainer);
        }
    }
    const totalPages = Math.ceil(allDocuments.length / itemsPerPage);
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    let html = '<nav><ul class="pagination">';
    html += `<li class="page-item${currentPage === 1 ? ' disabled' : ''}"><a class="page-link" href="#" onclick="goToDashboardPage(${currentPage - 1});return false;">&laquo;</a></li>`;

    // Lógica de paginação inteligente
    let startPage = Math.max(1, currentPage - 1);
    let endPage = Math.min(totalPages, currentPage + 1);
    if (currentPage <= 2) {
        startPage = 1;
        endPage = Math.min(3, totalPages);
    } else if (currentPage >= totalPages - 1) {
        startPage = Math.max(1, totalPages - 2);
        endPage = totalPages;
    }

    if (startPage > 1) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="goToDashboardPage(1);return false;">1</a></li>`;
        if (startPage > 2) {
            html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentPage) {
            html += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="goToDashboardPage(${i});return false;">${i}</a></li>`;
        }
    }
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
        html += `<li class="page-item"><a class="page-link" href="#" onclick="goToDashboardPage(${totalPages});return false;">${totalPages}</a></li>`;
    }

    html += `<li class="page-item${currentPage === totalPages ? ' disabled' : ''}"><a class="page-link" href="#" onclick="goToDashboardPage(${currentPage + 1});return false;">&raquo;</a></li>`;
    html += '</ul></nav>';
    paginationContainer.innerHTML = html;
}

window.goToDashboardPage = function(page) {
    const totalPages = Math.ceil(allDocuments.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    renderDocumentTablePage(page);
};

function getStatusClass(diasRestantes) {
    if (diasRestantes < 0) return 'table-danger';
    if (diasRestantes <= 10) return 'table-purple';
    if (diasRestantes <= 40) return 'table-yellow';
    return 'table-success';
}

function createTableRow(doc, statusClass) {
    const row = document.createElement('tr');
    row.className = statusClass;
    const statusText = doc.dias_restantes < 0 ? 'Vencido' :
                      doc.dias_restantes <= 10 ? 'Crítico' :
                      doc.dias_restantes <= 40 ? 'Vencendo' : 'Em Dia';
    row.innerHTML = `
        <td>${doc.nome_documento}</td>
        <td>${doc.funcionario_nome}</td>
        <td>${doc.data_validade}</td>
        <td>
            <span class="badge ${statusClass.replace('table-', 'bg-')} badge-pill">
                ${statusText}
            </span>
        </td>
        <td>
            ${doc.arquivo_url ? 
                `<a href="${doc.arquivo_url}" target="_blank" class="btn btn-outline-primary btn-sm">
                    <i class="bi bi-eye"></i> Visualizar
                </a>` : 
                '---'}
        </td>
        <td>
            <a href="/documento/${doc.id}/editar/" class="btn btn-sm btn-primary" data-bs-toggle="tooltip" title="Editar">
                <i class="bi bi-pencil"></i>
            </a>
            <a href="/documento/${doc.id}/excluir/" class="btn btn-sm btn-danger" data-bs-toggle="tooltip" title="Excluir">
                <i class="bi bi-trash"></i>
            </a>
        </td>
    `;
    return row;
} 