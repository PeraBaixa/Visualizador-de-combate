from random import choice
#Listas importantes
listaAtaques, criaturas, itens, magias = [], [], [], []

#Variáveis globais
auto = True

listatipos = [
    "concussivo",
    "cortante",
    "perfurante",
    "ácido",
    "elétrico",
    "energético",
    "ígneo",
    "gélido",
    "necrótico",
    "psíquico",
    "radiante",
    "trovejante",
    "venenoso"
    ]

listaraca = [
    "Anão",
    "Elfo",
    "Halfling",
    "Humano",
    "Draconato",
    "Gnomo",
    "Orc",
    "Tiefling"
]

listaclasses = [
    "Bárbaro",
    "Bardo",
    "Bruxo",
    "Clérigo",
    "Druida",
    "Feiticeiro",
    "Guerreiro",
    "Ladino",
    "Mago",
    "Monge",
    "Paladino",
    "Patrulheiro"
]

class Criatura:
    def __init__(obj, nome):
        obj.nome = nome
        obj.vidamax = 0
        obj.vida = [0,0] #pontos de vida atuais/pontos de vida temporários
        obj.armadura = 10
        obj.atrs = {
            "FOR": 10,
            "DES": 10,
            "CON": 10,
            "INT": 10,
            "SAB": 10,
            "CON": 10
        }
        
        criaturas.append(obj)
        obj.cod = len(criaturas)
        obj.acaoPri, obj.atqAcao = 1, 1
        
        obj.estadoCri = []

        obj.caracs = []
        obj.ataques = []
        obj.inventario = []
        obj.fraq, obj.resists, obj.imunis = [], [], []

    def setAtrs(obj, f, d, con, i, s, car):
        obj.atrs = {
            "FOR": f,
            "DES": d,
            "CON": con,
            "INT": i,
            "SAB":s,
            "CAR": car
        }

        obj.armadura += obj.atrs['DES']
        
    def getBon(obj, atr):
        if atr != "":
            return ((obj.atrs[atr.upper()])-10)//2
        else:
            return 0
    
    def __str__(obj):
        return f"Criatura de nome {obj.nome}"
    
    def sofrerDano(dano, tipo):
        if tipo in obj.resists: dano //= 2
        if tipo in imunis: dano = 0
        if tipo in fraq: dano *= 2

