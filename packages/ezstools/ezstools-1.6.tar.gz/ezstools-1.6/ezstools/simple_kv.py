# Reads a file and convert its to key value pairs using the following format:
"""
key : some text
more text

key2 : some text
"""

# pairs are separated by ;, key and value by a colon


from typing import Dict

def load_skv(filename:str, end_token=";", key_separation_token=":") -> Dict[str, str]:
    """
    #### Loads a dictionary from a simple key value file (.skv)
    - Note: Extension .skv is not required
    
    #### Params
    - filename: the name of the file to load
    
    #### Optional Params
    - end_token: the token that indicates end of a key value pair (default: ";")
    - key_separation_token: the token that separates the key from the value (default: ":")
        - Example: my_key : my_value
    
    #### Sample file format
    some_key_name : \n
    this is part of the value \n
    this is also part of the value \n
    below this line the key value pair is ended \n
    ;
    
    """
    
    result:Dict[str, str] = {}
    
    key, value = "", ""
    
    with open(filename, "r") as f:
        lines = f.readlines()
        
    for line in lines:
                    
        # detect key and value separation
        if key_separation_token in line and key == "":
            key, value = line.split(":", 1)
            key = key.strip()
            value += value.replace("\n", "").strip()
            
        # if empty line, skip
        elif key == "" and not line.strip():
            continue
            
        # ends adding line to value
        elif line.strip() == end_token:    
            
            # remove "\n" at the end        
            if value[-1] == "\n":
                value = value[:-1]

            result[key] = value 
            key, value = "", ""
            
        # keep adding line to value
        else:
            if key != "":
                value += line
            
    return result
                
    
        
