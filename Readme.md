# BVB Bonds Yield Plotter

## Description

**BVB Bonds Yield Plotter** is a Python tool that automatically fetches and visualizes the Yield to Maturity (YTM) for
Romanian government bonds (**Titluri de stat**) listed on the Bucharest Stock Exchange (**BVB**). It reads bond
information from the official BVB website, retrieves individual YTM values, caches them for efficiency, and plots the
data by bond maturity date.

The project handles both RON- and EUR-denominated bonds, splitting the data and displaying two charts side-by-side. It
also labels the bonds by their maturity date and ticker symbol, making the analysis easy and intuitive.

## Features

- Automatically downloads the latest bonds listing
- Extracts only Romanian government bonds (**Tip: Titluri de stat**)
- Separately processes RON and EUR bonds
- Fetches and caches Yield to Maturity (YTM) for each bond
- Randomized delay between requests to avoid rate-limiting
- Visualizes the data in clear, sorted plots
- Option to update the cache or use existing cached data

## Requirements

- Python 3.13+
- Libraries:
    - `requests`
    - `beautifulsoup4`
    - `matplotlib`

You can install the required libraries via pip:

```bash
pip install requests beautifulsoup4 matplotlib
```

## Usage

1. **Download the bonds list (bonds_list.csv) and update the cache (one-time or when needed):**

You can manually download the file from https://www.bvb.ro/FinancialInstruments/Markets/Bonds and replace the csv file in the project and then run.

```bash
python main.py --update
```

Or automatically download it (requires session cooke 'cookiesession1' obtained from the same download link above) by running:

```bash
python main.py --download-index --update
```

2. **Run the tool using cached data:**

```bash
python main.py
```

The script will generate two charts:

- Yield to Maturity (YTM) of Titluri de stat - RON
- Yield to Maturity (YTM) of Titluri de stat - EUR

## Notes

- The cookie value used for download (`cookiesession1`) may expire over time and might need updating if downloads fail. You can also manually download the bonds list from https://www.bvb.ro/FinancialInstruments/Markets/Bonds and replace the csv file in the project.

## License

MIT License

