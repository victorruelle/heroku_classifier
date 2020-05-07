import traceback

def get_clean_stack(err):
    return "Error stack:\n"+"\n".join(["{}\{}".format(s.filename,s.name) for s in traceback.extract_tb(err.__traceback__)])+"\nException caught : {}".format(err)