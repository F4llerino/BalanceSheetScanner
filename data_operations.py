import requests

headers2 = {
    "X-RapidAPI-Key": "Add your API-Key from RapidAPI",
    "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
}


# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
#  Get the required data
# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
def query(head, ticker):
    url_balance_sheet = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{0}/balance-sheet" \
        .format(ticker)
    url_income_statement = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{0}/income-statement" \
        .format(ticker)
    url_cashflow_statement = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{0}/cashflow-statement" \
        .format(ticker)

    response_balance_sheet = requests.request("GET", url_balance_sheet, headers=head)
    response_income_statement = requests.request("GET", url_income_statement, headers=head)
    response_cashflow_statement = requests.request("GET", url_cashflow_statement, headers=head)

    balance_sheet = response_balance_sheet.json()
    income_statement = response_income_statement.json()
    cashflow_statement = response_cashflow_statement.json()
    yearly_balance_sheet = balance_sheet.get("balanceSheetHistory", {}).get("balanceSheetStatements")[0]

    umsatz_ganzjahr = response_income_statement.json() \
        .get("incomeStatementHistory", {}).get("incomeStatementHistory")[0].get("totalRevenue").get("raw")
    anlagevermoegen_ganzjahr = yearly_balance_sheet.get("totalAssets").get("raw") - \
                               yearly_balance_sheet.get("totalCurrentAssets").get("raw")
    balance_sheet = balance_sheet.get("balanceSheetHistoryQuarterly", {}).get("balanceSheetStatements")[0]
    income_statement = income_statement.get("incomeStatementHistoryQuarterly", {}).get("incomeStatementHistory")[0]
    cashflow_statement = cashflow_statement.get("cashflowStatementHistory", {}).get("cashflowStatements")[0]

    return [balance_sheet, income_statement, cashflow_statement, umsatz_ganzjahr, anlagevermoegen_ganzjahr]


# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
#  Calculate the ratios
# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
def calculate_ratios(balance_sheet, income_statement, cashflow_statement, umsatz_ganzjahr, av):
    # Input Numbers
    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    #  Assign balance sheet positions
    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    # Balance Sheet
    gesamtkapital = balance_sheet.get("totalAssets", {}).get("raw")
    anlagevermoegen = balance_sheet.get("totalAssets",
                                        {}).get("raw") - balance_sheet.get("totalCurrentAssets", {}).get("raw")
    umlaufvermoegen = balance_sheet.get("totalCurrentAssets", {}).get("raw")
    zahlungsmittel = balance_sheet.get("cash", {}).get("raw")
    forderungen = balance_sheet.get("netReceivables", {}).get("raw")
    eigenkapital = balance_sheet.get("totalStockholderEquity", {}).get("raw")
    langfristiges_fremdkapital = balance_sheet.get("totalLiab",
                                                   {}).get("raw") - balance_sheet.get("totalCurrentLiabilities",
                                                                                      {}).get("raw")
    langfristiges_umlaufvermoegen = balance_sheet.get("netReceivables",
                                                      {}).get("raw") + balance_sheet.get("inventory",
                                                                                         {}).get("raw")
    vorraete = balance_sheet.get("inventory", {}).get("raw")
    kurzfristige_verbindlichkeiten = balance_sheet.get("totalCurrentLiabilities", {}).get("raw")

    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    #  Assign income statement positions
    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    # Income Statement
    netto_gewinn = income_statement.get("netIncome", {}).get("raw")
    umsatz = income_statement.get("totalRevenue", {}).get("raw")
    umsatz_fcf = umsatz_ganzjahr
    zinsaufwand = income_statement.get("interestExpense", {}).get("raw")
    herstellkosten = income_statement.get("costOfRevenue", {}).get("raw")
    if not income_statement.get("sellingGeneralAdministrative", {}):
        sga = 0
        print("Herstellkosten können nicht berechnet werden")
    else:
        sga = income_statement.get("sellingGeneralAdministrative", {}).get("raw")
    steuern = income_statement.get("incomeTaxExpense", {}).get("raw")
    ebit = income_statement.get("ebit", {}).get("raw")

    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    #  Assign cashflow statement positions
    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    # Cashflow Statement
    operativer_cf = cashflow_statement.get("totalCashFromOperatingActivities", {}).get("raw")
    capex = cashflow_statement.get("capitalExpenditures", {}).get("raw")

    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    #  Calculate the specific ratios
    # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
    # Profitable Ratios
    roi = round((((netto_gewinn / umsatz) * (umsatz / gesamtkapital)) * 100), 2)
    eigenkapitalrentabilitaet = round(((netto_gewinn / eigenkapital) * 100), 2)
    gesamtrentabilitaet = round((((netto_gewinn + zinsaufwand) / gesamtkapital) * 100), 2)
    umsatzrentabilitaet = round(((ebit / umsatz) * 100), 2)
    herstellkostenquote = round(((herstellkosten / umsatz) * 100), 2)
    if sga > 0:
        sga_quote = "{0}".format(round(((sga / umsatz) * 100), 2))
    else:
        sga_quote = "-"

    # Financially Ratios
    eigenkapitalquote = round(((eigenkapital / gesamtkapital) * 100), 2)
    anlagenintensitaet = round(((anlagevermoegen / gesamtkapital) * 100), 2)
    umlaufintensitaet = round(((umlaufvermoegen / gesamtkapital) * 100), 2)
    zahlungsmittelintensitaet = round(((zahlungsmittel / gesamtkapital) * 100), 2)
    forderungsintensitaet = round(((forderungen / gesamtkapital) * 100), 2)
    gbr1 = round((eigenkapital / anlagevermoegen) * 100, 2)
    gbr2 = round(((eigenkapital + langfristiges_fremdkapital) / anlagevermoegen) * 100, 2)
    gbr3 = round(((eigenkapital + langfristiges_fremdkapital) / (anlagevermoegen + langfristiges_umlaufvermoegen)) * 100, 2)
    lg1 = round((zahlungsmittel / kurzfristige_verbindlichkeiten) * 100, 2)
    lg2 = round(((zahlungsmittel + forderungen) / kurzfristige_verbindlichkeiten) * 100, 2)
    lg3 = round(((zahlungsmittel + forderungen + vorraete) / kurzfristige_verbindlichkeiten) * 100, 2)

    # Other Ratios
    fcf_quote = round((((operativer_cf + capex) / umsatz_fcf) * 100), 2)
    steuerquote = round(((steuern / ebit) * 100), 2)
    investitionsquote = round(((((-1) * capex) / av) * 100), 2)

    return [{"erfolgswirtschaftlich": [roi, eigenkapitalrentabilitaet, gesamtrentabilitaet, umsatzrentabilitaet,
                                       herstellkostenquote, sga_quote]},
            {"finanzwirtschaftlich": [eigenkapitalquote, anlagenintensitaet, umlaufintensitaet,
                                      zahlungsmittelintensitaet, forderungsintensitaet, gbr1, gbr2, gbr3, lg1, lg2,
                                      lg3]},
            {"sonstige": [fcf_quote, steuerquote, investitionsquote]}]
