import subprocess, os
import setuptools

def start():
    site_package = os.path.abspath(os.path.join(setuptools.__path__[0], '..'))
    folder = os.path.join(site_package,'tensorflow_opt','code','bin')
    filepath=os.path.join(folder, "start_opt_engine.bat")
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()