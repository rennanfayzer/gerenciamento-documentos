from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from datetime import datetime

def export_documentos_pdf(documentos, colunas=None):
    """Exporta documentos para PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="documentos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Criar o documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    elements.append(Paragraph("Relatório de Documentos", styles['Title']))
    elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Paragraph("", styles['Normal']))  # Espaço
    
    # Definir colunas padrão se não especificadas
    if not colunas:
        colunas = ['nome', 'funcionario', 'tipo', 'data_validade', 'status']
    
    # Preparar dados
    data = []
    headers = []
    
    # Mapear nomes das colunas
    coluna_names = {
        'nome': 'Nome',
        'funcionario': 'Funcionário',
        'tipo': 'Tipo',
        'data_validade': 'Data de Validade',
        'status': 'Status',
        'local': 'Local'
    }
    
    # Adicionar cabeçalhos
    for col in colunas:
        if col in coluna_names:
            headers.append(coluna_names[col])
    
    data.append(headers)
    
    # Adicionar dados
    for doc in documentos:
        row = []
        for col in colunas:
            if col == 'funcionario':
                row.append(str(doc.funcionario))
            elif col == 'data_validade':
                row.append(doc.data_validade.strftime('%d/%m/%Y'))
            elif col == 'status':
                row.append(doc.get_status_display())
            else:
                row.append(str(getattr(doc, col)))
        data.append(row)
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response 