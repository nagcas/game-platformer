import pgzrun
import random
import config
from levels import level_1, level_2
from dino import animate_dino

TITLE = 'Dino Adventure'
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

# avvia musica di sottofondo
music.play('bg_music')
music.set_volume(0.2)

# menu principale
start_btn = Actor('button_start', (WIDTH // 2, 300))
music_btn = Actor('button_music', (WIDTH // 2, 438))
sound_btn = Actor('button_sound', (WIDTH // 2, 576))

game_state = 'menu'
music_on = True
sound_on = True

current_level = 1
level = level_1

tiles = []
cherries = []
score = 0
total_score = 0
finish = False
flag = None
spiders = []
bees = []

tile_map = {
  '1': 'terrain_1',
  '2': 'terrain_2',
  '3': 'terrain_3',
  '4': 'terrain_4',
  '5': 'terrain_5',
  '6': 'terrain_6',
  '7': 'terrain_7',
  '8': 'terrain_8',
  '9': 'terrain_9',
  'a': 'terrain_10',
  'b': 'terrain_11',
  'c': 'terrain_12',
  'd': 'terrain_13',
  'e': 'terrain_14',
  'f': 'terrain_15',
  'g': 'terrain_16',
  'h': 'water_17',
  'i': 'water_18',
  'B': 'bush1',
  'C': 'cactus1',
  'D': 'bush_orange1',
  'E': 'bush_orange3',
  'F': 'fence',
  'G': 'tree',
  'H': 'tree_dead',
  'K': 'flag_yellow',
  'T': 'arrow',
  'J': 'spider',
  'M': 'bee',
}

# funzioni principali dino
player_dino = {
  'images': 0,
  'timer': 0,
  'last_direction': 'right',
  'velocity_y': 0,
  'on_ground': False,

  'dead': False,
  'dying': False,
  'death_anim_timer': 0,

  'lives': 3,
  'point': 0,
}

# controllo mouse per selezionare il menu'
def on_mouse_down(pos):
  global game_state, music_on, sound_on

  if game_state == "menu":
    
    if start_btn.collidepoint(pos):
      game_state = "playing"

    elif music_btn.collidepoint(pos):
      music_on = not music_on
      if music_on:
        music.play('bg_music')
      else:
        music.stop()

    elif sound_btn.collidepoint(pos):
      sound_on = not sound_on

def respawn():
  global level, current_level, tiles, cherries, spiders, bees

  current_level = 1
  level = level_1

  build_level()

  dino.pos = (32, 640)

  player_dino['velocity_y'] = 0
  player_dino['on_ground'] = False
  player_dino['dying'] = False
  player_dino['death_anim_timer'] = 0

def build_level():
  global tiles, cherries, flag, spiders, bees

  tiles = []
  cherries = []
  spiders = []
  bees = []
  flag = None

  for row_i, row in enumerate(level):
    for col_i, col in enumerate(row):

      x = col_i * config.TILE_SIZE + config.TILE_SIZE // 2
      y = row_i * config.TILE_SIZE + config.TILE_SIZE // 2

      if col == 'K':
        flag = Actor('flag_yellow')
        flag.pos = (x, y)

      elif col == 'P':
        cherry = Actor('cherry')
        cherry.pos = (x, y)
        cherries.append(cherry)

      elif col == 'J':
        spider = Actor('spider')
        spider.pos = (x, y)

        spider.start_x = x
        spider.direction = -1
        spider.range = 350
        spider.speed = 1.5
        spider.step = 0
        spider.anim_timer = 0
        spider.anim_index = 0

        spiders.append(spider)
      
      elif col == 'M':
        bee = Actor('bee')
        bee.pos = (x, y)
        bee.start_x = x
        bee.direction = -1
        bee.range = 1024
        bee.speed = 1.5
        bee.step = 0
        bee.anim_timer = 0
        bee.anim_index = 0
      
        bees.append(bee)

      elif col in tile_map:
        tile = Actor(tile_map[col])
        tile.pos = (x, y)
        tiles.append(tile)

build_level()

# sprite dino
dino = Actor('idle1')
dino.pos = 32, 640
run_dino_dx = ['run1','run2','run3','run4','run5','run6','run7','run8']
run_dino_sx = ['run9','run10','run11','run12','run13','run14','run15','run16']

# sprite spider
run_spider = ['spider','spider_walk1','spider_walk2']

# sprite bee
run_bee_dx = ['bee3', 'bee_fly4']
run_bee_sx = ['bee', 'bee_fly']


def get_tile_at(px, py):
  col = int(px // config.TILE_SIZE)
  row = int(py // config.TILE_SIZE)

  if 0 <= row < len(level) and 0 <= col < len(level[0]):
    return level[row][col]
  return None


def update():
  global level, current_level, score, total_score, finish
  
  if game_state != 'playing':
    return

  if finish:
    return
  
  if player_dino['dead']:
    return

  # se sta morendo blocca tutto il gioco
  if player_dino.get('dying', False):
    player_dino['death_anim_timer'] += 1

    if player_dino['death_anim_timer'] > 60:
      if player_dino['lives'] <= 0:
        player_dino['dead'] = True
        sounds.oops.stop()
      else:
        respawn()

      player_dino['dying'] = False

    return

  animate_dino(dino, keyboard, run_dino_dx, run_dino_sx, player_dino, get_tile_at, level, respawn, sounds, sound_on)

  # SPIDER MOVEMENT
  for spider in spiders:
    spider.x += spider.direction * spider.speed
    spider.step += spider.speed

    if spider.step >= spider.range:
      spider.direction *= -1
      spider.step = 0

    spider.anim_timer += 1
    if spider.anim_timer > 10:
      spider.image = run_spider[spider.anim_index]
      spider.anim_index = (spider.anim_index + 1) % len(run_spider)
      spider.anim_timer = 0
      
  # bee movement
  for bee in bees:
    bee.x += bee.direction * bee.speed
    
    # animazione
    bee.anim_timer += 1
    if bee.anim_timer > 10:
      if bee.direction == 1:
        bee.image = run_bee_dx[bee.anim_index]
      else:
        bee.image = run_bee_sx[bee.anim_index]
        
      bee.anim_index = (bee.anim_index + 1) % len(run_bee_sx)
      bee.anim_timer = 0

    # quando esce completamente dallo schermo
    if bee.x > WIDTH + 60 or bee.x < -60:

      # nuova altezza random
      bee.y = random.randint(100, HEIGHT - 100)

      # lato di spawn casuale
      if random.choice([True, False]):
        bee.x = -60
        bee.direction = 1
      else:
        bee.x = WIDTH + 60
        bee.direction = -1

      # velocità random
      bee.speed = random.uniform(1, 3)

  # cherry collisione
  for cherry in cherries[:]:
    if dino.colliderect(cherry):
      cherries.remove(cherry)
      if sound_on:
        sounds.coin.play()
      score += 1

  # flag collisione
  if flag and dino.colliderect(flag):
    total_score = score
    if sound_on:
      sounds.win.play()
    finish = True

  # spider collisione
  for spider in spiders:
    if dino.colliderect(spider) and not player_dino['dying'] and not player_dino['dead']:
      player_dino['lives'] -= 1
      player_dino['dying'] = True
      player_dino['death_anim_timer'] = 0
      dino.image = 'dead'
      if sound_on:
        sounds.oops.play()
      
      break
  
  # bee collisione
  for bee in bees:
    if dino.colliderect(bee) and not player_dino['dying'] and not player_dino['dead']:
      player_dino['lives'] -= 1
      player_dino['dying'] = True
      player_dino['death_anim_timer'] = 0
      dino.image = 'dead'
      if sound_on:
        sounds.oops.play()
      
      break
      
  # livello
  if dino.x > WIDTH:
    current_level = 2 if current_level == 1 else current_level
    level = level_2 if current_level == 2 else level_1
    build_level()
    dino.x = 10

  if dino.x < 0:
    current_level = 1 if current_level == 2 else current_level
    level = level_1 if current_level == 1 else level_2
    build_level()
    dino.x = WIDTH - 10

def draw():
  screen.clear()
  
  if game_state == 'menu':
    bg = 'background_color_forest'
    screen.blit(bg, (0, 0))

    screen.draw.text('DINO ADVENTURE', center = (WIDTH // 2, 150), fontsize = 80, color = (255, 255, 255))

    start_btn.draw()
    music_btn.draw()
    sound_btn.draw()
    
    screen.draw.text(
      'START GAME',
      center=(WIDTH//2, 292),
      fontsize=30,
      color=(0,0,0)
    )

    screen.draw.text(
      f"Music: {'ON' if music_on else 'OFF'}",
      center=(WIDTH//2, 428),
      fontsize=30,
      color=(0,0,0)
    )

    screen.draw.text(
      f"Sound: {'ON' if sound_on else 'OFF'}",
      center=(WIDTH//2, 566),
      fontsize=30,
      color=(0,0,0)
    )

    return
  
  else:
    bg = 'background_color_forest' if current_level == 1 else 'background_color_fall'
    screen.blit(bg, (0, 0))

    for tile in tiles:
      tile.draw()

    if flag:
      flag.draw()

    if not player_dino['dead'] and not finish:
      dino.draw()
      
      for spider in spiders:
        spider.draw()
      
      for bee in bees:
        bee.draw()
        
      for cherry in cherries:
        cherry.draw()
      
      screen.draw.text(f"Lives: {player_dino['lives']}", (20, 20), fontsize = 30, color = (0, 0, 0))
      screen.draw.text(f"Cherries: {score}", (WIDTH//2, 20), fontsize = 30, color = (0, 0, 0))
      screen.draw.text(f"Level: {current_level}", (900, 20), fontsize = 30, color = (0, 0, 0))
      
    if player_dino['dead']:
      screen.draw.text(
        f"GAME OVER\nTotal Score: {score}",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize = 80,
        color = (0, 0, 0)
      )
    elif finish:
      screen.draw.text(
        f"WINNER\nTotal Score: {total_score}",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize = 80,
        color = (0, 0, 0)
      )

pgzrun.go()