import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Theme colors: Forest Green (#1B4D3E) and Accent Gold (#C5A059)
        primary_color = colors.HexColor("#1B4D3E")
        charcoal = colors.HexColor("#2C3E50")
        
        # 1. Left side border line
        self.setStrokeColor(primary_color)
        self.setLineWidth(4)
        self.line(36, 36, 36, 756)
        
        # 2. Header text (on all pages)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(primary_color)
        self.drawString(54, 765, "AgriGuardian AI — Agricultural Health Report")
        
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(54, 758, 558, 758)
        
        # 3. Footer (Page numbers and disclaimer)
        self.line(54, 50, 558, 50)
        self.setFont("Helvetica", 8)
        self.setFillColor(charcoal)
        self.drawString(54, 38, "🛡️ AgriGuardian AI Protection System | Bangladesh BARC & BMD Integrated")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 38, page_str)
        self.restoreState()

def generate_report_pdf(report_data: dict, output_path: str = None) -> bytes:
    """
    Generates a professional agricultural health report PDF.
    If output_path is provided, writes to file. Otherwise returns the PDF bytes.
    """
    buffer = io.BytesIO()
    doc_target = output_path if output_path else buffer
    
    # Margins: Left margin 60 to clear the side border, Right 54, Top 54, Bottom 64
    doc = SimpleDocTemplate(
        doc_target,
        pagesize=letter,
        leftMargin=60,
        rightMargin=54,
        topMargin=54,
        bottomMargin=64
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1B4D3E")
    text_color = colors.HexColor("#2C3E50")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    story = []
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("🛡️ AgriGuardian AI Agricultural Health Report", title_style))
    
    # Metadata info panel
    location = report_data.get("location", "Dhaka").capitalize()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    mode_str = "Demo Simulation" if report_data.get("mode") == "demo" else "Live ADK Agentic Mode"
    
    info_data = [
        [Paragraph("<b>Location:</b>", body_style), Paragraph(location, body_style),
         Paragraph("<b>Date Generated:</b>", body_style), Paragraph(date_str, body_style)],
        [Paragraph("<b>Execution Mode:</b>", body_style), Paragraph(mode_str, body_style),
         Paragraph("<b>Status:</b>", body_style), Paragraph("<font color='#1B4D3E'><b>Completed</b></font>", body_style)]
    ]
    info_table = Table(info_data, colWidths=[100, 150, 100, 150])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F6F4")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))
    
    def format_text_block(text, story):
        if not text:
            return
        import re
        lines = text.split("\n")
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Check for header
            if line_str.startswith("####"):
                story.append(Paragraph(line_str.replace("####", "").strip(), h1_style))
            elif line_str.startswith("###"):
                story.append(Paragraph(line_str.replace("###", "").strip(), h1_style))
            elif line_str.startswith("**") and line_str.endswith("**"):
                story.append(Paragraph(line_str.replace("**", "").strip(), h1_style))
            # Bullet point
            elif line_str.startswith("- ") or line_str.startswith("* ") or (len(line_str) > 2 and line_str[0].isdigit() and line_str[1] == "."):
                bullet_text = line_str.lstrip("- *").strip()
                bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_text)
                story.append(Paragraph(f"&bull; {bullet_text}", bullet_style))
            else:
                body_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line_str)
                story.append(Paragraph(body_text, body_style))
                
    # Section 1: Symptom Profile
    story.append(Paragraph("1. Crop Profile & Symptom Detection", h1_style))
    format_text_block(report_data.get("detector_output", ""), story)
    story.append(Spacer(1, 10))
    
    # Section 2: Clinical Diagnosis
    story.append(Paragraph("2. Clinical Diagnosis", h1_style))
    format_text_block(report_data.get("diagnosis_output", ""), story)
    story.append(Spacer(1, 10))
    
    # Section 3: Treatment Recommendations
    story.append(Paragraph("3. Tiered Treatment Recommendations", h1_style))
    format_text_block(report_data.get("treatment_output", ""), story)
    story.append(Spacer(1, 10))
    
    # Section 4: Weather-Based Farming Advisory
    story.append(Paragraph("4. Weather-Based Farming Advisory", h1_style))
    format_text_block(report_data.get("weather_output", ""), story)
    story.append(Spacer(1, 10))
    
    # Section 5: Farmer Safety Checklist
    story.append(Paragraph("5. Farmer Safety Checklist", h1_style))
    safety_block = (
        "&bull; <b>Personal Protective Equipment:</b> Wear a protective face mask and thick rubber gloves before handling any chemical fungicide.<br/>"
        "&bull; <b>Wind Direction Awareness:</b> Do not spray against the wind direction to avoid pesticide inhalation.<br/>"
        "&bull; <b>Environmental Protection:</b> Dispose of unused sprays and packaging safely away from water sources and ponds.<br/>"
        "&bull; <b>Harvest Interval:</b> Observe the recommended Pre-Harvest Interval (PHI) of 14 days before harvest.<br/>"
        "&bull; <b>Hygiene:</b> Wash hands and face immediately after application with soap and water."
    )
    story.append(Paragraph(safety_block, body_style))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    
    if not output_path:
        buffer.seek(0)
        return buffer.getvalue()
    return b""
