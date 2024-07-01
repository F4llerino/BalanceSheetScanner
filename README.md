# BalanceSheetScanner

Scanning specific profitable and financial ratios  
**YouTube Link**: [Watch the BalanceSheetScanner](https://www.youtube.com/watch?v=9MGYmce9Trk)

**Important**: To properly use the program, you must first add an API key in the `data_operations` file!

## Introduction

The BalanceSheetScanner program displays various financial and performance metrics of companies. One of its key features is the ability to set different filters under "Settings" to highlight specific metrics. By default, no filters are applied. The results can be saved as a PDF file and printed as a hard copy.

## How It Works

- **Data Source**: The program uses data from the Yahoo Finance API, specifically the quarterly financial statements. Due to the absence of quarterly cash flow statements, the annual cash flow statements are used instead.
- **GUI Implementation**: The graphical user interface (GUI) is implemented using Tkinter. All functions are accessible via buttons in the `GUI.py` file.
- **PDF Generation**: The PDF reports are created using the FPDF module and saved in the directory where `main.py` is located.
- **Settings Storage**: User settings are stored in a JSON file within the same directory as `main.py`.

The program performs the configured mathematical comparisons and highlights the results in the results window if a condition is met.

## Features

1. **Initial PDF Creation**: If no PDF file is found in the directory upon first use, the application must be closed completely to create the PDF file for the first time. Once created, the PDF will always be overwritten directly, even if the application is not closed. This behavior must be considered when printing, as the print function is based on the PDF file.
2. **Handling Missing Data**: Some companies may have missing data for certain balance sheet positions, which can result in occasional errors. For example, Deutsche Telekom AG (dte.de) lacks data for the SG&A ratio. This issue has been partially resolved for a few positions.

## Tested Identifiers

The following identifiers have been tested and confirmed to work without errors:
- **lyb** (Lyondell Basell)
- **dte.de** (Deutsche Telekom AG)
- **aapl** (Apple Inc.)

## Usage

1. **Add API Key**: Open the `data_operations` file and add your API key.
2. **Run the Program**: Execute `main.py` to start the application.
3. **Set Filters**: Use the "Settings" menu to apply filters and customize the metrics displayed.
4. **Generate PDF**: Save the results as a PDF file via the provided option in the GUI.
5. **Print Results**: Print the PDF file as needed.

## Contact

For any questions or feedback, please feel free to open an issue on GitHub or reach out directly.

---

*Happy Scanning!* 📊
