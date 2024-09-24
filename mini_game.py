import pygame
import sys 
import time 
import os
import random

# erreur inclusion circulaire j'en ai marre 
#from playerCodeFile import playerCode

# 1 ==> rien # carré blanc 
# 0 ==> obstacle # carré gris 
# 4 ==> troll / ennmi # carré rouge 
# 2 ==> Harry  # carré bleu
# 3 ==> Voldemort # carré vert 
# la map peut faire une plus grande taille si il faut mais au début se sera 6 * 6

colors = {
    0: (128, 128, 128),  # Gris pour l'obstacle
    1: (255, 255, 255),  # Blanc pour rien
    2: (0, 0, 255),      # Bleu pour Harry
    3: (0, 255, 0),      # Vert pour Voldemort
    4: (255, 0, 0),       # Rouge pour le troll/ennemi
    5: (0, 0, 0) 			# noir 
}

#   N
#  W E
# 	S 
"""""
liste de fonction à faire 
1 ) move() OK 
2 ) turn_left() OK
3 ) turn_right() OK

4 ) can move() OK
5 ) is_in_front_of_enemy() OK
6 ) is_on_target() OK
7 ) destroy_voldemort() OK
8 ) get_direction() (renvoi la direction courante de harry NORTH, SOUTH, WEST, EAST) OK
9 ) get_x() (renvoi la co X de harry) OK
10 ) get_y() (renvoi la co Y de harry) OK
11 ) get_target_x() (renvoi la cordonnées X de voldemort) OK
12 ) get_target_y() (renvoi la coordonnée Y de voldemort) OK
"""""

# directions
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
DIRECTION = NORTH # regarde vers le nord au début 

##########################################
# la carte du jeux est ici :
# 1 cases vides
# 2 harry
# 3 voldemort
# 4 méchant
# tu peux agrandir la carte si tu veux , fait toi plaisir ! Il y à aussi plusieurs modèle en dessous 
# pour changer de carte tu dois modifier la ligne MAP = first/second/third, si tu veux crée ta propre 
# carte soit tu modifie une carte existante ou tu en copie colle une , change son nom 
# et tu le modifie et tu la met dans la ligne MAP = NOM_DE_TA_CARTE
#########################################
first = [
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [2, 0, 1, 4, 0, 3, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 4, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 4, 1, 1],
    [0, 0, 0, 1, 4, 1, 1, 1, 1, 1],
    [1, 1, 4, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
]

second = [
    [2, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 4, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 4, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 4, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 4],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 3],
]

third = [
    [2, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 4, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 4, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 4],
    [1, 3, 1, 1, 1, 1, 1, 1, 1, 1],
]

# *************************************************************************
# ***** CETTE LIGNE ICI POUR CHANGER LA CARTE : MAP = NOM_DE_TA_CARTE *****
# *************************************************************************
MAP = third
# *************************************************************************
# *************************************************************************


# la taille de chaque bloc 
blockHeight = 80
blockWidth = 80
# Utiliser len() pour obtenir la taille de la map
window_width, window_height = len(MAP[0]) * blockWidth, len(MAP) * blockHeight

# fonction utilisé pour bloquer le joueur quand nécessaire 
can_move_val = True
is_voldemort_dead = False #valeur pour savoir si voldemort est mort ou pas 
nbr_of_actions = 0



screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Code Killer")

# Initialiser une horloge pour gérer le temps
clock = pygame.time.Clock()

def pause_time(duration):
    paused = True
    pause_start_time = pygame.time.get_ticks()  # Temps où la pause commence

    while paused:
        # Obtenir le temps actuel et vérifier si la durée de la pause est atteinte
        current_time = pygame.time.get_ticks()
        
        # Si la durée spécifiée est atteinte, reprendre le jeu
        if current_time - pause_start_time >= duration:
            paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mettre à jour l'affichage et gérer les événements
        pygame.display.flip()

        # Limiter la vitesse de la boucle de pause (par exemple, 30 FPS)
        clock.tick(30)

