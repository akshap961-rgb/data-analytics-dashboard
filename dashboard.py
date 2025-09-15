import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import create_engine  # Importing SQLAlchemy for database connection

# ------------------ Function to fetch data from MySQL ------------------
def get_data():
    try:
        # Using SQLAlchemy to connect to MySQL
        engine = create_engine('mysql+mysqlconnector://root:root123@localhost/analytics_db')
        
        # Query to fetch data
        query = "SELECT * FROM sales"
        
        # Using pandas to fetch data from SQL using the engine
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return pd.DataFrame()

# ------------------ Dashboard Window ------------------
def open_dashboard():
    df = get_data()
    if df.empty:
        messagebox.showerror("Error", "No data found in Database!")
        return

    # Tkinter Window for Dashboard
    dash = tk.Tk()
    dash.title("Data Analytics Dashboard")
    dash.geometry("400x400")

    # Function to display sales trend
    def show_trend():
        plt.figure(figsize=(6,4))
        sns.lineplot(data=df, x="sale_date", y="price")
        plt.title("Sales Trend")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Function to display top products
    def show_top_products():
        top_products = df.groupby("product_name")["quantity"].sum().reset_index()
        plt.figure(figsize=(6,4))
        sns.barplot(data=top_products, x="product_name", y="quantity")
        plt.title("Top Selling Products")
        plt.tight_layout()
        plt.show()

    # Function to display daily revenue
    def show_revenue():
        df["revenue"] = df["quantity"] * df["price"]
        daily = df.groupby("sale_date")["revenue"].sum().reset_index()
        plt.figure(figsize=(6,4))
        sns.lineplot(data=daily, x="sale_date", y="revenue", marker="o")
        plt.title("Daily Revenue Trend")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Function to export data to Excel
    def export_excel():
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files","*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data exported to {file_path}")

    # Function to export data to PDF
    def export_pdf():
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files","*.pdf")])
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica", 10)
            text_obj = c.beginText(40, 750)
            text_obj.textLine("Sales Data Report")
            text_obj.moveCursor(0, 20)

            # Write DataFrame content into PDF
            for col in df.columns:
                text_obj.textLine(f"{col}",)
            text_obj.moveCursor(0, 20)

            for index, row in df.iterrows():
                text_obj.textLine(str(row.values))
            c.drawText(text_obj)
            c.save()
            messagebox.showinfo("Success", f"Report exported to {file_path}")

    # Tkinter UI buttons
    tk.Label(dash, text="Welcome to Analytics Dashboard", font=("Arial",14,"bold")).pack(pady=10)
    tk.Button(dash, text="📈 Sales Trend", width=20, command=show_trend).pack(pady=5)
    tk.Button(dash, text="🔥 Top Products", width=20, command=show_top_products).pack(pady=5)
    tk.Button(dash, text="💰 Revenue Trend", width=20, command=show_revenue).pack(pady=5)
    tk.Button(dash, text="⬇ Export to Excel", width=20, command=export_excel).pack(pady=5)
    tk.Button(dash, text="⬇ Export to PDF", width=20, command=export_pdf).pack(pady=5)

    dash.mainloop()

# This will run when called directly
if __name__ == "__main__":
    open_dashboard()
