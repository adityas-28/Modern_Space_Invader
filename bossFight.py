def main_boss_fight():   
    import pygame
    from pygame import mixer

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load(r'resources\images\spaceship.png')
    pygame.display.set_icon(icon)

    background = pygame.image.load(r'resources\images\boss_bg.png')
    background = pygame.transform.scale(background, (800, 600))

    mixer.music.load(r'resources\sounds\strangerThingdBGMTrim.mp3')
    mixer.music.set_volume(0.3)  
    mixer.music.play(-1) 

    boss_image = pygame.image.load(r'resources\images\ufo.png')
    boss_image = pygame.transform.scale(boss_image, (85, 85))
    boss_image_angry = pygame.image.load(r'resources\images\ufoAngry.png')
    boss_image_angry = pygame.transform.scale(boss_image_angry, (85, 85))
    boss_x = 358
    boss_y = 75

    def update_boss_health(x, y, hits):
        pygame.draw.rect(screen, (194, 194, 194), pygame.Rect(x, y, 100, 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 100 - (10 * hits), 10))

    def show_boss(x, y):
        if boss_phase == "vulnerable":
            screen.blit(boss_image, (x, y)) 
        else:
            screen.blit(boss_image_angry, (x, y)) 

    playerImage = pygame.image.load(r'resources\images\spaceship (1).png')
    playerImage = pygame.transform.scale(playerImage, (55, 55))
    playerX = 375
    playerY = 450
    playerX_change = 0
    playerY_change = 0

    bulletImage = pygame.image.load(r'resources\images\bullet.png');
    bulletImage = pygame.transform.scale(bulletImage, (17, 17))
    bullet_state = False
    bulletX = 0
    bulletY = 0

    enemyBulletImage = pygame.image.load(r'resources\images\bossLaser.png');
    enemyBulletImage = pygame.transform.scale(enemyBulletImage, (15, 15))
    enemy_bullets = []

    player_bullets = []

    def toggle_mute():
        global music_enabled
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            music_enabled = False
        else:
            pygame.mixer.music.unpause()
            music_enabled = True


    def boss_fire_bullets(x, y, vx=0, vy=5):
        enemy_bullets.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})

    def player_fire_bullets(x, y):
        player_bullets.append({'x': x, 'y': y})

    def player_collision(enemyBullet, playerX, playerY):
        bullet_rect = pygame.Rect(enemyBullet['x'], enemyBullet['y'], enemyBulletImage.get_width(), enemyBulletImage.get_height())
        player_rect = pygame.Rect(playerX, playerY, playerImage.get_width(), playerImage.get_height())
        return bullet_rect.colliderect(player_rect)

    def boss_collision(playerBullet, bossX, bossY):
        bullet_rect = pygame.Rect(playerBullet['x'], playerBullet['y'], bulletImage.get_width(), bulletImage.get_height())
        boss_rect = pygame.Rect(bossX, bossY, boss_image.get_width(), boss_image.get_height())
        return bullet_rect.colliderect(boss_rect)

    def show_player(x, y):
        screen.blit(playerImage, (x, y))

    def update_player_health(x, y, hits):
        pygame.draw.rect(screen, (194, 194, 194), pygame.Rect(x, y, 90, 10))
        pygame.draw.rect(screen, (48, 194, 56), pygame.Rect(x, y, 100 - (20 * hits), 10))

    def render_wrapped_text(text, font, color, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)  # Add the last line
        return lines


    start_font = pygame.font.Font(r'resources\fonts\typewriter.ttf', 28)


    def main_message():
        timer = pygame.time.Clock()
        
        messages = [
        "I’ve crushed every one of Zarnax’s minions. Only he remains.",
        "I’ve locked onto the source — a rogue planet, dead and drifting on the edge of the system. Dark. Dead. Orbiting nothing. That’s where he waits. This is my final descent. No retreat. No surrender.",
        "Zarnax — I’m coming for you."
        ]
        current_message = 0
        counter = 0
        speed = 1
        done = False
        box_width, box_height = 800, 200
        box_x = (800 - box_width) // 2 
        box_y = (600 - box_height) // 2  

        while True:
            screen.blit(background, (0, 0))
            timer.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and done:
                        if current_message < len(messages) - 1:
                            current_message += 1
                            counter = 0
                            done = False
                        else:
                            return  # Done with all messages

            dialogue_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            dialogue_box.fill((0, 0, 0, 180))
            screen.blit(dialogue_box, (box_x, box_y))

            if counter < speed * len(messages[current_message]):
                counter += 1
            else:
                done = True

            text_to_display = messages[current_message][0:counter // speed]
            wrapped_lines = render_wrapped_text(text_to_display, start_font, (255, 255, 255), box_width - 40)

            for i, line in enumerate(wrapped_lines):
                snip = start_font.render(line, True, (255, 255, 255))
                line_y = box_y + 20 + i * 30
                screen.blit(snip, (box_x + 20, line_y))

            pygame.display.update()

    running = True
    show_intro = True
    boss_hits = 0

    player_blink = False
    player_blink_start_time = 0
    player_invincible_duration = 1000  # milliseconds
    player_hits = 0
    playerSpeed = 1.25
    bossSpeed = 0.1
    boss_x_dir = 1 # right
    boss_y_dir = 1 # down
    BULLET_SPEED = 3
    last_shot_time = None
    player_last_shot_time = None
    boss_bullet_delay = 1000
    player_bullet_delay = 700
    boss_phase = "vulnerable"  # "burst" or "vulnerable"
    boss_burst_shots_fired = 0
    boss_last_shot_time = 0
    boss_burst_count = 100
    boss_burst_delay = 7  # time between each burst shot in milliseconds
    boss_vulnerable_start = 0
    boss_vulnerable_hit = False
    boss_hit_time = 0
    pt = None
    maxVulnerableDuration = 5000
    sfx_enabled = True
    isPaused = False
    pause_start_time = None
    pause_time = 0

    while running:
        if show_intro:
            main_message()
            show_intro = False  

        if isPaused:
            screen.blit(background, (0, 0))
            if pause_start_time is None:
                pause_start_time = pygame.time.get_ticks()
            # pause_time += pygame.time.get_ticks() - pause_start_time
            # pause_start_time = pygame.time.get_ticks()
            pause_font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 50)
            pause_text = pause_font.render("Paused", True, (133, 255, 253))
            pause_font_inner = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 25)
            pause_text_inner = pause_font_inner.render("Press P to Unpause", True, (255, 255, 255))
            
            screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
            screen.blit(pause_text_inner, (screen.get_width() // 2 - pause_text_inner.get_width() // 2, screen.get_height() // 2 + pause_text.get_height() // 2 + 15))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: 
                        pausesound = mixer.Sound(r'resources/sounds/pause.wav').play()
                        isPaused = not isPaused
                        if pause_start_time is not None:
                            pause_time += pygame.time.get_ticks() - pause_start_time
                        pause_start_time = None

                    elif event.key == pygame.K_m:
                        toggle_mute()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change -= playerSpeed
                if event.key == pygame.K_RIGHT:
                    playerX_change += playerSpeed
                if event.key == pygame.K_UP:
                    playerY_change -= playerSpeed
                if event.key == pygame.K_DOWN:
                    playerY_change += playerSpeed
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_p: 
                    isPaused = not isPaused
                    pausesound = mixer.Sound(r'resources/sounds/pause.wav').play()
                    # toggle_mute()
                if event.key == pygame.K_s:
                    sfx_enabled = not sfx_enabled
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    if sfx_enabled:
                        mixer.Sound(r'resources\sounds\laser2.wav').play()
                    if curr_time - player_last_shot_time > player_bullet_delay:
                        player_fire_bullets(playerX + 20, playerY)
                        player_last_shot_time = curr_time

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        screen.blit(background, (0, 0))

        boss_x += boss_x_dir
        boss_y += boss_y_dir

        if boss_x >= 700:
            boss_x_dir = -bossSpeed
        if boss_x <= 20:
            boss_x_dir = bossSpeed
        if boss_y >= 250:
            boss_y_dir = -bossSpeed
        if boss_y <= 25:
            boss_y_dir = bossSpeed

        show_boss(boss_x, boss_y)
        update_boss_health(boss_x - 10, boss_y - 25, boss_hits)

        playerX += playerX_change
        playerY += playerY_change
        if playerX < 25:
            playerX = 25
        if playerX >= 720:
            playerX = 720
        if playerY < 350:
            playerY = 350
        if playerY >= 525:
            playerY = 525
        # Handle blinking
        if player_blink:
            if (curr_time - player_blink_start_time) < player_invincible_duration:
                # Blink: Show player every few frames
                if (curr_time // 100) % 2 == 0:
                    show_player(playerX, playerY)  # visible
                # else: invisible this frame
            else:
                player_blink = False  # End blink
                show_player(playerX, playerY)
        else:
            show_player(playerX, playerY)

        update_player_health(playerX - 17, playerY + 60, player_hits)

        curr_time = pygame.time.get_ticks()

        if pt is None:
            pt = pygame.time.get_ticks()

        if boss_phase == "vulnerable" and not boss_vulnerable_hit:
            if curr_time - pt > maxVulnerableDuration:
                boss_phase = "burst"
                boss_last_shot_time = curr_time

        
        if player_last_shot_time is None:
            player_last_shot_time = pygame.time.get_ticks()

        if last_shot_time is None:
            last_shot_time = pygame.time.get_ticks()

        # Boss attack pattern logic
        if boss_phase == "burst":
            if boss_burst_shots_fired < boss_burst_count:
                if boss_burst_shots_fired == 0 and sfx_enabled:
                    mixer.Sound(r'resources\sounds\bossLaser.mp3').play()
                    

                if curr_time - boss_last_shot_time > boss_burst_delay:
                    # Fire 3-direction burst
                    boss_fire_bullets(boss_x + 32, boss_y + 70, vx=0, vy=2)
                    boss_fire_bullets(boss_x + 24, boss_y + 70, vx=-1, vy=2)
                    boss_fire_bullets(boss_x + 40, boss_y + 70, vx=1, vy=2)
                    
                    boss_burst_shots_fired += 1
                    boss_last_shot_time = curr_time
            else:
                boss_phase = "vulnerable"
                boss_vulnerable_start = curr_time
                boss_burst_shots_fired = 0
                pt = curr_time  # <-- Set PT correctly when entering vulnerable state
                boss_vulnerable_hit = False


        elif boss_phase == "vulnerable":
        # Wait for player to hit during this phase
            if boss_vulnerable_hit:
                if curr_time - boss_hit_time > 1000:  # 1 sec delay after hit
                    boss_phase = "burst"
                    boss_last_shot_time = curr_time
                    boss_vulnerable_hit = False  # Reset for next time


        for bullet in enemy_bullets[:]:
            bullet['x'] += bullet['vx']
            bullet['y'] += bullet['vy']

            screen.blit(enemyBulletImage, (bullet['x'], bullet['y']))

            if player_collision(bullet, playerX - 20, playerY + 10):
                if not player_blink:
                    if sfx_enabled:
                        mixer.Sound(r'resources\sounds\explosionWarning.mp3').play()
                    player_hits += 1
                    player_blink = True
                    player_blink_start_time = curr_time
                    if player_hits == 5:
                        return False
                enemy_bullets.remove(bullet)  # Remove bullet whether or not it caused damage

            if bullet['y'] > 600:
                enemy_bullets.remove(bullet)


        for bullet in player_bullets[:]:
            bullet['y'] -= BULLET_SPEED

            screen.blit(bulletImage, (bullet['x'], bullet['y']))

            if boss_collision(bullet, boss_x, boss_y):
                if sfx_enabled:
                    mixer.Sound(r'resources\sounds\explosion.wav').play()
                player_bullets.remove(bullet)
                if boss_phase == "vulnerable" and not boss_vulnerable_hit:
                    boss_hits += 1
                    boss_vulnerable_hit = True
                    boss_hit_time = curr_time  # Start 1-second timer after hit

                if boss_hits == 10:
                    return True
            if bullet['y'] <= 0:
                player_bullets.remove(bullet)

        pygame.display.update()