def pause_and_set_map(time):
    # Rafraîchir l'affichage et ajouter un délai
    createMAP()  # Redessine la carte avec la nouvelle direction
    pygame.display.update()  # Met à jour l'affichage
    pygame.time.delay(time)  # Pause de 500 ms pour ralentir la rotation

# Fonction pour imprimer la carte sous forme de texte dans un fichier
def printMAP(MAP):
    map_str = ""
    for row in MAP:
        map_str += ' '.join(map(str, row)) + '\n'
    return map_str

# fonction pour la position de dpéart de harry 
def find_harry():
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            if MAP[row][col] == 2:
                return row, col
    return None, None

# renvoi la posotion de voldemort
def find_voldemort():
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            if MAP[row][col] == 3:
                return row, col
    return None, None

# si on est sur un ennemi on arrete le jeux 
def isOnEnnemy():
    global harry_x, harry_y 
    if MAP[harry_y][harry_x] == 4:  # 4 représente un ennemi
        print("Harry a rencontré un ennemi.")
        return True
    return False

# si on est sur un mur on arrete le jeux
def isOnWall():
    global harry_x, harry_y
    if MAP[harry_y][harry_x] == 0:  # 0 représente un mur
        print("Harry a touché un mur.")
        return True
    return False

harry_y, harry_x = find_harry() # position initiale harry
voldemort_y, voldemort_x = find_voldemort() # position initiale voldemort

# UTILS
def get_new_position(harry_x, harry, DIRECTION):
    new_x, new_y = harry_x, harry_y

    # calculer la nouvelle pos en fonction de la direction 
    if DIRECTION == NORTH:
        new_y -= 1
    elif DIRECTION == EAST:
        new_x += 1
    elif DIRECTION == SOUTH:
        new_y += 1
    elif DIRECTION == WEST:
        new_x -= 1
    return new_x, new_y

# FUNCTIONS 


# fonction à appeller pour bouger 
def move():
    global harry_x, harry_y, can_move_val, is_voldemort_dead, nbr_of_actions # Valeur globale

    # Obtenir la nouvelle position en fonction de la direction actuelle
    new_x, new_y = get_new_position(harry_x, harry_y, DIRECTION)

    # Vérifier si le personnage peut se déplacer
    if can_move_val:
        nbr_of_actions += 1 # on augmente le compteur de mouvements
        if 0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP):
            # Si Harry s'avance vers un mur (0) ou un ennemi (4)
            if MAP[new_y][new_x] == 4 or MAP[new_y][new_x] == 0:
                # Mettre Harry sur la case tout de même, mais bloquer les mouvements suivants
                if (harry_y, harry_x) == (voldemort_y, voldemort_x) and is_voldemort_dead is False:
                    MAP[harry_y][harry_x] = 3
                else:
                    MAP[harry_y][harry_x] = 1  # L'ancienne case devient vide
                harry_x, harry_y = new_x, new_y  # Harry avance sur l'obstacle ou l'ennemi
                MAP[harry_y][harry_x] = 2  # Mettre à jour Harry sur la nouvelle case
                can_move_val = False  # Bloquer tout autre mouvement
                print("Harry est dans un mur ou sur un ennemi")
            else:
                # Sinon, déplacer Harry normalement
                if (harry_y, harry_x) == (voldemort_y, voldemort_x) and is_voldemort_dead is False:
                    MAP[harry_y][harry_x] = 3
                else:
                    MAP[harry_y][harry_x] = 1  # L'ancienne case devient vide
                harry_x, harry_y = new_x, new_y  # Harry avance
                MAP[harry_y][harry_x] = 2  # Mettre à jour Harry sur la nouvelle case
        
        if nbr_of_actions >= 300:
            can_move = False
            print("nbr of actions is 300 or above you have exceeded the autorized movements")
        
        pause_and_set_map(500)

