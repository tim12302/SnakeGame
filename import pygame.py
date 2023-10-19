# SNAKE GAME
''' 
Duik in de nostalgische wereld van Snake!!, 
een tijdloze klassieker die generaties gamers heeft geboeid. 
In deze moderne interpretatie navigeer je een groeiende slang door een speelveld, 
waarbij je probeert voedsel te eten zonder tegen de muren of jezelf aan te botsen. 
'''


import pygame
import random

# Initialisatie van pygame
pygame.init()
pygame.mixer.init()


''' Globale Constanten '''

# Kleuren
WIT = (255, 255, 255)
GROEN = (0, 128, 0)
ROOD = (255,0,0)

# Schermgrootte
BREEDTE, HOOGTE = 640, 480

# Grootte van een segment van de slang
SEG_SIZE = 25

# Snelheid van de slang
SNELHEID = 5

# Mogelijke richtingen van de slang 
UP = (0, -SNELHEID)
DOWN = (0, SNELHEID)
LEFT = (-SNELHEID, 0)
RIGHT = (SNELHEID, 0)

screen = pygame.display.set_mode((BREEDTE, HOOGTE))

pygame.display.set_caption("SNAKE GAME")



''' Functiedefinities'''

# Functie om highscores op te slaan
def save_highscore(new_score, player_name):
    try:
        with open("highscores.txt", "r") as file:
            entries = file.readlines()
            scores = [entry.strip().split(":")[1] for entry in entries]
            names = [entry.strip().split(":")[0] for entry in entries]
    except:
        scores = []
        names = []

    scores.append(str(new_score))
    names.append(player_name)
    
    combined = list(zip(names, scores))
    combined.sort(key=lambda x: int(x[1]), reverse=True)
    combined = combined[:5]  # Bewaar alleen de top 5 scores

    with open("highscores.txt", "w") as file:
        for name, score in combined:
            file.write(f"{name}:{score}\n")

# Functie om highscores te lezen
def get_highscores():
    try:
        with open("highscores.txt", "r") as file:
            entries = file.readlines()
            scores = [(entry.strip().split(":")[0], int(entry.strip().split(":")[1])) for entry in entries]
            return scores
    except:
        return []


# Functie om highscores te tonen
def show_highscores():
    scores = get_highscores()
    screen.fill(WIT)
    font = pygame.font.SysFont(None, 35)
    label = font.render("Highscores:", True, GROEN)
    screen.blit(label, (BREEDTE // 2 - 70, 50))
    
    for index, (name, score) in enumerate(scores):
        score_label = font.render(f"{index + 1}. {name}: {score}", True, GROEN)
        screen.blit(score_label, (BREEDTE // 2 - 100, 80 + index * 30))
    
    pygame.display.flip()
    pygame.time.wait(5000)  # Toon highscores voor 15 seconden

def get_player_name():
    font = pygame.font.SysFont(None, 35)
    input_box = pygame.Rect(BREEDTE // 2 - 70, HOOGTE // 2, 140, 32)
    color_inactive = pygame.Color('red')
    color_active = pygame.Color('red')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WIT)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        label = font.render("Voer je naam in:", True, GROEN)
        screen.blit(label, (BREEDTE // 2 - 70, HOOGTE // 2 - 40))

        pygame.display.flip()
        clock.tick(30)

    return text

def show_start_menu():
    menu_run= True
    while menu_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Start het spel wanneer Enter word ingedrukt
                    menu_run = False

        screen.fill(WIT)
        font = pygame.font.SysFont(None, 55)
        label = font.render("Welkom bij Snake Game!", True, GROEN)
        screen.blit(label, (BREEDTE // 2 - 200, HOOGTE // 2 - 40))
        
        font_small = pygame.font.SysFont(None, 35)
        start_label = font_small.render("Druk op Enter om te beginnen", True, GROEN)
        screen.blit(start_label, (BREEDTE // 2 - 150, HOOGTE // 2 + 20))
        
        pygame.display.flip()

# Functie om voedsel te tekenen
def Teken_voedsel(pos):
    pygame.draw.rect(screen, ROOD, pygame.Rect(pos[0], pos[1], SEG_SIZE, SEG_SIZE))

# Functie om de slang te tekenen
def Teken_Slang(slang):
    for segment in slang:
        pygame.draw.rect(screen, GROEN, pygame.Rect(segment[0], segment[1], SEG_SIZE, SEG_SIZE))

def Teken_score(score):
    font = pygame.font.SysFont(None, 35)
    score_tekst = font.render(f"Score: {score}", True, (0, 0, 0))  # Zwart kleur voor de tekst
    screen.blit(score_tekst, (10, 10))  # Positie van de score op het scherm




''' Hoofdprogramma'''

def main():

    show_start_menu()

    # laden van Muziek en instellen van Volume 
    achtergrond_Muziek = pygame.mixer.music.load("C:/Users/timst/OneDrive/Documenten/Bureaublad/programming/SnakeGAME/wubby dancer (loop).mp3")
    voedsel_geluid = pygame.mixer.Sound("C:/Users/timst/OneDrive/Documenten/Bureaublad/programming/SnakeGAME/FoodSound.wav")
    voedsel_geluid.set_volume(0.1) # Volume van het eten van voedsel op 10%
    pygame.mixer.music.set_volume(0.0) #m Muziek volume nu op 0%
    pygame.mixer.music.play(-1)

    # Score
    score = 0
    slang = [[100, 100],[90, 100], [80, 100]] # Beginpositie van de slang 
    direction = (SNELHEID, 0) # Begin richting naar rechts
    food = [random.randint(0, (BREEDTE//SEG_SIZE) - 1) * SEG_SIZE, random.randint(0, (HOOGTE//SEG_SIZE) - 1) * SEG_SIZE]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT          
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT   


        # Beweeg de slang
        Head = slang[0].copy()
        Head[0] += direction[0]
        Head[1] += direction[1]
        slang.insert(0, Head)

        # Controleer of de slang zichzelf heeft geraakt
        for segment in slang[1:]:
            if segment == Head:
                print("Snake ate his own tail.. GAME OVER")
                running = False
                break

        # Controleer of de slang de randen van het scherm heeft bereikt
        if Head[0] < 0 or Head[0] >= BREEDTE or Head[1] < 0 or Head[1] >= HOOGTE:
            print("GAME OVER")
            running = False

        # Controleer of de slang het voedsel heeft gegeten
        head_rect = pygame.Rect(Head[0], Head[1], SEG_SIZE, SEG_SIZE)
        food_rect = pygame.Rect(food[0], food[1], SEG_SIZE, SEG_SIZE)

        if head_rect.colliderect(food_rect):
            food = [random.randint(0, (BREEDTE//SEG_SIZE) - 1) * SEG_SIZE, random.randint(0, (HOOGTE//SEG_SIZE) - 1) * SEG_SIZE]
            score += 1
            voedsel_geluid.play()

            # Voeg drie nieuwe segmenten toe aan de slang
            for _ in range(5):
                slang.insert(0, Head.copy())

        else:
            slang.pop()
            
        screen.fill(WIT)
        Teken_Slang(slang)
        Teken_voedsel(food)
        Teken_score(score)

        pygame.display.flip()

        pygame.time.Clock().tick(30)
    
    player_name = get_player_name()
    # Opslaan van de score wanneer het spel eindigt
    save_highscore(score, player_name)

    # Toon highscores na het spel
    show_highscores()    

    pygame.quit()

if __name__ == "__main__":
    main()
