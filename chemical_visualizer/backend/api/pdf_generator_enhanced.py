"""
Enhanced PDF Report Generator with Graphs and Professional Formatting

This module generates comprehensive PDF reports with:
- Executive summary page
- Statistical visualizations (bar charts, scatter plots, heatmaps)
- AI insights with proper formatting
- Outlier detection results
- Correlation analysis with visual heatmaps
- Professional styling and layout
"""

from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for server-side rendering
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
import logging

logger = logging.getLogger(__name__)

# Set matplotlib style for professional plots
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (6, 4)


def create_bar_chart(data_dict, title, xlabel, ylabel, color='#4a90e2'):
    """Create a bar chart and return as BytesIO buffer"""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    items = list(data_dict.items())
    if len(items) > 10:
        items = items[:10]  # Limit to top 10
    
    labels, values = zip(*items) if items else ([], [])
    
    bars = ax.bar(labels, values, color=color, alpha=0.8, edgecolor='black')
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate labels if needed
    if len(str(max(labels, key=len, default=''))) > 8:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_scatter_plot(df, x_col, y_col, title, color='#e74c3c'):
    """Create a scatter plot and return as BytesIO buffer"""
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.scatter(df[x_col], df[y_col], alpha=0.6, s=50, color=color, edgecolor='black', linewidth=0.5)
    ax.set_xlabel(x_col, fontsize=11, fontweight='bold')
    ax.set_ylabel(y_col, fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_correlation_heatmap(corr_matrix, column_names):
    """Create a correlation heatmap and return as BytesIO buffer"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Convert to numpy array if it's a list
    if isinstance(corr_matrix, list):
        corr_array = np.array(corr_matrix)
    else:
        corr_array = corr_matrix
    
    # Create heatmap
    sns.heatmap(
        corr_array, 
        annot=True, 
        fmt='.2f', 
        cmap='RdBu_r', 
        center=0,
        vmin=-1, 
        vmax=1,
        xticklabels=column_names,
        yticklabels=column_names,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Correlation Coefficient'},
        ax=ax
    )
    
    ax.set_title('Parameter Correlation Matrix', fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    
    return buf


def create_parameter_ranges_chart(min_values, max_values, avg_values):
    """Create a grouped bar chart showing min, max, and average values"""
    fig, ax = plt.subplots(figsize=(7, 4))
    
    parameters = list(avg_values.keys())
    x = np.arange(len(parameters))
    width = 0.25
    
    mins = [min_values.get(p, 0) for p in parameters]
    maxs = [max_values.get(p, 0) for p in parameters]
    avgs = [avg_values.get(p, 0) for p in parameters]
    
    ax.bar(x - width, mins, width, label='Minimum', color='#3498db', alpha=0.8)
    ax.bar(x, avgs, width, label='Average', color='#2ecc71', alpha=0.8)
    ax.bar(x + width, maxs, width, label='Maximum', color='#e74c3c', alpha=0.8)
    
    ax.set_xlabel('Parameters', fontsize=11, fontweight='bold')
    ax.set_ylabel('Values', fontsize=11, fontweight='bold')
    ax.set_title('Parameter Ranges Overview', fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([p.capitalize() for p in parameters])
    ax.legend(frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close(fig)
    
    return buf


def generate_enhanced_report(summary, data, dataset=None):
    """
    Generate an enhanced PDF report with graphs and professional formatting.
    
    Args:
        summary (dict): Summary statistics from the analysis
        data (list): List of dictionaries containing the raw data
        dataset (Dataset): Dataset model instance with AI fields (optional)
    
    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.75*inch, 
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        spaceBefore=0,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8,
        backColor=colors.HexColor('#ecf0f1')
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # ============ COVER PAGE ============
    elements.append(Spacer(1, 1.5*inch))
    
    title = Paragraph("Chemical Equipment<br/>Parameter Analysis Report", title_style)
    elements.append(title)
    
    elements.append(Spacer(1, 0.3*inch))
    
    subtitle = Paragraph(
        f"Comprehensive Analysis of {summary.get('total_count', 0)} Equipment Records<br/>"
        "with AI-Powered Insights and Statistical Visualizations",
        subtitle_style
    )
    elements.append(subtitle)
    
    elements.append(Spacer(1, 2*inch))
    
    # Summary box on cover
    summary_data = [
        ['Total Equipment', str(summary.get('total_count', 0))],
        ['Equipment Types', str(len(summary.get('type_distribution', {})))],
        ['Parameters Analyzed', '3 (Flowrate, Pressure, Temperature)'],
    ]
    
    if dataset:
        if dataset.outliers and dataset.outliers.get('total_outliers'):
            summary_data.append(['Outliers Detected', str(dataset.outliers['total_outliers'])])
        if dataset.ai_insights and dataset.ai_insights.get('risk_level'):
            risk_level = dataset.ai_insights['risk_level'].upper()
            summary_data.append(['Risk Level', risk_level])
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#2c3e50')),
    ]))
    
    elements.append(summary_table)
    elements.append(PageBreak())
    
    # ============ EXECUTIVE SUMMARY (AI INSIGHTS) ============
    if dataset and dataset.ai_insights and dataset.ai_insights.get('executive_summary'):
        elements.append(Paragraph("Executive Summary", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        ai_insights = dataset.ai_insights
        
        # Risk Level Badge
        if ai_insights.get('risk_level'):
            risk_level = ai_insights['risk_level'].upper()
            risk_colors_map = {
                'LOW': colors.green,
                'MEDIUM': colors.orange,
                'HIGH': colors.orangered,
                'CRITICAL': colors.red,
                'UNKNOWN': colors.grey
            }
            risk_color = risk_colors_map.get(risk_level, colors.grey)
            
            risk_data = [[f"RISK LEVEL: {risk_level}"]]
            risk_table = Table(risk_data, colWidths=[5*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), risk_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 16),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ]))
            elements.append(risk_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Executive Summary Text
        summary_style = ParagraphStyle(
            'ExecutiveSummary',
            parent=styles['Normal'],
            fontSize=11,
            leading=18,
            alignment=TA_JUSTIFY,
            firstLineIndent=0.25*inch
        )
        exec_text = Paragraph(ai_insights['executive_summary'], summary_style)
        elements.append(exec_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Key Findings
        if ai_insights.get('key_findings'):
            elements.append(Paragraph("Key Findings", subheading_style))
            for idx, finding in enumerate(ai_insights['key_findings'][:5], 1):
                finding_text = Paragraph(f"{idx}. {finding}", styles['Normal'])
                elements.append(finding_text)
                elements.append(Spacer(1, 0.08*inch))
            elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        if ai_insights.get('recommendations'):
            elements.append(Paragraph("Strategic Recommendations", subheading_style))
            for idx, rec in enumerate(ai_insights['recommendations'][:5], 1):
                rec_text = Paragraph(f"{idx}. {rec}", styles['Normal'])
                elements.append(rec_text)
                elements.append(Spacer(1, 0.08*inch))
        
        elements.append(PageBreak())
    
    # ============ STATISTICAL OVERVIEW ============
    elements.append(Paragraph("Statistical Overview", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Total count
    count_text = Paragraph(
        f"<b>Total Equipment Analyzed:</b> {summary.get('total_count', 0)} units",
        styles['Normal']
    )
    elements.append(count_text)
    elements.append(Spacer(1, 0.15*inch))
    
    # Equipment Type Distribution Chart
    type_distribution = summary.get('type_distribution', {})
    if type_distribution:
        elements.append(Paragraph("Equipment Type Distribution", subheading_style))
        try:
            chart_buf = create_bar_chart(
                type_distribution,
                'Equipment Count by Type',
                'Equipment Type',
                'Count',
                color='#3498db'
            )
            chart_img = Image(chart_buf, width=5*inch, height=3.33*inch)
            elements.append(chart_img)
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
        elements.append(Spacer(1, 0.2*inch))
    
    # Parameter Ranges Visualization
    avg_values = summary.get('averages', {})
    min_values = summary.get('min_values', {})
    max_values = summary.get('max_values', {})
    
    if avg_values and min_values and max_values:
        elements.append(Paragraph("Parameter Ranges Analysis", subheading_style))
        try:
            ranges_buf = create_parameter_ranges_chart(min_values, max_values, avg_values)
            ranges_img = Image(ranges_buf, width=5.5*inch, height=3.67*inch)
            elements.append(ranges_img)
        except Exception as e:
            logger.error(f"Error creating ranges chart: {e}")
        elements.append(Spacer(1, 0.2*inch))
    
    # Statistical Table
    elements.append(Paragraph("Detailed Statistics", subheading_style))
    
    stat_data = [
        ['Parameter', 'Minimum', 'Average', 'Maximum'],
    ]
    
    for param in ['flowrate', 'pressure', 'temperature']:
        stat_data.append([
            param.capitalize(),
            f"{min_values.get(param, 0):.2f}",
            f"{avg_values.get(param, 0):.2f}",
            f"{max_values.get(param, 0):.2f}"
        ])
    
    stat_table = Table(stat_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ecf0f1'), colors.white]),
    ]))
    
    elements.append(stat_table)
    elements.append(PageBreak())
    
    # ============ CORRELATION ANALYSIS ============
    if dataset and dataset.correlation_matrix:
        elements.append(Paragraph("Correlation Analysis", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        corr_matrix = dataset.correlation_matrix.get('matrix')
        column_names = dataset.correlation_matrix.get('columns', ['Flowrate', 'Pressure', 'Temperature'])
        
        if corr_matrix:
            elements.append(Paragraph("Correlation Heatmap", subheading_style))
            try:
                heatmap_buf = create_correlation_heatmap(corr_matrix, column_names)
                heatmap_img = Image(heatmap_buf, width=5.5*inch, height=4.13*inch)
                elements.append(heatmap_img)
            except Exception as e:
                logger.error(f"Error creating heatmap: {e}")
            
            elements.append(Spacer(1, 0.2*inch))
        
        # Strong correlations table
        strong_corrs = dataset.correlation_matrix.get('strong_correlations', [])
        if strong_corrs:
            elements.append(Paragraph("Strong Correlations (|r| > 0.7)", subheading_style))
            
            corr_data = [['Parameter 1', 'Parameter 2', 'Coefficient', 'Strength']]
            
            for corr in strong_corrs[:10]:
                coef = corr.get('coefficient', 0)
                if abs(coef) > 0.9:
                    strength = 'Very Strong'
                elif abs(coef) > 0.7:
                    strength = 'Strong'
                else:
                    strength = 'Moderate'
                
                corr_data.append([
                    corr.get('param1', 'N/A'),
                    corr.get('param2', 'N/A'),
                    f"{coef:.3f}",
                    strength
                ])
            
            corr_table = Table(corr_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.3*inch])
            corr_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d6eaf8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#d6eaf8'), colors.white]),
            ]))
            
            elements.append(corr_table)
        
        elements.append(PageBreak())
    
    # ============ OUTLIER DETECTION ============
    if dataset and dataset.outliers and dataset.outliers.get('total_outliers', 0) > 0:
        elements.append(Paragraph("Outlier Detection Results", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        total_outliers = dataset.outliers.get('total_outliers', 0)
        outlier_text = Paragraph(
            f"<b>Total Anomalies Detected:</b> {total_outliers} outliers across all parameters",
            styles['Normal']
        )
        elements.append(outlier_text)
        elements.append(Spacer(1, 0.15*inch))
        
        note_text = Paragraph(
            "<i>Outliers detected using the Interquartile Range (IQR) method. "
            "Values outside 1.5×IQR from Q1/Q3 are flagged as anomalies.</i>",
            styles['Italic']
        )
        elements.append(note_text)
        elements.append(Spacer(1, 0.2*inch))
        
        outliers_by_param = dataset.outliers.get('outliers_by_parameter', {})
        
        for param, param_outliers in list(outliers_by_param.items())[:3]:
            elements.append(Paragraph(f"{param.capitalize()} Outliers", subheading_style))
            
            outlier_data = [['Equipment', 'Type', 'Value', 'Expected Range', 'Deviation']]
            
            for outlier in param_outliers[:8]:  # Limit to 8 per parameter
                value = outlier.get('value', 0)
                exp_range = outlier.get('expected_range', [0, 0])
                
                # Calculate deviation percentage
                if exp_range[1] > 0:
                    if value > exp_range[1]:
                        deviation = ((value - exp_range[1]) / exp_range[1]) * 100
                        dev_str = f"+{deviation:.1f}%"
                    else:
                        deviation = ((exp_range[0] - value) / exp_range[0]) * 100
                        dev_str = f"-{deviation:.1f}%"
                else:
                    dev_str = "N/A"
                
                outlier_data.append([
                    outlier.get('equipment_name', 'N/A')[:15],
                    outlier.get('equipment_type', 'N/A')[:12],
                    f"{value:.2f}",
                    f"[{exp_range[0]:.1f}, {exp_range[1]:.1f}]",
                    dev_str
                ])
            
            outlier_table = Table(outlier_data, colWidths=[1.3*inch, 1.2*inch, 0.9*inch, 1.3*inch, 0.8*inch])
            outlier_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fadbd8'), colors.white]),
            ]))
            
            elements.append(outlier_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    try:
        doc.build(elements)
        buffer.seek(0)
        return buffer
    except Exception as e:
        logger.error(f"Error building PDF: {e}")
        # Fallback to basic report
        from .pdf_generator import generate_report as generate_basic_report
        return generate_basic_report(summary, data, dataset)