# permet au personnage de tourner à gauche
def turn_left():
    global DIRECTION, can_move_val, nbr_of_actions
    if can_move_val is True and nbr_of_actions <= 300:
        DIRECTION = (DIRECTION - 1) % 4
        nbr_of_actions += 1
        pause_and_set_map(500)

# permet au personnage de tourner à gauche
def turn_right():
    global DIRECTION, can_move_val, nbr_of_actions
    if can_move_val is True and nbr_of_actions <= 300:
        DIRECTION = (DIRECTION + 1) % 4
        nbr_of_actions += 1
        pause_and_set_map(500)


def can_move():
    global harry_x, harry_y, DIRECTION
    new_x, new_y = harry_x, harry_y # calculer la nouvelle position 

    new_x, new_y = get_new_position(harry_x, harry_y, DIRECTION)
    
    if not (0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP)):
        return False
    
    if MAP[new_y][new_x] == 0:
        return False
    return True

# nous dit si on est en face d'un ennemi
def is_in_front_of_enemy():
    global harry_x, harry_y, DIRECTION
    new_x, new_y = harry_x, harry_y # calculer la nouvelle position 

    new_x, new_y = get_new_position(harry_x, harry_y, DIRECTION)
    
    if not (0 <= new_x < len(MAP[0]) and 0 <= new_y < len(MAP)):
        return False
    
    if MAP[new_y][new_x] == 4:
        return True
    return False

# Vérifier si Harry est sur la même case que Voldemort
def is_on_target():
    global harry_x, harry_y, voldemort_x, voldemort_y
    #print("harry x harry y voldemor x voldemort y ", harry_x, harry_y, voldemort_x, voldemort_y)
    return (harry_x, harry_y) == (voldemort_x, voldemort_y)

#########################################################################
#########################################################################


# Vérifier si une cellule est valide (pas un mur ou un ennemi et dans les limites de la carte)
def is_valid_cell(MAP, x, y, visited):
    rows, cols = len(MAP), len(MAP[0])
    return 0 <= x < cols and 0 <= y < rows and MAP[y][x] != 0 and MAP[y][x] != 4 and not visited[y][x]

# Fonction pour explorer les chemins possibles
def find_paths_util(MAP, source, destination, visited, path, paths, max_moves):
    """Utilisation de la recherche en profondeur pour trouver les chemins"""
    x, y = source
    voldemort_x, voldemort_y = destination

    # Si nous avons atteint Voldemort ou dépassé le nombre maximum de coups
    if (x, y) == (voldemort_x, voldemort_y):
        paths.append(path[:])  # Chemin trouvé
        return

    if max_moves <= 0:
        return  # Si le nombre de mouvements est épuisé, on arrête la recherche

    # Marquer la case actuelle comme visitée
    visited[y][x] = True

    # Directions possibles (Nord, Est, Sud, Ouest)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # Explorer les quatre directions
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy

        # Vérifier si la nouvelle cellule est valide
        if is_valid_cell(MAP, new_x, new_y, visited):
            path.append((new_x, new_y))
            find_paths_util(MAP, (new_x, new_y), destination, visited, path, paths, max_moves - 1)
            path.pop()  # Backtrack

    # Décocher la cellule actuelle
    visited[y][x] = False

# Fonction principale pour trouver les chemins
def findPath(MAP, harry_x, harry_y, voldemort_x, voldemort_y, max_moves=300):
    rows, cols = len(MAP), len(MAP[0])

    # Matrice de cellules visitées
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Initialiser les chemins et le chemin actuel
    paths = []
    path = [(harry_x, harry_y)]

    # Lancer la recherche DFS
    find_paths_util(MAP, (harry_x, harry_y), (voldemort_x, voldemort_y), visited, path, paths, max_moves)

    # Si au moins un chemin est trouvé, la carte est faisable
    if paths:
        print("Chemin(s) trouvé(s), la carte est faisable.")
        return True
    else:
        print("Aucun chemin trouvé ou trop de coups nécessaires.")
        printMAP(MAP)
        return False


