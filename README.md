# Aviation Authority Document Scraper

This tool fetches and stores documents from various national aviation authority websites in a structured manner.

## Requirements

- Python 3
- Google Chrome or Chromium
- ChromeDriver (for Selenium)

### Install Chrome/Chromium and ChromeDriver (Ubuntu/Debian)
```
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-driver
```

## Usage

Install dependencies:
```
pip install --break-system-packages -r requirements.txt
```

Run the scraper:
```
python scraper.py
```

## Notes
- CASA Australia is included as a dynamic authority and requires Selenium/ChromeDriver.
- Logs are saved to `scraper.log`.
