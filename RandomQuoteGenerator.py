import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор цитат")
        self.root.geometry("600x500")
        
        self.quotes = [
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "жизнь"},
            {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "изменения"},
            {"text": "Только тот, кто рискует идти далеко, может узнать, как далеко можно зайти.", "author": "Т.С. Элиот", "theme": "риск"},
            {"text": "Сложно победить того, кто никогда не сдается.", "author": "Бейб Рут", "theme": "мотивация"},
        ]
        
        self.history = []
        self.load_history()
        self.create_gui()
    
    def create_gui(self):
        self.gen_btn = tk.Button(self.root, text="Сгенерировать цитату", 
                                  command=self.generate_quote, font=("Arial", 12))
        self.gen_btn.pack(pady=10)
        
        self.quote_text = tk.Text(self.root, height=4, width=60, wrap=tk.WORD, font=("Arial", 11))
        self.quote_text.pack(pady=5)
        self.quote_text.insert("1.0", "Нажмите кнопку")
        self.quote_text.config(state="disabled")
        
        self.quote_info = tk.Label(self.root, text="", font=("Arial", 10, "italic"))
        self.quote_info.pack(pady=5)
        
        self.add_btn = tk.Button(self.root, text="Добавить свою цитату", 
                                 command=self.add_quote)
        self.add_btn.pack(pady=5)
        
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Фильтр по автору:").pack(side=tk.LEFT, padx=5)
        self.author_filter = ttk.Combobox(filter_frame, values=self.get_authors(), width=15)
        self.author_filter.pack(side=tk.LEFT, padx=5)
        self.author_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history())
        
        tk.Label(filter_frame, text="Фильтр по теме:").pack(side=tk.LEFT, padx=5)
        self.theme_filter = ttk.Combobox(filter_frame, values=self.get_themes(), width=15)
        self.theme_filter.pack(side=tk.LEFT, padx=5)
        self.theme_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history())
        
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filters).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.root, text="История цитат:", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.history_listbox = tk.Listbox(self.root, height=10, width=70)
        self.history_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.update_history()
    
    def generate_quote(self):
        quote = random.choice(self.quotes)
        
        self.quote_text.config(state="normal")
        self.quote_text.delete("1.0", tk.END)
        self.quote_text.insert("1.0", f'"{quote["text"]}"')
        self.quote_text.config(state="disabled")
        
        self.quote_info.config(text=f"— {quote['author']} (Тема: {quote['theme']})")
        
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history()
    
    def add_quote(self):
        text = simpledialog.askstring("Новая цитата", "Введите текст цитаты:")
        if not text or not text.strip():
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        
        author = simpledialog.askstring("Автор", "Введите имя автора:")
        if not author or not author.strip():
            messagebox.showerror("Ошибка", "Имя автора не может быть пустым!")
            return
        
        theme = simpledialog.askstring("Тема", "Введите тему цитаты:")
        if not theme or not theme.strip():
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        
        self.quotes.append({"text": text.strip(), "author": author.strip(), "theme": theme.strip()})
        self.author_filter['values'] = self.get_authors()
        self.theme_filter['values'] = self.get_themes()
        messagebox.showinfo("Успех", "Цитата добавлена!")
    
    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        
        author = self.author_filter.get()
        theme = self.theme_filter.get()
        
        for item in reversed(self.history):
            if author and item["author"] != author:
                continue
            if theme and item["theme"] != theme:
                continue
            display_text = f'{item["time"]} — "{item["text"][:50]}..." — {item["author"]}'
            self.history_listbox.insert(tk.END, display_text)
    
    def reset_filters(self):
        self.author_filter.set('')
        self.theme_filter.set('')
        self.update_history()
    
    def get_authors(self):
        return sorted(list(set(q["author"] for q in self.quotes)))
    
    def get_themes(self):
        return sorted(list(set(q["theme"] for q in self.quotes)))
    
    def save_history(self):
        # Сохраняем на рабочий стол
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "history.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "history.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()