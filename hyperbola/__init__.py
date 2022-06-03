from os.path import dirname, basename, isfile, join
import glob
prob = glob.glob(join(dirname(__file__), 'problems', "*.py"))
__all__ =  [basename(f)[:-3] for f in prob if isfile(f)]