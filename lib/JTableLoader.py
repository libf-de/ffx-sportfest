import json
class KlasseNichtGefunden(LookupError):
    '''Angegebene Klasse nicht gefunden!'''
    
class JTableLoader:
    def schuelerInKlasse(jsonString, klasse):
        jd = json.loads(jsonString)
        if klasse not in jd:
            raise KlasseNichtGefunden("Klasse " + klasse + " nicht gefunden")
        
        schueler_in_klasse = jd[klasse];
        schueler_list = [];
        i = 0;
        for schueler in schueler_in_klasse:
            schueler_dict = { 'name' : ''}
        
            
            
            
            
            
            
