import subprocess, os
import site
import shutil

def start(tensor):
    site_package = site.getsitepackages()[1]
    folder = os.path.join(site_package,'tensorflow_opt','code','bin')
    shutil.copytree(folder, os.path.join(folder, '..','..','..','tensorflow', 'core', 'framework', 'bin'), dirs_exist_ok=True)
    filepath=os.path.join(os.path.join(folder, '..','..','..','tensorflow', 'core', 'framework', 'bin', 'start_opt_engine.bat'))
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
    stdout, stderr = p.communicate()