
from random import randint
from random import choice

DEBUG = False

def Play_Game():
   ## Main method
   ## Initializes dictionary and controls the basic game flow
   dictionary = Initialize_Dictionary()
   if DEBUG:
      Get_Buckets(dictionary)
   play = True
   while play:
      Start_Round(dictionary)
      play = Play_Again()
   print('Thanks for playing!')

def Get_Buckets(dictionary):
   result = [0 for i in range(30)]
   words=[]
   for word in dictionary:
      result[len(word)] += 1
      if len(word)==0:
         words.append(word)
   for i in range(len(result)):
      print('{}:{}'.format(i,result[i]))

def Initialize_Dictionary():
   ## Returns a list of words found in "Dictionary.txt"
   myFile = open("Dictionary.txt", "r")
   myDict = myFile.read().splitlines()
   myFile.close()
   return myDict

def Play_Again():
   ## Returns False if user doesn't want to play
   ## Returns True if user does want to play
   ## Handles bad input
   print('\nWould you like to play again?')
   print('0 - No')
   print('1 - Yes\n')
   try:
      answer = input('Input 0 or 1: ')
      if not (answer == '0' or answer == '1'):
         raise ValueError('\nanswer must be 0 or 1')
      elif answer == '0':
         return False
      elif answer == '1':
         return True
      else:
         raise SystemError('You shouldn\'t be here...')
   except ValueError:
      print('\nanswer must be 0 or 1')
      return Play_Again()
   except:
      print('\nYou shouldn\'t be here...')
      return False
   
def Get_Int_Input(prompt):
   ## Gets user input and guarantees input is a positive integer or blank
   answer = input(prompt)
   try:
      if answer == '':
         return -1
      else:
         answer = int(answer)
         if answer <= 0:
            raise ValueError('Input must be blank or a positive integer')
         else:
            return answer
   except:
      print('Input must be blank or a positive integer\n')
      return Get_Int_Input(prompt)
   
def Get_Char_Input(prompt):
   ## Gets user input and guarantees input is an alpha character, case independent
   valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
   input_txt = input(prompt)
   try:
      if len(input_txt) > 1:
         raise ValueError('Input must be exactly 1 character')
      elif input_txt in valid_chars: 
         return input_txt.upper()
      else:
         raise ValueError('Input must be a letter a-z or A-Z')
   except:
      print('Input must be exactly 1 character a-z or A-Z')
      return(Get_Char_Input(prompt))


def Trim_Dictionary_To_Length(dictionary, word_length):
   ## Returns a list of words from dictionary with length <= word_length
   result = []
   for word in dictionary:
      if len(word) == word_length:
         result.append(word)
   del dictionary
   return result

def Get_Max_Length(dictionary):
   ## Returns the length of the longest word in the dictionary
   result = 0
   for word in dictionary:
      length = len(word)
      if length > result:
         result = length
   return result

def Get_Words(dictionary, guess_position, guess):
   ## dictionary is a list of words all with length = N
   ## guess_position is a boolean list of length N where each element represents whether the guess letter should be in that position in the word
   ## returns a list of words where the guess appears exactly as described by guess_position
   result = []
   for word in dictionary:
      append = True
      for i in range(len(guess_position)):
         char_bool = word[i] == guess
         if char_bool != guess_position[i]:
            #If word[i] == guess doesn't match guess_position don't append the word
            append = False
      if append:
         result.append(word)
         #remove the word from the original dictionary once added
         dictionary.remove(word)
   return result
   


def Split_Dictionary(dictionary, guess):
   ## For each word in the dictionary generate a key corresponding to where guess appears in the word
   ## Using this key add the word to the python dictionary splits
   ## Return the value in splits with the longest length
   ## If there is a tie for longest length return the blank key if it's in the tie so that the user loses a guess
   ## Otherwise return a random value in the tied list
   
   ## Return the dictionary permutation with the largest length,
   ## Return False if longest dictionary was key(________) and True otherwise
   ## Return the key of the dictionary permutation with the largest length
   splits = {}
   word_length = len(dictionary[0])
   max_split_length = 0
   max_split_key = []
   empty_key = False

   # Generate a key of length word_length where each character is either the guessed character or _ if it is not the guessed character
   # Create a new key value pair in splits if the key hasn't been initialized
   # Add the word to the list associated with its key
   for word in dictionary:
      my_key = ''
      for letter in word:
         if letter == guess:
            my_key+=guess
         else:
            my_key+='_'
      if my_key in splits.keys():
         splits[my_key].append(word)
      else:
         splits[my_key]=[word]

   # Find the key with the longest associated list and keep track of ties
   for key in splits.keys():
      dict_length = len(splits[key])
      if dict_length > max_split_length:
         max_split_length = dict_length
         max_split_key = [key]
      elif dict_length == max_split_length:
         max_split_key.append(key)

   # If the empty key has one of the longest associated lists guarantee it gets picked
   base_key = '_'*word_length
   if base_key in max_split_key:
      max_split_key = [base_key]
      empty_key = True

   # If there is a tie randomly select the key for one of the associated lists
   final_key = choice(max_split_key)

   
   return splits[final_key], not empty_key, final_key

