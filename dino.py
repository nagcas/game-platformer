import config

solid_tiles = ['1', '2', '4', '6', 'b', 'd', 'e', 'f']
deadly_tiles = ['h', 'i']

# animazione player dinosauro
def animate_dino(dino, keyboard, run_dino_dx, run_dino_sx, player_dino, get_tile_at, level, respawn, sounds, sound_on):
  
  if player_dino.get('dying', False):
    return
  
  if player_dino.get('dead', False): 
    return

  moving = False
  dx = 0
  direction = None
  OFFSET_Y = 4

  # controlli tastiera
  if keyboard.right:
    dx = config.player_speed
    moving = True
    direction = 'right'
  elif keyboard.left:
    dx = -config.player_speed
    moving = True
    direction = 'left'
  
  # controllo salto
  if keyboard.up and player_dino['on_ground']:
    if sound_on:
      sounds.sfx_jump_high.play()
    player_dino['velocity_y'] = config.jump_strength
    player_dino['on_ground'] = False

  # controllo gravità
  player_dino['velocity_y'] += config.GRAVITY
  if player_dino['velocity_y'] > config.max_fall_speed:
    player_dino['velocity_y'] = config.max_fall_speed

  # movimento verticale
  dino.y += player_dino['velocity_y'] * 0.6

  # collisione con tile solo sotto
  foot_y = dino.y + dino.height // 2
  left_x = dino.x - dino.width // 3
  right_x = dino.x + dino.width // 3

  tile_left = get_tile_at(left_x, foot_y)
  tile_right = get_tile_at(right_x, foot_y)
  
  body_y = dino.y
  tile_center = get_tile_at(dino.x, body_y)

  if tile_center in deadly_tiles:
    player_dino['velocity_y'] *= 0.6  # affonda

    player_dino['death_timer'] += 1

    # dopo un po' muore
    if player_dino['death_timer'] > 20:
      sounds.oops.play()
      player_dino['lives'] -= 1

      if player_dino['lives'] <= 0:
        player_dino['dead'] = True
      else:
        respawn()

      return
  else:
    # reset se esce dall'acqua
    player_dino['death_timer'] = 0

  if (tile_left in solid_tiles or tile_right in solid_tiles) and player_dino['velocity_y'] >= 0:
    # allinea il player sopra il tile
    row = int(foot_y // config.TILE_SIZE)
    dino.y = row * config.TILE_SIZE - dino.height // 2 + OFFSET_Y

    player_dino['velocity_y'] = 0
    player_dino['on_ground'] = True
  else:
    player_dino['on_ground'] = False
    if dino.y > config.HEIGHT:
      player_dino['dead'] = True
      
      return
  
  # collisione laterale
  left_tile = get_tile_at(dino.x - dino.width // 2, dino.y)
  right_tile = get_tile_at(dino.x + dino.width // 2, dino.y)

  if dx > 0 and right_tile in solid_tiles:
    dx = 0  # blocca destra

  if dx < 0 and left_tile in solid_tiles:
    dx = 0  # blocca sinistra
    
  dino.x += dx
  
  # collisione con terreno
  ground_y = (len(level) - 1) * config.TILE_SIZE
  if dino.y >= ground_y:
    dino.y = ground_y
    player_dino['velocity_y'] = 0
    player_dino['on_ground'] = True
  
  # salva direzione
  if direction:
    player_dino['last_direction'] = direction
  
  # movimento dinosauro
  if moving:
    player_dino['timer'] += 1
    if player_dino['timer'] > 3:
      if player_dino['last_direction'] == 'right':
        dino.image = run_dino_dx[player_dino['images']]
        player_dino['images'] = (player_dino['images'] + 1) % len(run_dino_dx)

      elif player_dino['last_direction'] == 'left':
        dino.image = run_dino_sx[player_dino['images']]
        player_dino['images'] = (player_dino['images'] + 1) % len(run_dino_sx)

      player_dino['timer'] = 0
  else:
    if player_dino['last_direction'] == 'right':
      dino.image = 'idle1'
    else:
      dino.image = 'idle2'

    player_dino['images'] = 0
    player_dino['timer'] = 0