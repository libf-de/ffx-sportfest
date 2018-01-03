class CalcNote:
    def Sprint(self, klasse,  time,  male):
        if klasse.startswith("5"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 8.5:
                        return 1
                    elif time <= 8.9:
                        return 2
                    elif time <= 9.5:
                        return 3
                    elif time <= 10.0:
                        return 4
                    elif time <= 10.9:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 8.7:
                        return 1
                    elif time <= 9.2:
                        return 2
                    elif time <= 9.8:
                        return 3
                    elif time <= 10.5:
                        return 4
                    elif time <= 11.1:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("6"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 8.2:
                        return 1
                    elif time <= 8.5:
                        return 2
                    elif time <= 9.2:
                        return 3
                    elif time <= 9.7:
                        return 4
                    elif time <= 10.6:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 8.5:
                        return 1
                    elif time <= 9.0:
                        return 2
                    elif time <= 9.6:
                        return 3
                    elif time <= 10.3:
                        return 4
                    elif time <= 10.9:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("7"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 11.6:
                        return 1
                    elif time <= 12.3:
                        return 2
                    elif time <= 13.3:
                        return 3
                    elif time <= 13.9:
                        return 4
                    elif time <= 15.0:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 12.0:
                        return 1
                    elif time <= 12.5:
                        return 2
                    elif time <= 13.4:
                        return 3
                    elif time <= 14.3:
                        return 4
                    elif time <= 15.3:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("8"): #75m
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 11.2:
                        return 1
                    elif time <= 11.9:
                        return 2
                    elif time <= 12.9:
                        return 3
                    elif time <= 13.5:
                        return 4
                    elif time <= 14.7:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 11.9:
                        return 1
                    elif time <= 12.4:
                        return 2
                    elif time <= 13.6:
                        return 3
                    elif time <= 14.2:
                        return 4
                    elif time <= 15.1:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("9"): #100m
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 13.8:
                        return 1
                    elif time <= 14.4:
                        return 2
                    elif time <= 15.4:
                        return 3
                    elif time <= 16.9:
                        return 4
                    elif time <= 18.9:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 15.7:
                        return 1
                    elif time <= 16.5:
                        return 2
                    elif time <= 17.2:
                        return 3
                    elif time <= 18.4:
                        return 4
                    elif time <= 20.2:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("10"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 13.3:
                        return 1
                    elif time <= 14.0:
                        return 2
                    elif time <= 14.7:
                        return 3
                    elif time <= 16.0:
                        return 4
                    elif time <= 18.0:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 15.7:
                        return 1
                    elif time <= 16.5:
                        return 2
                    elif time <= 17.2:
                        return 3
                    elif time <= 18.3:
                        return 4
                    elif time <= 20.1:
                        return 5
                    else:
                        return 6
        else:
            return 6
            
    def Lauf(self,  klasse, time,  male):
        if klasse.startswith("5"):
            if male: #TODO: Notentabelle Jungen!!!!!!
                if time == 0:
                    return 6
                else:
                    if time <= 180:
                        return 1
                    elif time <= 195:
                        return 2
                    elif time <= 225:
                        return 3
                    elif time <= 265:
                        return 4
                    elif time <= 300:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 205:
                        return 1
                    elif time <= 222:
                        return 2
                    elif time <= 255:
                        return 3
                    elif time <= 281:
                        return 4
                    elif time <= 331:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("6"):
            if male: #TODO: Notentabelle Jungen!!!!!!
                if time == 0:
                    return 6
                else:
                    if time <= 176:
                        return 1
                    elif time <= 187:
                        return 2
                    elif time <= 220:
                        return 3
                    elif time <= 238:
                        return 4
                    elif time <= 290:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 200:
                        return 1
                    elif time <= 217:
                        return 2
                    elif time <= 250:
                        return 3
                    elif time <= 276:
                        return 4
                    elif time <= 325:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("7"):
            if male: #TODO: Notentabelle Jungen!!!!!!
                if time == 0:
                    return 6
                else:
                    if time <= 172:
                        return 1
                    elif time <= 183:
                        return 2
                    elif time <= 215:
                        return 3
                    elif time <= 232:
                        return 4
                    elif time <= 275:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 196:
                        return 1
                    elif time <= 213:
                        return 2
                    elif time <= 243:
                        return 3
                    elif time <= 268:
                        return 4
                    elif time <= 322:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("8"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 165:
                        return 1
                    elif time <= 176:
                        return 2
                    elif time <= 198:
                        return 3
                    elif time <= 217:
                        return 4
                    elif time <= 255:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 195:
                        return 1
                    elif time <= 210:
                        return 2
                    elif time <= 222:
                        return 3
                    elif time <= 248:
                        return 4
                    elif time <= 319:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("9"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 159:
                        return 1
                    elif time <= 170:
                        return 2
                    elif time <= 187:
                        return 3
                    elif time <= 203:
                        return 4
                    elif time <= 225:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 194:
                        return 1
                    elif time <= 208:
                        return 2
                    elif time <= 239:
                        return 3
                    elif time <= 245:
                        return 4
                    elif time <= 316:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("10"):
            if male:
                if time == 0:
                    return 6
                else:
                    if time <= 157:
                        return 1
                    elif time <= 165:
                        return 2
                    elif time <= 183:
                        return 3
                    elif time <= 198:
                        return 4
                    elif time <= 238:
                        return 5
                    else:
                        return 6
            else:
                if time == 0:
                    return 6
                else:
                    if time <= 193:
                        return 1
                    elif time <= 205:
                        return 2
                    elif time <= 235:
                        return 3
                    elif time <= 241:
                        return 4
                    elif time <= 307:
                        return 5
                    else:
                        return 6
        else:
            return 6
                
    def Sprung(self, klasse, dist, male):
        if klasse.startswith("5"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.40:
                        return 1
                    elif dist >= 3.00:
                        return 2
                    elif dist >= 2.70:
                        return 3
                    elif dist >= 2.40:
                        return 4
                    elif dist >= 2.20:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist > 3.20:
                        return 1
                    elif dist > 2.90:
                        return 2
                    elif dist > 2.60:
                        return 3
                    elif dist > 2.30:
                        return 4
                    elif dist > 2.10:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("6"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.55:
                        return 1
                    elif dist >= 3.31:
                        return 2
                    elif dist >= 2.98:
                        return 3
                    elif dist >= 2.73:
                        return 4
                    elif dist >= 2.35:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.30:
                        return 1
                    elif dist >= 3.10:
                        return 2
                    elif dist >= 2.70:
                        return 3
                    elif dist >= 2.57:
                        return 4
                    elif dist >= 2.20:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("7"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.80:
                        return 1
                    elif dist >= 3.57:
                        return 2
                    elif dist >= 3.19:
                        return 3
                    elif dist >= 2.95:
                        return 4
                    elif dist >= 2.50:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.60:
                        return 1
                    elif dist >= 3.35:
                        return 2
                    elif dist >= 2.96:
                        return 3
                    elif dist >= 2.70:
                        return 4
                    elif dist >= 2.30:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("8"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 4.00:
                        return 1
                    elif dist >= 3.70:
                        return 2
                    elif dist >= 3.31:
                        return 3
                    elif dist >= 3.05:
                        return 4
                    elif dist >= 2.70:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.70:
                        return 1
                    elif dist >= 3.45:
                        return 2
                    elif dist >= 3.11:
                        return 3
                    elif dist >= 2.80:
                        return 4
                    elif dist >= 2.40:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("9"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 4.30:
                        return 1
                    elif dist >= 4.03:
                        return 2
                    elif dist >= 3.57:
                        return 3
                    elif dist >= 3.25:
                        return 4
                    elif dist >= 2.80:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.75:
                        return 1
                    elif dist >= 3.55:
                        return 2
                    elif dist >= 3.15:
                        return 3
                    elif dist >= 2.90:
                        return 4
                    elif dist >= 2.40:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("10"):
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 4.60:
                        return 1
                    elif dist >= 4.33:
                        return 2
                    elif dist >= 3.90:
                        return 3
                    elif dist >= 3.60:
                        return 4
                    elif dist >= 3.10:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 3.80:
                        return 1
                    elif dist >= 3.60:
                        return 2
                    elif dist >= 3.20:
                        return 3
                    elif dist >= 2.95:
                        return 4
                    elif dist >= 2.50:
                        return 5
                    else:
                        return 6
        else:
            return 6
            
    def Wurf(self, klasse,  dist,  male):
        if klasse.startswith("5"): #200g Schlagball (Kommentierte Werte = 80g)
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 35.50: #40.00
                        return 1
                    elif dist >= 31.00: #34.00
                        return 2
                    elif dist >= 25.00: #28.00
                        return 3
                    elif dist >= 22.00: #24.00
                        return 4
                    elif dist >= 16.00: #18.00
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 24.00: #27.00
                        return 1
                    elif dist >= 20.50: #23.50
                        return 2
                    elif dist >= 16.00: #18.50
                        return 3
                    elif dist >= 13.00: #15.50
                        return 4
                    elif dist >= 9.50: #11.50
                        return 5
                    else:
                        return 6
        elif klasse.startswith("6"): #200g Schlagball (Kommentierte Werte = 80g)
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 41.00: #46.00
                        return 1
                    elif dist >= 36.00: #39.50
                        return 2
                    elif dist >= 29.00: #32.50
                        return 3
                    elif dist >= 25.00: #28.00
                        return 4
                    elif dist >= 18.00: #22.00
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 26.50: #30.00
                        return 1
                    elif dist >= 22.50: #26.50
                        return 2
                    elif dist >= 17.50: #21.50
                        return 3
                    elif dist >= 14.50: #18.00
                        return 4
                    elif dist >= 11.50: #16.50
                        return 5
                    else:
                        return 6
        elif klasse.startswith("7"): #3kg Kugelstoß
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 8.20:
                        return 1
                    elif dist >= 7.30:
                        return 2
                    elif dist >= 6.10:
                        return 3
                    elif dist >= 5.20:
                        return 4
                    elif dist >= 4.30:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 6.54:
                        return 1
                    elif dist >= 5.90:
                        return 2
                    elif dist >= 5.16:
                        return 3
                    elif dist >= 4.50:
                        return 4
                    elif dist >= 3.70:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("8"): #3kg Kugelstoß
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 8.60:
                        return 1
                    elif dist >= 7.90:
                        return 2
                    elif dist >= 6.75:
                        return 3
                    elif dist >= 6.25:
                        return 4
                    elif dist >= 5.30:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 6.94:
                        return 1
                    elif dist >= 6.30:
                        return 2
                    elif dist >= 5.56:
                        return 3
                    elif dist >= 4.80:
                        return 4
                    elif dist >= 3.90:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("9"): #Jungen 4kg, Mädchen 3kg Kugelstoß
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 9.00:
                        return 1
                    elif dist >= 8.50:
                        return 2
                    elif dist >= 7.90:
                        return 3
                    elif dist >= 7.00:
                        return 4
                    elif dist >= 5.40:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 7.30:
                        return 1
                    elif dist >= 6.70:
                        return 2
                    elif dist >= 6.00:
                        return 3
                    elif dist >= 5.30:
                        return 4
                    elif dist >= 4.80:
                        return 5
                    else:
                        return 6
        elif klasse.startswith("10"): #4kg Kugelstoß
            if male:
                if dist == 0:
                    return 6
                else:
                    if dist >= 9.60:
                        return 1
                    elif dist >= 8.90:
                        return 2
                    elif dist >= 8.30:
                        return 3
                    elif dist >= 7.90:
                        return 4
                    elif dist >= 6.90:
                        return 5
                    else:
                        return 6
            else:
                if dist == 0:
                    return 6
                else:
                    if dist >= 7.00:
                        return 1
                    elif dist >= 6.30:
                        return 2
                    elif dist >= 5.56:
                        return 3
                    elif dist >= 4.90:
                        return 4
                    elif dist >= 4.10:
                        return 5
                    else:
                        return 6
        else:
            return 6