#########################################################################
#########################################################################


#def replaceVol(MAP, harry_x, harry_y, voldemort_x, voldemort_y):
#    rows = len(MAP)
#    cols = len(MAP[0])
#    
#    # Vérifier si Voldemort ou Harry ont des indices None
#    if voldemort_x is None or voldemort_y is None:
#        voldemort_x, voldemort_y = 0, 0  # Initialiser Voldemort à une position valide
#    if harry_x is None or harry_y is None:
#        harry_x, harry_y = rows - 1, cols - 1  # Initialiser Harry à une position valide
#
#    # Remettre les anciennes positions de Harry et Voldemort à '1' (case vide)
#    MAP[harry_y][harry_x] = 1
#    MAP[voldemort_y][voldemort_x] = 1
#
#    # Vérifier si Harry et Voldemort sont déjà dans des coins opposés
#    if (harry_x, harry_y) == (0, 0) and (voldemort_x, voldemort_y) == (rows - 1, cols - 1):
#        # Si c'est le cas, on les échange
#        harry_x, harry_y = rows - 1, cols - 1  # Mettre Harry en bas à droite
#        voldemort_x, voldemort_y = 0, 0  # Mettre Voldemort en haut à gauche
#    elif (harry_x, harry_y) == (rows - 1, cols - 1) and (voldemort_x, voldemort_y) == (0, 0):
#        # Si Harry et Voldemort sont déjà dans l'autre configuration, on les replace ailleurs
#        harry_x, harry_y = random.choice([(0, cols - 1), (rows - 1, 0)])  # Mettre Harry dans un autre coin
#        voldemort_x, voldemort_y = random.choice([(0, 0), (rows - 1, cols - 1)])  # Placer Voldemort ailleurs
#    else:
#        # Sinon, on les place aux coins opposés
#        harry_x, harry_y = 0, 0  # Mettre Harry en haut à gauche
#        voldemort_x, voldemort_y = rows - 1, cols - 1  # Mettre Voldemort en bas à droite
#    
#    # Placer les nouveaux emplacements de Harry et Voldemort sur la carte
#    MAP[harry_y][harry_x] = 2  # Harry
#    MAP[voldemort_y][voldemort_x] = 3  # Voldemort
#
#    return harry_x, harry_y, voldemort_x, voldemort_y, MAP

def replaceVol(MAP, harry_x, harry_y, voldemort_x, voldemort_y):
    rows = len(MAP)
    cols = len(MAP[0])

    # Vérifier si Voldemort ou Harry ont des indices None ou sont hors limites
    if voldemort_x is None or voldemort_y is None or not (0 <= voldemort_x < cols and 0 <= voldemort_y < rows):
        voldemort_x, voldemort_y = 0, 0  # Initialiser Voldemort à une position valide
    if harry_x is None or harry_y is None or not (0 <= harry_x < cols and 0 <= harry_y < rows):
        harry_x, harry_y = rows - 1, cols - 1  # Initialiser Harry à une position valide

    # Remettre les anciennes positions de Harry et Voldemort à '1' (case vide)
    if 0 <= harry_y < rows and 0 <= harry_x < cols:
        MAP[harry_y][harry_x] = 1
    if 0 <= voldemort_y < rows and 0 <= voldemort_x < cols:
        MAP[voldemort_y][voldemort_x] = 1

    # Vérifier si Harry et Voldemort sont déjà dans des coins opposés
    if (harry_x, harry_y) == (0, 0) and (voldemort_x, voldemort_y) == (rows - 1, cols - 1):
        # Si c'est le cas, on les échange
        harry_x, harry_y = rows - 1, cols - 1  # Mettre Harry en bas à droite
        voldemort_x, voldemort_y = 0, 0  # Mettre Voldemort en haut à gauche
    elif (harry_x, harry_y) == (rows - 1, cols - 1) and (voldemort_x, voldemort_y) == (0, 0):
        # Si Harry et Voldemort sont déjà dans l'autre configuration, on les replace ailleurs
        harry_x, harry_y = random.choice([(0, cols - 1), (rows - 1, 0)])  # Mettre Harry dans un autre coin
        voldemort_x, voldemort_y = random.choice([(0, 0), (rows - 1, cols - 1)])  # Placer Voldemort ailleurs
    else:
        # Sinon, on les place aux coins opposés
        harry_x, harry_y = 0, 0  # Mettre Harry en haut à gauche
        voldemort_x, voldemort_y = rows - 1, cols - 1  # Mettre Voldemort en bas à droite

    # Placer les nouveaux emplacements de Harry et Voldemort sur la carte
    if 0 <= harry_y < rows and 0 <= harry_x < cols:
        MAP[harry_y][harry_x] = 2  # Harry
    if 0 <= voldemort_y < rows and 0 <= voldemort_x < cols:
        MAP[voldemort_y][voldemort_x] = 3  # Voldemort

    return harry_x, harry_y, voldemort_x, voldemort_y, MAP

