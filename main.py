import pygame
import space_invader
import settings

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r'resources/images/spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load(r'resources/images/menuBG.jpg')
background = pygame.transform.scale(background, (800, 600))

pygame.mixer.music.load(r'resources/sounds/strangerThingdBGMTrim.mp3')
pygame.mixer.music.set_volume(0.3)  #
pygame.mixer.music.play(-1)  

isPaused = False

def toggle_mute():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        settings.music_enabled = False
    else:
        pygame.mixer.music.unpause()
        settings.music_enabled = True

def main_menu():
    while True:
        global isPaused
        if isPaused:
            screen.blit(background, (0, 0))
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
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: 
                        pygame.mixer.Sound(r'resources/sounds/pause.wav').play()
                        isPaused = not isPaused

                    elif event.key == pygame.K_m:
                        toggle_mute()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            continue

        screen.blit(background, (0, 0))
        font = pygame.font.Font(r'resources/fonts/SPACEBOY.ttf', 55)
        text = font.render("Space Invaders", True, (82, 242, 242))
        screen.blit(text, (55, 125))

        font = pygame.font.Font(r'resources/fonts/SPACEBOY.ttf', 32)
        text = font.render("Press Enter to Start", True, (188, 113, 245))
        screen.blit(text, (125, 225))

        font = pygame.font.Font(r'resources/fonts/SPACEBOY.ttf', 24)
        text = font.render("Controls : ", True, (117, 252, 38))
        screen.blit(text, (135, 300))

        font = pygame.font.Font(r'resources/fonts/SPACEBOY.ttf', 18)
        text = font.render("1. Arrow keys to move  ", True, (159, 245, 185))
        screen.blit(text, (145, 350))

        text = font.render("2. SPACE to shoot", True, (159, 245, 185))
        screen.blit(text, (145, 375))

        text = font.render("3. P to pause", True, (159, 245, 185))
        screen.blit(text, (145, 400))

        text = font.render("4. M to mute", True, (159, 245, 185))
        screen.blit(text, (145, 425))

        text = font.render("5. S to mute SFX", True, (159, 245, 185))
        screen.blit(text, (145, 450))

        text = font.render("6. ESC to Exit", True, (159, 245, 185))
        screen.blit(text, (145, 475))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_p: 
                        pygame.mixer.Sound(r'resources/sounds/pause.wav').play()
                        isPaused = not isPaused
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                 
                if event.key == pygame.K_RETURN:
                    space_invader.main_game()
                    return 

        pygame.display.update()

main_menu()