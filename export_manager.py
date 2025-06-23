import csv
from datetime import datetime
from PyQt5 import QtWidgets
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from database_manager import DatabaseManager

class ExportManager:
    def __init__(self, app):
        self.app = app
        self.db_manager = DatabaseManager()

    def export_to_csv(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.app, "Save CSV File", "", "CSV Files (*.csv)"
            )
            if file_name:
                with open(file_name, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Title", "Category", "Date", "Status", "Notes"])
                    writer.writerows(self.db_manager.get_history_data())
                QtWidgets.QMessageBox.information(self.app, "Sukses", "Riwayat berhasil diekspor ke CSV!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.app, "Error", f"Gagal mengekspor CSV: {str(e)}")

    def export_to_pdf(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.app, "Save PDF File", "", "PDF Files (*.pdf)"
            )
            if file_name:
                doc = SimpleDocTemplate(
                    file_name,
                    pagesize=letter,
                    leftMargin=50,
                    rightMargin=50,
                    topMargin=50,
                    bottomMargin=50
                )
                data = [["Name", "Title", "Category", "Date", "Status", "Notes"]]
                styles = getSampleStyleSheet()
                style_normal = styles['Normal']
                style_normal.fontName = 'Helvetica'
                style_normal.fontSize = 8
                style_normal.wordWrap = 'CJK'
                for row in self.db_manager.get_history_data():
                    wrapped_row = [
                        Paragraph(str(col or ""), style_normal) if col else ""
                        for col in row
                    ]
                    data.append(wrapped_row)
                page_width = letter[0] - 100
                col_widths = [
                    page_width * 0.15,
                    page_width * 0.20,
                    page_width * 0.15,
                    page_width * 0.15,
                    page_width * 0.18,
                    page_width * 0.17
                ]
                table = Table(data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                header_style = ParagraphStyle(
                    name='Header',
                    fontName='Helvetica-Bold',
                    fontSize=14,
                    alignment=1
                )
                subheader_style = ParagraphStyle(
                    name='Subheader',
                    fontName='Helvetica',
                    fontSize=10,
                    alignment=1
                )
                elements = [
                    Paragraph("MenuPlanner+ Riwayat Menu", header_style),
                    Spacer(1, 12),
                    Paragraph(f"Diekspor pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subheader_style),
                    Spacer(1, 24),
                    table
                ]
                doc.build(elements)
                QtWidgets.QMessageBox.information(self.app, "Sukses", "Riwayat berhasil diekspor ke PDF!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.app, "Error", f"Gagal mengekspor PDF: {str(e)}")

    def clear_history(self):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self.app, "Konfirmasi Hapus",
                "Yakin ingin menghapus semua riwayat?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.No:
                return
            self.db_manager.clear_history()
            self.db_manager.load_history(self.app)
            QtWidgets.QMessageBox.information(self.app, "Sukses", "Riwayat berhasil dihapus!")
        except Exception as e:
            pass