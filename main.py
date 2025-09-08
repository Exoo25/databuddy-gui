import databuddy as db
from customtkinter import *
from tkinter import filedialog, messagebox
import os
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

    # if the user picked a folder, create an output filename inside it
    if os.path.isdir(folder_or_file):
        base = os.path.basename(input_path)
        if base.lower().endswith(".enc"):
            base = base[:-4]   # remove .enc
        out_path = os.path.join(folder_or_file, base)
    else:
        out_path = folder_or_file   # assume user typed a file

    try:
        db.decrypt(input_path, password=password, out_path=out_path)
        messagebox.showinfo("Success", f"Decrypted to {out_path}")
    except PermissionError:
        messagebox.showerror("Permission Error",
                             "Can't write there. Pick a folder you own.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

title_label = CTkLabel(app, text="DataBuddy", font=("Segoe UI Bold", 28), text_color="#00FF99")
title_label.pack(pady=18)

# Tabs
tabview = CTkTabview(app, width=400)
tabview.pack(pady=8, padx=8, fill="both", expand=True)
tabview.add("Convert")
tabview.add("Encrypt & Decrypt")
tabview.add('Visualize')

# Convert Tab
convert_tab = tabview.tab("Convert")

frame_input = CTkFrame(convert_tab, fg_color="#222831")
frame_input.pack(pady=PADY, padx=18, fill="x")
entry_input_path = CTkEntry(frame_input, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path.pack(side="left", padx=8, pady=8)
btn_browse_input = CTkButton(frame_input, text="Browse", command=lambda: browse_input(entry_input_path), width=80, fg_color="#00adb5")
btn_browse_input.pack(side="right", padx=8, pady=8)

frame_output = CTkFrame(convert_tab, fg_color="#222831")
frame_output.pack(pady=PADY, padx=18, fill="x")
entry_output_path = CTkEntry(frame_output, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_output_path.pack(side="left", padx=8, pady=8)
btn_browse_output = CTkButton(frame_output, text="Browse", command=lambda: browse_output(entry_output_path), width=80, fg_color="#00adb5")
btn_browse_output.pack(side="right", padx=8, pady=8)

combo_label = CTkLabel(convert_tab, text="Select Format", font=("Segoe UI", 13))
combo_label.pack(pady=(PADY, 0))
combo_format = CTkComboBox(convert_tab, values=["json", "yml", "csv", "xlsx"], width=ENTRY_WIDTH, font=("Segoe UI", 13))
combo_format.pack(pady=6)

entry_name = CTkEntry(convert_tab, width=ENTRY_WIDTH, placeholder_text="Output File Name", font=("Segoe UI", 14))
entry_name.pack(pady=PADY)

btn_convert = CTkButton(convert_tab, text="Convert", command=convert, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5")
btn_convert.pack(pady=PADY)

# Encrypt & Decrypt Tab
enc_tab = tabview.tab("Encrypt & Decrypt")

frame_input_enc = CTkFrame(enc_tab, fg_color="#222831")
frame_input_enc.pack(pady=PADY, padx=18, fill="x")
entry_input_path_enc = CTkEntry(frame_input_enc, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path_enc.pack(side="left", padx=8, pady=8)
btn_browse_input_enc = CTkButton(frame_input_enc, text="Browse", command=lambda: browse_input(entry_input_path_enc), width=80, fg_color="#00adb5")
btn_browse_input_enc.pack(side="right", padx=8, pady=8)

frame_output_enc = CTkFrame(enc_tab, fg_color="#222831")
frame_output_enc.pack(pady=PADY, padx=18, fill="x")
entry_output_path_enc = CTkEntry(frame_output_enc, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_output_path_enc.pack(side="left", padx=8, pady=8)
btn_browse_output_enc = CTkButton(frame_output_enc, text="Browse", command=lambda: browse_output(entry_output_path_enc), width=80, fg_color="#00adb5")
btn_browse_output_enc.pack(side="right", padx=8, pady=8)

entry_password = CTkEntry(enc_tab, width=ENTRY_WIDTH, placeholder_text="Password", font=("Segoe UI", 14), show="*")
entry_password.pack(pady=PADY)

btn_encrypt = CTkButton(enc_tab, text="Encrypt Output File", command=encrypt_file, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5")
btn_encrypt.pack(pady=PADY)

btn_decrypt = CTkButton(enc_tab, text="Decrypt Output File", command=decrypt_file, width=BTN_WIDTH, height=38, font=("Segoe UI Semibold", 15), fg_color="#393e46", hover_color="#00adb5")
btn_decrypt.pack(pady=PADY)

v_tab = tabview.tab('Visualize')
# Visualization Tab
frame_input_v = CTkFrame(v_tab, fg_color="#222831")
frame_input_v.pack(pady=PADY, padx=18, fill="x")
entry_input_path_v = CTkEntry(frame_input_v, width=ENTRY_WIDTH, font=("Segoe UI", 14))
entry_input_path_v.pack(side="left", padx=8, pady=8)
btn_browse_input_v = CTkButton(frame_input_v, text="Browse", command=lambda: browse_input(entry_input_path_v), width=80, fg_color="#00adb5")
btn_browse_input_v.pack(side="right", padx=8, pady=8)
frame_options_v = CTkFrame(v_tab, fg_color="#222831")
frame_options_v.pack(pady=2, padx=18, fill="x")
combo_label_v = CTkLabel(frame_options_v, text="Select Chart Type", font=("Segoe UI", 13))
combo_label_v.pack(pady=2)
combo_format_v = CTkComboBox(frame_options_v, values=["Pie", "Donut", "Line", "Bar","Area"], width=ENTRY_WIDTH, font=("Segoe UI", 13))
combo_format_v.pack(pady=2)
a = CTkSwitch(frame_options_v, text="Show Legend", font=("Segoe UI", 12), width=20)
a.pack(pady=2)
c = CTkSwitch(frame_options_v, text="Toggle Percentages", font=("Segoe UI", 12), width=20)
c.pack(pady=2)
def visualize():
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import yaml

    # ---- load file ----
    path = entry_input_path_v.get().strip()
    ext = os.path.splitext(path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    elif ext == ".csv":
        df = pd.read_csv(path)
    elif ext in [".yml", ".yaml"]:
        # yaml.load can give dicts; normalise to DataFrame
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        df = pd.json_normalize(data) if isinstance(data, (dict, list)) else pd.DataFrame(data)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # ---- set index if first col is labels ----
    if not pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
        df = df.set_index(df.columns[0])

    chart = combo_format_v.get().strip().lower()


    if chart in ("bar", "line", "area"):
    
        df.plot(kind=chart, ylabel='', legend=bool(a.get()))
        plt.legend(loc="best")

    elif chart == "pie":
        # needs a single Series
        col = df.columns[0]       # pick first column by default
        df[col].plot(kind="pie", autopct="%1.1f%%" if c.get() == 1 else "%d", ylabel='', legend=bool(a.get()))
        plt.gca().set_aspect('equal')

    elif chart == "donut":
        col = df.columns[0]
        wedges, texts, autotexts = plt.pie(df[col], labels=df.index, autopct="%1.1f%%")
        # white circle for donut
        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        plt.gca().add_artist(centre_circle)
        plt.gca().set_aspect('equal')
    else:
        raise ValueError(f"Unknown chart type: {chart}")

    plt.tight_layout()
    plt.show()

   

btn_load_v = CTkButton(v_tab, text="Load Data", command=visualize)
btn_load_v.pack(pady=PADY)


# Footer
footer = CTkLabel(app, text="© 2024 DataBuddy", font=("Segoe UI", 10), text_color="#aaaaaa")
footer.pack(side="bottom", pady=8)

app.mainloop()
