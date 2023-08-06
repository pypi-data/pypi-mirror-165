
import os
class AbstractSourceAccessor(object):
    """
    Permet de transformer les sources en fichiers recuperables
    La source doit pouvoir etre copie sur une machine
    """
    def __init__(self, name, global_config, source_config):
        """
        Recupere la source si besoin pour la rendre accessible en fichier
        """
        # Definition des attributs communs
        self.local_path = os.path.abspath(source_config.get('path::local'))
        self.machine_path = os.path.abspath(source_config.get('path::machine'))
        self.readonly = False
        self.work_directory = os.path.abspath(global_config.get('core::work_directory')) + '/' + name


    def __del__(self):
        """
        Nettoyage des fichiers temporaires si necessaire
        """
        pass
