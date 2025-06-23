import sqlite3
import random
from datetime import datetime
from PyQt5 import QtWidgets

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('menu.db')
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_list (
                    name VARCHAR,
                    category VARCHAR,
                    taste VARCHAR,
                    prep_time VARCHAR,
                    cost VARCHAR,
                    method VARCHAR,
                    ingredients VARCHAR
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS history_list (
                    Name VARCHAR,
                    Title VARCHAR,
                    Category VARCHAR,
                    Date VARCHAR,
                    Status VARCHAR,
                    Notes VARCHAR
                )
            ''')
            self.conn.commit()
        except Exception as e:
            raise Exception("Gagal menginisialisasi database!")

    def load_history(self, app):
        try:
            if not hasattr(app, 'historyTable'):
                QtWidgets.QMessageBox.warning(app, "Error", "Widget historyTable tidak ditemukan di UI!")
                return
            app.historyTable.setRowCount(0)
            app.historyTable.setColumnCount(6)
            app.historyTable.setHorizontalHeaderLabels(["Name", "Title", "Category", "Date", "Status", "Notes"])
            app.historyTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            header = app.historyTable.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
            header.setStretchLastSection(True)
            self.cursor.execute("SELECT Name, Title, Category, Date, Status, Notes FROM history_list")
            rows = self.cursor.fetchall()
            if not rows:
                QtWidgets.QMessageBox.information(app, "Info", "Tidak ada data riwayat untuk ditampilkan.")
                return
            for row_data in rows:
                row = app.historyTable.rowCount()
                app.historyTable.insertRow(row)
                for col, data in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(data or ""))
                    app.historyTable.setItem(row, col, item)
            app.historyTable.resizeColumnsToContents()
            app.historyTable.resizeRowsToContents()
        except Exception as e:
            QtWidgets.QMessageBox.critical(app, "Error", f"Gagal memuat riwayat ke tabel: {str(e)}")

    def get_menu_options(self, category, taste, prep_time, cost):
        try:
            options = []
            fallback_used = False
            used_flavor_label = taste
            reason = ""
            query = """
                SELECT name, ingredients FROM menu_list 
                WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                AND (prep_time = ? OR prep_time = 'Any')
            """
            self.cursor.execute(query, [category, taste, cost, prep_time])
            options = [(row[0], row[1]) for row in self.cursor.fetchall()]
            if not options:
                query = """
                    SELECT name, ingredients FROM menu_list 
                    WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                """
                self.cursor.execute(query, [category, taste, cost])
                options = [(row[0], row[1]) for row in self.cursor.fetchall()]
                if options:
                    fallback_used = True
                    reason = f"Waktu persiapan '{prep_time}' tidak tersedia untuk rasa {taste}."
            if not options:
                fallback_used = True
                valid_tastes = ["Manis", "Asin", "Pedas", "Asam"]
                if taste == "Pedas" and category == "Sarapan":
                    reason = f"Rasa {taste} kurang cocok untuk {category}, mencoba rasa lain."
                elif taste == "Asam" and category == "Sarapan":
                    reason = f"Rasa {taste} kurang umum untuk {category}, mencoba rasa lain."
                else:
                    reason = f"Tidak ada menu dengan rasa {taste} untuk {category}."
                for fallback_taste in valid_tastes:
                    query = """
                        SELECT name, ingredients FROM menu_list 
                        WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                    """
                    self.cursor.execute(query, [category, fallback_taste, cost])
                    new_options = [(row[0], row[1]) for row in self.cursor.fetchall()]
                    options.extend(new_options)
                    if new_options:
                        used_flavor_label = fallback_taste
                        break
            if not options:
                query = "SELECT name, ingredients FROM menu_list WHERE category = ? AND method = 'Masak Sendiri'"
                self.cursor.execute(query, [category])
                options = [(row[0]) for row in self.cursor.fetchall()]
                used_flavor_label = taste
                reason = f"Tidak ada menu yang cocok untuk {category} dengan kriteria rasa atau tujuan."
                fallback_used = True
            if options:
                selected_menu = random.choice(options)
                return selected_menu, used_flavor_label, reason, fallback_used
            else:
                return None, used_flavor_label, reason, fallback_used
        except Exception as e:
            return None, taste, "", False

    def save_history(self, name, title, category, status, notes, app):
        try:
            if not all([name, title, category, status, notes]):
                raise ValueError("Semua parameter riwayat harus diisi!")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO history_list (Name, Title, Category, Date, Status, Notes) VALUES (?, ?, ?, ?, ?, ?)",
                (name, title, category, date, status, notes)
            )
            self.conn.commit()
        except Exception as e:
            QtWidgets.QMessageBox.warning(app, "Error", f"Gagal menyimpan riwayat: {str(e)}")

    def clear_history(self):
        try:
            self.cursor.execute("DELETE FROM history_list")
            self.conn.commit()
        except Exception as e:
            pass

    def get_history_data(self):
        try:
            self.cursor.execute("SELECT Name, Title, Category, Date, Status, Notes FROM history_list")
            return self.cursor.fetchall()
        except Exception as e:
            return []