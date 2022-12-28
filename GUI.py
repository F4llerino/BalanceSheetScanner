import json
import tkinter as tk
from tkinter import ttk
import data_operations
from fpdf import FPDF
from datetime import date
import os

stock = None
operators = None


class MainWindow:
    def __init__(self, master):
        self.master = master
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create notebook and frames
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Create Notebook
        self.notebook = ttk.Notebook(self.master)
        notebook = self.notebook

        # Notebook Frames
        self.mainframe = tk.Frame(notebook, width=400, height=280)
        self.settings = tk.Frame(notebook, width=400, height=280)
        self.help = tk.Frame(notebook, width=600, height=280)

        # Notebook Layout
        self.mainframe.pack(fill="both", expand=True)
        self.settings.pack(fill="both", expand=True)
        self.help.pack(fill="both", expand=True)

        # Notebook Configuration
        notebook.add(self.mainframe, text="Menü")
        notebook.add(self.settings, text="Einstellungen")
        notebook.add(self.help, text="Hilfe")

        # Mainframe-Widgets
        self.label = tk.Label(self.mainframe, text="Bitte Aktien-Kennzeichnung eingeben!", font=12)
        self.entry = tk.Entry(self.mainframe)
        self.submit = tk.Button(self.mainframe, text="submit", bg="lawngreen", width=15, command=self.submit)

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create scrollbars for setting_frame and help_frame
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Setting-Scrollbar
        setting_canvas = tk.Canvas(self.settings, height=600)
        setting_canvas.config(highlightthickness=0, borderwidth=0)
        setting_canvas.pack(side="left", fill="both", expand=1)

        my_scrollbar_setting = ttk.Scrollbar(self.settings, orient="vertical", command=setting_canvas.yview)
        my_scrollbar_setting.pack(side="right", fill="y")

        setting_canvas.configure(yscrollcommand=my_scrollbar_setting.set)
        setting_canvas.bind("<Configure>", lambda e: setting_canvas.configure(scrollregion=setting_canvas.bbox("all")))

        self.second_setting_canvas = tk.Frame(setting_canvas)

        setting_canvas.create_window((0, 0), window=self.second_setting_canvas, anchor="nw")

        # Help-Scrollbar
        my_canvas = tk.Canvas(self.help, width=475)
        my_canvas.config(highlightthickness=0, borderwidth=0)
        my_canvas.pack(side="left", fill="both", expand=1)

        my_scrollbar = ttk.Scrollbar(self.help, orient="vertical", command=my_canvas.yview)
        my_scrollbar.pack(side="right", fill="y")

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        self.help_canvas = tk.Frame(my_canvas)
        my_canvas.create_window((0, 0), window=self.help_canvas, anchor="nw")

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create widgets for setting_frame
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Labels
        # Header
        self.settings_header = tk.Label(self.second_setting_canvas, text="Ergebnisse der Kennzahlenanalyse",
                                        font=("Arial", 16, "bold"), fg="royalblue")
        self.ew_kennzahlen = tk.Label(self.second_setting_canvas, text="Erfolgswirtschaftliche Kennzahlen",
                                      font=("Arial", 14, "bold"), fg="royalblue")
        self.fw_kennzahlen = tk.Label(self.second_setting_canvas, text="Finanzwirtschaftliche Kennzahlen",
                                      font=("Arial", 14, "bold"), fg="royalblue")
        self.s_kennzahlen = tk.Label(self.second_setting_canvas, text="Sonstige Kennzahlen",
                                     font=("Arial", 14, "bold"), fg="royalblue")

        # Profitable Ratios
        self.roi = tk.Label(self.second_setting_canvas, text="Return on Investment:", font=12)
        self.eigenkapitalrenatibilitaet = tk.Label(self.second_setting_canvas,
                                                   text="Eigenkapitalrentabilität:", font=12)
        self.gesamtrentabilitaet = tk.Label(self.second_setting_canvas, text="Gesamtrentabilität:", font=12)
        self.umsatzrentabilitaet = tk.Label(self.second_setting_canvas, text="Umsatzrentabilität:", font=12)

        # Financially Ratios
        self.eigenkapitalquote = tk.Label(self.second_setting_canvas, text="Eigenkapitalquote:", font=12)
        self.bilanzregel = tk.Label(self.second_setting_canvas, text="Goldene Bilanzregel:", font=12)
        self.lg1 = tk.Label(self.second_setting_canvas, text="Liquidität 1. Grades:", font=12)
        self.lg2 = tk.Label(self.second_setting_canvas, text="Liquidität 2. Grades:", font=12)
        self.lg3 = tk.Label(self.second_setting_canvas, text="Liquidität 3. Grades:", font=12)

        # Other Ratios
        self.fcf_quote = tk.Label(self.second_setting_canvas, text="Free-Cashflow-Quote:", font=12)
        self.marge = tk.Label(self.second_setting_canvas, text="Marge:", font=12)

        # Entries
        # Profitable Ratios
        self.roi_e = tk.Entry(self.second_setting_canvas)
        self.eigenkapitalrenatibilitaet_e = tk.Entry(self.second_setting_canvas)
        self.gesamtrentabilitaet_e = tk.Entry(self.second_setting_canvas)
        self.umsatzrentabilitaet_e = tk.Entry(self.second_setting_canvas)

        # Financially Ratios
        self.eigenkapitalquote_e = tk.Entry(self.second_setting_canvas)
        self.bilanzregel_e = tk.Entry(self.second_setting_canvas)
        self.lg1_e = tk.Entry(self.second_setting_canvas)
        self.lg2_e = tk.Entry(self.second_setting_canvas)
        self.lg3_e = tk.Entry(self.second_setting_canvas)

        # Other Ratios
        self.fcf_quote_e = tk.Entry(self.second_setting_canvas)

        # Option-Menus
        operators = ["<", "<=", ">=", ">"]
        # Option-Menu ROI
        self.roi_om_var = tk.StringVar(self.second_setting_canvas)
        self.roi_om = tk.OptionMenu(self.second_setting_canvas, self.roi_om_var, *operators,
                                    command=self.get_setting_operators)
        # Option-Menu Eigenkapitalrentabilität
        self.eigenkapitalrenatibilitaet_om_var = tk.StringVar(self.second_setting_canvas)
        self.eigenkapitalrenatibilitaet_om = tk.OptionMenu(self.second_setting_canvas,
                                                           self.eigenkapitalrenatibilitaet_om_var,
                                                           *operators)
        # Option-Menu Gesamtrentabilität
        self.gesamtrentabilitaet_om_var = tk.StringVar(self.second_setting_canvas)
        self.gesamtrentabilitaet_om = tk.OptionMenu(self.second_setting_canvas, self.gesamtrentabilitaet_om_var,
                                                    *operators)
        # Option-Menu Umsatzrentabilität
        self.umsatzrentabilitaet_om_var = tk.StringVar(self.second_setting_canvas)
        self.umsatzrentabilitaet_om = tk.OptionMenu(self.second_setting_canvas, self.umsatzrentabilitaet_om_var,
                                                    *operators)
        # Option-Menu Eigenkapitalquote
        self.eigenkapitalquote_om_var = tk.StringVar(self.second_setting_canvas)
        self.eigenkapitalquote_om = tk.OptionMenu(self.second_setting_canvas, self.eigenkapitalquote_om_var,
                                                  *operators)
        # Option-Menu Goldene Bilanzregel
        self.bilanzregel_om_var = tk.StringVar(self.second_setting_canvas)
        self.bilanzregel_om = tk.OptionMenu(self.second_setting_canvas, self.bilanzregel_om_var,
                                            *operators)
        # Option-Menu Liquidität 1. Grades
        self.lg1_om_var = tk.StringVar(self.second_setting_canvas)
        self.lg1_om = tk.OptionMenu(self.second_setting_canvas, self.lg1_om_var,
                                    *operators)
        # Option-Menu Liquidität 2. Grades
        self.lg2_om_var = tk.StringVar(self.second_setting_canvas)
        self.lg2_om = tk.OptionMenu(self.second_setting_canvas, self.lg2_om_var,
                                    *operators)
        # Option-Menu Liquidität 3. Grades
        self.lg3_om_var = tk.StringVar(self.second_setting_canvas)
        self.lg3_om = tk.OptionMenu(self.second_setting_canvas, self.lg3_om_var,
                                    *operators)
        # Option-Menu FCF-Quote
        self.fcf_quote_om_var = tk.StringVar(self.second_setting_canvas)
        self.fcf_quote_om = tk.OptionMenu(self.second_setting_canvas, self.fcf_quote_om_var,
                                          *operators)

        # Buttons
        self.default_button = tk.Button(self.second_setting_canvas, text="Default", width=10, bg="plum",
                                        command=self.default_settings)
        self.save_button = tk.Button(self.second_setting_canvas, text="Save", width=10, bg="lawngreen",
                                     command=self.save_settings)
        self.delete_button = tk.Button(self.second_setting_canvas, text="Delete all", width=10, bg="tomato",
                                       command=self.delete_setting_entries)

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Layout for main_frame and setting_frame
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Layout-Mainframe
        self.label.pack(pady=15)
        self.entry.pack(pady=10)
        self.submit.pack(pady=15)

        # Layout Settings
        # Labels
        # Header
        self.settings_header.grid(column=1, row=1, columnspan=3, pady=15)
        self.ew_kennzahlen.grid(column=1, row=2, columnspan=3, pady=15)
        self.fw_kennzahlen.grid(column=1, row=7, columnspan=3, pady=15)
        self.s_kennzahlen.grid(column=1, row=13, columnspan=3, pady=15)

        # Profitable Ratios
        self.roi.grid(column=1, row=3)
        self.eigenkapitalrenatibilitaet.grid(column=1, row=4)
        self.gesamtrentabilitaet.grid(column=1, row=5)
        self.umsatzrentabilitaet.grid(column=1, row=6)

        # Financially Ratios
        self.eigenkapitalquote.grid(column=1, row=8)
        self.bilanzregel.grid(column=1, row=9)
        self.lg1.grid(column=1, row=10)
        self.lg2.grid(column=1, row=11)
        self.lg3.grid(column=1, row=12)

        # Other Ratios
        self.fcf_quote.grid(column=1, row=14)

        # Entries
        # Profitable Ratios
        self.roi_e.grid(column=3, row=3)
        self.eigenkapitalrenatibilitaet_e.grid(column=3, row=4)
        self.gesamtrentabilitaet_e.grid(column=3, row=5)
        self.umsatzrentabilitaet_e.grid(column=3, row=6)

        # Financially Ratios
        self.eigenkapitalquote_e.grid(column=3, row=8)
        self.bilanzregel_e.grid(column=3, row=9)
        self.lg1_e.grid(column=3, row=10)
        self.lg2_e.grid(column=3, row=11)
        self.lg3_e.grid(column=3, row=12)

        # Other Ratios
        self.fcf_quote_e.grid(column=3, row=14)

        # Option-Menus
        self.roi_om.grid(column=2, row=3)
        self.eigenkapitalrenatibilitaet_om.grid(column=2, row=4)
        self.gesamtrentabilitaet_om.grid(column=2, row=5)
        self.umsatzrentabilitaet_om.grid(column=2, row=6)
        self.eigenkapitalquote_om.grid(column=2, row=8)
        self.bilanzregel_om.grid(column=2, row=9)
        self.lg1_om.grid(column=2, row=10)
        self.lg2_om.grid(column=2, row=11)
        self.lg3_om.grid(column=2, row=12)
        self.fcf_quote_om.grid(column=2, row=14)

        # Buttons
        self.default_button.grid(column=1, row=16, pady=15)
        self.save_button.grid(column=2, row=16, pady=15)
        self.delete_button.grid(column=3, row=16, pady=15)

        # Window-Layout
        notebook.pack(pady=10, expand=True)

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create widgets for help_frame
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Labels
        # Header
        self.help_header_def = tk.Label(self.help_canvas, text="Erklärungen der Kennzahlen", font=("Arial", 16, "bold"))
        self.ew_kennzahlen_def = tk.Label(self.help_canvas, text="Erfolgswirtschaftliche Kennzahlen",
                                          font=("Arial", 14, "bold"), fg="royalblue")
        self.fw_kennzahlen_def = tk.Label(self.help_canvas, text="Finanzwirtschaftliche Kennzahlen",
                                          font=("Arial", 14, "bold"), fg="royalblue")
        self.s_kennzahlen_def = tk.Label(self.help_canvas, text="Sonstige Kennzahlen",
                                         font=("Arial", 14, "bold"), fg="royalblue")

        # Profitable Ratios
        self.roi_def = tk.Label(self.help_canvas, text="Return on Investment", font=("Arial", 12, "bold"), fg="crimson")
        self.roi_txt = tk.Label(self.help_canvas, text="Gibt Auskunft über die Verzinsung des eingesetzten Kapitals \n"
                                                       "((Jahresüberschuss / Umsatz) * (Umsatz / Gesamtkapital)) * 100",
                                font=("Arial", 10), fg="black")

        self.eigenkapitalrenatibilitaet_def = tk.Label(self.help_canvas,
                                                       text="Eigenkapitalrentabilität", font=("Arial", 12, "bold"),
                                                       fg="crimson")
        self.eigenkapitalrenatibilitaet_txt = tk.Label(self.help_canvas,
                                                       text="Gibt Auskunft über die Verzinsung des Eigenkapitals \n"
                                                            "(Jahresüberschuss / Eigenkapital) * 100",
                                                       font=("Arial", 10), fg="black")

        self.gesamtrentabilitaet_def = tk.Label(self.help_canvas, text="Gesamtrentabilität", font=("Arial", 12, "bold"),
                                                fg="crimson")
        self.gesamtrentabilitaet_txt = tk.Label(self.help_canvas,
                                                text="Gibt Auskunft über die Verzinsung des Gesamtkapitals \n"
                                                     "((Jahresüberschuss + Zinsaufwendungen) / Gesamtkapital) * 100",
                                                font=("Arial", 10), fg="black")

        self.umsatzrentabilitaet_def = tk.Label(self.help_canvas, text="Umsatzrentabilität", font=("Arial", 12, "bold"),
                                                fg="crimson")
        self.umsatzrentabilitaet_txt = tk.Label(self.help_canvas,
                                                text="Gibt Auskunft über die Marge eines Unternehmens \n"
                                                     "(ebit / umsatz) * 100",
                                                font=("Arial", 10), fg="black")

        self.materialintensitaet_def = tk.Label(self.help_canvas, text="Herstellkostenquote",
                                                font=("Arial", 12, "bold"), fg="crimson")
        self.materialintensitaet_txt = tk.Label(self.help_canvas, text="Anteil der Herstellkosten am Umsatz \n"
                                                                       "(herstellkosten / umsatz) * 100)",
                                                font=("Arial", 10), fg="black")

        self.personalinteansitaet_def = tk.Label(self.help_canvas, text="SG&A-Quote", font=("Arial", 12, "bold"),
                                                 fg="crimson")
        self.personalinteansitaet_txt = tk.Label(self.help_canvas,
                                                 text="Anteil der Vertriebs- und Verwaltungsgemeinkosten \n"
                                                      "am Umsatz\n (sga / umsatz) * 100)",
                                                 font=("Arial", 10), fg="black")

        # Financially Ratios
        self.eigenkapitalquote_def = tk.Label(self.help_canvas, text="Eigenkapitalquote", font=("Arial", 12, "bold"),
                                              fg="crimson")
        self.eigenkapitalquote_txt = tk.Label(self.help_canvas, text="Gibt Auskunft über den Anteil am Gesamtkapital \n"
                                                                     "(eigenkapital / gesamtkapital) * 100",
                                              font=("Arial", 10), fg="black")

        self.anlagenintensitaet_def = tk.Label(self.help_canvas, text="Anlagenintensität", font=("Arial", 12, "bold"),
                                               fg="crimson")
        self.anlagenintensitaet_txt = tk.Label(self.help_canvas,
                                               text="Gibt Auskunft über den Anteil des Anlagevermögens \n"
                                                    "am Gesamtkapital \n (anlagevermoegen / gesamtkapital) * 100",
                                               font=("Arial", 10), fg="black")

        self.umlaufintensitaet_def = tk.Label(self.help_canvas, text="Umlaufintensität", font=("Arial", 12, "bold"),
                                              fg="crimson")
        self.umlaufintensitaet_txt = tk.Label(self.help_canvas,
                                              text="Gibt Auskunft über den Anteil des Umlaufvermögens \n"
                                                   "am Gesamtkapital \n (umlaufvermoegen / gesamtkapital) * 100",
                                              font=("Arial", 10), fg="black")

        self.zahlungsmittelintensitaet_def = tk.Label(self.help_canvas, text="Zahlungsmittelintensität",
                                                      font=("Arial", 12, "bold"), fg="crimson")
        self.zahlungsmittelintensitaet_txt = tk.Label(self.help_canvas,
                                                      text="Gibt Auskunft über den Anteil der Zahlungsmittel \n"
                                                           "am Gesamtkapital \n (zahlungsmittel / gesamtkapital) * 100",
                                                      font=("Arial", 10), fg="black")

        self.forderungsintensitaet_def = tk.Label(self.help_canvas, text="Forderungsintensität",
                                                  font=("Arial", 12, "bold"), fg="crimson")
        self.forderungsintensitaet_txt = tk.Label(self.help_canvas,
                                                  text="Gibt Auskunft über den Anteil der Forderungen \n"
                                                       "am Gesamtkapital \n (forderungen / gesamtkapital) * 100",
                                                  font=("Arial", 10), fg="black")

        self.gbr_def = tk.Label(self.help_canvas, text="Goldene Bilanzregel", font=("Arial", 12, "bold"), fg="crimson")
        self.gbr_txt = tk.Label(self.help_canvas, text="Sämtliche Investitionen in Anlagevermögen müssen über \n"
                                                       "das Eigenkapital finanzierbar sein \n"
                                                       "(eigenkapital / anlagevermoegen)",
                                font=("Arial", 10), fg="black")

        self.lg_def = tk.Label(self.help_canvas, text="Liquiditätsgrade", font=("Arial", 12, "bold"), fg="crimson")
        self.lg_txt = tk.Label(self.help_canvas,
                               text="Gibt Auskunft über die Möglichkeit, kurzfristig anfallende \n"
                                    "Verbindlichkeiten mit dem Barvermögen, Geldvermögen oder \n"
                                    "dem ganzen Umlaufvermögen zu decken \n"
                                    "(zahlungsmittel / kurzfristige_verbindlichkeiten) * 100 \n"
                                    "(zahlungsmittel + forderungen) / kurzfristige_verbindlichkeiten) * 100 \n"
                                    "(zahlungsmittel + forderungen + vorraete) / kurzfristige_verbindlichkeiten) * 100",
                               font=("Arial", 10), fg="black")

        # Other Ratios
        self.fcf_quote_def = tk.Label(self.help_canvas, text="Free-Cashflow-Quote", font=("Arial", 12, "bold"),
                                      fg="crimson")
        self.fcf_quote_txt = tk.Label(self.help_canvas,
                                      text="Gibt Auskunft über den Anteil des Free-Cashflows am Umsatz \n"
                                           "(operativer Cashflow + capex) / Free-Cashflow) * 100)",
                                      font=("Arial", 10), fg="black")

        self.steuerquote_def = tk.Label(self.help_canvas, text="Steuerquote", font=("Arial", 12, "bold"), fg="crimson")
        self.steuerquote_txt = tk.Label(self.help_canvas, text="Gibt Auskunft über den Anteil der Steuern am EBIT \n"
                                                               "(steuern / ebit) * 100",
                                        font=("Arial", 10), fg="black")

        self.investitionsquote_def = tk.Label(self.help_canvas, text="Investitionsquote", font=("Arial", 12, "bold"),
                                              fg="crimson")
        self.investitionsquote_txt = tk.Label(self.help_canvas,
                                              text="Gibt Auskunft über den prozentuallen Anteil der \n"
                                                   "Investitionen am Anlagevermögen \n"
                                                   "(capex) / anlagevermoegen) * 100",
                                              font=("Arial", 10), fg="black")

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Layout for help_frame
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Header
        self.help_header_def.grid(columnspan=3, column=1, row=1, pady=15)
        self.ew_kennzahlen_def.grid(columnspan=3, column=1, row=2, pady=15)
        self.fw_kennzahlen_def.grid(columnspan=3, column=1, row=15, pady=15)
        self.s_kennzahlen_def.grid(columnspan=3, column=1, row=30, pady=15)

        # Profitable Ratios
        self.roi_def.grid(column=1, row=3)
        self.roi_txt.grid(column=1, row=4)

        self.eigenkapitalrenatibilitaet_def.grid(column=1, row=5, pady=10)
        self.eigenkapitalrenatibilitaet_txt.grid(column=1, row=6)

        self.gesamtrentabilitaet_def.grid(column=1, row=7, pady=10)
        self.gesamtrentabilitaet_txt.grid(column=1, row=8)

        self.umsatzrentabilitaet_def.grid(column=1, row=9, pady=10)
        self.umsatzrentabilitaet_txt.grid(column=1, row=10)

        self.materialintensitaet_def.grid(column=1, row=11, pady=10)
        self.materialintensitaet_txt.grid(column=1, row=12)

        self.personalinteansitaet_def.grid(column=1, row=13, pady=10)
        self.personalinteansitaet_txt.grid(column=1, row=14)

        # Financially Ratios
        self.eigenkapitalquote_def.grid(column=1, row=16, pady=10)
        self.eigenkapitalquote_txt.grid(column=1, row=17)

        self.anlagenintensitaet_def.grid(column=1, row=18, pady=10)
        self.anlagenintensitaet_txt.grid(column=1, row=19)

        self.umlaufintensitaet_def.grid(column=1, row=20, pady=10)
        self.umlaufintensitaet_txt.grid(column=1, row=21)

        self.zahlungsmittelintensitaet_def.grid(column=1, row=22, pady=10)
        self.zahlungsmittelintensitaet_txt.grid(column=1, row=23)

        self.forderungsintensitaet_def.grid(column=1, row=24, pady=10)
        self.forderungsintensitaet_txt.grid(column=1, row=25)

        self.gbr_def.grid(column=1, row=26, pady=10)
        self.gbr_txt.grid(column=1, row=27)

        self.lg_def.grid(column=1, row=28, pady=10)
        self.lg_txt.grid(column=1, row=29)

        # Other Ratios
        self.fcf_quote_def.grid(column=1, row=31, pady=10)
        self.fcf_quote_txt.grid(column=1, row=32)

        self.steuerquote_def.grid(column=1, row=33, pady=10)
        self.steuerquote_txt.grid(column=1, row=34)

        self.investitionsquote_def.grid(column=1, row=35, pady=10)
        self.investitionsquote_txt.grid(column=1, row=36)

    # Return chosen operators
    def get_setting_operators(self, value):
        global operators
        val = value
        roi_op = self.roi_om_var.get()
        eigenkapitalrenatibilitaet_op = self.eigenkapitalrenatibilitaet_om_var.get()
        gesamtrentabilitaet_op = self.gesamtrentabilitaet_om_var.get()
        umsatzrentabilitaet_op = self.umsatzrentabilitaet_om_var.get()
        eigenkapitalquote_op = self.eigenkapitalquote_om_var.get()
        bilanzregel_op = self.bilanzregel_om_var.get()
        lg1_op = self.lg1_om_var.get()
        lg2_op = self.lg2_om_var.get()
        lg3_op = self.lg3_om_var.get()
        fcf_quote_op = self.fcf_quote_om_var.get()

        return {"roi": roi_op}, \
               {"eigenkapitalrentabilitaet": eigenkapitalrenatibilitaet_op}, \
               {"gesamtrentabilitaet": gesamtrentabilitaet_op}, \
               {"umsatzrentabilitaet": umsatzrentabilitaet_op}, \
               {"eigenkapitalquote": eigenkapitalquote_op}, \
               {"bilanzregel": bilanzregel_op}, \
               {"lg1": lg1_op}, \
               {"lg2": lg2_op}, \
               {"lg3": lg3_op}, \
               {"fcf_quote": fcf_quote_op}

    # Return chosen numbers for comparison
    def get_setting_entries(self):
        setting_entries = {"roi_entry": self.roi_e.get()}, \
                          {"eigenkapitalrentabilitaet_entry": self.eigenkapitalrenatibilitaet_e.get()}, \
                          {"gesamtrentabilitaet_entry": self.gesamtrentabilitaet_e.get()}, \
                          {"umsatzrentabilitaet_entry": self.umsatzrentabilitaet_e.get()}, \
                          {"eigenkapitalquote_entry": self.eigenkapitalquote_e.get()}, \
                          {"bilanzregel_entry": self.bilanzregel_e.get()}, \
                          {"lg1_entry": self.lg1_e.get()}, \
                          {"lg2_entry": self.lg2_e.get()}, \
                          {"lg3_entry": self.lg3_e.get()}, \
                          {"fcf_quote_entry": self.fcf_quote_e.get()}
        return setting_entries

    # Save chosen settings (operators & numbers) in a JSON-File
    def save_settings(self):
        op = self.get_setting_operators(3)
        nums = self.get_setting_entries()
        output = op, nums

        txt_file = open("settings.json", "w")
        txt_file.write(json.dumps(output))
        txt_file.close()

    # Save no operators and no numbers as default settings
    def default_settings(self):
        default_entry_dict = {"roi_entry": ""}, \
                             {"eigenkapitalrentabilitaet_entry": ""}, \
                             {"gesamtrentabilitaet_entry": ""}, \
                             {"umsatzrentabilitaet_entry": ""}, \
                             {"eigenkapitalquote_entry": ""}, \
                             {"bilanzregel_entry": ""}, \
                             {"lg1_entry": ""}, \
                             {"lg2_entry": ""}, \
                             {"lg3_entry": ""}, \
                             {"fcf_quote_entry": ""}
        default_operator_dict = {"roi": ""}, \
                                {"eigenkapitalrentabilitaet": ""}, \
                                {"gesamtrentabilitaet": ""}, \
                                {"umsatzrentabilitaet": ""}, \
                                {"eigenkapitalquote": ""}, \
                                {"bilanzregel": ""}, \
                                {"lg1": ""}, \
                                {"lg2": ""}, \
                                {"lg3": ""}, \
                                {"fcf_quote": ""}

        output = default_operator_dict, default_entry_dict
        txt_file = open("settings.json", "w")
        txt_file.write(json.dumps(output))
        txt_file.close()

    # Delete all entries in setting_frame
    def delete_setting_entries(self):
        # Profitable Ratios
        self.roi_e.delete(0, "end")
        self.eigenkapitalrenatibilitaet_e.delete(0, "end")
        self.gesamtrentabilitaet_e.delete(0, "end")
        self.umsatzrentabilitaet_e.delete(0, "end")

        # Financially Ratios
        self.eigenkapitalquote_e.delete(0, "end")
        self.bilanzregel_e.delete(0, "end")
        self.lg1_e.delete(0, "end")
        self.lg2_e.delete(0, "end")
        self.lg3_e.delete(0, "end")

        # Other Ratios
        self.fcf_quote_e.grid(column=3, row=14)

    # Get the Stock
    def get_entry(self):
        global stock

        stock = self.entry.get()
        self.entry.delete(0, "end")

    # Open the ResultWindow
    def submit(self):
        self.get_entry()
        show_result_window()


# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
#  Create ResultWindow
# *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
class ResultWindow:
    def __init__(self, master):
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create frames and scrollbar
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        global stock
        self.master = master
        self.first_frame = tk.Frame(self.master, height=600)
        self.first_frame.grid(column=1, row=1)

        # Setting-Scrollbar
        result_canvas = tk.Canvas(self.first_frame, height=600, width=425)
        result_canvas.config(highlightthickness=0, borderwidth=0)
        result_canvas.pack(side="left", fill="both", expand=1)

        my_scrollbar_setting = ttk.Scrollbar(self.first_frame, orient="vertical", command=result_canvas.yview)
        my_scrollbar_setting.pack(side="right", fill="y")

        result_canvas.configure(yscrollcommand=my_scrollbar_setting.set)
        result_canvas.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

        self.second_result_canvas = tk.Frame(result_canvas)

        result_canvas.create_window((0, 0), window=self.second_result_canvas, anchor="nw")

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Get the data of yahoo finance to calculate the ratios
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        balance_sheet = data_operations.query(data_operations.headers2, stock)[0]
        income_statement = data_operations.query(data_operations.headers2, stock)[1]
        cashflow_statement = data_operations.query(data_operations.headers2, stock)[2]
        umsatz_j = data_operations.query(data_operations.headers2, stock)[3]
        anlagevermoegen_j = data_operations.query(data_operations.headers2, stock)[4]

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create widgets for ResultWindow
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Labels
        # Header
        self.result_header = tk.Label(self.second_result_canvas, text="Kennzahlen-Ergebnisse von: \n{0}".format(stock),
                                      font=("Arial", 16, "bold"), fg="black")
        self.ew_kennzahlen = tk.Label(self.second_result_canvas, text="Erfolgswirtschaftliche Kennzahlen",
                                      font=("Arial", 14, "bold"), fg="royalblue")
        self.fw_kennzahlen = tk.Label(self.second_result_canvas, text="Finanzwirtschaftliche Kennzahlen",
                                      font=("Arial", 14, "bold"), fg="royalblue")
        self.s_kennzahlen = tk.Label(self.second_result_canvas, text="Sonstige Kennzahlen", font=("Arial", 14, "bold"),
                                     fg="royalblue")

        # Profitable Ratios
        self.roi = tk.Label(self.second_result_canvas, text="Return on Investment:", font=("Arial", 12, "bold"),
                            fg="black")
        self.eigenkapitalrenatibilitaet = tk.Label(self.second_result_canvas, text="Eigenkapitalrentabilität:",
                                                   font=("Arial", 12, "bold"), fg="black")
        self.gesamtrentabilitaet = tk.Label(self.second_result_canvas, text="Gesamtrentabilität:",
                                            font=("Arial", 12, "bold"), fg="black")
        self.umsatzrentabilitaet = tk.Label(self.second_result_canvas, text="Umsatzrentabilität:",
                                            font=("Arial", 12, "bold"), fg="black")
        self.materialintensitaet = tk.Label(self.second_result_canvas, text="Herstellkostenquote:",
                                            font=("Arial", 12, "bold"), fg="black")
        self.personalinteansitaet = tk.Label(self.second_result_canvas, text="SG&A-Quote:", font=("Arial", 12, "bold"),
                                             fg="black")

        # Financially Ratios
        self.eigenkapitalquote = tk.Label(self.second_result_canvas, text="Eigenkapitalquote:",
                                          font=("Arial", 12, "bold"), fg="black")
        self.anlagenintensitaet = tk.Label(self.second_result_canvas, text="Anlagenintensität:",
                                           font=("Arial", 12, "bold"), fg="black")
        self.umlaufintensitaet = tk.Label(self.second_result_canvas, text="Umlaufintensität:",
                                          font=("Arial", 12, "bold"), fg="black")
        self.zahlungsmittelintensitaet = tk.Label(self.second_result_canvas, text="Zahlungsmittelintensität:",
                                                  font=("Arial", 12, "bold"), fg="black")
        self.forderungsintensitaet = tk.Label(self.second_result_canvas, text="Forderungsintensität:",
                                              font=("Arial", 12, "bold"), fg="black")
        self.gbr1 = tk.Label(self.second_result_canvas, text="1. Goldene Bilanzregel:", font=("Arial", 12, "bold"),
                             fg="black")
        self.gbr2 = tk.Label(self.second_result_canvas, text="2. Goldene Bilanzregel:", font=("Arial", 12, "bold"),
                             fg="black")
        self.gbr3 = tk.Label(self.second_result_canvas, text="3. Goldene Bilanzregel:", font=("Arial", 12, "bold"),
                             fg="black")
        self.lg1 = tk.Label(self.second_result_canvas, text="Liquidität 1. Grades:", font=("Arial", 12, "bold"),
                            fg="black")
        self.lg2 = tk.Label(self.second_result_canvas, text="Liquidität 2. Grades:", font=("Arial", 12, "bold"),
                            fg="black")
        self.lg3 = tk.Label(self.second_result_canvas, text="Liquidität 3. Grades:", font=("Arial", 12, "bold"),
                            fg="black")

        # Other Ratios
        self.fcf_quote = tk.Label(self.second_result_canvas, text="Free-Cashflow-Quote:", font=("Arial", 12, "bold"),
                                  fg="black")
        self.steuerquote = tk.Label(self.second_result_canvas, text="Steuerquote:", font=("Arial", 12, "bold"),
                                    fg="black")
        self.investitionsquote = tk.Label(self.second_result_canvas, text="Investitionsquote:",
                                          font=("Arial", 12, "bold"), fg="black")

        # Buttons
        self.close_button = tk.Button(self.second_result_canvas, width=10, bg="tomato", text="Close",
                                      command=self.master.destroy)
        self.pdf_button = tk.Button(self.second_result_canvas, width=10, bg="orchid", text="Save as PDF",
                                    command=self.pdf_save)
        self.print_button = tk.Button(self.second_result_canvas, width=10, bg="orange", text="Print",
                                      command=self.print_result)

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Calculate the ratios and save them in a Tkinter-Label
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Results
        # Data
        data = data_operations.calculate_ratios(balance_sheet, income_statement, cashflow_statement, umsatz_j,
                                                anlagevermoegen_j)

        # Profitable Ratios
        self.roi_result = tk.Label(self.second_result_canvas,
                                   text="{0}%".format(data[0].get("erfolgswirtschaftlich")[0]),
                                   font=("Arial", 12, "bold"), fg="black")
        self.eigenkapitalrenatibilitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                          .format(data[0].get("erfolgswirtschaftlich")[1]),
                                                          font=("Arial", 12, "bold"), fg="black")
        self.gesamtrentabilitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                   .format(data[0].get("erfolgswirtschaftlich")[2]),
                                                   font=("Arial", 12, "bold"), fg="black")
        self.umsatzrentabilitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                   .format(data[0].get("erfolgswirtschaftlich")[3]),
                                                   font=("Arial", 12, "bold"), fg="black")
        self.materialintensitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                   .format(data[0].get("erfolgswirtschaftlich")[4]),
                                                   font=("Arial", 12, "bold"), fg="black")
        self.personalinteansitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                    .format(data[0].get("erfolgswirtschaftlich")[5]),
                                                    font=("Arial", 12, "bold"), fg="black")

        # Financially Ratios
        self.eigenkapitalquote_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                 .format(data[1].get("finanzwirtschaftlich")[0]),
                                                 font=("Arial", 12, "bold"), fg="black")
        self.anlagenintensitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                  .format(data[1].get("finanzwirtschaftlich")[1]),
                                                  font=("Arial", 12, "bold"), fg="black")
        self.umlaufintensitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                 .format(data[1].get("finanzwirtschaftlich")[2]),
                                                 font=("Arial", 12, "bold"), fg="black")
        self.zahlungsmittelintensitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                         .format(data[1].get("finanzwirtschaftlich")[3]),
                                                         font=("Arial", 12, "bold"), fg="black")
        self.forderungsintensitaet_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                     .format(data[1].get("finanzwirtschaftlich")[4]),
                                                     font=("Arial", 12, "bold"), fg="black")
        self.gbr1_result = tk.Label(self.second_result_canvas, text="{0}%"
                                    .format(data[1].get("finanzwirtschaftlich")[5]), font=("Arial", 12, "bold"),
                                    fg="black")
        self.gbr2_result = tk.Label(self.second_result_canvas, text="{0}%"
                                    .format(data[1].get("finanzwirtschaftlich")[6]), font=("Arial", 12, "bold"),
                                    fg="black")
        self.gbr3_result = tk.Label(self.second_result_canvas, text="{0}%"
                                    .format(data[1].get("finanzwirtschaftlich")[7]), font=("Arial", 12, "bold"),
                                    fg="black")
        self.lg1_result = tk.Label(self.second_result_canvas, text="{0}%"
                                   .format(data[1].get("finanzwirtschaftlich")[8]), font=("Arial", 12, "bold"),
                                   fg="black")
        self.lg2_result = tk.Label(self.second_result_canvas, text="{0}%"
                                   .format(data[1].get("finanzwirtschaftlich")[9]), font=("Arial", 12, "bold"),
                                   fg="black")
        self.lg3_result = tk.Label(self.second_result_canvas, text="{0}%"
                                   .format(data[1].get("finanzwirtschaftlich")[10]), font=("Arial", 12, "bold"),
                                   fg="black")

        # Other Ratios
        self.fcf_quote_result = tk.Label(self.second_result_canvas, text="{0}%"
                                         .format(data[2].get("sonstige")[0]), font=("Arial", 12, "bold"), fg="black")
        self.steuerquote_result = tk.Label(self.second_result_canvas, text="{0}%"
                                           .format(data[2].get("sonstige")[1]), font=("Arial", 12, "bold"), fg="black")
        self.investitionsquote_result = tk.Label(self.second_result_canvas, text="{0}%"
                                                 .format(data[2].get("sonstige")[2]), font=("Arial", 12, "bold"),
                                                 fg="black")

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Layout for ResultWindow
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # Header
        self.result_header.grid(columnspan=3, column=1, row=1, pady=15)
        self.ew_kennzahlen.grid(columnspan=3, column=1, row=2, pady=15)
        self.fw_kennzahlen.grid(columnspan=3, column=1, row=9, pady=15)
        self.s_kennzahlen.grid(columnspan=3, column=1, row=21, pady=15)

        # Profitable Ratios
        self.roi.grid(column=1, row=3)
        self.eigenkapitalrenatibilitaet.grid(column=1, row=4)
        self.gesamtrentabilitaet.grid(column=1, row=5)
        self.umsatzrentabilitaet.grid(column=1, row=6)
        self.materialintensitaet.grid(column=1, row=7)
        self.personalinteansitaet.grid(column=1, row=8)

        # Financially Ratios
        self.eigenkapitalquote.grid(column=1, row=10)
        self.anlagenintensitaet.grid(column=1, row=11)
        self.umlaufintensitaet.grid(column=1, row=12)
        self.zahlungsmittelintensitaet.grid(column=1, row=13)
        self.forderungsintensitaet.grid(column=1, row=14)
        self.gbr1.grid(column=1, row=15)
        self.gbr2.grid(column=1, row=16)
        self.gbr3.grid(column=1, row=17)
        self.lg1.grid(column=1, row=18)
        self.lg2.grid(column=1, row=19)
        self.lg3.grid(column=1, row=20)

        # Other Ratios
        self.fcf_quote.grid(column=1, row=22)
        self.steuerquote.grid(column=1, row=24)
        self.investitionsquote.grid(column=1, row=25)

        # Results
        # Profitable Ratios
        self.roi_result.grid(column=3, row=3)
        self.eigenkapitalrenatibilitaet_result.grid(column=3, row=4)
        self.gesamtrentabilitaet_result.grid(column=3, row=5)
        self.umsatzrentabilitaet_result.grid(column=3, row=6)
        self.materialintensitaet_result.grid(column=3, row=7)
        self.personalinteansitaet_result.grid(column=3, row=8)

        # Financially Ratios
        self.eigenkapitalquote_result.grid(column=3, row=10)
        self.anlagenintensitaet_result.grid(column=3, row=11)
        self.umlaufintensitaet_result.grid(column=3, row=12)
        self.zahlungsmittelintensitaet_result.grid(column=3, row=13)
        self.forderungsintensitaet_result.grid(column=3, row=14)
        self.gbr1_result.grid(column=3, row=15)
        self.gbr2_result.grid(column=3, row=16)
        self.gbr3_result.grid(column=3, row=17)
        self.lg1_result.grid(column=3, row=18)
        self.lg2_result.grid(column=3, row=19)
        self.lg3_result.grid(column=3, row=20)

        # Other Ratios
        self.fcf_quote_result.grid(column=3, row=22)
        self.steuerquote_result.grid(column=3, row=24)
        self.investitionsquote_result.grid(column=3, row=25)

        # Buttons
        self.close_button.grid(column=1, row=26, pady=15)
        self.pdf_button.grid(column=2, row=26, pady=15, padx=(0, 30))
        self.print_button.grid(column=3, row=26, pady=15)

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Lists with data for some methods
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        self.label_list_for_color = [self.roi_result,
                                     self.eigenkapitalrenatibilitaet_result,
                                     self.gesamtrentabilitaet_result,
                                     self.umsatzrentabilitaet_result,
                                     self.eigenkapitalquote_result,
                                     self.gbr1_result,
                                     self.lg1_result,
                                     self.lg2_result,
                                     self.lg3_result,
                                     self.fcf_quote_result]
        self.result_list_for_pdf = [self.roi_result,
                                    self.eigenkapitalrenatibilitaet_result,
                                    self.gesamtrentabilitaet_result,
                                    self.umsatzrentabilitaet_result,
                                    self.materialintensitaet_result,
                                    self.personalinteansitaet_result,
                                    self.eigenkapitalquote_result,
                                    self.gbr1_result,
                                    self.gbr2_result,
                                    self.gbr3_result,
                                    self.lg1_result,
                                    self.lg2_result,
                                    self.lg3_result,
                                    self.fcf_quote_result,
                                    self.steuerquote_result,
                                    self.investitionsquote_result]

        self.value_list_for_color = [data[0].get("erfolgswirtschaftlich")[0],
                                     data[0].get("erfolgswirtschaftlich")[1],
                                     data[0].get("erfolgswirtschaftlich")[2],
                                     data[0].get("erfolgswirtschaftlich")[3],
                                     data[1].get("finanzwirtschaftlich")[0],
                                     data[1].get("finanzwirtschaftlich")[5],
                                     data[1].get("finanzwirtschaftlich")[8],
                                     data[1].get("finanzwirtschaftlich")[9],
                                     data[1].get("finanzwirtschaftlich")[10],
                                     data[2].get("sonstige")[0]]
        self.value_list_for_pdf = [data[0].get("erfolgswirtschaftlich")[0],
                                   data[0].get("erfolgswirtschaftlich")[1],
                                   data[0].get("erfolgswirtschaftlich")[2],
                                   data[0].get("erfolgswirtschaftlich")[3],
                                   data[0].get("erfolgswirtschaftlich")[4],
                                   data[0].get("erfolgswirtschaftlich")[5],
                                   data[1].get("finanzwirtschaftlich")[0],
                                   data[1].get("finanzwirtschaftlich")[1],
                                   data[1].get("finanzwirtschaftlich")[2],
                                   data[1].get("finanzwirtschaftlich")[3],
                                   data[1].get("finanzwirtschaftlich")[4],
                                   data[1].get("finanzwirtschaftlich")[5],
                                   data[1].get("finanzwirtschaftlich")[6],
                                   data[1].get("finanzwirtschaftlich")[7],
                                   data[1].get("finanzwirtschaftlich")[8],
                                   data[1].get("finanzwirtschaftlich")[9],
                                   data[1].get("finanzwirtschaftlich")[10],
                                   data[2].get("sonstige")[0],
                                   data[2].get("sonstige")[1],
                                   data[2].get("sonstige")[2]]

        self.show_colours(self.label_list_for_color, self.value_list_for_color)
        self.set_operators()

    # Get the operators of the JSON-file
    def set_operators(self):
        json_file = open("settings.json", "r", encoding='utf-8', errors="ignore")
        operator_dict = json.load(json_file)[0]

        # Profitable Ratios
        roi_operator = operator_dict[0].get("roi")
        eigenkapitalrenatibilitaet_operator = operator_dict[1].get("eigenkapitalrentabilitaet")
        gesamtrentabilitaet_operator = operator_dict[2].get("gesamtrentabilitaet")
        umsatzrentabilitaet_operator = operator_dict[3].get("umsatzrentabilitaet")

        # Financially Ratios
        eigenkapitalquote_operator = operator_dict[4].get("eigenkapitalquote")
        bilanzregel_operator = operator_dict[5].get("bilanzregel")
        lg1_operator = operator_dict[6].get("lg1")
        lg2_operator = operator_dict[7].get("lg2")
        lg3_operator = operator_dict[8].get("lg3")

        # Other Ratios
        fcf_quote_operator = operator_dict[9].get("fcf_quote")

        return [roi_operator,
                eigenkapitalrenatibilitaet_operator,
                gesamtrentabilitaet_operator,
                umsatzrentabilitaet_operator,
                eigenkapitalquote_operator,
                bilanzregel_operator,
                lg1_operator,
                lg2_operator,
                lg3_operator,
                fcf_quote_operator]

    # Get the entries of the JSON-file
    def set_entries(self):
        json_file = open("settings.json", "r")
        entry_dict = json.load(json_file)[1]

        # Profitable Ratios
        roi_entry = entry_dict[0].get("roi_entry")
        eigenkapitalrenatibilitaet_entry = entry_dict[1].get("eigenkapitalrentabilitaet_entry")
        gesamtrentabilitaet_entry = entry_dict[2].get("gesamtrentabilitaet_entry")
        umsatzrentabilitaet_entry = entry_dict[3].get("umsatzrentabilitaet_entry")

        # Financially Ratios
        eigenkapitalquote_entry = entry_dict[4].get("eigenkapitalquote_entry")
        bilanzregel_entry = entry_dict[5].get("bilanzregel_entry")
        lg1_entry = entry_dict[6].get("lg1_entry")
        lg2_entry = entry_dict[7].get("lg2_entry")
        lg3_entry = entry_dict[8].get("lg3_entry")

        # Other Ratios
        fcf_quote_entry = entry_dict[9].get("fcf_quote_entry")

        return [roi_entry,
                eigenkapitalrenatibilitaet_entry,
                gesamtrentabilitaet_entry,
                umsatzrentabilitaet_entry,
                eigenkapitalquote_entry,
                bilanzregel_entry,
                lg1_entry,
                lg2_entry,
                lg3_entry,
                fcf_quote_entry]

    # Change background color of result-labels in relation to the settings
    def show_colours(self, label_list, value_list):
        op_list = self.set_operators()
        entry_list = self.set_entries()
        color_results = []

        for idx in range(len(label_list)):
            if op_list[idx] == "<" and float(value_list[idx]) < float(entry_list[idx]):
                label_list[idx].config(bg="aqua")
                color_results.append([value_list[idx], True])
            elif op_list[idx] == "<=" and float(value_list[idx]) <= float(entry_list[idx]):
                label_list[idx].config(bg="aqua")
                color_results.append([value_list[idx], True])
            elif op_list[idx] == ">=" and float(value_list[idx]) >= float(entry_list[idx]):
                label_list[idx].config(bg="aqua")
                color_results.append([value_list[idx], True])
            elif op_list[idx] == ">" and float(value_list[idx]) > float(entry_list[idx]):
                label_list[idx].config(bg="aqua")
                color_results.append([value_list[idx], True])
            else:
                color_results.append([value_list[idx], False])

        return color_results

    # Save Result in a PDF
    def pdf_save(self):
        global stock
        label_list = ["Return on Investment", "Eigenkapitalrentabilität", "Gesamtrentabilität", "Umsatzrentabilität",
                      "Materialintensität", "Personalintensität", "Eigenkapitalquote", "Anlagenintensität",
                      "Umlaufintensität", "Zahlungsmittelintensität", "Forderungsintensität", "1. Goldene Bilanzregel",
                      "2. Goldene Bilanzregel", "3. Goldene Bilanzregel", "Liquidität 1. Grades",
                      "Liquidität 2. Grades", "Liquidität 3. Grades", "FCF-Quote", "Steuerquote", "Investitionsquote"]
        result_list = self.value_list_for_pdf
        color_operations = self.show_colours(self.label_list_for_color, self.value_list_for_color)
        today_date = date.today()
        color_value_list = [color_operations[0], color_operations[1], color_operations[2], color_operations[3],
                            ["", ""], ["", ""], color_operations[4], ["", ""], ["", ""], ["", ""], ["", ""],
                            color_operations[5], ["", ""], ["", ""], color_operations[6], color_operations[7],
                            color_operations[8], color_operations[9], ["", ""], ["", ""]]

        # Create a list with data for the table
        table_data = []
        for label in range(len(label_list)):
            table_data.append([label_list[label], result_list[label]])

        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        #  Create PDF-file
        # *----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*
        # PDF-Layout
        pdf = FPDF(format="A4", unit="cm")
        pdf.add_page()
        pdf.set_font("Arial", "", 10)

        # Keine Ahnung - Mal sehen
        epw = pdf.w - 2 * pdf.l_margin
        col_width = epw / 4

        # Title
        pdf.set_font('Times', 'B', 14)
        pdf.cell(epw, 0.0, 'Ergbnis der Kennzahlenanalyse von {0}'.format(stock), align='L')
        pdf.set_font('Times', '', 10)
        pdf.ln(0.5)

        # Table
        th = pdf.font_size * 1.5
        count = 0
        for row in table_data:

            for el in row:
                if count <= 19 and el == color_value_list[count][0] and color_value_list[count][1] is True:
                    pdf.set_fill_color(0, 255, 255)
                    pdf.cell(col_width, th, "{0}%".format(el), border=1, fill=True)
                elif el not in label_list:
                    pdf.cell(col_width, th, "{0}%".format(el), border=1, fill=False)
                else:
                    pdf.cell(col_width, th, str(el), border=1, fill=False)
            count += 1
            pdf.ln(th)

        pdf.ln(th)
        pdf.cell(col_width, th, str(today_date))

        pdf.output(name="result.pdf")

    # Print the pdf as a hard copy
    def print_result(self):
        self.pdf_save()
        path = "result.pdf"
        os.startfile(path, "Print")


# Initialize ResultWindow
def show_result_window():
    global stock

    result_root = tk.Tk()
    result_root.geometry("450x600")
    app = ResultWindow(result_root)
    result_root.title("{0} - Ergebnis".format(stock))
    result_root.mainloop()


# Initialize MainWindow
def main():
    root = tk.Tk()
    root.title("Balance Sheet Scanner")
    root.geometry("500x600")
    root.maxsize(500, 600)
    app = MainWindow(root)
    root.mainloop()
