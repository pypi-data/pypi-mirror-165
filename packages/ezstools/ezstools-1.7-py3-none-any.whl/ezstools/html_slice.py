import base64, re, os
from typing import Callable, Dict, List, Optional

# expression to divide files into slices
slicing_patterm = re.compile(r"""
                             ([a-zA-Z0-9_\-]*) # slice name
                             \s? 
                             { # start of slice content
                             \s? 
                             ([^}]*) # slice content
                             \s? 
                             }  # end of slice content
                             """, re.VERBOSE)

def make(filename:str) -> None:
    """
    #### Creates a .htmlslice file using passed html file as <Template>

    #### Params
    - `filename`: file to use as template (with extension | HTML file) 
    """
    
    # route from file + name.htmlslice    
    template_content = open(filename, "r").read()
    
    filename = filename[:-5] + ".htmlslice"
    
    with open(filename, "w") as f:
        f.write(f"TEMPLATE {{\n{template_content}\n}}")

def close(filename:str, slices:Optional[List[str]] = "all") -> None:
    """
    #### Encodes a .htmlslice file

    #### Params
    - `filename`: file to read (with extension)
    
    #### Optional Params
    - slices : Iterable of slices to decode (default : All)
    """
    
    # file contents
    content = open(filename, "r").read()
    
    # get all slices
    for match in slicing_patterm.finditer(content):
        slice_name, slice_content = match.groups()
        
        # if slice has to be encoded
        if slices == "all" or slice_name in slices:
            
            try:
                # decode slice
                encoded_content = base64.b64encode(slice_content.encode()).decode()

                # replace slice content
                content = content.replace(slice_content, encoded_content + "\n")
            
            except:
                continue
                
    # save file
    with open(filename, "w") as f:
        f.write(content)        
    
def use(filename:str, slices:Optional[List[str]] = "all") -> None:
    """
    #### Decodes a .htmlslice file

    #### Params
    - `filename`: file to read (with extension)
    
    #### Optional Params
    - slices : Iterable of slices to decode (default : All)
    """

    content = open(filename, "r").read()

     # get all slices
    for match in slicing_patterm.finditer(content):

        slice_name, slice_content = match.groups()
        
        # if slice has to be decoded
        if slices == "all" or slice_name in slices:
            
            try:
                # decode slice
                decoded_content = base64.b64decode(slice_content.encode()).decode()

                # replace slice content
                content = content.replace(slice_content, decoded_content)
                
            except:
                continue    
                
    # save file
    with open(filename, "w") as f:
        f.write(content)
    
def get_slice(filename:str, slice:str) -> str:
    """
    #### returns slice content from a .htmlslice file 

    #### Params
    - `file`: file to read (with extension)
    - `slice` : slice name to get
    """
    content = open(filename, "r").read()
    
    # get all slices
    for match in slicing_patterm.finditer(content):
        slice_name, slice_content = match.groups()
        
        if slice_name != slice: continue
        
        # try decode slice
        try:
            # decode slice
            slice_content = base64.b64decode(slice_content.encode()).decode()
            
        except: pass
        
        return slice_content
        
    else: return None
    
def get_slice_names(filename:str) -> List[str]:   
    """
    #### Returns all slice names in a .htmlslice file
    
    #### Params
    - filename : file to read (with extension)
    """
    
    content = open(filename, "r").read()
    
    names:List[str] = []
    
    # get all slice names
    for match in slicing_patterm.finditer(content):
        slice_name, _ = match.groups()
        names.append(slice_name)
    
    return names

def get_slices(filename:str, slices:Optional[List[str]] = "all") -> Dict[str, str]:   
    """
    #### Returns a dict containing all slices in a .htmlslice file 
    
    #### Params
    - filename : file to read (with extension)
    
    #### Optional Params
    - slices : Iterable of slice names to get (default : All)
    """
    
    content = open(filename, "r").read()
    
    file_slices:List[str] = {}
    
    # get all slices
    for match in slicing_patterm.finditer(content):
        slice_name, slice_content = match.groups()
                 
        if slices == "all" or slice_name in slices:
            file_slices[slice_name] = slice_content
    
    return file_slices
                    
