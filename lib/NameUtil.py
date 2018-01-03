import random
class NameUtil:
    FEMALE_NAMES = [ "laura", "julia", "emilia", "lea", "lina", "anna", "lena", "lara", "sarah", "elena", "amelie", "sophie", "vanessa", "alina", "juna", "mia", "nina", "mila", "lisa", "leonie", "hannah", "marie", "selina", "anouk", "jana", "luisa", "emma", "emily", "tanja", "jasmin", "melina", "shirin", "mina", "valentina", "mira", "johanna", "maria", "ava", "sandra", "melanie", "michelle", "charlotte", "pia", "hanka", "sabrina", "katharina", "jessica" ]
    MALE_NAMES = [ "liam", "milan", "jonas", "elias", "julian", "levi", "tim", "michael", "linus", "luca", "daniel", "david", "alexander", "samuel", "lukas", "jan", "noah", "marcel", "leon", "moritz", "florian", "thomas", "simon", "valentin", "sebastian", "tobias", "patrick", "emil", "paul", "felix", "fabian", "oskar", "finn", "joshua", "benjamin", "joris", "jax", "christian", "ben", "robin", "marco", "anton", "raphael", "maximilian", "markus", "andreas", "manuel", "stefan" ]
    SURNAMES = [ "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Schulz", "Becker", "Hoffmann", "Schäfer", "Koch", "Richter", "Bauer", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann", "Braun", "Hofmann", "Krüger", "Hartmann", "Lange", "Schmitt", "Werner", "Schmitz", "Krause", "Meier", "Lehmann", "Schmid", "Schulze", "Maier", "Köhler", "Herrmann", "Walter", "König", "Mayer", "Huber", "Kaiser", "Fuchs", "Peters", "Lang", "Scholz", "Möller", "Weiß", "Jung", "Hahn", "Schubert", "Vogel", "Friedrich", "Günther", "Keller", "Winkler", "Frank", "Berger", "Roth", "Beck", "Lorenz", "Baumann", "Franke", "Albrecht", "Schuster", "Simon", "Ludwig", "Böhm", "Winter", "Kraus", "Martin", "Schumacher", "Krämer", "Vogt", "Otto", "Jäger", "Stein", "Groß", "Sommer", "Seidel", "Heinrich", "Haas", "Brandt", "Schreiber", "Graf", "Dietrich", "Schulte", "Kühn", "Ziegler", "Kuhn", "Pohl", "Engel", "Horn", "Bergmann", "Voigt", "Busch", "Thomas", "Sauer", "Arnold", "Pfeiffer", "Wolff" ]
    
    def loadData(self):
        with open(fname) as f:
            content = f.readlines()
        content = [x.strip() for x in content] 
    
    def rateGeschlecht(self, name):
        if name.lower() in self.FEMALE_NAMES:
            print("For {} guessing W".format(name))
            return "W"
        elif name.lower() in self.MALE_NAMES:
            print("For {} guessing M".format(name))
            return "M"
        else:
            print("For {} guessing None".format(name))
            return None
            
    def zufallsGeschlecht(self):
        if random.randint(0, 1) == 1:
            return "W"
        else:
            return "M"
            
    def zufallsNameMaennlich(self):
        return str(self.MALE_NAMES[random.randint(0, len( self.MALE_NAMES ) )]).title()
        
    def zufallsNameWeiblich(self):
        return str(self.FEMALE_NAMES[random.randint(0, len( self.FEMALE_NAMES ) )]).title()
        
    def zufallsNachname(self):
        return str(self.SURNAMES[random.randint(0, len( self.SURNAMES ) )]).title()
