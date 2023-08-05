import subprocess, os
import setuptools

def start():
    folder = os.path.join(setuptools.__path__[0],'..','tensorflow_opt','code','bin')
    filepath=os.path.join(folder, "start_opt_engine.bat")
    print(filepath)
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()