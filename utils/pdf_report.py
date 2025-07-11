from fpdf import FPDF
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "MelanoAI Diagnosis Report", ln=True, align="C")
        self.ln(10)

    def add_prediction(self, label, confidence):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Prediction: {label.upper()}", ln=True)
        self.cell(0, 10, f"Confidence: {confidence*100:.2f}%", ln=True)
        self.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        self.ln(10)

    def add_image(self, img_path):
        self.image(img_path, w=100)
        self.ln(10)

    def add_model_info(self, meta):
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Model: {meta['model_name']}", ln=True)
        self.cell(0, 10, f"Version: {meta['version']}", ln=True)
        self.cell(0, 10, f"Trained on: {meta['trained_on']}", ln=True)

def generate_pdf(label, confidence, img_path, meta):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_prediction(label, confidence)
    pdf.add_image(img_path)
    pdf.add_model_info(meta)

    filename = f"MelanoAI_Report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("data", filename)
    pdf.output(filepath)
    return filepath
