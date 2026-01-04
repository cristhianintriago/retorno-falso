import pygame
import sys
import random


# CONFIGURACION INICIAL DEL JUEGO
# TAMAÑO DE CADA CELDA DEL MAPA EN PIXELES
TILE_SIZE = 24  

# DIMENSIONES DEL MAPA EN NUMERO DE CELDAS
COLS = 34   # COLUMNAS (ANCHO)
FILAS = 25  # FILAS (ALTO)


# CLASE MAPA
# ESTA CLASE MANEJA TODO LO RELACIONADO CON EL LABERINTO
class Mapa:
    
    # CONSTRUCTOR DE LA CLASE
    def __init__(self):
        try:
            # CARGAR IMAGENES DESDE LA CARPETA ASSETS
            self.img_suelo = pygame.image.load("assets/suelo.png")
            self.img_muro = pygame.image.load("assets/muro.png")
            
            # CAMBIAR EL TAMAÑO DE LAS IMAGENES
            self.img_suelo = pygame.transform.scale(self.img_suelo, (TILE_SIZE, TILE_SIZE))
            self.img_muro = pygame.transform.scale(self.img_muro, (TILE_SIZE, TILE_SIZE))
            
            # GENERAR POSICION ALEATORIA DE LA SALIDA
            # LA SALIDA ESTARA EN LA SEGUNDA MITAD DEL MAPA
            min_col = COLS // 2
            max_col = COLS - 2
            min_fila = FILAS // 2
            max_fila = FILAS - 2
            
            # GENERAR COORDENADAS ALEATORIAS PARA LA SALIDA
            self.salida_col = random.randint(min_col, max_col)
            self.salida_fila = random.randint(min_fila, max_fila)
            print("Salida en Columna:", self.salida_col, "Fila:", self.salida_fila)
            
            # GENERAR LA MATRIZ DEL NIVEL
            # 0 REPRESENTA SUELO Y 1 REPRESENTA MURO
            self.matriz_nivel = self._generar_nivel_con_camino()
            
            # LISTA PARA GUARDAR LOS RECTANGULOS DE COLISION
            self.muros = [] 
            self._crear_hitbox_muros()
            
        except Exception as e:
            print("ERROR: No se pudo cargar el mapa.", e)
            sys.exit()


    # METODO PARA GENERAR EL NIVEL CON UN CAMINO GARANTIZADO
    def _generar_nivel_con_camino(self):
        
        # PASO 1: CREAR MAPA BASE CON MUROS ALEATORIOS
        nueva_matriz = []
        
        # RECORRER TODAS LAS FILAS
        for fila in range(FILAS):
            fila_lista = []
            
            # RECORRER TODAS LAS COLUMNAS
            for col in range(COLS):
                # LOS BORDES SIEMPRE SON MUROS
                if fila == 0 or fila == FILAS - 1 or col == 0 or col == COLS - 1:
                    fila_lista.append(1)  # AGREGAR MURO
                else:
                    # GENERAR MUROS ALEATORIOS EN EL INTERIOR
                    # 35 POR CIENTO DE PROBABILIDAD DE CREAR UN MURO
                    if random.random() < 0.35:
                        fila_lista.append(1)  # MURO
                    else:
                        fila_lista.append(0)  # SUELO
            
            nueva_matriz.append(fila_lista)
        
        # PASO 2: CREAR CAMINO GARANTIZADO HACIA LA META
        # EMPEZAMOS EN LA POSICION 1,1
        x = 1
        y = 1
        nueva_matriz[y][x] = 0  # ASEGURAR QUE EL INICIO SEA SUELO
        
        # VARIABLES DE CONTROL PARA EVITAR BUCLES INFINITOS
        intentos = 0
        max_intentos = COLS * FILAS * 2 
        
        # CICLO QUE CREA EL CAMINO HASTA LLEGAR A LA SALIDA
        while (x != self.salida_col or y != self.salida_fila) and intentos < max_intentos:
            opciones = []
            
            # INTENTAR MOVERSE HACIA LA META
            if x < self.salida_col:
                opciones.append("DERECHA")
            if y < self.salida_fila:
                opciones.append("ABAJO")
            
            # SI NO HAY OPCIONES PERMITIR CUALQUIER DIRECCION VALIDA
            if len(opciones) == 0: 
                if x < COLS - 2:
                    opciones.append("DERECHA")
                if y < FILAS - 2:
                    opciones.append("ABAJO")
            
            # EJECUTAR EL MOVIMIENTO
            if len(opciones) > 0:
                direccion = random.choice(opciones)
                if direccion == "DERECHA":
                    x = x + 1
                else:
                    y = y + 1
                
                # CONVERTIR LA CELDA EN SUELO
                nueva_matriz[y][x] = 0
            
            intentos = intentos + 1
        
        # ASEGURAR QUE LA META SEA SUELO
        nueva_matriz[self.salida_fila][self.salida_col] = 0
        
        return nueva_matriz


    # METODO PARA CREAR RECTANGULOS DE COLISION PARA CADA MURO
    def _crear_hitbox_muros(self):
        
        self.muros = []  # LIMPIAR LA LISTA
        
        # RECORRER TODA LA MATRIZ
        for fila_idx in range(len(self.matriz_nivel)):
            for col_idx in range(len(self.matriz_nivel[fila_idx])):
                valor = self.matriz_nivel[fila_idx][col_idx]
                
                # SI ES UN MURO
                if valor == 1:
                    # CALCULAR POSICION EN PIXELES
                    x = col_idx * TILE_SIZE
                    y = fila_idx * TILE_SIZE
                    
                    # CREAR RECTANGULO Y AGREGARLO A LA LISTA
                    rectangulo = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.muros.append(rectangulo)


    # METODO PARA DIBUJAR EL MAPA EN LA PANTALLA CON VISION LIMITADA
    def dibujar(self, pantalla, jugador_rect):
        
        # CALCULAR POSICION DEL JUGADOR EN LA CUADRICULA
        col_jugador = jugador_rect.centerx // TILE_SIZE
        fila_jugador = jugador_rect.centery // TILE_SIZE
        
        # RANGO DE VISION (3 CELDAS EN CADA DIRECCION)
        RANGO = 3 
        
        # RECORRER TODA LA MATRIZ PARA DIBUJAR
        for fila_idx in range(len(self.matriz_nivel)):
            for col_idx in range(len(self.matriz_nivel[fila_idx])):
                valor = self.matriz_nivel[fila_idx][col_idx]
                
                # POSICION EN PIXELES
                x = col_idx * TILE_SIZE
                y = fila_idx * TILE_SIZE
                
                # CALCULAR DISTANCIA AL JUGADOR
                distancia_fila = abs(fila_idx - fila_jugador)
                distancia_col = abs(col_idx - col_jugador)
                
                # VERIFICAR SI ESTA DENTRO DEL RANGO DE VISION
                if distancia_fila <= RANGO and distancia_col <= RANGO:
                    # DIBUJAR LA META (CUADRO VERDE)
                    if col_idx == self.salida_col and fila_idx == self.salida_fila:
                        pygame.draw.rect(pantalla, (0, 255, 0), (x, y, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, TILE_SIZE, TILE_SIZE), 2)
                    # DIBUJAR MURO
                    elif valor == 1:
                        pantalla.blit(self.img_muro, (x, y))
                    # DIBUJAR SUELO
                    else:
                        pantalla.blit(self.img_suelo, (x, y))
                else:
                    # FUERA DEL RANGO DE VISION: DIBUJAR NEGRO
                    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE))
