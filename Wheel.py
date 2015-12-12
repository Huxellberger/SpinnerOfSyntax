# Program to spin a wheel and choose a language
# Created By Jake Huxell For Advent Of Code 2015
"""
Some notes about the program.

TODO:

1. Upkeep and bug fix as I go along
"""
# Get pygame libraries  
import pygame, sys, random
from pygame.locals import *

# Generate random seed for the program - Use current time
random.seed()

# Initiliase, needed to use classes
pygame.init() 

# Global variables so user can easily change wheel properties
LANGUAGES = ("Python", "C++", "C", "Java", "JavaScript", "ASM", "RPG Maker",
             "Prolog", "Lua")

# Set up the colours that make up the sections of the wheel
BLACK = (0, 0, 0)
MAROON_RED = (128, 0, 0)
RED = (255, 0, 0)
LIME_GREEN = (0, 128, 0)
GREEN = (0, 255, 0)
NAVY_BLUE = (0, 0, 128)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
CREAM = (255, 255, 153)

# Slap them all in an array so the wheel can choose one at random
COLOURS = (MAROON_RED, RED, LIME_GREEN, GREEN, NAVY_BLUE, BLUE, PURPLE, YELLOW)

# Variables to hold size of the window
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600

# Pi - Used for drawing segments of the wheel
PI = 3.141592

# Clock to set the game fps
clock = pygame.time.Clock()

# Font objects
titleFont = pygame.font.Font(None, (20+(WINDOW_WIDTH/20)))
wheelFont = pygame.font.Font(None, 350/len(LANGUAGES))
whamFont = pygame.font.Font(None, 500/len(LANGUAGES))
buttonFont = pygame.font.Font(None, (WINDOW_WIDTH/24))
titleWham = titleFont.render("Poetry In Motion!", True, (10, 10, 10))
titleGrind = titleFont.render("PHYSICS ARE SHAMBLED", True, (10, 10, 10))
buttonSplash = buttonFont.render("Spin Here!", True, WHITE)
buttonWham = buttonFont.render("Click!", True, YELLOW)


# Function to draw a wheel on the screen
# Takes the distance the wheel has spun as variable
def drawWheel(currentDisplay, wheelCentre, currentOffset):
  # Draw annoying flashing wheel outline!
  for segment in range (0, len(LANGUAGES)):
    pygame.draw.arc(currentDisplay, COLOURS[random.randint(0, len(COLOURS) - 1)],
      (wheelCentre[0], wheelCentre[1], WINDOW_WIDTH/1.5, WINDOW_HEIGHT/1.5), 
      (((2*PI)/len(LANGUAGES)*segment)),
      (((2*PI)/len(LANGUAGES)*(segment+1))), 10)

  # Draw exciting wheel interior!
  for segment in range (0, len(LANGUAGES)):
    colour = (currentOffset+segment - 2)%len(COLOURS)
    pygame.draw.arc(currentDisplay, COLOURS[colour],
      ((wheelCentre[0] + 10), (wheelCentre[1] + 10), 
      (WINDOW_WIDTH/1.5 - 20), (WINDOW_HEIGHT/1.5 - 20)), 
      ((2*PI)/len(LANGUAGES)*segment),
      ((2*PI)/len(LANGUAGES)*(segment+1)), 50)

  # Draw centre elipse and line that goes straight up to indicate the winner
  pygame.draw.ellipse(currentDisplay, ORANGE, ((wheelCentre[0]+40), 
                     (wheelCentre[1]+40), (WINDOW_WIDTH/1.5-80),                   
                     (WINDOW_HEIGHT/1.5-80)))

  POINT = WINDOW_HEIGHT/2 - 100
  # Draw line that points to the winner
  pygame.draw.line(currentDisplay, BLACK, 
                  (WINDOW_WIDTH/2 - 30, WINDOW_HEIGHT/2), 
                  (WINDOW_WIDTH/2 - 30, WINDOW_HEIGHT/2 - WINDOW_HEIGHT/3)
                  , 10)

  # Draw arrow on line 
  pygame.draw.polygon(currentDisplay, BLACK, 
                   ((WINDOW_WIDTH/2 - 25, WINDOW_HEIGHT/2 - WINDOW_HEIGHT/3), 
                    (WINDOW_WIDTH/2 - 35, WINDOW_HEIGHT/2 - WINDOW_HEIGHT/3),
                    (WINDOW_WIDTH/2 - 30, WINDOW_HEIGHT/2 - WINDOW_HEIGHT/3 - 20)))

  # Draw Bottom of wheel 
  pygame.draw.polygon(currentDisplay, BLACK, 
                     ((wheelCentre[0] + WINDOW_WIDTH/1.5, 
                     wheelCentre[1] + WINDOW_HEIGHT/1.5 + WINDOW_HEIGHT/8),
                     (wheelCentre[0] + WINDOW_WIDTH/3, 
                     wheelCentre[1] + WINDOW_HEIGHT/1.5),
                     (wheelCentre[0], 
                     wheelCentre[1] + WINDOW_HEIGHT/1.5 + WINDOW_HEIGHT/8)))
 
  return # End of drawWheel function

