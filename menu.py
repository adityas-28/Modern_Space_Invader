import pygame

pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r'resources/images/spaceship.png')
pygame.display.set_icon(icon)
# Background
background = pygame.image.load(r'resources/images/menuBG.jpg')
background = pygame.transform.scale(background, (800, 600))
# Music
pygame.mixer.music.load(r'resources/sounds/strangerThingdBGMTrim.mp3')
pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
pygame.mixer.music.play(-1)  # Play the music indefinitely
# Mute functionality    
def toggle_mute():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
# # Event handler for key presses
# def handle_key_events():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_m:  # M key to toggle mute
#                 toggle_mute()
#             if event.key == pygame.K_p:  # P key to pause
#                 if pygame.mixer.music.get_busy():
#                     pygame.mixer.music.pause()
#                 else:
#                     pygame.mixer.music.unpause()
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 exit()
                



def main_menu():
    while True:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    toggle_mute()
                if event.key == pygame.K_p: 
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                 
                if event.key == pygame.K_RETURN:
                    return 

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    # Start the game
    import space_invader    