from thonny import get_workbench

from datetime import datetime
import getpass
import hashlib

class FormatData:
    """
        The goal of this class is to format the data in a general way
        wich can be use as a base to convert in other export format

        data is outputed in dict objects as this :
            'run_program' : {'eventID','eventType','timestamp','stdin','stdout','stderr','status','command','userID','sessionID'},
            'run_command' : {'eventID','eventType','timestamp','stdin','stdout','stderr','status','command','userID','sessionID'},
            'openSave' : {'eventID','eventType','timestamp','filename','userID','sessionID'},
            'newfile' : {'eventID','eventType','timestamp','userID','sessionID'},
            'session' : {'eventID','eventType','timestamp','status','userID','sessionID'}
            'l1Tests" : {'eventID','eventType','timestamp','userID','sessionID','status',filename','tested_line','expected_result','obtained_result','exception'}

        In the functions of this class, there is 2 types of events defined :
            The shorts events : Just simples events where the data received in init_event is
                formatted and "ended" in an unique execution of the fonction
            The longs events : Theses are events like commands wich runs the program, where
                we need to get more informations like the inputs made by the user during the execution,
                the results of the executions (stdout,stderr) and all the informations that can occurs
                during the run of a program.
                All theses informations received by init_event when the attribute 'on_progress'
                is True will be processed and stored as it should be, and will be only send when
                the function 'end_event()' will be triggered.
        """


    def __init__(self, logger) -> None:
        self.logger = logger
        self.on_progress = False
        self.current = dict()
        self.userID = hashlib.sha224(bytes(getpass.getuser(),"utf-8")).hexdigest()[:15]
        self.sessionID = id(get_workbench())

    # A lancer lors du prompt '>>>'
    def end_event(self):
        """
        End long event if one is currently active by changing the state of
        the class attribute "on_progress" to False and sending to the EventLogger
        instance the finished formatted log.
        """
        self.on_progress = False
        self.logger.receive_formatted_logs(self.current)
        self.current = dict()

    def init_event(self, data, id):
        """
        Initiate an event by defining if it will be a long event or a short event
        (see the class documentation) and store the data in the class attribute 'current'
        """
        # Si programme ou commande longue lancée :
        if self.on_progress:
            #Ajout des éléments suivant l'execution
            if data['sequence'] == 'TextInsert':
                if 'stdout' in data['tags'] or 'value' in data['tags']:
                    self.current['stdout'] += data['text']
                if 'stderr' in data['tags']:
                    self.current['stderr'] += data['text']
                    self.current['status'] = False

            elif data['sequence'] == 'ShellInput':
                self.current['stdin'] += data['input_text']

        # Cas ou il n'y a pas d'execution en plusieurs temps / seulement des events simples
        else:
            #Informations générales
            self.current['timestamp'] = data['time']
            self.current['eventID'] = id
            self.current['userID'] = self.userID
            self.current['sessionID'] = self.sessionID

            # Cas des runs commandes ou programme
            if data['sequence'] == 'ShellCommand':
                self.format_ShellComand(data)

            # Cas des ouvertures / sauvegardes / nouveau fichiers
            elif data['sequence'] in {'Open', 'Save', 'SaveAS'}:
                self.format_open_save(data)
            

            #Cas non référencés
            
            else :
                self.current['eventType'] = data['sequence']
                for el in data :
                    if el not in self.current and el not in {'sequence','tags'}:
                        self.current[el] = data[el]
                self.end_event()


    def format_ShellComand(self,data):
        """
        Format the current event to be a long event and define if its a Run_program or Run_command
        """
        # On veut avoir les sorties de la commande/du programme
        self.on_progress = True

        # initialisation des champs
        for el in {'stdin', 'stdout', 'stderr'}:
            self.current[el] = ''
        self.current['status'] = True
        self.current['command'] = data['command_text']

        if data['command_text'][:4] == '%Run':
            self.current['eventType'] = 'Run_program'
            self.current['codestate'] = data['editorContent']
        else:
            self.current['eventType'] = 'Run_command'        

    def format_open_save(self,data):
        """
        Make and end an Open / Save / SaveAs event
        """
        if data['sequence'] == 'SaveAs':
            data['sequence'] = 'Save'
        self.current['eventType'] = data['sequence']
        self.current['filename'] = data['filename']
        self.current['codestate'] = data['editorContent']
        self.end_event()


    def begin_session(self, id):
        """
        Create an event "Session_start" and end it immediatly
        Triggered when Thonny is started
        """
        self.current = {
            'eventID': id,
            'eventType': 'Session_start',
            'status': True,
            'timestamp': datetime.now().isoformat(),
            'userID': self.userID,
            'sessionID':  self.sessionID
        }
        self.current['L1Test'] = self.checks_if_plugin_installed('thonnycontrib.l1test')
        self.end_event()

    def end_session(self, id):
        """
        Create an event "Session_end" and end it immediatly
        Triggered when Thonny is closed.
        """
        self.current = {
            'eventID': id,
            'eventType': 'Session_end',
            'status': 'end',
            'timestamp': datetime.now().isoformat(),
            'userID': self.userID,
            'sessionID':  self.sessionID
        }
        self.end_event()

    def isOnProgress(self):
        return self.on_progress

    def checks_if_plugin_installed(self,name):
        import sys
        return name in sys.modules