# Function to draw the text 
# Which one is flashing depends on the segment at the top of the wheel. 
def drawText(currentDisplay, textNormal, textWham, highlighted):
  division = WINDOW_HEIGHT / len(LANGUAGES)
  for selection in range(0, len(LANGUAGES)):
    if selection == highlighted:
      currentDisplay.blit(textWham[selection], (0, division*selection))
    else:
      currentDisplay.blit(textNormal[selection], (0, division *selection))
  return

# Function to draw the button 
# Will flash if someone hovers over it
def drawButton(currentDisplay):
  mousePos = pygame.mouse.get_pos()
  if mousePos[0] < 10*WINDOW_WIDTH/12 or mousePos[1] < 11*WINDOW_HEIGHT/12: 
    pygame.draw.rect(currentDisplay, BLACK, (10*WINDOW_WIDTH/12,
                     11*WINDOW_HEIGHT/12, WINDOW_WIDTH/6, WINDOW_HEIGHT/12))
    currentDisplay.blit(buttonSplash, (10*WINDOW_WIDTH/12, 11*WINDOW_HEIGHT/12))
  else:
    pygame.draw.rect(currentDisplay, PURPLE, (10*WINDOW_WIDTH/12,
                     11*WINDOW_HEIGHT/12, WINDOW_WIDTH/6, WINDOW_HEIGHT/12))
    currentDisplay.blit(buttonWham, (10*WINDOW_WIDTH/12, 11*WINDOW_HEIGHT/12))
  return

# Function to check if the button has been pressed or not
def isPressed(currentDisplay):
  clicks = pygame.mouse.get_pressed()
  mousePos = pygame.mouse.get_pos()
  if clicks[0] and (mousePos[0] >= 10*WINDOW_WIDTH/12 and 
                               mousePos[1] >= 11*WINDOW_HEIGHT/12):
    return True
  else:
    return False  

# Main program that creates the window and sets the logic up
def main():
  # Start up the window 
  pygame.mixer.music.load("assets/Waiting.wav")
  pygame.mixer.music.play(-1, 0.0)
  DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption("Spinner Of Syntax")
  titleSplash = titleFont.render("Get Ready To Spin!", True, (10, 10, 10))
  # Create arrays to hold the text for the wheel
  languagesUnselected = []
  languagesWham = []
  wheelStopped = True
  wheelBackSpinning = False
  offset = random.randint(0, len(LANGUAGES))
  clockSpeed = 1
  newSong = False
  upperBound = random.randrange(350, 400)
  # Establish top-left corner of the wheel
  wheelCentre = (WINDOW_WIDTH/8, WINDOW_HEIGHT/8)

  for language in range(0, len(LANGUAGES)):
    languagesUnselected.append(wheelFont.render(LANGUAGES[language], True,
                               (10, 10, 10)))
    languagesWham.append(whamFont.render(LANGUAGES[language], True, 
                         (255, 15, 30)))
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

    # Stationary wheel logic
    if wheelStopped:
      if newSong:
        pygame.mixer.music.load("assets/Waiting.wav")
        pygame.mixer.music.play(-1, 0.0)
        newSong = False
      DISPLAY.fill((CREAM))
      DISPLAY.blit(titleSplash, (3*WINDOW_WIDTH/12, 0)) 
      drawWheel(DISPLAY, wheelCentre, offset)
      drawText(DISPLAY, languagesUnselected, languagesWham, offset)
      drawButton(DISPLAY)
      wheelStopped = not isPressed(DISPLAY)
      newSong = not wheelStopped

    # Wheel spinning logic
    else:
      if not wheelBackSpinning:
        if newSong:
          pygame.mixer.music.load("assets/Spinning.wav")
          pygame.mixer.music.play(-1, 0.0)
          newSong = False
        offset += 1
        if offset >= len(LANGUAGES):
          offset = 0
        DISPLAY.fill((CREAM))
        DISPLAY.blit(titleWham, (3*WINDOW_WIDTH/12, 0))
        drawWheel(DISPLAY, wheelCentre, offset) 
        drawText(DISPLAY, languagesUnselected, languagesWham, offset)
        pygame.time.wait(clockSpeed)
        clockSpeed += random.randint(1, 3)
        if clockSpeed >= upperBound:
          wheelBackSpinning = True
          newSong = True
      else:
        if newSong:
          pygame.mixer.music.load("assets/GrindingHalt.wav")
          pygame.mixer.music.play(-1, 0.0)
          newSong = False
        offset -= 1
        if offset < 0:
          offset = len(LANGUAGES) - 1
        DISPLAY.fill((CREAM))
        DISPLAY.blit(titleGrind, (3*WINDOW_WIDTH/12, 0))
        drawWheel(DISPLAY, wheelCentre, offset) 
        drawText(DISPLAY, languagesUnselected, languagesWham, offset)
        pygame.time.wait(clockSpeed)
        clockSpeed += 10        
        if clockSpeed >= 520:
          wheelBackSpinning = False
          wheelStopped = True
          pygame.mixer.music.load("assets/WinnerRevealed.wav")
          pygame.mixer.music.play(-1, 0.0)
          titleSplash = titleFont.render(LANGUAGES[offset] + " Wins!", True,
                                         COLOURS[offset])
          clockSpeed = 1
          
     
      
    pygame.display.flip()
    clock.tick(30)
  

 

main()