def build(filename:str, output:Optional[str] = "Default", slices:Optional[List[str]] = "all",
          conditions:Optional[Dict[str, Callable[[], bool]]] = {}) -> None:
    """
    #### builds a html file using a htmlslice file
    
    #### Params
    - filename : file to build (with extension)

    #### Optional Params
    - output : output html file (with extension) (default: <filename>.html)
    - slices : Iterable of slices to build in html file (default : All)
    - conditions : dict of coditions {slice_name: function} if function returns True, slice is included 
    """
    
    # decode all slices
    use(filename)

    # get template
    template = get_slice(filename, "TEMPLATE")

    # output file
    output = output if output != "Default" else filename[:-5] + ".html"
    
    slices_dict = get_slices(filename, slices)
    slices = list(slices_dict.keys()) if slices == "all" else slices
    
    # insert slices
    for name in slices:
        for match in re.finditer(f"<<{name}>>", template):
            if conditions and name in conditions:
                if conditions[name]():
                    template = template.replace(match.group(), slices_dict[name])

                else:
                    template = template.replace(match.group(), "")

            else:
                template = template.replace(match.group(), slices_dict[name])

    with open(output, "w") as f:
        f.write(template)

# class for object-like sintax
class HTMLSlice:
    """
    #### Class for object-like sintax for html slices
    
    #### Params
    - `file`: file to load from or use as template (with extension) (.htmlslice or .html)
    """
    
    def __init__(self, filename:str):
        self.slices:Dict[str, str] = {}
        
        # if is .html file:    
        if filename.endswith(".html"):
            # make htmlslice file using file as template

            self.filename = filename[:-5] + ".htmlslice"

            if self.filename not in os.listdir():
                make(filename)
        
            self.slices.update(get_slices(self.filename))

        # if is .htmlslice file:
        elif filename.endswith(".htmlslice"):
            # read htmlslice file
            self.slices.update(get_slices(filename))
            
            self.filename = filename
            
        # if not valid file
        else:
            raise ValueError(f"Invalid file: {filename} \n File must be .html or .htmlslice")

    # slice getter
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.slices[key]
        
        elif isinstance(key, int):
            return list(self.slices.keys())[key]
        
        else:
            raise ValueError(f"Invalid key: {key}")
        
    def use(self, slices:Optional[List[str]] = "all") -> None:
        """
        #### Decodes slices in htmlslice file
        
        #### Optional Params
        - slices : Iterable of slices to decode (default : All)
        """
        use(self.filename, slices)
            
    def close(self, slices:Optional[List[str]] = "all") -> None:
        """
        #### Encodes slices in htmlslice file

        #### Optional Params (kwargs)
        - slices : Iterable of slices to encode (default : All)
        """
        close(self.filename, slices)
        
    def build(self, output: Optional[str] = "Default", 
                    slices: Optional[List[str]] = "all", 
                    conditions: Optional[Dict[str, callable]] = {}) -> None:
        """
        #### Builds html file using htmlslice file

        #### Optional Params (kwargs)
        - output : output html file (with extension) (default: <filename>.html)
        - slices : Iterable of slices to build in html file (default : All)
        - conditions : dict of coditions {slice_name: function} if function returns True, slice is included 
        """
        
        build(self.filename, output=output, conditions=conditions, slices=slices)  

    def add_slices(self, slices:Dict[str, str]) -> None:
        """
        #### Adds a dict of slices to file
        
        #### Params
        - `slices`: dict of slices to add: {slice_name: slice_content}
        """
        
        # add slices to file and object
        for name, content in slices.items():
            
            # if slice name is alredy taken
            if name in self.slices.keys():
                raise ValueError(f"Slice name alredy in use: {name}")
            
            self.slices[name] = content
            
            with open(self.filename, "a") as f:
                f.write(f"\n{name} {{\n {content}\n}}")
                
    def remove_slices(self, names:List[str]) -> None:
        """
        #### Removes a list of slices from file
        
        #### Params
        - `names`: name of the slices
        """

        # remove slices from file and objects
        content = open(self.filename, "r").read()

        for name in names:
            if name in self.slices:
                del self.slices[name]
            
            search_pattern = re.compile(f"{name}" + r"\s*\{\s*\n.*?\n\s*\}", re.DOTALL)
            
            for match in re.finditer(search_pattern, content):
                content = content.replace(match.group(), "")
                
        with open(self.filename, "w") as f:
            f.write(content)

    def update_slices(self, slices:Dict[str, str]) -> None:   
        """
        #### Updates file slices using passed dict of slices
        
        #### Params
        - slices : {slice_name : new_content } dict of slices to update
        """     
        content = open(self.filename, "r").read()
        
        # iterate throght slices in file
        for match in slicing_patterm.finditer(content):
    
            slice_name, slice_content = match.groups()
            
            if slice_name in slices.keys():
                content = content.replace(slice_content, slices[slice_name] + "\n")
                                
        with open(self.filename, "w") as f:
            f.write(content)        