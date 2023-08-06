from abstract_provisionner import AbstractProvisionner
from log_manager import logging
log = logging.getLogger('provisionner.EmptyProvisionner')
class EmptyProvisionner(AbstractProvisionner):

    def initialise(self, machine_controller, machine_name):
        log.debut('EmptyProvisionner', 'Initialisation du provisionner', machine_name=machine_name)
        self.machine_controller = machine_controller
        log.fin('EmptyProvisionner', 'Initialisation du provisionner', machine_name=machine_name)


    def run_cmd(self, command):
        '''
        Lance une commande.
        '''
        log.debut('EmptyProvisionner-run_cmd', 'lancement commande ', command=command)
        ret, stdout = self.machine_controller.run_cmd(command)
        log.fin('EmptyProvisionner-run_cmd', 'lancement commande ', command=command, ret=ret, stdout=stdout)
        # Conversion du code retour en statut (True, False)
        return ret == 0, stdout