#########################################################################
#########################################################################


#########################################################################
#########################################################################

import random

def generate2DMAP(MAP):



    max_attempts = 10000  # To avoid infinite loops
    attempts = 0

    while attempts < max_attempts:
        attempts += 1

        # Randomly choose map size between 6x6 and 11x11
        #rows = random.randint(6, 11)
        #cols = random.randint(6, 11)
        rows = len(MAP)
        cols = len(MAP[0])

        # Initialize the map with 1s (empty spaces)
        MAP = [[1 for _ in range(cols)] for _ in range(rows)]

        # Initially set Harry and Voldemort positions to None
        harry_x, harry_y = None, None
        voldemort_x, voldemort_y = None, None

        # Place enemies
        num_enemies = random.randint(4, 12)
        enemies_placed = 0
        while enemies_placed < num_enemies:
            enemy_x = random.randint(0, cols - 1)
            enemy_y = random.randint(0, rows - 1)

            # Avoid placing on Harry or Voldemort positions (will be set later)
            if MAP[enemy_y][enemy_x] != 1:
                continue  # Cell is occupied

            MAP[enemy_y][enemy_x] = 4  # Place an enemy
            enemies_placed += 1

        # Place walls
        num_walls = random.randint(int(rows * cols * 0.1), int(rows * cols * 0.3))  # Between 10% to 30% of the map
        walls_placed = 0
        while walls_placed < num_walls:
            wall_x = random.randint(0, cols - 1)
            wall_y = random.randint(0, rows - 1)

            # Avoid placing on enemies
            if MAP[wall_y][wall_x] != 1:
                continue  # Cell is occupied

            MAP[wall_y][wall_x] = 0  # Place a wall
            walls_placed += 1

        # Now place Harry and Voldemort using replaceVol()
        harry_x, harry_y, voldemort_x, voldemort_y, MAP = replaceVol(MAP, harry_x, harry_y, voldemort_x, voldemort_y)

        # Ensure that the cells adjacent to Harry and Voldemort are not walls or enemies
        def clear_adjacent(x, y):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cols and 0 <= ny < rows:
                        if MAP[ny][nx] in [0, 4] and (nx, ny) not in [(harry_x, harry_y), (voldemort_x, voldemort_y)]:
                            MAP[ny][nx] = 1  # Clear cell

        clear_adjacent(harry_x, harry_y)
        clear_adjacent(voldemort_x, voldemort_y)

        # Use findPath() to check if there is a valid path
        if findPath(MAP, harry_x, harry_y, voldemort_x, voldemort_y):
            print(f"Map generated successfully after {attempts} attempts.")
            #printMAP(MAP)
            return MAP
        else:
            continue  # Generate a new map

    print(f"Failed to generate a valid map after {max_attempts} attempts.")
    return None


#########################################################################
#########################################################################


def destroy_voldemort():
    global nbr_of_actions
    if is_on_target() is True:
        print("YOU WON")
        print("nbr of actions is : ", nbr_of_actions)
        exit()
    else:
        print("You are not on Voldemort")


