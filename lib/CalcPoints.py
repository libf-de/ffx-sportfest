import math

class CalcPoints:
    
    def Sprint(self, klasse,  time,  male):
        if klasse.startswith("5"):
            if male:
                return self.Herren_50m(time)
            else:
                return self.Damen_50m(time)
        elif klasse.startswith("6"):
            if male:
                return self.Herren_50m(time)
            else:
                return self.Damen_50m(time)
        elif klasse.startswith("7"):
            if male:
                return self.Herren_75m(time)
            else:
                return self.Damen_75m(time)
        elif klasse.startswith("8"):
            if male:
                return self.Herren_75m(time)
            else:
                return self.Damen_75m(time)
        elif klasse.startswith("9"):
            if male:
                return self.Herren_100m(time)
            else:
                return self.Damen_100m(time)
        elif klasse.startswith("10"):
            if male:
                return self.Herren_100m(time)
            else:
                return self.Damen_100m(time)
        else:
            return 0
            
    def Lauf(self, klasse, time,  male):
        if male:
            return self.Herren_800m(time)
        else:
            return self.Damen_800m(time)
                
    def Sprung(self, klasse, dist, male):
        if male:
            return self.Herren_Weitsprung(dist)
        else:
            return self.Damen_Weitsprung(dist)
            
    def Wurf(self, klasse,  dist,  male):
        if klasse.startswith("5"):
            if male:
                return self.Herren_Ballwurf(dist)
            else:
                return self.Damen_Ballwurf(dist)
        elif klasse.startswith("6"):
            if male:
                return self.Herren_Ballwurf(dist)
            else:
                return self.Damen_Ballwurf(dist)
        elif klasse.startswith("7"):
            if male:
                return self.Herren_Kugelstoss(dist)
            else:
                return self.Damen_Kugelstoss(dist)
        elif klasse.startswith("8"):
            if male:
                return self.Herren_Kugelstoss(dist)
            else:
                return self.Damen_Kugelstoss(dist)
        elif klasse.startswith("9"):
            if male:
                return self.Herren_Kugelstoss(dist)
            else:
                return self.Damen_Kugelstoss(dist)
        elif klasse.startswith("10"):
            if male:
                return self.Herren_Kugelstoss(dist)
            else:
                return self.Damen_Kugelstoss(dist)
        else:
            return 0       
            
    
    def Herren_800m(self, time):
        if time == 0 or ( time >= (800/2.325)):
            return 0
        else:
            return int(round(((800 / (time + 0.24)) - 2.325) / 0.00644, 0))
            
    def Damen_800m(self, time):
        if time == 0 or ( time >= (800/2.0232)):
            return 0
        else:
            return int(round(((800 / (time + 0.24)) - 2.0232) / 0.00647, 0))
    
    
    def Herren_50m(self, time):
        if time == 0 or ( time >= (50/3.79)):
            return 0
        else:
            return int(round(((50 / (time + 0.24)) - 3.79) / 0.0069, 0))
            
    def Damen_50m(self, time):
        if time == 0 or ( time >= (50/3.648)):
            return 0
        else:
            return int(round(((50 / (time + 0.24)) - 3.648) / 0.0066, 0))
            
    def Herren_75m(self, time):
        if time == 0 or ( time >= (75/4.1)):
            return 0
        else:
            return int(round(((75 / (time + 0.24)) - 4.1) / 0.00664, 0))
            
    def Damen_75m(self, time):
        if time == 0 or ( time >= (75/3.998)):
            return 0
        else:
            return int(round(((75 / (time + 0.24)) - 3.998) / 0.0066, 0))
            
    def Herren_100m(self, time):
        if time == 0 or ( time >= (100/4.341)):
            return 0
        else:
            return int(round(((100 / (time + 0.24)) - 4.341) / 0.00676, 0))
            
    def Damen_100m(self, time):
        if time == 0 or ( time >= (100/4.0062)):
            return 0
        else:
            return int(round(((100 / (time + 0.24)) - 4.0062) / 0.00656, 0))
            
    def Herren_Weitsprung(self, dist):
        if dist == 0 or ( dist <= math.pow(1.15028, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.15028)/0.00219, 0))
            
    def Damen_Weitsprung(self, dist):
        if dist == 0 or ( dist <= math.pow(1.0935, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.0935)/0.00208, 0))
            
    def Herren_Kugelstoss(self, dist):
        if dist == 0 or ( dist <= math.pow(1.4250, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.4250)/0.0037, 0))
            
    def Damen_Kugelstoss(self, dist):
        if dist == 0 or ( dist <= math.pow(1.279, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.279)/0.00398, 0))
            
    def Herren_Ballwurf(self, dist):
        if dist == 0 or ( dist <= math.pow(1.936, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.936)/0.0124, 0))
            
    def Damen_Ballwurf(self, dist):
        if dist == 0 or ( dist <= math.pow(1.4149, 2)):
            return 0
        else:
            return int(round((math.sqrt(dist)-1.4149)/0.01039, 0))
