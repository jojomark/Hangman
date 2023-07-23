import pygame
import random

pygame.init()

#window setup
HEIGHT = 700
WIDTH = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

#choosing the word from the file
def choose_word():
    with open ("words.txt", "r") as file:
        words = file.read()
        return random.choice(words.split('\n'))
word = choose_word()

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

#fonts + texts
INSTRUCTION_FONT = pygame.font.SysFont("comicsans", 16)
LETTER_FONT = pygame.font.SysFont("comicsans", 30)
WORD_FONT = pygame.font.SysFont("comicsans", 50)
GAME_OVER_FONT = pygame.font.SysFont("impact", 80)
GAME_OVER_TEXT = GAME_OVER_FONT.render("YOU LOSE!", True, BLUE, WHITE)
YOU_WIN_TEXT = GAME_OVER_FONT.render("YOU WIN!", True, BLUE)

#variables
current_word = ["_" for i in range(len(word))]

spacing = len(word)*50
instruction = "Type any letter to guess it!"
state = "running"
mistakes = 0
wrong_letters = []
guessed_letters = []
hangman_states = ["pygame.draw.circle(win, BLACK, (300, 125), 25, width=1)", "pygame.draw.line(win, BLACK, (300, 150), (300, 225))",
"pygame.draw.line(win, BLACK, (300, 165), (325, 220))", "pygame.draw.line(win, BLACK, (300, 165), (275, 220))", 
"pygame.draw.line(win, BLACK, (300, 225), (325, 305))", "pygame.draw.line(win, BLACK, (300, 225), (275, 305))"]

#gameplay functions
def check_winlose():
    state = "running"
    if mistakes == 6:
        state = "lose"
    if "".join(current_word) == word:
        state = "win"
    return state

def retry():
    # Just realised that a class-based approach would be way better
    # Old habits die hard I guess
    global current_word, word, mistakes, guessed_letters, instruction, state, wrong_letters 
    word = choose_word()
    current_word = ["_" for i in range(len(word))]
    mistakes = 0
    wrong_letters = []
    guessed_letters = []
    instruction = "Type any letter to guess it!"
    state = "running"

#logic for correct or incorrect guess  
def update_word(guess): 
    if (guess not in guessed_letters):
        correct = False
        guessed_letters.append(guess)
        for i in range(len(word)):
            if word[i] == guess:
                current_word[i] = guess
                correct = True
        if correct == False:
            global mistakes, wrong_letters
            mistakes += 1
            wrong_letters.append(guess)
    else:
        global instruction
        instruction = "You cannot guess the same letter twice!"
    

#draw function
def draw():
    win.fill(WHITE)
    #drawing the hangman
    pygame.draw.lines(win, BLACK, False, [(500,400), (500,50), (300, 50), (300,100)]) 
    for i in range(mistakes):
        exec(hangman_states[i]) # this method saves many lines of code compared to coding each state  

    #drawing the word
    current_word_str = " ".join(current_word)
    word_text = LETTER_FONT.render(current_word_str, True, BLACK)
    win.blit(word_text, ((WIDTH//2 - spacing//3, 450)))

    #Instructions
    INSTRUCTION_TEXT = INSTRUCTION_FONT.render(instruction, True, BLACK)
    win.blit(INSTRUCTION_TEXT, ((10, 20)))
    
    #wrong letters
    wrong_letters_instructions = INSTRUCTION_FONT.render("Incorrect guesses:", True, BLACK) # SysFont does not support multiple lines
    wrong_letters_text = INSTRUCTION_FONT.render(" ,".join(wrong_letters), True, BLACK)
    win.blit(wrong_letters_instructions, ((520, 350)))
    win.blit(wrong_letters_text, ((525, 370)))

clock = pygame.time.Clock()
FPS = 60
run = True

#main loop
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if state == "running":
                if event.key >= ord('a') and event.key <= ord('z'):
                    update_word(pygame.key.name(event.key))
                else:
                    instruction = "Guess must be a lowercase letter!"       
            else:
                retry()    

    if state == "running":
        draw()
        if check_winlose() == "lose":
            win.blit(GAME_OVER_TEXT, ((200, 350)))
            correct_word_text = LETTER_FONT.render("The correct word was: " + word, True, BLACK)
            win.blit(correct_word_text, ((50, 500)))
            state = "retry"
        elif check_winlose() == "win":
            win.blit(YOU_WIN_TEXT, ((200, 350)))
            state = "retry"
    elif state == "retry":
        win.fill(WHITE, rect = (0, 600, 700, 100))
        INSTRUCTION_TEXT = LETTER_FONT.render("Press any key to play again!", True, BLACK)
        win.blit(INSTRUCTION_TEXT, ((300, 600)))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()