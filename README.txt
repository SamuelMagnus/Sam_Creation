╔══════════════════════════════════════════════════════════╗
║             SAMCREATION — USB Inventory App              ║
║                   Setup & Usage Guide                    ║
╚══════════════════════════════════════════════════════════╝

REQUIREMENTS
─────────────────────────────────────────────────────────
• Python 3.7 or later must be installed on the Windows PC
  you plug this USB into.

  Check by opening Command Prompt and typing:  python --version

  If not installed, download free from:
  https://www.python.org/downloads/
  ⚠ During install, tick "Add Python to PATH"


HOW TO USE
─────────────────────────────────────────────────────────
1. Plug in the USB stick
2. Open the USB drive in File Explorer
3. Double-click  START.bat
4. A small black window will appear — leave it open!
5. Your browser opens automatically with the app
6. Use the app as normal. Data saves automatically to this
   USB stick in the  data/inventory.json  file.
7. When finished, close the browser tab, then close the
   black server window (or press Ctrl+C in it).


FILE STRUCTURE ON THE USB STICK
─────────────────────────────────────────────────────────
StockKeeper/
├── START.bat            ← Double-click to launch
├── server.py            ← The local web server (don't delete)
├── README.txt           ← This file
├── app/
│   └── index.html       ← The app interface
└── data/
    └── inventory.json   ← Your inventory data (auto-created)


TIPS
─────────────────────────────────────────────────────────
• Ctrl+S  in the app forces an immediate save
• Ctrl+N  opens the Add Item form
• Use Export CSV for a spreadsheet backup
• The data/inventory.json file is plain text —
  you can open it in Notepad as a backup copy

MOVING COMPUTERS
─────────────────────────────────────────────────────────
The app works on any Windows PC with Python installed.
Just plug in the USB and double-click START.bat again.
Your data travels with the stick.

PORT USED: 17383 (local only, not accessible over internet)
