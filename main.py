import csv
import datetime
import json
import os
import random
import re
import time
import traceback

import matplotlib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

matplotlib.use("TkAgg")


def download_bonds_list_csv(output_file="bonds_list.csv"):
    url = "https://www.bvb.ro/FinancialInstruments/Markets/BondsListForDownload.ashx"
    headers = {
        "Cookie": "BVBCulturePref=ro-RO; cookiesession1=****",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Bond list saved as {output_file}")
    else:
        print("Failed to download bond list.")


def get_ytm(code):
    try:
        url = f"https://m.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s={code}"
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data for {code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        match = re.search(r"Randament \(YTM\)\*\s*(\d+,\d+)%", text)

        if match:
            ytm_value = float(match.group(1).replace(',', '.'))
            print(f"Retrieved YTM for {code}: {ytm_value}%")
            return ytm_value
        else:
            print(f"YTM not found for {code}")
            return None
    except Exception:
        print("An exception occurred")
        print(traceback.format_exc())
        return None


def read_codes_and_maturity_from_csv(filename):
    bonds = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            simbol = row.get('Simbol')
            tip = row.get('Tip')
            maturity_date = row.get('Data maturitate')
            if simbol and tip and tip.strip() == 'Titluri de stat' and maturity_date:
                bonds.append((simbol.strip(), maturity_date.strip()))
    return bonds


def load_cached_data(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            return json.load(file)
    return {}


def save_cached_data(cache_file, data):
    with open(cache_file, 'w') as file:
        json.dump(data, file)


def prepare_plot_data(maturities, results):
    sorted_items = sorted(results.items(), key=lambda x: datetime.datetime.strptime(maturities[x[0]], '%d.%m.%Y'))
    x_labels = [f"{maturities[code]} ({code})" for code, _ in sorted_items]
    y_values = [ytm for _, ytm in sorted_items]
    return x_labels, y_values


def plot_ytm_all(maturities_ron, results_ron, maturities_eur, results_eur):
    fig, axs = plt.subplots(2, 1, figsize=(14, 12))

    if results_ron:
        x_labels_ron, y_values_ron = prepare_plot_data(maturities_ron, results_ron)
        axs[0].plot(x_labels_ron, y_values_ron, marker='o', linestyle='-', color='blue')
        axs[0].set_title("Yield to Maturity (YTM) of Titluri de stat - RON")
        axs[0].set_xlabel("Maturity Date (Symbol)")
        axs[0].set_ylabel("YTM (%)")
        axs[0].tick_params(axis='x', rotation=45)
        axs[0].grid(True)

    if results_eur:
        x_labels_eur, y_values_eur = prepare_plot_data(maturities_eur, results_eur)
        axs[1].plot(x_labels_eur, y_values_eur, marker='o', linestyle='-', color='green')
        axs[1].set_title("Yield to Maturity (YTM) of Titluri de stat - EUR")
        axs[1].set_xlabel("Maturity Date (Symbol)")
        axs[1].set_ylabel("YTM (%)")
        axs[1].tick_params(axis='x', rotation=45)
        axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def main(update_cache=False):
    bonds_csv = "bonds_list.csv"
    if not os.path.exists(bonds_csv):
        print(f"Bond list file '{bonds_csv}' not found. Download it first with --download-bonds.")
        return

    bonds = read_codes_and_maturity_from_csv(bonds_csv)
    cache_file = "cache.json"
    cached_data = load_cached_data(cache_file)

    results_ron = {}
    maturities_ron = {}
    results_eur = {}
    maturities_eur = {}

    for code, maturity in bonds:
        if not update_cache:
            if code in cached_data:
                print(f"Using cached YTM for {code}: {cached_data[code]}%")
                ytm = cached_data[code]
            else:
                print(f"No cached found for {code}")
                ytm = None
        else:
            ytm = get_ytm(code)
            if ytm is not None:
                cached_data[code] = ytm
            time.sleep(random.uniform(0.5, 1.5))  # Random delay between 0.5 and 1.5 seconds

        if ytm is not None:
            if code.endswith('E'):
                results_eur[code] = ytm
                maturities_eur[code] = maturity
            else:
                results_ron[code] = ytm
                maturities_ron[code] = maturity

    save_cached_data(cache_file, cached_data)

    plot_ytm_all(maturities_ron, results_ron, maturities_eur, results_eur)


if __name__ == "__main__":
    import sys

    update_cache_flag = "--update" in sys.argv
    if "--download-index" in sys.argv:
        download_bonds_list_csv()
    main(update_cache=update_cache_flag)