class Personagem(Criatura):
    def __init__(obj, nome, raca, classe, nvl=1):
        super().__init__(nome)
        obj.nvl = nvl
        if raca.lower() in listaraca:
            obj.raca = raca.lower()
        else:
            obj.raca = choice(listaraca)
        obj.classe = classe.lower().capitalize()

        obj.estado = "normal"

        Ataque("Ataque Desarmado", "1d4", "concussivo", "FOR").adiAtaque(obj)
    
    def setAtrs(obj, f, d, con, i, s, car):
        obj.vidamax += ((con - obj.atrs["CON"])//2)*obj.nvl
        obj.vida[0] += ((con - obj.atrs["CON"])//2)*obj.nvl
        super().setAtrs(f, d, con, i, s, car)

class Item:
    def __init__(obj, nome, desc):
        obj.nome = nome
        obj.desc = desc
        obj.qt = 0
        obj.perso = None
        itens.append(obj)
        obj.cod = len(itens)
    
    def adiItem(obj, perso):
        obj.qt += 1
        if obj.qt == 1:
            perso.inventario.append(obj.cod)
            obj.perso = perso.cod
    
    def perdeItem(obj, perso):
        obj.qt -= 1
        if obj.qt == 0:
            perso.inventario.remove(obj.cod)
            obj.perso = None

class Arma(Item):
    def __init__(obj, nome, desc, dano, tipo, mod=""):
        super().__init__(nome, desc)
        obj.dano = dano.lower() + " " + tipo.lower()
        bonAt = ""
        match mod.lower():
            case "leve":
               bonAt = "DES"
            case __:
                bonAt = "FOR"
        obj.codatk = Ataque(obj.nome, dano, tipo, bonAt).cod
    
    def adiItem(obj, perso):
        super().adiItem(perso)
        perso.ataques.append(obj.codatk)
        retornaObj(obj.codatk, listaAtaques).perso = perso.cod
    
    def perdeItem(obj, perso):
        super().perdeItem(perso)
        perso.ataques.remove(obj.codatk)

class Ataque:
    def __init__(obj, nome, dano, tipo, atrbon="", bonusbase=0, melee=True):
        obj.nome = nome
        obj.qtdado, obj.dado, obj.bonus = 0, 0, 0
        obj.tipo = "concussivo"
        if tipo in listatipos: obj.tipo = tipo.lower()
        obj.iniciaDano(dano.lower())
        obj.bonusbase = bonusbase
        obj.atrbon = atrbon
        obj.melee = melee
        obj.perso = None
        listaAtaques.append(obj)
        obj.cod = len(listaAtaques)

    def iniciaDano(obj, dano):
        d = dano.index('d')
        if '+' in dano: b = dano.index('+')
        else: b = 0

        obj.qtdado = int(dano[:d])
        if b: obj.dado = int(dano[(d+1):b])
        else: obj.dado = int(dano[(d+1):])
        if b: obj.bonus = int(dano[(b+1):])
    
    def adiAtaque(obj, perso):
        obj.perso = perso.cod
        perso.ataques.append(obj.cod)

    def perdeAtaque(obj, perso):
        if obj.cod in perso.ataques:
            perso.ataques.remove(obj.cod)
        else:
            print("Esse personagem não tem este ataque")

    def getDano(obj):
        perso = retornaObj(obj.perso, criaturas)
        b = obj.bonus + perso.getBon(obj.atrbon)
        if b > 0:
            b = "+"+str(b)
        elif b < 0:
            b = str(b)
        
        return f"{obj.qtdado}d{obj.dado}{b if b != 0 else ''}"

    def __str__(obj):
        if obj.bonus > 0: bon = '+'+str(obj.bonus)+'atrbon'
        else: bon = ''
        return f"O ataque '{obj.nome}' dá {obj.qtdado}d{obj.dado}{bon} de dano {obj.tipo}"

class Magia:
    def __init__(obj, nome, classe, desc, nvlMin=0, dist=0, alvos="1 pessoa"):
        obj.nome = nome
        obj.classe = classe #Em qual lista de classe a magia está
        obj.desc = desc
        obj.nvlMin = nvlMin #"0" significa truque
        obj.dist = dist #Em metros. '0' significa "ao toque"
        obj.alvos = alvos
        obj.perso = None
        magias.append(obj)
        obj.cod = len(magias)

    def adiMagia(obj, perso):
        try:
            perso.magiasProntas.append(obj.cod)
            obj.perso = perso.cod
        except:
            print("O personagem não pertence a uma classe conjuradora!")
        
    def perdeMagia(obj, perso):
        try:
            if obj.cod in perso.magiasProntas:
                perso.magiasProntas.remove(obj.cod)
            else:
                print("Esse personagem não tem essa magia")
        except:
            print("O personagem não pertence a uma classe conjuradora!")

    def afetarAlvo(obj, alvo):
        pass

class MagiaDeAtaque(Magia):
    def __init__(obj, nome, desc, dano, tipo, nvlMin=0, dist=0, alvos="1 pessoa"):
        super().__init__(nome, desc, nvlMin, dist, alvos)
        obj.dano = dano
        obj.tipo = tipo #Tipo de dano
        obj.codatk = Ataque(obj.nome, obj.dano, obj.tipo, melee=(dist==0)).cod

    def adiMagia(obj, perso):
        super().adiMagia(perso)
        try:
            perso.magiasProntas[0]
            perso.ataques.append(obj.codatk)
        except:
            pass

def retornaObj(cod, lista):
    for e in lista:
        if e.cod == cod:
            return e

link = Personagem("Link", "Elfo", "Guerreiro")
Magia("Explosão Solar", "Clérigo", "Uma literal explosão de puro poder estelar").adiMagia(link)
