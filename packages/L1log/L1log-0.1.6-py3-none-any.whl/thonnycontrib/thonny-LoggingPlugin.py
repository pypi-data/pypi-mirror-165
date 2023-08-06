from thonnycontrib.thonny_LoggingPlugin.configuration.globals import TERMS_OF_USE, URL_TERMS_OF_USE, WB
from thonnycontrib.thonny_LoggingPlugin import mainApp

from thonnycontrib.thonny_LoggingPlugin.configuration import configuration
from thonny.config import *

import tkinter as tk

from thonny import ui_utils
from thonny.ui_utils import CommonDialog


def load_plugin():
    """
    Load the plugin and and a command to configure it in thonny
    """
    configuration.init_options()

    if configuration.get_option("first_run") :
        if display_terms_of_use() :
            configuration.accept_terms_of_uses()
        WB.set_option("loggingPlugin.first_run",False)

    logger = mainApp.EventLogger()
    WB.add_configuration_page("LoggingPlugin", "LoggingPlugin", configuration.plugin_configuration_page, 30)
    
    WB.add_command( command_id="about_logger",
                    menu_name="tools",
                    command_label="Logging Plugin",
                    handler=display_about_plugin)
    return

def display_about_plugin():
    ui_utils.show_dialog(AboutLoggingPlugin(WB))

class AboutLoggingPlugin(CommonDialog):
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

def display_terms_of_use():
    return tk.messagebox.askyesno(title="Thonny LoggingPlugin", message=TERMS_OF_USE)