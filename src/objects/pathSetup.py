import os
import sys

class pathSetup:
    def __init__(self, root=""):
        self.scripts      = os.path.dirname(os.path.abspath(root))
        self.data         = os.path.join(self.scripts, "data")
        self.outputs      = os.path.join(self.scripts, "outputs")
        self.outputs_temp = os.path.join(self.outputs, "temperature")
        self.outputs_hdd  = os.path.join(self.outputs, "hdd")
        self.outputs_rw   = os.path.join(self.outputs, "random-walk")
        
        self.createDirectory(self.outputs)
        self.createDirectory(self.outputs_temp)
        self.createDirectory(self.outputs_hdd)
        self.createDirectory(self.outputs_rw)
    
    def createDirectory(self, folder):
        if not os.path.isdir(folder):
            os.makedirs(folder)