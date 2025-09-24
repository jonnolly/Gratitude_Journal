import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import os
import sys
import random
import glob
import re
import csv

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
        self.create_menu()
        self.create_widgets()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import from Presently", command=self.import_from_presently)

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

        # Shuffle button (bottom right corner)
        self.shuffle_btn = tk.Button(
            self.root,
            text="🔀",
            command=self.show_random_entry,
            font=("Arial", 16),
            bg='#e74c3c',
            fg='white',
            width=3,
            height=1,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.shuffle_btn.place(x=450, y=350)

        # Create tooltip for shuffle button
        self.create_tooltip(self.shuffle_btn, "View random entry")
    
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
            
            # Generate filename with today's date and counter
            today = datetime.now().strftime("%Y-%m-%d")
            base_filename = f"{today} Gratitude"
            counter = 0

            # Find the next available filename
            while True:
                if counter == 0:
                    filename = f"{base_filename}.md"
                else:
                    filename = f"{base_filename}_{counter}.md"

                filepath = os.path.join(folder_path, filename)

                if not os.path.exists(filepath):
                    break

                counter += 1

            # Create the content with variable number of entries
            num_entries = len(self.gratitude_entries)
            if num_entries == 3:
                header = "## Three things I'm grateful for today:"
            elif num_entries == 1:
                header = "## One thing I'm grateful for today:"
            elif num_entries == 2:
                header = "## Two things I'm grateful for today:"
            else:
                header = f"## {num_entries} things I'm grateful for today:"

            gratitude_list = "\n".join([f"{i+1}. {entry}" for i, entry in enumerate(self.gratitude_entries)])

            content = f"""{header}
{gratitude_list}

---
Tags: #gratitude"""
            
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
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.configure(bg='black')

            label = tk.Label(
                tooltip,
                text=text,
                bg='black',
                fg='white',
                font=("Arial", 9),
                padx=5,
                pady=2
            )
            label.pack()

            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def show_random_entry(self):
        try:
            # Try to find gratitude journal files
            folder_paths = [
                r"D:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal",
                r"G:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal"
            ]

            all_files = []
            for folder_path in folder_paths:
                if os.path.exists(folder_path):
                    pattern = os.path.join(folder_path, "*Gratitude*.md")
                    files = glob.glob(pattern)
                    all_files.extend(files)

            if not all_files:
                messagebox.showinfo("No Entries", "No gratitude journal entries found to display.")
                return

            # Select a random file
            random_file = random.choice(all_files)

            # Read the content
            with open(random_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract the gratitude items using regex
            pattern = r'\d+\.\s+(.+?)(?=\n\d+\.|\n---|\Z)'
            matches = re.findall(pattern, content, re.DOTALL)

            if matches:
                # Create a new window to display the random entry
                self.display_random_entry_window(random_file, matches)
            else:
                messagebox.showinfo("Error", "Could not parse the selected gratitude entry.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load random entry:\n{str(e)}")

    def display_random_entry_window(self, filename, gratitude_items):
        # Create new window
        random_window = tk.Toplevel(self.root)
        random_window.title("Random Gratitude Entry")
        random_window.geometry("450x400")
        random_window.resizable(True, True)
        random_window.configure(bg='#f0f8ff')

        # Center the window
        random_window.update_idletasks()
        x = (random_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (random_window.winfo_screenheight() // 2) - (400 // 2)
        random_window.geometry(f"450x400+{x}+{y}")

        # Extract date from filename
        filename_only = os.path.basename(filename)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename_only)
        date_str = date_match.group(1) if date_match else "Unknown Date"

        # Title
        title_label = tk.Label(
            random_window,
            text="Random Gratitude Entry",
            font=("Arial", 16, "bold"),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=15)

        # Date
        date_label = tk.Label(
            random_window,
            text=date_str,
            font=("Arial", 12),
            bg='#f0f8ff',
            fg='#7f8c8d'
        )
        date_label.pack(pady=5)

        # Button frame FIRST (to reserve space at bottom)
        button_frame = tk.Frame(random_window, bg='#f0f8ff')
        button_frame.pack(side='bottom', pady=10, fill='x')

        # Main container frame (fills remaining space)
        main_container = tk.Frame(random_window, bg='#f0f8ff')
        main_container.pack(pady=(10,0), padx=20, fill='both', expand=True)

        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(main_container, bg='#f0f8ff', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display gratitude items in scrollable frame
        for i, item in enumerate(gratitude_items, 1):
            item_label = tk.Label(
                scrollable_frame,
                text=f"{i}. {item.strip()}",
                font=("Arial", 11),
                bg='#f0f8ff',
                fg='#2c3e50',
                wraplength=380,
                justify='left'
            )
            item_label.pack(pady=8, anchor='w', padx=10)

        # View Another Random Entry button
        another_btn = tk.Button(
            button_frame,
            text="View Another Random Entry",
            command=lambda: self.view_another_random_entry(random_window),
            font=("Arial", 10),
            bg='#3498db',
            fg='white',
            padx=15,
            pady=5,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        another_btn.pack(side='left', padx=5)

        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=random_window.destroy,
            font=("Arial", 10),
            bg='#95a5a6',
            fg='white',
            padx=15,
            pady=5,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        close_btn.pack(side='left', padx=5)

        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def view_another_random_entry(self, current_window):
        """Load and display another random entry, replacing the current content"""
        try:
            # Try to find gratitude journal files
            folder_paths = [
                r"D:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal",
                r"G:\.shortcut-targets-by-id\1SfWBu4Xcf-45vCVl2D6nlal18FFde6c5\62.50 Gratitude Journal"
            ]

            all_files = []
            for folder_path in folder_paths:
                if os.path.exists(folder_path):
                    pattern = os.path.join(folder_path, "*Gratitude*.md")
                    files = glob.glob(pattern)
                    all_files.extend(files)

            if not all_files:
                messagebox.showinfo("No Entries", "No gratitude journal entries found to display.")
                return

            # Select a random file
            random_file = random.choice(all_files)

            # Read the content
            with open(random_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract the gratitude items using regex - handle both original and imported formats
            pattern = r'\d+\.\s+(.+?)(?=\n\d+\.|\n---|\Z)'
            matches = re.findall(pattern, content, re.DOTALL)

            if matches:
                # Close the current window and open a new one with the new entry
                current_window.destroy()
                self.display_random_entry_window(random_file, matches)
            else:
                messagebox.showinfo("Error", "Could not parse the selected gratitude entry.")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load random entry:\n{str(e)}")

    def import_from_presently(self):
        file_path = filedialog.askopenfilename(
            title="Select Presently Backup File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            imported_count = 0
            skipped_count = 0

            with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)

                for row in csv_reader:
                    entry_date = row['entryDate'].strip()
                    entry_content = row['entryContent'].strip()

                    if entry_date and entry_content:
                        success = self.create_gratitude_file_from_presently(entry_date, entry_content)
                        if success:
                            imported_count += 1
                        else:
                            skipped_count += 1

            messagebox.showinfo(
                "Import Complete",
                f"Import completed!\n\n"
                f"Successfully imported: {imported_count} entries\n"
                f"Skipped (already exist): {skipped_count} entries"
            )

        except Exception as e:
            messagebox.showerror(
                "Import Error",
                f"Could not import the Presently backup file:\n{str(e)}"
            )

    def create_gratitude_file_from_presently(self, entry_date, entry_content):
        try:
            # Split entry content by double line-breaks to get individual gratitude items
            # Handle both \r\n\r\n and \n\n patterns
            gratitude_items = re.split(r'\r?\n\r?\n', entry_content.strip())

            # Filter out empty items and strip whitespace
            gratitude_items = [item.strip() for item in gratitude_items if item.strip()]

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

            base_filename = f"{entry_date} Gratitude"
            counter = 0

            while True:
                if counter == 0:
                    filename = f"{base_filename}.md"
                else:
                    filename = f"{base_filename}_{counter}.md"

                filepath = os.path.join(folder_path, filename)

                if not os.path.exists(filepath):
                    break

                counter += 1

            # Create content with numbered list of gratitude items
            gratitude_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(gratitude_items)])

            content = f"""## Things I'm grateful for today (Imported from Presently):
{gratitude_list}

---
Tags: #gratitude #imported-presently"""

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error creating file for {entry_date}: {str(e)}")
            return False

    def cancel(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GratitudeJournal()
    app.run()