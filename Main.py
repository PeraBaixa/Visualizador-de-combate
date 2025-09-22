from Classes import *

link = Personagem("Link", "Elfo", "Guerreiro")
link = Barbaro(link)
link.setAtrs(12, 15, 12, 16, 15, 18)
link.iniciaClasse()

print(link.furia)
link.aumentaNivel(19)
print(link.furia)