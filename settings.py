import sys, os
import numpy as np
import yaml


class Settings():

    def __init__(self, pathToSettingsFile):
        """
        pathToSettingsFile: path to settings file.
        """    

        with open(pathToSettingsFile, 'r') as f:
            yamlAttributes = yaml.safe_load(f)
            print(yamlAttributes)
            if(yamlAttributes['pathToSettingsFile'] != pathToSettingsFile and yamlAttributes['pathToSettingsFile'].lower().strip() not in ['none', '','default'] ):
                if(os.path.isfile(pathToSettingsFile)):
                    self = Settings(yamlAttributes['pathToSettingsFile'])
                    return
                elif(pathToSettingsFile.lower().strip() in ['none', 'default', '', '-']):
                    pass
                else:
                    print('Unvalid path to YAML settings file, defaulting to settings file at: %s.' % pathToSettingsFile)
            
            for setting, value in yamlAttributes.items():
                setattr(self, setting, value)
        try:
            self.numberOfSessions += 1 
        except:
           self.numberOfSessions = 1
        print('Settings loaded.')
        
        
    def convertToPrimitive(self):
        settings = self.settings()
        
        for key, value in settings.items():

            try:
                len(self[key])
                setattr(self, key, list(value))
            except:
                try:
                    scalar = np.asscalar(value)
                    setattr(self, key, scalar) 
                except:
                    pass
            
            
                    
                    
            
        
    def saveToSettingsFile(self, path):  
        """
        path: path to settings file.
        """
        self.convertToPrimitive()    
        with open(path, 'w') as f:
                yaml.dump(self.settings(), f)
                
    def settings(self):
        settings = [a for a in dir(self) if not callable(getattr(self, a)) and not a.startswith("__")]
        settingsDict = {}
        for s in settings:
            settingsDict[s] = getattr(self, s)
        
        return settingsDict
        
        
    def saveLastUsedSettings(self):
        pathToSettingsFile = sys.path[0] + '\\settings\\lastSettings.yaml' 
        self.saveToSettingsFile(pathToSettingsFile)
        
    def __del__(self):
        try:
            self.saveLastUsedSettings()
        except:
            print('Could not save settings, or settings saved when main window was closed.')
    