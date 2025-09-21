import databuddy as db
from customtkinter import *
from tkinter import filedialog, messagebox
import os, json

app = CTk()
app.geometry("450x540")
app.title("DataBuddy GUI")
set_default_color_theme("green")
set_appearance_mode("dark")
app.resizable(False, False)

ENTRY_WIDTH = 280
BTN_WIDTH = 200
PADY = 12

def browse_input(entry):
    path = filedialog.askopenfilename(title="Select Input File")
    entry.delete(0, END)
    entry.insert(0, path)

def browse_output(entry):
    path = filedialog.askdirectory(title="Select Output Folder")
    entry.delete(0, END)
    entry.insert(0, path)

def convert():
    input_path = entry_input_path.get()
    output_path = entry_output_path.get()
    format = combo_format.get()
    name = entry_name.get()
    try:
        db.convert(input_path, f"{output_path}/{name}.{format}")
        messagebox.showinfo("Success", f"Converted {input_path} to {output_path}/{name}.{format}")
    except PermissionError:
        messagebox.showerror("Permission Error", "You do not have permission to access the selected file or folder.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def encrypt_file():
    input_path = entry_input_path_enc.get()
    password = entry_password.get()
    try:
        db.encrypt(input_path, password=password)
        messagebox.showinfo("Success", f"Encrypted {input_path}")
    except PermissionError:
        messagebox.showerror("Permission Error", "You do not have permission to access the selected file or folder.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_file():
    folder_or_file = entry_output_path_enc.get()
    input_path = entry_input_path_enc.get()
    password = entry_password.get()

    if os.path.isdir(folder_or_file):
        base = os.path.basename(input_path)
        if base.lower().endswith(".enc"):
            base = base[:-4]
        out_path = os.path.join(folder_or_file, base)
    else:
        out_path = folder_or_file

    try:
        db.decrypt(input_path, password=password, out_path=out_path)
        messagebox.showinfo("Success", f"Decrypted to {out_path}")
    except PermissionError:
        messagebox.showerror("Permission Error", "Can't write there. Pick a folder you own.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Title
CTkLabel(app, text="DataBuddy", font=("Segoe UI Bold", 28), text_color="#00FF99").pack(pady=18)

# Tabs
tabview = CTkTabview(app, width=400)
tabview.pack(pady=8, padx=8, fill="both", expand=True)
tabview.add("Convert")
tabview.add("Encrypt & Decrypt")
tabview.add("Visualize")
tabview.add("HTML")

# ---------------- Convert Tab ----------------
convert_tab = tabview.tab("Convert")
frame_input = CTkFrame(convert_tab, fg_color="#222831")
frame_input.pack(pady=PADY, padx=18, fill="x")
entry_input_path = CTkEntry(frame_input, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path.pack(side="left", padx=8, pady=8)
CTkButton(frame_input, text="Browse", command=lambda: browse_input(entry_input_path), width=80, fg_color="#00adb5").pack(side="right", padx=8, pady=8)

frame_output = CTkFrame(convert_tab, fg_color="#222831")
frame_output.pack(pady=PADY, padx=18, fill="x")
entry_output_path = CTkEntry(frame_output, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_output_path.pack(side="left", padx=8, pady=8)
CTkButton(frame_output, text="Browse", command=lambda: browse_output(entry_output_path), width=80, fg_color="#00adb5").pack(side="right", padx=8, pady=8)

CTkLabel(convert_tab, text="Select Format", font=("Segoe UI", 13)).pack(pady=(PADY, 0))
combo_format = CTkComboBox(convert_tab, values=["json", "yml", "csv", "xlsx"], width=ENTRY_WIDTH, font=("Segoe UI", 13))
combo_format.pack(pady=6)

entry_name = CTkEntry(convert_tab, width=ENTRY_WIDTH, placeholder_text="Output File Name", font=("Segoe UI", 14))
entry_name.pack(pady=PADY)

CTkButton(convert_tab, text="Convert", command=convert, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5").pack(pady=PADY)

# ---------------- Encrypt & Decrypt Tab ----------------
enc_tab = tabview.tab("Encrypt & Decrypt")
frame_input_enc = CTkFrame(enc_tab, fg_color="#222831")
frame_input_enc.pack(pady=PADY, padx=18, fill="x")
entry_input_path_enc = CTkEntry(frame_input_enc, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path_enc.pack(side="left", padx=8, pady=8)
CTkButton(frame_input_enc, text="Browse", command=lambda: browse_input(entry_input_path_enc), width=80, fg_color="#00adb5").pack(side="right", padx=8, pady=8)

frame_output_enc = CTkFrame(enc_tab, fg_color="#222831")
frame_output_enc.pack(pady=PADY, padx=18, fill="x")
entry_output_path_enc = CTkEntry(frame_output_enc, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_output_path_enc.pack(side="left", padx=8, pady=8)
CTkButton(frame_output_enc, text="Browse", command=lambda: browse_output(entry_output_path_enc), width=80, fg_color="#00adb5").pack(side="right", padx=8, pady=8)

entry_password = CTkEntry(enc_tab, width=ENTRY_WIDTH, placeholder_text="Password", font=("Segoe UI", 14), show="*")
entry_password.pack(pady=PADY)

CTkButton(enc_tab, text="Encrypt Output File", command=encrypt_file, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5").pack(pady=PADY)
CTkButton(enc_tab, text="Decrypt Output File", command=decrypt_file, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5").pack(pady=PADY)

# ---------------- Visualize Tab ----------------
v_tab = tabview.tab('Visualize')
frame_input_v = CTkFrame(v_tab, fg_color="#222831")
frame_input_v.pack(pady=PADY, padx=18, fill="x")
entry_input_path_v = CTkEntry(frame_input_v, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path_v.pack(side="left", padx=8, pady=8)
CTkButton(frame_input_v, text="Browse", command=lambda: browse_input(entry_input_path_v), width=80, fg_color="#00adb5").pack(side="right", padx=8, pady=8)

frame_options_v = CTkFrame(v_tab, fg_color="#222831")
frame_options_v.pack(pady=2, padx=18, fill="x")
CTkLabel(frame_options_v, text="Select Chart Type", font=("Segoe UI", 13)).pack(pady=2)
combo_format_v = CTkComboBox(frame_options_v, values=["Pie", "Donut", "Line", "Bar","Area"], width=ENTRY_WIDTH, font=("Segoe UI", 13))
combo_format_v.pack(pady=2)
a = CTkSwitch(frame_options_v, text="Show Legend", font=("Segoe UI", 12), width=20)
a.pack(pady=2)
c = CTkSwitch(frame_options_v, text="Toggle Percentages", font=("Segoe UI", 12), width=20)
c.pack(pady=2)

def visualize():
    import pandas as pd
    import matplotlib as mpl
    mpl.use("TkAgg") 
    import matplotlib.pyplot as plt
    import yaml

    path = entry_input_path_v.get().strip()
    ext = os.path.splitext(path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    elif ext == ".csv":
        df = pd.read_csv(path)
    elif ext in [".yml", ".yaml"]:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        df = pd.json_normalize(data) if isinstance(data, (dict, list)) else pd.DataFrame(data)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    if not pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
        df = df.set_index(df.columns[0])

    chart = combo_format_v.get().strip().lower()

    if chart in ("bar", "line", "area"):
        df.plot(kind=chart, ylabel='', legend=bool(a.get()))
        plt.legend(loc="best")
    elif chart == "pie":
        col = df.columns[0]
        df[col].plot(kind="pie", autopct="%1.1f%%" if c.get() == 1 else "%d", ylabel='', legend=bool(a.get()))
        plt.gca().set_aspect('equal')
    elif chart == "donut":
        col = df.columns[0]
        wedges, texts, autotexts = plt.pie(df[col], labels=df.index, autopct="%1.1f%%")
        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        plt.gca().add_artist(centre_circle)
        plt.gca().set_aspect('equal')
    else:
        raise ValueError(f"Unknown chart type: {chart}")

    plt.tight_layout()
    plt.show()

CTkButton(v_tab, text="Load Data", command=visualize).pack(pady=PADY)

# ---------------- HTML Tab ----------------
html_tab = tabview.tab("HTML")
frame_html = CTkFrame(html_tab, fg_color="#222831")
frame_html.pack(pady=PADY, padx=18, fill="both", expand=True)
def load_data(path):
    temp_json = os.path.expanduser("~/temp.json")
    try:
        
        db.convert(path, temp_json)
        with open(temp_json, "r", encoding="utf-8", errors="ignore") as f:
            return json.load(f)
    except Exception:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".json":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return json.load(f)
        elif ext in [".xlsx", ".xls"]:
            return pd.read_excel(path).to_dict(orient="records")
        elif ext == ".csv":
            return pd.read_csv(path).to_dict(orient="records")
        elif ext in [".yml", ".yaml"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = yaml.safe_load(f)
            return pd.json_normalize(data).to_dict(orient="records") if isinstance(data, (dict, list)) else []
        else:
            return []

entry_html = CTkEntry(frame_html, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_html.pack(pady=8, padx=8, fill="x")
CTkButton(frame_html, text="Browse", command=lambda: browse_input(entry_html), width=80, fg_color="#00adb5").pack(pady=8, padx=8)

output_html = CTkTextbox(frame_html, width=ENTRY_WIDTH, font=("Segoe UI", 14), height=200)
output_html.pack(pady=8, padx=8, fill="both", expand=True)

CTkButton(frame_html, text="Save HTML File", command=lambda: save_html_file(output_html.get("1.0", "end")), width=BTN_WIDTH, fg_color="#393e46", hover_color="#00adb5").pack(pady=4)
def save_html_file(html):
    path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])

    save_path = path
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("<html><body>\n" + html + "\n</body></html>")
    return save_path

def preview_in_browser(html):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
        tmp.write("<html><body>\n" + html + "\n</body></html>")
        tmp.flush()
        webbrowser.open("file://" + tmp.name)

def json_to_html_table(path):
    try:
        data = load_data(path)
        if not data:
            return "<table></table>"

        html = "<table border='1'>\n<tr>"
        for key in data[0].keys():
            html += f"<th>{key}</th>"
        html += "</tr>\n"

        for row in data:
            html += "<tr>"
            for value in row.values():
                html += f"<td>{value}</td>"
            html += "</tr>\n"

        html += "</table>"
        return html
    except Exception as e:
        return f"Error: {e}"

CTkButton(frame_html, text="Make HTML Table", command=lambda: output_html.insert("1.0", json_to_html_table(entry_html.get()))).pack()

# Footer
CTkLabel(app, text="© 2024 DataBuddy", font=("Segoe UI", 10), text_color="#aaaaaa").pack(side="bottom", pady=8)

app.mainloop()
import json, os, pandas as pd, yaml, webbrowser, tempfile, html as html_escape

# ✅ Unified loader using db.convert first



# ✅ Convert to HTML
def to_html_table(data):
    if not data:
        return "<table></table>"
    html = "<table border='1'>\n<tr>"
    for key in data[0].keys():
        html += f"<th>{html_escape.escape(str(key))}</th>"
    html += "</tr>\n"
    for row in data:
        html += "<tr>"
        for value in row.values():
            html += f"<td>{html_escape.escape(str(value))}</td>"
        html += "</tr>\n"
    html += "</table>"
    return html

# ✅ Hook for textbox
def make_html_from_file(path, textbox_widget):
    try:
        data = load_data(path)
        html = to_html_table(data)
        textbox_widget.delete("1.0", "end")
        textbox_widget.insert("end", html)
    except Exception as e:
        textbox_widget.delete("1.0", "end")
        textbox_widget.insert("end", f"Error: {e}")

# ✅ Save/Preview buttons


# ✅ Convert to safe HTML table

def to_html_table(data):
    if not data:
        return "<table></table>"

    html = "<table border='1'>\n<tr>"
    for key in data[0].keys():
        html += f"<th>{html_escape.escape(str(key))}</th>"
    html += "</tr>\n"

    for row in data:
        html += "<tr>"
        for value in row.values():
            html += f"<td>{html_escape.escape(str(value))}</td>"
        html += "</tr>\n"

    html += "</table>"
    return html


# ✅ Hook for GUI (textbox preview + save + browser)

def make_html_from_file(path, textbox_widget):
    try:
        data = load_data(path)
        html = to_html_table(data)
        textbox_widget.delete("1.0", "end")
        textbox_widget.insert("end", html)
    except Exception as e:
        textbox_widget.delete("1.0", "end")
        textbox_widget.insert("end", f"Error: {e}")


def save_html_file(html):
    save_path = os.path.expanduser("~/table.html")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("<html><body>\n" + html + "\n</body></html>")
    return save_path


def preview_in_browser(html):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
        tmp.write("<html><body>\n" + html + "\n</body></html>")
        tmp.flush()
        webbrowser.open("file://" + tmp.name)
        return tmp.name
