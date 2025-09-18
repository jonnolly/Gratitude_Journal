# Gratitude Journal

A simple, elegant desktop application for daily gratitude journaling. Record three things you're grateful for each day and save them automatically to your preferred location.

## Features

- **Simple GUI Interface** - Clean, user-friendly design for daily use
- **Three Daily Entries** - Prompts for three gratitude entries per day
- **Automatic File Management** - Creates uniquely named files for multiple entries per day
- **Configurable Storage** - Set your preferred save location via configuration file
- **Silent Execution** - Runs without console windows or distractions

## Quick Start

1. **Download** - Get the latest `gratitude_journal.exe` from the repository
2. **Run** - Double-click the executable to start
3. **First Time Setup** - Choose where to save your gratitude journal files
4. **Daily Use** - Enter your three daily gratitudes and click "Finish"

## File Structure

```
Gratitude_Journal/
├── gratitude_journal.exe    # Main application (double-click to run)
├── gratitude_journal.py     # Source code
├── config.txt              # Directory configuration
└── README.md               # This file
```

## Configuration

The application uses `config.txt` to determine where to save your gratitude files. You can edit this file to:

- Add multiple backup locations
- Change the primary save directory
- Set network drive paths

### Example config.txt:
```
# Primary location
C:\Users\YourName\Documents\Gratitude Journal

# Backup locations
D:\Backups\Gratitude
G:\GoogleDrive\Gratitude
```

## Output Format

Each gratitude entry is saved as a Markdown file with the format:

**Filename:** `YYYY-MM-DD Gratitude.md` (with counter for multiple daily entries)

**Content:**
```markdown
## Three things I'm grateful for today:
1. Your first gratitude entry
2. Your second gratitude entry
3. Your third gratitude entry

---
Tags: #gratitude
```

## Requirements

- **For Executable:** Windows 10/11 (no additional software needed)
- **For Source Code:** Python 3.7+ with tkinter

## Development

To run from source:
```bash
python gratitude_journal.py
```

To build executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name gratitude_journal gratitude_journal.py
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.