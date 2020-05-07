import traceback
import os

def get_clean_stack(err):
    return "Error stack:\n"+"\n".join(["{}\{}".format(s.filename,s.name) for s in traceback.extract_tb(err.__traceback__)])+"\nException caught : {}".format(err)


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))