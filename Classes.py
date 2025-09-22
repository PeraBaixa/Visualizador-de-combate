from random import randint
from genclasses import *


class Classe(Personagem):
    def __init__(obj, perso):
        super().__init__(perso.nome, perso.raca, perso.classe, perso.nvl)
        obj.dadovida = 4
        obj.classe = "Plebeu"

    def iniciaClasse(obj):
        obj.vidamax = obj.dadovida + obj.getBon("CON")
        obj.vida[0] = obj.dadovida + obj.getBon("CON")
       

        if obj.nvl > 1:
            obj.aumentaNivel(obj.nvl-1)

    def aumentaNivel(obj, qtNvl=1):
        obj.nvl = 1
        aum = 0
        cont = 0

        while cont < (qtNvl) and obj.nvl < 21:
            obj.nvl += 1
            if auto:
                aum += randint(1, obj.dadovida)
            else:
                print("Vida atual: " + str(obj.vidamax))
                v = int(input("Insira a vida a ser adicionada: "))
                while True:
                    if v > obj.dadovida or v < 0:
                        print("Valor inválido")
                    else:
                        aum += v
                        break

            if obj.nvl > 20: obj.nvl = 20
            cont += 1
            obj.recebeCarac()

        obj.vidamax += (aum + obj.getBon("CON"))
        obj.vida[0] += (aum + obj.getBon("CON"))

    def recebeCarac(obj):
        pass

class Barbaro(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 12
        obj.classe = "Bárbaro"
        obj.furia = {"estado": False, "qtDesc": 2, "danoBon": 2}

    def iniciaClasse(obj):
        super().iniciaClasse()
        obj.armadura = 10 + obj.getBon("DES") + obj.getBon("CON")
    
    def recebeCarac(obj):      
        match obj.nvl:
            case 2:
                obj.resists.append("resDes")
            case 3:
                obj.furia["qtDesc"] = 3
            case 4:
                pass
            case 5:
                pass
            case 6:
                obj.furia["qtDesc"] = 4
            case 7:
                pass
            case 8:
                pass
            case 9:
                obj.furia["danoBon"] = 3
            case 10:
                pass
            case 11:
                pass
            case 12:
                obj.furia["qtDesc"] = 5
            case 13:
                pass
            case 14:
                pass
            case 15:
                pass
            case 16:
                obj.furia["danoBon"] = 4
            case 17:
                obj.furia["qtDesc"] = 6
            case 18:
                pass
            case 19:
                pass
            case 20:
                obj.furia["qtDesc"] = 1000

    def ativarFuria(obj):
        if not obj.furia["estado"]:
            obj.furia["estado"] = True
            obj.resists += ["concussivo", "cortante", "perfurante", "resFor"]

            for a in obj.ataques:
                atk = retornaObj(a, listaAtaques)
                if atk.atrbon == "FOR" and atk.melee:
                    atk.bonus += obj.furia["danoBon"]
    
    def desativarFuria(obj):
        if obj.furia["estado"]:
            obj.furia["estado"] = False
            obj.resists.remove("concussivo")
            obj.resists.remove("cortante")
            obj.resists.remove("perfurante")
            obj.resists.remove("resFor")

            for a in obj.ataques:
                atk = retornaObj(a, listaAtaques)
                if atk.atrbon == "FOR":
                    atk.bonus -= obj.furia["danoBon"]
      
class Bardo(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "Bardo"
        
class Bruxo(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "Bruxo"

class Clerigo(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "clérigo"

class Druida(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "Druida"

class Feiticeiro(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 6
        obj.classe = "Feiticeiro"

class Guerreiro(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 10
        obj.classe = "Guerreiro"

class Ladino(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "Ladino"

class Mago(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 6
        obj.classe = "Mago"

class Monge(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 8
        obj.classe = "Monge"

class Paladino(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 10
        obj.classe = "Paladino"

class Patrulheiro(Classe):
    def __init__(obj, perso):
        super().__init__(perso)
        obj.dadovida = 10
        obj.classe = "Patrulheiro"