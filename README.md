# Water-Chan

---

[![GitHub repo](https://img.shields.io/badge/GitHub-AzuritilDev%2FWaterChan-green.svg?style=plastic&logo=github)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/AzuritilDev/Water-Chan?color=green&label=Code%20Size&style=plastic&logo=github)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub license](https://img.shields.io/github/license/AzuritilDev/Water-Chan?color=green&logo=github&style=plastic&label=License)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub last commit](https://img.shields.io/github/last-commit/AzuritilDev/Water-Chan?color=green&logo=github&style=plastic&label=Last%20Commit)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub issues](https://img.shields.io/github/issues/AzuritilDev/Water-Chan?color=green&logo=github&style=plastic&label=Issues)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub release](https://img.shields.io/github/release/AzuritilDev/Water-Chan?color=green&logo=github&style=plastic&label=Release)](https://github.com/AzuritilDev/Water-Chan)
[![GitHub stars](https://img.shields.io/github/stars/AzuritilDev/Water-Chan?color=green&logo=github&style=plastic&label=Stars)](https://github.com/AzuritilDev/Water-Chan)

## Introduction:
waterchan is a Tkinter-based Python desktop application that reminds you to drink water in a random time between 7 PM - 9 PM locally.
## Overview:
**Disclaimer:** This is a joke application I made for a friend and I do __not__ recommend it for personal use, professional use & especially medical use. Limitation and warranty is limited.
## Packaging:
To build the application directly from the source code, follow these instructions:

-Clone the repository by running:
```bash
git clone https://github.com/AzuritilDev/Water-Chan.git
```

-Change your directory into the cloned repository's directory:
```bash
cd water-chan
```

-Install pyinstaller (skip if you have already done that):
```bash
pip install pyinstaller
```

-Lastly, run this command:

(Windows)
```bash
pyinstaller --onefile --noconsole --paths=. --add-data "assets;assets" --add-data "pyproject;." src/main.py
```

(Linux/MacOS)
```bash
pyinstaller --onefile --noconsole --paths=. --add-data "assets:assets" --add-data "pyproject:." src/main.py
```

-**Note:** This app wasn't built for Linux nor MacOS and it may not run at all yet alone run properly in these operating systems.

## Authors:
[@AzuritilDev](https://github.com/AzuritilDev), The Maintainer (Contact: azuriteluadev@proton.me)
## License:
Distributed under [GNU General Public License v3.0](LICENSE)