def get_direction():
    #if DIRECTION == NORTH:
    #	print("NORTH")
    #elif DIRECTION == SOUTH:
    #	print("SOUTH")
    #elif DIRECTION == WEST:
    #	print("WEST")
    #elif DIRECTION == EAST:
    #	print("EAST")
    return DIRECTION

def get_x():
    global harry_x
    return harry_x

def get_y():
    global harry_y
    return harry_y

def get_target_x():
    global voldemort_x
    return voldemort_x

def get_target_y():
    global voldemort_y
    return voldemort_y


# AFFICHAGE

# fonction pour afficher harry avec ça flèche 
def draw_harry_with_arrow(x, y, direction):
    pygame.draw.rect(screen, colors[2], (x * blockWidth, y * blockHeight, blockWidth, blockHeight)) # harry

    # centre de la case
    center_x = x * blockWidth + blockWidth // 2
    center_y = y * blockHeight + blockHeight // 2
    
    arrow_size = 20
    if direction == NORTH:
        # Flèche vers le NORD
        arrow_points = [
                (center_x, center_y - arrow_size),  # Pointe de la flèche (haut)
            (center_x - 10, center_y + 10),     # Coin gauche de la base
            (center_x + 10, center_y + 10)      # Coin droit de la base
        ]
    elif direction == EAST:
        # Flèche vers l'EST
        arrow_points = [
                (center_x + arrow_size, center_y),  # Pointe de la flèche (droite)
            (center_x - 10, center_y - 10),     # Coin haut de la base
            (center_x - 10, center_y + 10)      # Coin bas de la base
        ]
    elif direction == SOUTH:
        # Flèche vers le SUD
        arrow_points = [
                (center_x, center_y + arrow_size),  # Pointe de la flèche (bas)
            (center_x - 10, center_y - 10),     # Coin gauche de la base
            (center_x + 10, center_y - 10)      # Coin droit de la base
        ]
    elif direction == WEST:
        # Flèche vers l'OUEST
        arrow_points = [
                (center_x - arrow_size, center_y),  # Pointe de la flèche (gauche)
            (center_x + 10, center_y - 10),     # Coin haut de la base
            (center_x + 10, center_y + 10)      # Coin bas de la base
        ]
    
    # Dessiner la flèche en bleu foncé
    pygame.draw.polygon(screen, (0, 0, 139), arrow_points)


# fonction qui crée une MAP
def createMAP():
    # on crée la MAP 
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            element = MAP[row][col]
            
            if element == 2:
                draw_harry_with_arrow(col, row, DIRECTION)
            else:
                color = colors[element]
                pygame.draw.rect(screen, color, (col * blockWidth, row * blockHeight, blockWidth, blockHeight))

    # dessiner les lignes de grille
    for x in range(0, window_width, blockWidth):# axe x 
        pygame.draw.line(screen, colors[5], (x, 0), (x, window_height), 1)
    for y in range(0, window_height, blockHeight): # axe y 
        pygame.draw.line(screen, colors[5], (0, y), (window_width, y), 1)


