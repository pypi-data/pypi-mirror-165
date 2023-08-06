from thonnycontrib.thonny_LoggingPlugin.configuration.globals import TERMS_OF_USE, URL_TERMS_OF_USE, WB
from thonnycontrib.thonny_LoggingPlugin import mainApp

from thonnycontrib.thonny_LoggingPlugin.configuration import configuration
from thonny.config import *

import tkinter as tk

from thonny import ui_utils
from thonny.ui_utils import CommonDialog
from thonny.languages import get_button_padding, tr
from typing import Optional

def load_plugin():
    """
    Load the plugin and and a command to configure it in thonny
    """
    configuration.init_options()

    if configuration.get_option("first_run") :
        reponse = display_terms_of_use()
        configuration.accept_terms_of_uses(reponse)
        WB.set_option("loggingPlugin.first_run",False)

    logger = mainApp.EventLogger()
    WB.add_configuration_page("LoggingPlugin", "LoggingPlugin", configuration.plugin_configuration_page, 30)
    
    WB.add_command( command_id="about_logger",
                    menu_name="tools",
                    command_label="Logging Plugin",
                    handler=display_about_plugin)
    return

def display_about_plugin():
    '''
    Affiche une pop-up avec une url.
    '''
    ui_utils.show_dialog(AboutLoggingPlugin(WB))

def display_terms_of_use():
    '''
    Ouvre la fenêtre de consentement. Renvoie True si l'utilisateur
    est d'accord pour la collecte de ses données.
    
    Result:
       (bool) vrai si l'utilisateur a cliqué sur "oui", faux
       pour toute autre interaction.
    '''
    fenetre_consentement = ConsentementDialog(WB)
    ui_utils.show_dialog(fenetre_consentement)
    reponse = fenetre_consentement.get_result()
    return reponse == "oui"

    
class AboutLoggingPlugin(CommonDialog):
    '''
    Définit une pop-up avec une url d'info.
    '''
    def __init__(self, master):
        import webbrowser

        super().__init__(master)

        main_frame = tk.ttk.Frame(self, width = 800, height = 100)
        main_frame.grid(sticky=tk.NSEW, ipadx=50, ipady=100)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.title("About Thonny_LoggingPLugin")



        url_font = tk.font.nametofont("TkDefaultFont").copy()
        url_font.configure(underline=1)
        url_label = tk.ttk.Label(
            main_frame, text=URL_TERMS_OF_USE, style="Url.TLabel", cursor="hand2", font=url_font
        )
        url_label.grid()
        url_label.bind("<Button-1>", lambda _: webbrowser.open(URL_TERMS_OF_USE))



# Mirabelle
# inspiré de thonny.ui_utils.QueryDialog, certaines choses sont
# peut-être inutiles.
class ConsentementDialog(ui_utils.CommonDialogEx):
    '''
    Définition d'une pop-up lancée au premier démarrage de Thonny
    qui demande si l'utilisateur consent à ce qu'on collecte 
    ses données.
    Si la fenêtre est fermée sans avoir cliqué oui ou non, 
    l'absence de réponse est interprétée comme "non".
    '''
    def __init__(
            self,
            master,
            entry_width: Optional[int] = None,
    ):
        super().__init__(master)

        # question posée
        self.question="Acceptez vous que les données utilisateur issues de Thonny soient collectées\n à des fins de recherche ?"
        bold_font = tk.font.nametofont("TkDefaultFont").copy()
        bold_font.configure(weight=tk.font.BOLD)
        # autres textes à afficher ds la pop-up            
        self.prompt1="Les commentaires en tête de fichier et son nom ne sont pas collectés\n car pouvant contenir des données personnelles (nom, prénom, groupe).\n Attention de ne pas faire figurer de données personnelles dans le reste du code."
        self.prompt2="Vous pourrez modifier votre choix à tout moment\n dans le menu outils-->options, onglet LoggingPlugin"
        self.prompt3="Pour valider: tapez Entrée ou cliquez sur ce bouton"
        
        # résultat issu de la pop-up : None, "oui", "non"
        self.result = None

        # ??? 
        margin = self.get_large_padding()
        spacing = margin // 2

        # titre de la pop-up
        self.title("Conditions d'utilisation")

        # positionnement question + annonces
        self.prompt_question = tk.ttk.Label(self.main_frame, text=self.question, font=bold_font)
        self.prompt_question.grid(row=1, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        self.prompt_label1 = tk.ttk.Label(self.main_frame, text=self.prompt1)
        self.prompt_label1.grid(row=2, column=1, columnspan=2, padx=margin, pady=(margin, spacing))
        self.prompt_label2 = tk.ttk.Label(self.main_frame, text=self.prompt2)
        self.prompt_label2.grid(row=3, column=1, columnspan=2, padx=margin, pady=(margin, spacing))

        # bouton oui
        self.oui_button = tk.ttk.Button(
            self.main_frame, text=tr("oui"), command=self.on_oui, default="active")
        self.oui_button.grid(row=4, column=1, padx=(margin, spacing), pady=(0, margin))
        # bouton non
        self.non_button = tk.ttk.Button(
            self.main_frame, text=tr("non"), command=self.on_non, default="active")
        self.non_button.grid(row=5, column=1, padx=(margin, spacing), pady=(0, margin))
        
        # ???
        self.main_frame.columnconfigure(1, weight=1)
        # taper Entrée a la même action que le clic sur "non"
        #self.bind("<Return>", self.on_non, True)

    def on_oui(self, event=None):
        self.result = "oui"
        self.destroy()

    def on_non(self, event=None):
        self.result = "non"
        self.destroy()
        
    def on_cancel(self, event=None):
        self.result = None
        self.destroy()

    def get_result(self) -> Optional[str]:
        '''
        Renvoie :
        - "oui" si click sur le bouton "oui"
        - "non" si click sur le bouton "non"
        - None si fermeture fenêtre sans click
        '''
        return self.result

    
