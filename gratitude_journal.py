import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os
import sys

class GratitudeJournal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Gratitude Journal")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set window icon (if icon file exists)
        try:
            self.root.iconbitmap("gratitude_icon.ico")
        except:
            pass  # Ignore if icon file doesn't exist
        
        # Center the window
        self.center_window()
        
        # Configure style
        self.root.configure(bg='#f0f8ff')
        
        # Variables to store gratitude entries
        self.gratitude_entries = []
        self.current_entry = 0
        
        # Create the UI
        self.create_widgets()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="My Gratitude Journal", 
            font=("Arial", 20, "bold"),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Date
        today = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(
            self.root,
            text=today,
            font=("Arial", 12),
            bg='#f0f8ff',
            fg='#7f8c8d'
        )
        date_label.pack(pady=5)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(pady=20, padx=30, fill='x')
        
        # Question label
        self.question_label = tk.Label(
            main_frame,
            text="What is the first thing you're grateful for today?",
            font=("Arial", 14),
            bg='#f0f8ff',
            fg='#2c3e50',
            wraplength=400,
            justify='center'
        )
        self.question_label.pack(pady=15)
        
        # Entry field
        self.entry_var = tk.StringVar()
        self.entry_field = tk.Entry(
            main_frame,
            textvariable=self.entry_var,
            font=("Arial", 12),
            width=50,
            relief='ridge',
            bd=2
        )
        self.entry_field.pack(pady=10)
        self.entry_field.focus()
        
        # Bind Enter key to submit
        self.entry_field.bind('<Return>', lambda event: self.submit_entry())
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#f0f8ff')
        button_frame.pack(pady=20)
        
        # Submit button
        self.submit_btn = tk.Button(
            button_frame,
            text="Next",
            command=self.submit_entry,
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.submit_btn.pack(side='left', padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=8,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        cancel_btn.pack(side='left', padx=10)
        
        # Progress indicator
        self.progress_label = tk.Label(
            main_frame,
            text="Entry 1 of 3",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#7f8c8d'
        )
        self.progress_label.pack(pady=10)
    
    def submit_entry(self):
        entry_text = self.entry_var.get().strip()
        
        if not entry_text:
            messagebox.showwarning("Empty Entry", "Please enter something you're grateful for.")
            return
        
        # Store the entry
        self.gratitude_entries.append(entry_text)
        self.current_entry += 1
        
        # Clear the entry field
        self.entry_var.set("")
        
        if self.current_entry < 3:
            # Update for next entry
            questions = [
                "What is the first thing you're grateful for today?",
                "What is the second thing you're grateful for today?",
                "What is the third thing you're grateful for today?"
            ]
            self.question_label.config(text=questions[self.current_entry])
            self.progress_label.config(text=f"Entry {self.current_entry + 1} of 3")
            
            if self.current_entry == 2:
                self.submit_btn.config(text="Finish")
            
            self.entry_field.focus()
        else:
            # All entries collected, save the file
            self.save_gratitude_journal()
    
    def save_gratitude_journal(self):
        try:
            # Try D: drive first, fallback to G: drive
            folder_paths = [
                r"D:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal",
                r"G:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal"
            ]
            
            folder_path = None
            for path in folder_paths:
                try:
                    os.makedirs(path, exist_ok=True)
                    folder_path = path
                    break
                except OSError:
                    continue
            
            if folder_path is None:
                raise OSError("Neither D: nor G: drive is accessible")
            
            # Generate filename with today's date
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"{today} Gratitude.md"
            filepath = os.path.join(folder_path, filename)
            
            # Create the content
            content = f"""## Three things I'm grateful for today:
1. {self.gratitude_entries[0]}
2. {self.gratitude_entries[1]}
3. {self.gratitude_entries[2]}

---
Tags: #gratitude"""
            
            # Check if file already exists
            if os.path.exists(filepath):
                result = messagebox.askyesno(
                    "File Exists", 
                    f"A gratitude journal for today already exists.\nDo you want to overwrite it?"
                )
                if not result:
                    return
            
            # Write the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Show success message
            messagebox.showinfo(
                "Success!", 
                f"Your gratitude journal has been saved!\n\nFile: {filename}\nLocation: {folder_path}"
            )
            
            # Close the application
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Could not save the gratitude journal:\n{str(e)}\n\nPlease check if the D: or G: drive is accessible."
            )
    
    def cancel(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GratitudeJournal()
    app.run()