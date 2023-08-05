import subprocess

def start():
    # p = Popen("start_topt_engine.bat", cwd=r"./bin")
    # stdout, stderr = p.communicate()
    filepath="./bin/start_topt_engine.bat"
    p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

    stdout, stderr = p.communicate()