#######################################################################################################
#######################################################################################################
# !!!!! CEST ICI EN DESSOUS QUE TU DOIS METTRE TON CODE :) 
#######################################################################################################
#######################################################################################################
"""""
LEXIQUE :
dans ce programme il y à un certain nombre de fonctions qui te permet de faire un certain nombre de choses, en voici la liste et ce que elle fonts

1 ) move() :: fait avancer Harry dans la direction vers la quel il regarde , il peut regarder vers NORTH, SOUTH, WEST, EAST
2 ) turn_left() :: fait tourner Harry de 90 degré vers la GAUCHE, si il regarde vers le NORTH et que tu utilise cette ofnction il regardera vers le WEST
3 ) turn_right() :: fait tourner Harry de 90 degré vers la DROITE, si il regarde vers le NORTH et que tu utilise cette ofnction il regardera vers le EAST

4 ) can move() :: Revoi False si Harry se trouve en face d'un mur et renvoi True en face de toute autre chose, ATTENTION : ne détecte pas les monstre
5 ) is_in_front_of_enemy() :: Renvoi True quand Harry est en face d'un monstre et False quand il est face à toute autre chose
6 ) is_on_target() :: Renvoi True quand Harry est sur la meme case que Voldemort
7 ) destroy_voldemort() :: Détruit Voldemort si cette fonction est appellé quand Harry est sur la meme case que lui, t'offrant aisni la victoire
8 ) get_direction() :: renvoi la direction courante de harry NORTH, SOUTH, WEST, EAST
9 ) get_x() :: Renvoi la coordonnée X de Harry
10 ) get_y() :: Renvoi la coordonnée Y de Harry
11 ) get_target_x() :: Renvoi la coordonnée X de Voldemort
12 ) get_target_y() :: Renvoi la coorodnnées Y de Voldemort

BOUSSOLE :

#   N
#  W E
# 	S 

"""""
# ***************************************************************
# tu dois mettre ton code dans cette fonction en suivant l'indentation python ,
# exemple : https://www.docstring.fr/glossaire/indentation/#:~:text=Il%20est%20recommand%C3%A9%20avec%20Python,%7D%20)%20pour%20sp%C3%A9cifier%20ces%20blocs.

def playerCode():
    global MAP 

    turn_right()
    move()
    move()
    turn_right()
    turn_right()




#######################################################################################################
#######################################################################################################

# Fonction pour lire ou écrire la carte depuis ou dans un fichier
def go_get_map(MAP, filename="MAP.txt"):
    # Vérifier si le fichier existe
    if os.path.exists(filename):
        # Le fichier existe, on le lit
        with open(filename, 'r') as file:
            content = file.readlines()
            if content:  # Si le fichier n'est pas vide
                new_map = []
                for line in content:
                    row = list(map(int, line.strip().split()))
                    new_map.append(row)
                return new_map
            else:
                # Si le fichier est vide, écrire la carte actuelle dedans
                with open(filename, 'w') as file_write:
                    file_write.write(printMAP(MAP))
                print(f"Fichier {filename} était vide, carte actuelle écrite dans le fichier.")
                return MAP
    else:
        # Si le fichier n'existe pas, le créer et y écrire la carte actuelle
        with open(filename, 'w') as file:
            file.write(printMAP(MAP))
        print(f"Fichier {filename} créé avec la carte actuelle.")
        return MAP


pygame.init()



def Principal():
    global can_move_val, nbr_of_actions, MAP, harry_y, harry_x, voldemort_x, voldemort_y

    # Generate a new random map
    #gen_map = generate2DMAP(MAP)
    #
    ## If no valid map was generated, exit
    #if gen_map is None:
    #    print("Failed to generate a valid map.")
    #    return
#
    ## Update the global MAP with the newly generated map
    #MAP = gen_map
    #
    ## Print the newly generated map (optional, for debugging)
    #print("Generated Map:")
    #print(printMAP(MAP))
    
    # ici on vas tester la fonction de création de map 

    running = True  # Le jeu continue tant que cette variable est vraie
    try:
        while running:
            
            for event in pygame.event.get():
                # Gérer les événements
                if event.type == pygame.QUIT:
                    running = False

            # Dessiner la carte
            createMAP()

            # Vérifier si le délai est écoulé
            if can_move_val == True and nbr_of_actions <= 300:
                #pause_time(3000)
                playerCode()
            elif can_move_val == False or nbr_of_actions > 300:
                print("can move is : ", can_move_val , " nbr of cations is : ", nbr_of_actions)
                #break

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Limiter la vitesse de la boucle principale à 60 FPS
            clock.tick(60)
            
    except KeyboardInterrupt:
        print("Arret du jeu")  # En cas de ctrl + C

    pygame.quit()
Principal()
