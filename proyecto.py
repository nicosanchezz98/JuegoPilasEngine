import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar(gravedad=(0, 0))
pilas.avisar("Moverse con A ; D / Pausa: ALT+P")

musica = pilas.musica.cargar("SKRILLEX - Bangarang [Official Music Video].mp3")
musica.reproducir()
class Ladrillos(pilas.actores.Bomba):
    
    def __init__(self, x=0, y=0):
        pilas.actores.Bomba.__init__(self, x=0, y=0)
        self.radio_de_colision = 25
        self.image_normal = pilas.imagenes.cargar('ladrillo.png')
        self.definir_imagen(self.image_normal)
        self.radio_de_colision = 10

        
ladrillo=Ladrillos()

class Piso(pilas.actores.Bomba):
    
    def __init__(self, x=0, y=0):
        pilas.actores.Bomba.__init__(self, x=0, y=-230)
        self.radio_de_colision = 40
        self.image_normal = pilas.imagenes.cargar('piso.png')
        self.definir_imagen(self.image_normal)
        self.radio_de_colision = 15

piso=Piso()


teclas = {pilas.simbolos.a: 'izquierda',
          pilas.simbolos.d: 'derecha'}

mi_control = pilas.control.Control(pilas.escena_actual(), teclas)

class MiProtagonista(pilas.actores.Mono):
    
    def __init__(self, x=0, y=0):
        pilas.actores.Mono.__init__(self, x=0, y=-195)
        self.radio_de_colision = 50
        self.image_normal = pilas.imagenes.cargar('barra.png')
        self.definir_imagen(self.image_normal)
        self.aprender(pilas.habilidades.MoverseConElTeclado, control=mi_control)
    
        

barra = MiProtagonista()
barra.aprender(pilas.habilidades.SeMantieneEnPantalla, permitir_salida=False)
fondo = pilas.fondos.DesplazamientoHorizontal()
fondo.agregar("espacio-azul.jpg", velocidad=0)



from pilas.actores import Bomba

class BombaConMovimiento(Bomba):


    def __init__(self, x=0, y=0, activo=0):
        Bomba.__init__(self, x, y) 
        self.direccionx =  "POSITIVO"
        self.direcciony =  "POSITIVO"
        #aca definimos la imagen de la bomba, hay otra para probar que es bolas.png es otro modelo que hice de bombas
        self.image_normal = pilas.imagenes.cargar('bola.png')
        self.definir_imagen(self.image_normal)
        self.dx = 10
        self.dy = 10
        if activo:
            self.iniciar()


    def iniciar(self):
        self.circulo = pilas.fisica.Circulo(self.x, self.y, 20, restitucion=1, friccion=0, amortiguacion=0)
        self.imitar(self.circulo)
        self._empujar()        

    def _empujar(self):        
        self.circulo.impulsar(self.dx, self.dy)

    def rebotar(self, movx,movy):
        if movx=="POSITIVO" and movy=="POSITIVO":
            self.circulo.impulsar(self.dx*2, self.dy*2)
        if movx=="POSITIVO" and movy=="NEGATIVO":        
            self.circulo.impulsar(self.dx*2, -self.dy*2)
        if movx=="NEGATIVO" and movy=="POSITIVO":        
            self.circulo.impulsar(-self.dx*2, self.dy*2)
        if movx=="NEGATIVO" and movy=="NEGATIVO":        
            self.circulo.impulsar(-self.dx*2, -self.dy*2)


bomba_1 = BombaConMovimiento(x=60, y=213, activo=0)
bomba_2 = BombaConMovimiento(x=111, y=213, activo=0)
bomba_3 = BombaConMovimiento(x=0, y=-120, activo=1)
lista_de_bombas = [bomba_1, bomba_2, bomba_3]


ladrillos=ladrillo*33

tamx = 48
inix=-250
tamy=12
iniy=-10
cant=0

for ladrillo in ladrillos:
    ladrillo.x = inix
    ladrillo.y = iniy
    if cant < 10:        
        inix = inix + tamx
        cant=cant+1
    else:
        tamx = 48
        inix=-250
        iniy=iniy+tamy
        cant=0

pisos=piso*20


tamx = 80
inix=-330
tamy=52
iniy=-230
cant=0


for piso in pisos:
    piso.x = inix
    piso.y = iniy
    if cant < 10:        
        inix = inix + tamx
        cant=cant+1

def cuando_colisionan(bomba, ladrillo):
    movx = "POSITIVO"
    movy = "POSITIVO"
    if bomba.x < ladrillo.x:        
        movx="NEGATIVO"
    if bomba.y < ladrillo.y:        
        movy="NEGATIVO"
    ladrillo.explotar()
    bomba.rebotar(movx,movy)
    puntos1.aumentar(1)
    a=puntos1.obtener()
    if a == 33:
        mensaje = pilas.actores.Texto("GANASTE!")
        bomba_3.explotar()
        bomba_1.explotar()
        bomba_2.explotar()
        puntos.eliminar()

def cuando_colisionan1(bomba, barra):
    movx = "POSITIVO"
    movy = "POSITIVO"
    if bomba.x < barra.x:        
        movx="NEGATIVO"
    if bomba.y < barra.y:        
        movy="NEGATIVO"
    bomba.rebotar(movx,movy)

def cuando_colisionan_piso(bomba, piso):  
    puntos.aumentar(-1)
    p=puntos.obtener()
    pilas.avisar("PERDISTE UNA VIDA!")
    bomba.explotar()
    if p == 0:
        mensaje = pilas.actores.Texto("GAME OVER!")
        ladrillos.eliminar()
    else:
        lista_de_bombas[p-1].iniciar()
 
pilas.mundo.colisiones.agregar(lista_de_bombas, barra, cuando_colisionan1) 
pilas.mundo.colisiones.agregar(lista_de_bombas, ladrillos, cuando_colisionan)
pilas.mundo.colisiones.agregar(lista_de_bombas, pisos, cuando_colisionan_piso)



puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.aumentar(3)

puntos1 = pilas.actores.Puntaje(x=500, y=500, color=pilas.colores.blanco)
puntos1.aumentar(0)

pilas.actores.Sonido()

pilas.ejecutar()
