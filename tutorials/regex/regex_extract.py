import re 

def char_extract(input_string): 
    chars = [char for char in input_string if char.islower()]
    #print([char for char in input_string if char.islower()])
    return chars 

def word_extract(input_string):     
    words = [word for word in re.findall(r'\w+', input_string) if word.islower()]
    #print([word for word in re.findall(r'\w+', input_string) if word.islower()])
    return words
 
def int_extract(input_string): 
    ints = [int(char) for char in re.findall(r'\d+', input_string)]
    #print([int(char) for char in re.findall(r'\d+', input_string)])
    return ints
    
