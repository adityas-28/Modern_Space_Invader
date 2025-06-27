def main_boss_fight():  
    import pygame
    from pygame import mixer
    import time 
    import math
    import settings

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
    boss_x = 50
    boss_y = 50

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

    bulletImage = pygame.image.load(r'resources\images\bulletLaser.png');
    bulletImage = pygame.transform.scale(bulletImage, (17, 17))

    enemyBulletImage = pygame.image.load(r'resources\images\bossLaser.png');
    enemyBulletImage = pygame.transform.scale(enemyBulletImage, (15, 15))
    enemy_bullets = []

    player_bullets = []

    def toggle_mute():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def boss_fire_bullets(x, y, vx=0, vy=5):
        enemy_bullets.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})

    def player_fire_bullets(x, y, angle):
        speed = 12
        radians = math.radians(angle)
        vx = math.cos(radians) * speed
        vy = -math.sin(radians) * speed  # negative because y-axis is downward

        player_bullets.append({
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'angle': angle
        })


    def player_collision(enemyBullet, playerX, playerY):
        bullet_rect = pygame.Rect(enemyBullet['x'], enemyBullet['y'], enemyBulletImage.get_width(), enemyBulletImage.get_height())
        player_rect = pygame.Rect(playerX, playerY, playerImage.get_width(), playerImage.get_height())
        return bullet_rect.colliderect(player_rect)

    def boss_collision(playerBullet, bossX, bossY):
        bullet_rect = pygame.Rect(playerBullet['x'], playerBullet['y'], bulletImage.get_width(), bulletImage.get_height())
        boss_rect = pygame.Rect(bossX, bossY, boss_image.get_width(), boss_image.get_height())
        return bullet_rect.colliderect(boss_rect)

    def show_rotated_player(player_x, player_y, boss_x, boss_y, player_img):
        dx = boss_x - player_x
        dy = boss_y - player_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        rotated_img = pygame.transform.rotate(player_img, angle)
        rotated_rect = rotated_img.get_rect(center=(player_x + player_img.get_width() // 2,
                                                    player_y + player_img.get_height() // 2))
        screen.blit(rotated_img, rotated_rect.topleft)


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

    def main_message3(victory=True):
        end_font = pygame.font.Font(r'resources/fonts/typewriter.ttf', 28)
        enter_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 20)
        enter_message = enter_font.render("Press Enter to continue", True, (255, 255, 255))
        timer = pygame.time.Clock()

        # Load images
        playerImage = pygame.image.load(r'resources\images\spaceship (1).png')
        playerImage = pygame.transform.scale(playerImage, (150, 150))

        bossImage = pygame.image.load(r'resources\images\ufoAngry.png')
        bossImage = pygame.transform.scale(bossImage, (150, 150))

        # Messages
        if victory:
            messages = [
                "Zarnax is no more. The rogue planet crumbles without his power. The galaxy is safe... for now. But peace never lasts forever."
            ]
            image_to_show = playerImage
        else:
            messages = [
                "Your ship lies in ruins. Zarnax watches as silence returns to space. You fought bravely — but it wasn’t enough. This galaxy now belongs to me. HaHaHa !"
            ]
            image_to_show = bossImage

        current_message = 0
        counter = 0
        speed = 2
        done = False
        box_width, box_height = 800, 200
        box_x = (800 - box_width) // 2
        box_y = (600 - box_height) // 2 + 50

        isPaused = False
        pause_start_time = None
        pause_time = 0
        first_time = True

        while True:
            if isPaused:
                screen.blit(background, (0, 0))
                if pause_start_time is None:
                    pause_start_time = pygame.time.get_ticks()
                pause_font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 50)
                pause_text = pause_font.render("Paused", True, (133, 255, 253))
                pause_text_inner = enter_font.render("Press P to Unpause", True, (255, 255, 255))

                screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
                screen.blit(pause_text_inner, (screen.get_width() // 2 - pause_text_inner.get_width() // 2, screen.get_height() // 2 + pause_text.get_height() // 2 + 15))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p: 
                            mixer.Sound(r'resources/sounds/pause.wav').play()
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

            screen.blit(background, (0, 0))
            screen.blit(image_to_show, (screen.get_width() // 2 - image_to_show.get_width() // 2, 80))
            screen.blit(enter_message, (screen.get_width() // 2 - enter_message.get_width() // 2, 500))
            if first_time:
                time.sleep(1)
                first_time = False

            timer.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()
                    if event.key == pygame.K_p:
                        mixer.Sound(r'resources/sounds/pause.wav').play()
                        isPaused = not isPaused
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_RETURN:
                        if not done:
                            counter = speed * len(messages[current_message])
                            done = True
                        else:
                            if current_message < len(messages) - 1:
                                current_message += 1
                                counter = 0
                                done = False
                            else:
                                return


            dialogue_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            dialogue_box.fill((0, 0, 0, 180))
            screen.blit(dialogue_box, (box_x, box_y))

            if counter < speed * len(messages[current_message]):
                counter += 1
            else:
                done = True

            text_to_display = messages[current_message][0:counter // speed]
            wrapped_lines = render_wrapped_text(text_to_display, end_font, (255, 255, 255), box_width - 40)

            for i, line in enumerate(wrapped_lines):
                snip = end_font.render(line, True, (255, 255, 255))
                line_y = box_y + 20 + i * 30
                screen.blit(snip, (box_x + 20, line_y))

            pygame.display.update()


    def second_message():
        enter_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 20)
        enter_message = enter_font.render("Press Enter to continue", True, (255, 255, 255))
        timer = pygame.time.Clock()

        boss_image = pygame.image.load(r'resources\images\ufo.png')
        boss_image = pygame.transform.scale(boss_image, (150, 150))

        dialogue_font = pygame.font.Font(r'resources\fonts\typewriter.ttf', 28)
        messages = [
    "So... you've made it this far. Impressive — for a mortal. But your journey ends here. You truly believe you can defeat *me*? Foolish. Now, prepare to be annihilated!"
    ]

        current_message = 0
        counter = 0
        speed = 3
        done = False
        box_width, box_height = 800, 200
        box_x = (800 - box_width) // 2 
        box_y = (600 - box_height) // 2 + 50

        isPaused = False
        pause_start_time = None
        pause_time = 0

        while True:
            if isPaused:
                screen.blit(background, (0, 0))
                if pause_start_time is None:
                    pause_start_time = pygame.time.get_ticks()
                pause_font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 50)
                pause_text = pause_font.render("Paused", True, (133, 255, 253))
                pause_text_inner = enter_font.render("Press P to Unpause", True, (255, 255, 255))

                screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
                screen.blit(pause_text_inner, (screen.get_width() // 2 - pause_text_inner.get_width() // 2, screen.get_height() // 2 + pause_text.get_height() // 2 + 15))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p: 
                            mixer.Sound(r'resources/sounds/pause.wav').play()
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

            screen.blit(background, (0, 0))
            screen.blit(boss_image, (screen.get_width() // 2 - boss_image.get_width() // 2, 80))

            screen.blit(enter_message, (screen.get_width() // 2 - enter_message.get_width() // 2, 500))
            timer.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()
                    if event.key == pygame.K_p:
                        isPaused = not isPaused
                        mixer.Sound(r'resources/sounds/pause.wav').play()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_RETURN:
                        if not done:
                            counter = speed * len(messages[current_message])
                            done = True
                        else:
                            if current_message < len(messages) - 1:
                                current_message += 1
                                counter = 0
                                done = False
                            else:
                                return


            dialogue_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            dialogue_box.fill((0, 0, 0, 180))
            screen.blit(dialogue_box, (box_x, box_y))

            if counter < speed * len(messages[current_message]):
                counter += 1
            else:
                done = True

            text_to_display = messages[current_message][0:counter // speed]
            wrapped_lines = render_wrapped_text(text_to_display, dialogue_font, (255, 255, 255), box_width - 40)

            for i, line in enumerate(wrapped_lines):
                snip = dialogue_font.render(line, True, (255, 255, 255))
                line_y = box_y + 20 + i * 30
                screen.blit(snip, (box_x + 20, line_y))

            pygame.display.update()



    def main_message():
        time.sleep(1)
        enter_font = pygame.font.Font(r'resources/fonts/SPACEBOY.TTF', 20)
        enter_message = enter_font.render("Press Enter to continue", True, (255, 255, 255))

        timer = pygame.time.Clock()
        
        messages = [
        "I’ve crushed every one of Zarnax’s minions. Only he remains.",
        "I’ve locked onto the source — a rogue planet, dead and drifting on the edge of the system. That’s where he waits.",
        " This is my final descent. Zarnax — I’m coming for you."
        ]
        current_message = 0
        counter = 0
        speed = 3
        done = False
        box_width, box_height = 800, 200
        box_x = (800 - box_width) // 2 
        box_y = (600 - box_height) // 2  

        isPaused = False
        pause_start_time = None
        pause_time = 0

        while True:
            if isPaused:
                screen.blit(background, (0, 0))
                if pause_start_time is None:
                    pause_start_time = pygame.time.get_ticks()
                pause_font = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 50)
                pause_text = pause_font.render("Paused", True, (133, 255, 253))
                pause_font_inner = pygame.font.Font(r'resources\fonts\SPACEBOY.TTF', 25)
                pause_text_inner = pause_font_inner.render("Press P to Unpause", True, (255, 255, 255))
                
                screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
                screen.blit(pause_text_inner, (screen.get_width() // 2 - pause_text_inner.get_width() // 2, screen.get_height() // 2 + pause_text.get_height() // 2 + 15))

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p: 
                            mixer.Sound(r'resources/sounds/pause.wav').play()
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

            screen.blit(background, (0, 0))
            timer.tick(60)
            screen.blit(enter_message, (screen.get_width() // 2 - enter_message.get_width() // 2, 500))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        toggle_mute()
                    if event.key == pygame.K_p: 
                        isPaused = not isPaused
                        mixer.Sound(r'resources/sounds/pause.wav').play()
                        # toggle_mute()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_RETURN:
                        if not done:
                            counter = speed * len(messages[current_message])
                            done = True
                        else:
                            if current_message < len(messages) - 1:
                                current_message += 1
                                counter = 0
                                done = False
                            else:
                                return

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

    def boss_hits_player(boss_x, boss_y, player_x, player_y, boss_image, player_image):
        boss_rect = pygame.Rect(boss_x, boss_y, boss_image.get_width(), boss_image.get_height())
        player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
        return boss_rect.colliderect(player_rect)


    running = True
    show_intro = True
    boss_hits = 0

    player_blink = False
    player_blink_start_time = 0
    player_invincible_duration = 1000 
    player_hits = 0
    playerSpeed = 7
    bossSpeed = 2
    boss_x_dir = 1 
    boss_y_dir = 1 
    last_shot_time = None
    player_last_shot_time = None
    player_bullet_delay = 700
    boss_phase = "vulnerable"  # "burst" or "vulnerable"
    boss_burst_shots_fired = 0
    boss_last_shot_time = 0
    boss_burst_count = 55
    boss_burst_delay = 7 
    boss_vulnerable_hit = False
    boss_hit_time = 0
    pt = None
    maxVulnerableDuration = 3500
    settings.sfx_enabled = True
    isPaused = False
    pause_start_time = None
    pause_time = 0
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        if show_intro:
            main_message()
            second_message()
            show_intro = False  

        if isPaused:
            screen.blit(background, (0, 0))
            if pause_start_time is None:
                pause_start_time = pygame.time.get_ticks()
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
                        mixer.Sound(r'resources/sounds/pause.wav').play()
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
                    mixer.Sound(r'resources/sounds/pause.wav').play()
                    # toggle_mute()
                if event.key == pygame.K_s:
                    settings.sfx_enabled = not settings.sfx_enabled
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    if settings.sfx_enabled:
                        mixer.Sound(r'resources\sounds\laser2.wav').play()
                    if curr_time - player_last_shot_time > player_bullet_delay:
                        dx = boss_x - playerX
                        dy = boss_y - playerY
                        angle = math.degrees(math.atan2(-dy, dx)) 

                        player_center_x = playerX + playerImage.get_width() // 2
                        player_center_y = playerY + playerImage.get_height() // 2
                        player_fire_bullets(player_center_x, player_center_y, angle)

                        player_last_shot_time = curr_time

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        screen.blit(background, (0, 0))

        boss_x += bossSpeed * boss_x_dir
        boss_y += bossSpeed * boss_y_dir

        if boss_x >= 700:
            boss_x_dir = -1
        if boss_x <= 25:
            boss_x_dir = 1
        if boss_y >= 490:
            boss_y_dir = -1
        if boss_y <= 30:
            boss_y_dir = 1


        show_boss(boss_x, boss_y)
        update_boss_health(boss_x - 10, boss_y - 25, boss_hits)

        playerX += playerX_change
        playerY += playerY_change
        if playerX < 25:
            playerX = 25
        if playerX >= 710:
            playerX = 710
        if playerY <= 15:
            playerY = 15
        if playerY >= 525:
            playerY = 525
        # Handle blinking
        if player_blink:
            if (curr_time - player_blink_start_time) < player_invincible_duration:
                # Blink: Show player every few frames
                if (curr_time // 100) % 2 == 0:
                    show_rotated_player(playerX, playerY, boss_x, boss_y, playerImage)  # visible
                # else: invisible this frame
            else:
                player_blink = False  # End blink
                show_rotated_player(playerX, playerY, boss_x, boss_y, playerImage)
        else:
            show_rotated_player(playerX, playerY, boss_x, boss_y, playerImage)

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
                if boss_burst_shots_fired == 0 and settings.sfx_enabled:
                    mixer.Sound(r'resources\sounds\bossLaser.mp3').play()

                # Spiral radial bullet pattern
                if curr_time - boss_last_shot_time > boss_burst_delay:
                    bullets_per_shot = 5 # Increase for denser spiral
                    spiral_speed = 10    # Adjust bullet speed
                    angle_offset = boss_burst_shots_fired * 1 # For spiral motion

                    for i in range(bullets_per_shot):
                        angle_deg = (360 / bullets_per_shot) * i + angle_offset
                        angle_rad = math.radians(angle_deg)

                        vx = math.cos(angle_rad) * spiral_speed
                        vy = math.sin(angle_rad) * spiral_speed

                        boss_fire_bullets(boss_x + 40, boss_y + 40, vx=vx, vy=vy)

                    boss_burst_shots_fired += 1
                    boss_last_shot_time = curr_time
                    
            else:
                boss_phase = "vulnerable"
                boss_burst_shots_fired = 0
                pt = curr_time  
                boss_vulnerable_hit = False


        elif boss_phase == "vulnerable":
            if boss_vulnerable_hit:
                if curr_time - boss_hit_time > 550: 
                    boss_phase = "burst"
                    boss_last_shot_time = curr_time
                    boss_vulnerable_hit = False  

        if boss_hits_player(boss_x, boss_y, playerX, playerY, boss_image, playerImage):
            if not player_blink: 
                player_hits += 1
                player_blink = True
                player_blink_start_time = curr_time
                if settings.sfx_enabled:
                    mixer.Sound(r'resources\sounds\explosionWarning.mp3').play()
                if player_hits >= 5:
                    return False 


        for bullet in enemy_bullets[:]:
            bullet['x'] += bullet['vx']
            bullet['y'] += bullet['vy']

            screen.blit(enemyBulletImage, (bullet['x'], bullet['y']))

            if player_collision(bullet, playerX - 20, playerY + 10):
                if not player_blink:
                    if settings.sfx_enabled:
                        mixer.Sound(r'resources\sounds\explosionWarning.mp3').play()
                    player_hits += 1
                    player_blink = True
                    player_blink_start_time = curr_time
                    if player_hits == 5:
                        main_message3(victory=False)
                        return False
                enemy_bullets.remove(bullet)  

            if bullet['y'] > 600:
                enemy_bullets.remove(bullet)


        for bullet in player_bullets[:]:
            bullet['x'] += bullet['vx']
            bullet['y'] += bullet['vy']

            rotated_bullet = pygame.transform.rotate(bulletImage, bullet['angle'])
            bullet_rect = rotated_bullet.get_rect(center=(bullet['x'], bullet['y']))

            screen.blit(rotated_bullet, bullet_rect.topleft)

            if boss_collision(bullet, boss_x, boss_y):
                if settings.sfx_enabled:
                    mixer.Sound(r'resources\sounds\explosion.wav').play()
                player_bullets.remove(bullet)
                if boss_phase == "vulnerable" and not boss_vulnerable_hit:
                    boss_hits += 1
                    boss_vulnerable_hit = True
                    boss_hit_time = curr_time  

                if boss_hits == 10:
                    main_message3(victory=True)
                    return True
                
            if bullet['y'] < 0 or bullet['y'] > 600 or bullet['x'] < 0 or bullet['x'] > 800:
                player_bullets.remove(bullet)

        pygame.display.update()

# main_boss_fight()