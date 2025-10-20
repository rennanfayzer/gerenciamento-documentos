// Atalhos de teclado
document.addEventListener('keydown', function(e) {
    // Ctrl + D: Dashboard
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        window.location.href = '/dashboard/';
    }
    
    // Ctrl + F: Lista de Funcionários
    if (e.ctrlKey && e.key === 'f') {
        e.preventDefault();
        window.location.href = '/funcionarios/';
    }
    
    // Ctrl + L: Lista de Locais
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        window.location.href = '/locais/';
    }
    
    // Ctrl + N: Novo Documento
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/documentos/novo/';
    }
    
    // Ctrl + S: Busca
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }
    
    // Ctrl + E: Exportar
    if (e.ctrlKey && e.key === 'e') {
        e.preventDefault();
        document.getElementById('exportBtn').click();
    }
    
    // Ctrl + T: Alternar Tema
    if (e.ctrlKey && e.key === 't') {
        e.preventDefault();
        toggleTheme();
    }
    
    // Esc: Fechar Modal
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }

    // Atalho para busca avançada (Ctrl + B)
    if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        window.location.href = '/busca-avancada/';
    }
}); 