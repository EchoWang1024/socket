import subprocess


def get_process_id(name):
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    print response
    return [int(pid) for pid in response.split()]

print(get_process_id("tomcat"))

