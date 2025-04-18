import sys
import pygame

pygame.font.init()

# Font object to be used in all functions
font = pygame.font.SysFont("Arial", 40)

def display_message(message):
    screen = pygame.display.get_surface() 
    screen.fill((0, 0, 0))  
    
    text = font.render(message, True, (255, 255, 255))  
    
    # Position the text in the center of the screen
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                      screen.get_height() // 2 - text.get_height() // 2))
    
    pygame.display.flip()  
    pygame.time.wait(2000)  

def ask_play_again():
    while True:
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))  
        
        # Render "Play Again?" text
        text = font.render("Play Again? (Y/N)", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                           screen.get_height() // 2 - text.get_height() // 2))
        
        pygame.display.flip()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Continue playing
                if event.key == pygame.K_n:
                    return False  # Go back to the main menu

def main_menu():
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))  
    
    # Render "Welcome to Connect 4!" text
    text = font.render("Welcome to Connect 4!", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                       screen.get_height() // 2 - text.get_height() // 2 - 50))
    
    # Render menu options
    menu_text = font.render("Press 'P' to Play", True, (255, 255, 255))
    screen.blit(menu_text, (screen.get_width() // 2 - menu_text.get_width() // 2, 
                            screen.get_height() // 2 - menu_text.get_height() // 2 + 50))
    quit_text = font.render("Press 'Q' to Quit", True, (255, 255, 255))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 
                            screen.get_height() // 2 - quit_text.get_height() // 2 + 100))

    pygame.display.flip()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return True  
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

def difficulty_menu():
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))  
    
    # Render "Select Difficulty" text
    text = font.render("Select Difficulty", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 
                       screen.get_height() // 2 - text.get_height() // 2 - 50))
    
    # Render difficulty options
    easy_text = font.render("Press '1' for Easy", True, (255, 255, 255))
    screen.blit(easy_text, (screen.get_width() // 2 - easy_text.get_width() // 2, 
                            screen.get_height() // 2 - easy_text.get_height() // 2 + 50))
    medium_text = font.render("Press '2' for Medium", True, (255, 255, 255))
    screen.blit(medium_text, (screen.get_width() // 2 - medium_text.get_width() // 2, 
                            screen.get_height() // 2 - medium_text.get_height() // 2 + 100))
    hard_text = font.render("Press '3' for Hard", True, (255, 255, 255))
    screen.blit(hard_text, (screen.get_width() // 2 - hard_text.get_width() // 2, 
                            screen.get_height() // 2 - hard_text.get_height() // 2 + 150))

    pygame.display.flip() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 'Easy'  # Easy difficulty selected
            elif event.key == pygame.K_2:
                return 'Medium'  # Medium difficulty selected
            elif event.key == pygame.K_3:
                return 'Hard'  # Hard difficulty selected
