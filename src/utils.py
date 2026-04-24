import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Entry, Button, LEFT, X, BOTH, END, CENTER, W
from datetime import datetime

# --- QUẢN LÝ DỮ LIỆU ---
def load_data(filename, default_val=[]):
    if not os.path.exists("data"): 
        os.makedirs("data")
    path = f"data/{filename}"
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f: 
            json.dump(default_val, f)
        return default_val
    with open(path, "r", encoding="utf-8") as f:
        try: 
            return json.load(f)
        except: 
            return default_val

def save_data(filename, data):
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_questions():
    return load_data("questions.json")

def get_top_history(limit=6):
    history = load_data("history.json")
    # Sắp xếp theo điểm cao nhất
    return sorted(history, key=lambda x: -x.get('score', 0))[:limit]

def save_score(name, score, correct_shots, total_q):
    """Lưu kết quả chi tiết: Tên, Điểm, Accuracy (X/Y)"""
    history = load_data("history.json")
    q_count = total_q if total_q > 0 else 1 
    
    history.append({
        "name": name if name.strip() else "Player 1",
        "score": score,
        "accuracy": f"{correct_shots}/{q_count}",
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    save_data("history.json", history)

# --- GIAO DIỆN QUẢN LÝ ---
def open_add_question_ui():
    root = tk.Tk()
    root.title("HỆ THỐNG QUẢN TRỊ GAME")
    root.geometry("1100x700")
    
    tab_control = ttk.Notebook(root)
    tab1 = Frame(tab_control, bg="#f5f6fa")
    tab2 = Frame(tab_control, bg="#f5f6fa")
    tab_control.add(tab1, text=' QUẢN LÝ CÂU HỎI ')
    tab_control.add(tab2, text=' LỊCH SỬ CHI TIẾT ')
    tab_control.pack(expand=1, fill="both")

    # TAB 1: CÂU HỎI
    top_f = Frame(tab1, bg="#f5f6fa", pady=10)
    top_f.pack(fill=X)
    
    def create_field(parent, label, width):
        f = Frame(parent, bg="#f5f6fa")
        f.pack(side=LEFT, padx=10)
        Label(f, text=label, bg="#f5f6fa", font=("Arial", 9, "bold")).pack(anchor=W)
        e = Entry(f, font=("Arial", 11), width=width)
        e.pack(); return e

    en_q = create_field(top_f, "Câu hỏi:", 30)
    en_a = create_field(top_f, "Đúng:", 10)
    en_w1 = create_field(top_f, "Sai 1:", 10)
    en_w2 = create_field(top_f, "Sai 2:", 10)

    tree_q = ttk.Treeview(tab1, columns=("q", "a", "w1", "w2"), show="headings", height=15)
    for c, h in zip(("q", "a", "w1", "w2"), ("CÂU HỎI", "ĐÚNG", "SAI 1", "SAI 2")):
        tree_q.heading(c, text=h)
        tree_q.column(c, width=150)
    tree_q.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def on_select(event):
        sel = tree_q.selection()
        if sel:
            v = tree_q.item(sel[0])['values']
            for e, val in zip([en_q, en_a, en_w1, en_w2], v):
                e.delete(0, END); e.insert(0, val)
    tree_q.bind("<<TreeviewSelect>>", on_select)

    def add_update():
        sel = tree_q.selection()
        vals = (en_q.get(), en_a.get(), en_w1.get(), en_w2.get())
        if all(vals):
            if sel: tree_q.item(sel[0], values=vals)
            else: tree_q.insert("", END, values=vals)
            for e in [en_q, en_a, en_w1, en_w2]: e.delete(0, END)

    btn_f = Frame(tab1, bg="#f5f6fa", pady=10)
    btn_f.pack()
    Button(btn_f, text="THÊM/CẬP NHẬT", bg="#2ecc71", fg="white", width=15, command=add_update).pack(side=LEFT, padx=5)
    Button(btn_f, text="XÓA", bg="#e74c3c", fg="white", width=15, command=lambda: [tree_q.delete(s) for s in tree_q.selection()]).pack(side=LEFT, padx=5)
    Button(btn_f, text="LƯU DỮ LIỆU", bg="#3498db", fg="white", width=15, command=lambda: [
        save_data("questions.json", [{"question": str(tree_q.item(i)['values'][0]), "correct": str(tree_q.item(i)['values'][1]), 
                                     "options": [str(tree_q.item(i)['values'][1]), str(tree_q.item(i)['values'][2]), str(tree_q.item(i)['values'][3])]} 
                                    for i in tree_q.get_children()]),
        messagebox.showinfo("Thông báo", "Đã lưu!"), root.destroy()]).pack(side=LEFT, padx=5)

    for q in load_data("questions.json"): 
        tree_q.insert("", END, values=(q['question'], q['correct'], q['options'][1], q['options'][2]))

    # TAB 2: LỊCH SỬ
    tree_h = ttk.Treeview(tab2, columns=("d", "n", "s", "a"), show="headings")
    for c, h in zip(("d", "n", "s", "a"), ("NGÀY", "TÊN", "ĐIỂM", "CHÍNH XÁC (ĐÚNG/TỔNG)")):
        tree_h.heading(c, text=h); tree_h.column(c, anchor=CENTER)
    tree_h.pack(fill=BOTH, expand=True, padx=10, pady=10)
    for h in sorted(load_data("history.json"), key=lambda x: -x.get('score', 0)):
        tree_h.insert("", END, values=(h.get('date'), h.get('name'), h.get('score'), h.get('accuracy')))

    root.mainloop()