from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def generate_report(summary, data, dataset=None):
    """
    Generate a PDF report for the chemical equipment dataset with AI insights.
    
    Args:
        summary (dict): Summary statistics from the analysis
        data (list): List of dictionaries containing the raw data
        dataset (Dataset): Dataset model instance with AI fields (optional)
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("Chemical Equipment Parameter Analysis Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary Section
    summary_heading = Paragraph("Summary Statistics", heading_style)
    elements.append(summary_heading)
    
    # Total Count
    total_text = Paragraph(f"<b>Total Equipment Count:</b> {summary.get('total_count', 0)}", styles['Normal'])
    elements.append(total_text)
    elements.append(Spacer(1, 0.1*inch))
    
    # Average Values Table
    avg_data = [
        ['Parameter', 'Average Value'],
        ['Flowrate', f"{summary.get('averages', {}).get('flowrate', 0):.2f}"],
        ['Pressure', f"{summary.get('averages', {}).get('pressure', 0):.2f}"],
        ['Temperature', f"{summary.get('averages', {}).get('temperature', 0):.2f}"],
    ]
    
    avg_table = Table(avg_data, colWidths=[3*inch, 2*inch])
    avg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(avg_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Equipment Type Distribution
    type_dist_heading = Paragraph("Equipment Type Distribution", heading_style)
    elements.append(type_dist_heading)
    
    type_distribution = summary.get('type_distribution', {})
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in type_distribution.items():
        type_data.append([str(eq_type), str(count)])
    
    if len(type_data) > 1:
        type_table = Table(type_data, colWidths=[3*inch, 2*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(type_table)
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Min and Max Values
    min_max_heading = Paragraph("Parameter Ranges", heading_style)
    elements.append(min_max_heading)
    
    min_values = summary.get('min_values', {})
    max_values = summary.get('max_values', {})
    
    range_data = [
        ['Parameter', 'Minimum', 'Maximum'],
        ['Flowrate', f"{min_values.get('flowrate', 0):.2f}", f"{max_values.get('flowrate', 0):.2f}"],
        ['Pressure', f"{min_values.get('pressure', 0):.2f}", f"{max_values.get('pressure', 0):.2f}"],
        ['Temperature', f"{min_values.get('temperature', 0):.2f}", f"{max_values.get('temperature', 0):.2f}"],
    ]
    
    range_table = Table(range_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    range_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(range_table)
    
    # AI Insights Section (if available)
    if dataset and dataset.ai_insights:
        elements.append(PageBreak())
        ai_heading = Paragraph("AI-Powered Insights", title_style)
        elements.append(ai_heading)
        elements.append(Spacer(1, 0.2*inch))
        
        ai_insights = dataset.ai_insights
        
        # Executive Summary
        if ai_insights.get('executive_summary'):
            exec_heading = Paragraph("Executive Summary", heading_style)
            elements.append(exec_heading)
            
            summary_style = ParagraphStyle(
                'Summary',
                parent=styles['Normal'],
                fontSize=11,
                leading=16,
                alignment=TA_JUSTIFY
            )
            exec_summary = Paragraph(ai_insights['executive_summary'], summary_style)
            elements.append(exec_summary)
            elements.append(Spacer(1, 0.2*inch))
        
        # Risk Level
        if ai_insights.get('risk_level'):
            risk_level = ai_insights['risk_level'].upper()
            risk_colors = {
                'LOW': colors.green,
                'MEDIUM': colors.orange,
                'HIGH': colors.orangered,
                'CRITICAL': colors.red,
                'UNKNOWN': colors.grey
            }
            risk_color = risk_colors.get(risk_level, colors.grey)
            
            risk_style = ParagraphStyle(
                'Risk',
                parent=styles['Normal'],
                fontSize=12,
                textColor=risk_color,
                fontName='Helvetica-Bold'
            )
            risk_text = Paragraph(f"Risk Level: {risk_level}", risk_style)
            elements.append(risk_text)
            elements.append(Spacer(1, 0.2*inch))
        
        # Key Findings
        if ai_insights.get('key_findings'):
            findings_heading = Paragraph("Key Findings", heading_style)
            elements.append(findings_heading)
            
            for finding in ai_insights['key_findings'][:5]:  # Limit to 5
                finding_text = Paragraph(f"• {finding}", styles['Normal'])
                elements.append(finding_text)
                elements.append(Spacer(1, 0.05*inch))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        if ai_insights.get('recommendations'):
            rec_heading = Paragraph("Recommendations", heading_style)
            elements.append(rec_heading)
            
            for rec in ai_insights['recommendations'][:5]:  # Limit to 5
                rec_text = Paragraph(f"• {rec}", styles['Normal'])
                elements.append(rec_text)
                elements.append(Spacer(1, 0.05*inch))
            
            elements.append(Spacer(1, 0.2*inch))
    
    # Outliers Section (if available)
    if dataset and dataset.outliers and dataset.outliers.get('total_outliers', 0) > 0:
        elements.append(PageBreak())
        outlier_heading = Paragraph("Detected Outliers", title_style)
        elements.append(outlier_heading)
        elements.append(Spacer(1, 0.2*inch))
        
        total_outliers = dataset.outliers.get('total_outliers', 0)
        outlier_count_text = Paragraph(
            f"<b>Total Anomalies Detected:</b> {total_outliers}",
            styles['Normal']
        )
        elements.append(outlier_count_text)
        elements.append(Spacer(1, 0.1*inch))
        
        outliers_by_param = dataset.outliers.get('outliers_by_parameter', {})
        
        for param, param_outliers in list(outliers_by_param.items())[:3]:  # Limit to 3 parameters
            param_heading = Paragraph(f"Parameter: {param}", heading_style)
            elements.append(param_heading)
            
            outlier_data = [['Equipment', 'Type', 'Value', 'Expected Range']]
            
            for outlier in param_outliers[:5]:  # Limit to 5 outliers per parameter
                outlier_data.append([
                    outlier.get('equipment_name', 'N/A'),
                    outlier.get('equipment_type', 'N/A'),
                    f"{outlier.get('value', 0):.2f}",
                    f"[{outlier.get('expected_range', [0,0])[0]:.1f}, {outlier.get('expected_range', [0,0])[1]:.1f}]"
                ])
            
            outlier_table = Table(outlier_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1.5*inch])
            outlier_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(outlier_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Correlation Analysis (if available)
    if dataset and dataset.correlation_matrix and dataset.correlation_matrix.get('strong_correlations'):
        elements.append(PageBreak())
        corr_heading = Paragraph("Strong Correlations", title_style)
        elements.append(corr_heading)
        elements.append(Spacer(1, 0.2*inch))
        
        strong_corrs = dataset.correlation_matrix.get('strong_correlations', [])
        
        if strong_corrs:
            corr_data = [['Parameter 1', 'Parameter 2', 'Coefficient']]
            
            for corr in strong_corrs[:10]:  # Limit to 10
                corr_data.append([
                    corr.get('param1', 'N/A'),
                    corr.get('param2', 'N/A'),
                    f"{corr.get('coefficient', 0):.3f}"
                ])
            
            corr_table = Table(corr_data, colWidths=[2*inch, 2*inch, 1.5*inch])
            corr_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d6eaf8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(corr_table)
            elements.append(Spacer(1, 0.1*inch))
            
            note_text = Paragraph(
                "<i>Note: Showing correlations with |coefficient| > 0.7</i>",
                styles['Italic']
            )
            elements.append(note_text)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    return buffer

