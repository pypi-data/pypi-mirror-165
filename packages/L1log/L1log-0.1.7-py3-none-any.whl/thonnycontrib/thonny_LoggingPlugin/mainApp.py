from thonny import get_workbench
from thonny.shell import ShellView

import tkinter as tk
import logging
from datetime import datetime
from copy import deepcopy
import os

from thonnycontrib.thonny_LoggingPlugin.processing import formatData
from thonnycontrib.thonny_LoggingPlugin.configuration import configuration
from thonnycontrib.thonny_LoggingPlugin.configuration.globals import *
from thonnycontrib.thonny_LoggingPlugin.communication.sendingClient import SendingClient
from thonnycontrib.thonny_LoggingPlugin.formats.xAPI_creation import convert_to_xAPI

import thonnycontrib.thonny_LoggingPlugin.utils.logger_utils as utils

class EventLogger:
    """
    Main class to generate logs from user's actions
    This class bind the thonny's event generator to the function 'prepare_log'
    When an event is generated :
        Data is extracted
        Additionnal informations can be added
        The data is send to a general formatter in order to have standardised names and informations
        This data in a general format is stored, printed and next, formatted in xAPI format and sended to a server
    """

    def __init__(self):
        """
        Construct an instance of EventLogger, initiates the attributes and makes the binds to get our data
        """
        # Stockage dans la ram des logs pour les enregistrer dans un fichier lors de la fermeture de thonny
        self.events = []
        self.formatted_logs = []
        self.xAPI_formatted_logs = []

        # Instance de la classe de formatage basique
        self.formatter = formatData.FormatData(self)
        
        #Configs :
        self.sending_client = SendingClient(configuration.get_option("server_address"))
        self.sending_logs = configuration.get_option("send_logs")
        self.log_in_console = configuration.get_option("log_in_console")
        self.store_logs = configuration.get_option("store_logs")
        self.folder = configuration.get_option("local_path")

        #Pour _buffer_errors
        self._stderrBuffer = dict()

        #Pour regroup_tests
        self.regrouped_tests = []


        #Attribut des éléments que l'on veut séléctionner :
        self._inDict = {
            "ShellCommand" : {'sequence','command_text','tags'},
            "ShellInput" : {'sequence','input_text','tags'},
            "TextInsert" : {'sequence','index','text','text_widget','text_widget_context','tags'},

            "Save" : {'sequence','editor','text_widget','filename'},
            "Open" : {'sequence','editor','text_widget','filename'},
            "SaveAs" : {'sequence','editor','text_widget','filename'},

            "l1Tests" : {'sequence','filename','tested_line','expected_result','obtained_result','exception','name','lineno','selected'},
            "l1Tests.DocGenerator" : {'sequence','name'}
        }

        for sequence in self._inDict:
            self._bind(sequence)
        self._bind("UiCommandDispatched")

        get_workbench().bind("WorkbenchClose", self._on_workbench_close, True)

        #Lance le début de Session du formater ici pour éviter problème de chargement de fichier avant début de session
        self.formatter.begin_session(id(self))

    def _on_workbench_close(self, event : object) -> None:
        """
        write logs in files in the directory specified in the config
        """
        self.formatter.end_session(id(event))
        # Créer le dossier de base s'il n'existe pas
        try :
            os.mkdir(self.folder)
        except FileExistsError :
            pass

        if self.store_logs:
            # Créer un dossier logs contenant tout les logs générés par le plugin
            try : 
                os.mkdir(self.folder+"logs")
            except FileExistsError as e :
                pass

            import json
            #Base logs
            with open(self.folder+'/logs/logs'+str(datetime.now())+'.json', encoding="UTF-8", mode="w") as fp:
                json.dump(self.events, fp, indent="    ")
            #Pre formatted logs
            with open(self.folder+'/logs/formatted_logs'+str(datetime.now())+'.json', encoding="UTF-8", mode="w") as fp:
                json.dump(self.formatted_logs,fp,indent="    ")
            #xAPI formatted logs
            with open(self.folder+'/logs/xAPI_logs'+str(datetime.now())+'.json', encoding="UTF-8", mode="w") as fp:
                json.dump(self.xAPI_formatted_logs,fp,indent="    ")

    def _bind(self,sequence : str) -> None:
        """
        Trigger the prepare_log function when the event type 'sequence' is produced

        Args: 
            sequence (str): the event type

        Returns:
            None
        """
        def handle(event):
            self._prepare_log(sequence,event)
        
        get_workbench().bind(sequence,handle,True)


    def _prepare_log(self,sequence : str,event : object) -> None:
        """
        extract, process and log the event

        Args:
            sequence (str): the event type
            event (obj:thonny.WorkbenchEvent:) The event
        """
        data = self._extract_interesting_data(event, sequence)

        data["time"] = datetime.now().isoformat()

        data = self._input_processing(data,event)

        self._log_event(data,event)


    def _log_event(self,data : dict, event : object) -> None:
        """
        Store raw data in a buffer and init an event in the formatter

        Args:
            data (obj:'dict'): the raw data
        """
        if data != {}:
            self.events.append(data)
            self.formatter.init_event(data,id(event))

    def _extract_interesting_data(self, event, sequence):
        """
        Extract data from an Thonny's WorkbenchEvent object and select only the informations defined in the in_Dict dictionnary.

        Args :
            event (obj:thonny.WorkbenchEvent) The event to extract data from
            sequence (str) This event type

        Returns:
            (obj:'dict'): the data in the format we want
        """
        attributes = vars(event)
        data = {'tags': () }


        if "text_widget" not in attributes:
            if "editor" in attributes:
                attributes["text_widget"] = attributes["editor"].get_text_widget()

            if "widget" in attributes and isinstance(attributes["widget"], tk.Text):
                attributes["text_widget"] = attributes["widget"]


        if "text_widget" in attributes:
            widget = attributes["text_widget"]
            if isinstance(widget.master.master, ShellView):
                attributes["text_widget_context"] = "shell"


        for elem in self._inDict[sequence]:
            if elem in attributes:
                value = attributes[elem]
                data[elem] = value
                if isinstance(value, (tk.BaseWidget, tk.Tk)):
                    data[elem + "_id"] = id(value)
                    data[elem + "_class"] = value.__class__.__name__

        return data

    def _input_processing(self, data : dict, event : object) -> dict :
        """
        Clean and additionnal informations to the data

        Args :
            data (object:'dict') Data to process
            event

        Returns :
            data (object:'dict') Data modified
        """
        # Partie nettoyage
        if 'editor' in data :
            del data['editor']
            del data['editor_class']
        if 'text_widget' in data :
            del data['text_widget']

        #Ajout contenu éditeur
        if data['sequence'] in {'ShellCommand','Open','Save','SaveAs'} :
            data['editorContent'] = utils.cut_topfile_comments(get_workbench().get_editor_notebook().get_current_editor_content())

        # Partie traitements
        if data['sequence'] == 'TextInsert' :
            if data["text_widget_class"] == 'ShellText':
                #Gestion cas de sortie trop lourdes pour l'envoi au serveur
                if 'text' in data :
                    if len(data['text']) > 1000 :
                        data['text'] = "TEXT TOO LONG"

                if not 'value' in data['tags'] and not 'stderr' in data['tags'] and not 'stdout' in data['tags']:
                    if 'prompt' in data['tags']:
                        data = self.send_buffer_error()
                        self._log_event(data,event)
                        self.formatter.end_event()
                        return {}
                    return {}
                    
                else :
                    if 'stderr' in data['tags']:
                        data['text'] = utils.hash_filename(data['text'])
                        self._buffer_errors(data)
                        return {}
            else : 
                return {}

        if data['sequence'] == 'l1Tests':
            if  'exception' in data or 'obtained_result' in data :
                data['status'] = False
            else :
                data['status'] = True 

            if not 'obtained_result' in data :
                if not 'exception' in data :
                    data['obtained_result'] = data['expected_result']
                else :
                    data['obtained_result'] = data['exception']

        if 'filename' in data :
            data['filename'] = utils.hash_filename(data['filename'])
            
        return data


    def _buffer_errors(self,data : dict) -> None:
        """
        Store in a buffer the data of user's text edition events and return when the user
        write somewhere else

        Args : 
            data (object:'dict'): Data to process

        """
        buf = deepcopy(self._stderrBuffer)
        if buf == {}:
            self._stderrBuffer = data
        else :
            self._stderrBuffer['text'] = buf['text']+data['text']

    def send_buffer_error(self) -> dict:
        """
        sends the error buffer
        """
        data = deepcopy(self._stderrBuffer)
        self._stderrBuffer = {}
        return data

    def receive_formatted_logs(self,formatted_log : dict) -> None:
        """
        Store and send the formatted logs in parameter to a Server if the user didn't desactivate it
        Args :
            formatted_log (object:'dict') the logs in a basic exportation format
        """
        if formatted_log != {}:
            self.formatted_logs.append(formatted_log)
            if self.log_in_console :
                print(formatted_log)
            try :
                    self.send_xAPI_statement(formatted_log)
            except KeyError as e :
                logging.info(formatted_log,e)
                return 

    def send_xAPI_statement(self,formatted_log : dict) -> None:
        """
        Convert data to the xAPI format, and send it to the LRS

        Args :
            data (object: dict()): dict of the data in a basic format
        """
        xAPI_statement = convert_to_xAPI(formatted_log)
        self.xAPI_formatted_logs += [xAPI_statement]
        if self.sending_logs :
            try :
                self.sending_client.send(xAPI_statement,"/statements/")
            except Exception as e:
                self.sending_logs = False
                logging.warning(" Server can't be reach, restart Thonny to retry\n"+str(e))
