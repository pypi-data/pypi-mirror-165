import libcst
import re 

def last_header_comment(s : str) -> str:
    """
    Return the last header comment
    """
    parsed_file = libcst.parse_module(s).header
    for i in range(len(parsed_file)-1, -1, -1):
        comment = parsed_file[i].comment
        if comment:
            return comment.value
    return None


def cut_topfile_comments(s : str) -> str:
    """
    cut the header of the file where the program begins
    """
    if not isinstance(s,str):
        return s
    last_comment = last_header_comment(s)
    if last_comment:
        return s[s.find(last_comment)+len(last_comment)+1:]
    return s

def cut_filename(s : str) -> str:
        """
        Cut the filename to keep only the last part, that is the name
        without the access path.

        Args : 
            s (str) the filename

        Return :
            (str) the filename cutted

        """
        try :
            return re.search("\/[^\/]*$",s).group()
        except Exception as e :
            return s

def hash_filename(s : str) -> str:
    """
    Returns a hashed name for s : its hash value.
    """
    return "file_" + str(s.__hash__()) 
