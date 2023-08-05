import subprocess, os
import sysconfig

def start():
    folder = os.path.join(sysconfig.get_paths()["purelib"],'tensorflow_opt','code','bin')
    filepath=os.path.join(folder, "start_opt_engine.bat")
    print(filepath)
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()