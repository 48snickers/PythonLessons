import sys
import os
from random import randint
from typing import Set

HIDDEN_LETTER = "_"
DELIMITER = " "
DEFAULT_FILENAME = "sowpods.txt"

hangman_pics = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# TODO: tests

# Shows the uncovered portions of the word. E.g., if the word is CAT, and you've guessed 
# A and T previously, returns "_ A T"
def presentable_word(word: str, past_guesses: Set[str]) -> str:
  progress = ""
  for letter in word.upper():
    if letter in (past_guess.upper() for past_guess in past_guesses):  # case insensitive
      progress += (letter)
    else:
      progress += (HIDDEN_LETTER)
    progress += DELIMITER
  return progress


# Returns True if all letters are guessed.
def is_won(word: str, past_guesses: Set[str]) -> Set[str]:
  for letter in word.upper():
    if letter not in (past_guess.upper() for past_guess in past_guesses): # case insensitive
      return False
  return True


# Fetch a valid letter guess from the player.
def request_guess(guessed_letters: Set[str]) -> str:
  while True:
    new_letter = input("What is your letter guess? ")
    if is_valid_guess(new_letter, guessed_letters):
      return new_letter
    else:
      print("A valid guess is a single letter that has not already been guessed. Please try again.")
      print()
  return None


# Validate guesses (must be a single letter that hasn't already been guessed)
def is_valid_guess(guess: str, past_guesses: Set[str]) -> bool:
  return guess.isalpha() and len(guess) == 1 and guess.upper() not in (past_guess.upper() for past_guess in past_guesses) 


# Get a word from the Scrabble dictionary
def get_word() -> str:
  wordfile = os.path.join(sys.path[0], DEFAULT_FILENAME)
  if len(sys.argv) == 2: # get word filename from command line if specified.
    wordfile = sys.argv[1]
    print(f"loading words from {sys.argv[0]}")
  word_list_file = open(wordfile, "r")
  word_list = word_list_file.read().splitlines()
  word_list_file.close()

  return word_list[randint(0, len(word_list))]


# game play
def play() -> None:
  max_guesses = len(hangman_pics) # max guesses is defined by the number of frames in the hangman pics.
  remaining_guesses = max_guesses 
  word = get_word().upper()
  guessed_letters = set()

  while True:

    # reset display via command-line
    os.system("clear")
    # render play
    print(hangman_pics[max_guesses - remaining_guesses])
    print()
    print(f"The word is: {presentable_word(word, guessed_letters)}")
    print()
    print(f"You have guessed: {guessed_letters if len(guessed_letters) != 0 else 'nothing yet.'}")
    print()

    # check for end states
    if is_won(word, guessed_letters):
      print("YOU WON!")
      return
    elif remaining_guesses == 1: # reads as wtf.
      print(f"YOU LOSE! The word was {word}")
      return

    # get a new guess
    new_letter = request_guess(guessed_letters).upper()
    guessed_letters.add(new_letter)

    # see if guessed letter is a ding
    if new_letter not in word:
      remaining_guesses -= 1


# loop for game play
while True:
  play()
  print()
  play_again = input("Play again? (Y/N)").upper()
  if play_again[0] != "Y":
    break