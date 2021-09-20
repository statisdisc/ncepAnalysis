import os
import sys

class pathSetup:
    def __init__(self, root=""):
        self.scripts = os.path.dirname(os.path.abspath(root))
        self.data    = os.path.join(self.scripts, "data")
        self.outputs = os.path.join(self.scripts, "outputs")
        
        self.createDirectory(self.outputs)
    
    def createDirectory(self, folder):
        if not os.path.isdir(folder):
            os.makedirs(folder)