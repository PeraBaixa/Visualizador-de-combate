from random import choice
#Listas importantes
listaAtaques, criaturas, itens = [], [], []

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
        
        return f"{obj.qtdado}d{obj.dado}{b if b != 0 else ""}"

    def __str__(obj):
        if obj.bonus > 0: bon = '+'+str(obj.bonus)+'atrbon'
        else: bon = ''
        return f"O ataque '{obj.nome}' dá {obj.qtdado}d{obj.dado}{bon} de dano {obj.tipo}"

class Caracteristica:
    def __init__(obj, nome, desc):
        obj.nome = nome
        obj.desc = desc

    def adiCarac(obj, perso):
        perso.caracs.append(obj)
    
    def perdeCarac(obj, perso):
        perso.caracs
    
    def __str__(obj):
        return f"Essa Carcterística não tem efeitos mecânicos"

class LinguaDeVeludo(Caracteristica):
    def __init__(obj):
        super().__init__("Língua de Veludo", "O personagem é um safado")
        
def retornaObj(cod, lista):
    for e in lista:
        if e.cod == cod:
            return e