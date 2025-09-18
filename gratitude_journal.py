import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog
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

    def load_config_paths(self):
        """Load directory paths from config.txt file"""
        config_file = os.path.join(os.path.dirname(__file__), 'config.txt')
        paths = []

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        paths.append(line)
        except FileNotFoundError:
            # Prompt user for directory and create config file
            paths = self.create_config_from_user_input(config_file)
        except Exception as e:
            messagebox.showerror(
                "Configuration Error",
                f"Error reading config.txt:\n{str(e)}\n\nPlease select a directory."
            )
            paths = self.create_config_from_user_input(config_file)

        return paths

    def create_config_from_user_input(self, config_file):
        """Prompt user for directory and create config file"""
        while True:
            # Show informational message first
            messagebox.showinfo(
                "First Time Setup",
                "No configuration file found.\n\nPlease select a directory where you want to store your gratitude journal files."
            )

            # Let user choose directory
            directory = filedialog.askdirectory(
                title="Select Directory for Gratitude Journal Files",
                initialdir=os.path.expanduser("~")
            )

            if not directory:
                # User cancelled - ask if they want to try again or exit
                if messagebox.askyesno("Exit?", "No directory selected. Do you want to exit the application?"):
                    self.root.quit()
                    sys.exit()
                continue

            # Test if directory is writable
            test_path = os.path.join(directory, "test_write_permission.tmp")
            try:
                with open(test_path, 'w') as f:
                    f.write("test")
                os.remove(test_path)

                # Directory is accessible, create config file
                self.save_config_file(config_file, directory)

                messagebox.showinfo(
                    "Setup Complete",
                    f"Configuration saved!\n\nYour gratitude journal files will be saved to:\n{directory}\n\nYou can modify the config.txt file later to add more directories."
                )

                return [directory]

            except Exception as e:
                # Directory not accessible, ask user to choose again
                retry = messagebox.askyesno(
                    "Directory Not Accessible",
                    f"Cannot write to the selected directory:\n{directory}\n\nError: {str(e)}\n\nWould you like to choose a different directory?"
                )
                if not retry:
                    self.root.quit()
                    sys.exit()

    def save_config_file(self, config_file, directory):
        """Create a new config.txt file with the user's chosen directory"""
        config_content = f"""# Gratitude Journal Configuration
# List the directories where gratitude journal files should be saved
# The program will try each directory in order until one is accessible
# You can add, remove, or modify these paths as needed

# User selected directory
{directory}

# You can add additional backup locations below:
# C:\\Users\\YourUsername\\Documents\\Gratitude Journal
# C:\\Gratitude Journal
# ~/Documents/Gratitude Journal"""

        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config_content)
        except Exception as e:
            messagebox.showerror(
                "Configuration Error",
                f"Could not save configuration file:\n{str(e)}"
            )
    
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
            # Load paths from configuration file
            folder_paths = self.load_config_paths()

            if not folder_paths:
                raise OSError("No directory paths configured in config.txt")

            folder_path = None
            last_error = None

            for path in folder_paths:
                try:
                    os.makedirs(path, exist_ok=True)
                    folder_path = path
                    break
                except OSError as e:
                    last_error = e
                    continue

            if folder_path is None:
                error_msg = f"None of the configured directories are accessible"
                if last_error:
                    error_msg += f":\nLast error: {str(last_error)}"
                raise OSError(error_msg)
            
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

            # Create the content
            content = f"""## Three things I'm grateful for today:
1. {self.gratitude_entries[0]}
2. {self.gratitude_entries[1]}
3. {self.gratitude_entries[2]}

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
                f"Could not save the gratitude journal:\n{str(e)}\n\nPlease check the directory paths in config.txt and ensure at least one is accessible."
            )
    
    def cancel(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GratitudeJournal()
    app.run()