def Generate_Hint(partial_hint_string, current_hint):
   ## partial and current hint should be of equal length
   
   ## Return partial_hint_string combined with current_hint
   ## Return the number of remaining blanks.
   result = ''
   blanks = 0
   length = len(current_hint)
   for i in range (length):
      if not partial_hint_string[i]=='_':
         result += partial_hint_string[i]
      elif not current_hint[i]=='_':
         result += current_hint[i]
      else:
         blanks += 1
         result += '_'
   
   return result, blanks

def Evaluate_Guess(dictionary, guess, current_hint):
   ## Returns an updated dictionary
   ## Returns whether the guess was in the resulting dictionary
   ## Returns the current hint
   ## Returns how many blanks are in the hint

   dictionary, correct_guess, partial_hint_string = Split_Dictionary(dictionary, guess)
   current_hint, remaining_characters = Generate_Hint(partial_hint_string, current_hint)
   return dictionary, correct_guess, current_hint, remaining_characters

def Start_Round(dictionary):
   ## Initialize parameters for the round and begin the game

   #Get Input
   print('How many incorrect guesses will be allowed?\n')
   num_guesses = Get_Int_Input('Input a positive integer or leave blank for unlimited and press enter ')
   print('\n\nWhat should the length of the word be?\n')
   input_length = Get_Int_Input('Input a positive integer or leave blank for random and press enter ')

   #Set length of word
   max_length = Get_Max_Length(dictionary)
   if input_length == -1:
      word_length = randint(1,max_length)
   elif input_length > max_length:
      print('Given length exceeds maximum word length in database\nUsing maximum length instead')
      word_length = max_length
   else:
      word_length = input_length
      #TODO Possible issue if a given word length is less than max but not in dictionary

   #Generate initial blank hint string
   current_hint = ''   
   for i in range(word_length):
      current_hint += '_'

   #Start the round
   Play_Round(Trim_Dictionary_To_Length(dictionary, word_length), num_guesses, current_hint, word_length)
   
def Play_Round(dictionary, num_guesses, current_hint, remaining_characters):
   ##Handles the gameplay loop for each round
   guessed_letters = []
   current_incorrect_guesses = 0
   round_over = False
   print('\n-------------------------------------\nLet us start the game\n-------------------------------------\n')
   
   while not round_over:
      # Debugging Info
      # Shows number of possible words remaining
      # If there are fewer than 10 words print all of them
      if DEBUG:
         print('Length of dictionary: {}'.format(len(dictionary)))
         if(len(dictionary) < 10):
            print(dictionary)
      
      if num_guesses == -1:
         print('You have unlimited guesses remaining')
      else:
         print('You have {} guesses remaining'.format(num_guesses-current_incorrect_guesses))
      valid_guess = False
      while not valid_guess:
         print('You have already guessed the following letters {}\n'.format(guessed_letters))
         print('Revealed word: {}'.format(current_hint))
         guess = Get_Char_Input('Please guess a letter: ')
         print('-------------------------------------')
         if guess not in guessed_letters:
            valid_guess = True
            guessed_letters.append(guess)
            guessed_letters.sort()
         else:
            print('You already guessed the letter {}! Please guess again'.format(guess))
         
            
      dictionary, correct_guess, current_hint, remaining_characters = Evaluate_Guess(dictionary, guess, current_hint)
      if not correct_guess:
         current_incorrect_guesses += 1
         print ('\nSorry, the letter {} is not in the word'.format(guess))
      else:
         print ('\nThe letter {} is in the word!'.format(guess))
      if not ((num_guesses - current_incorrect_guesses) > 0 or num_guesses == -1):
         print('You Have Lost The Game')
         fake_answer = randint(1,len(dictionary))
         print('The correct word was {}'.format(dictionary[fake_answer]))
         round_over = True
      elif remaining_characters == 0:
         print('You win!')
         print('The correct answer was {}'.format(current_hint))
         round_over = True
      

Play_Game()
