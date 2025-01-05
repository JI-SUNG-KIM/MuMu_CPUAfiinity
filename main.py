'''
MuMu App Player Affinity Changer for 7950x3d
'''

import subprocess

def count_process(name):
    command = f"""
    $process = Get-Process {name}
    $process.Length
    """

    returned = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )

    return int(returned.stdout)

def set_affinity(name, count):
    command = f"""
    $process = Get-Process {name}
    """
    for i in range(count):
        command += f"\n$process[{i}].ProcessorAffinity = 65535"

    subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )


process_name_list = ["MuMuPlayer", "MuMuVMMHeadless"]
for process_name in process_name_list:
    print(f"Working for {process_name}")
    process_count = count_process(process_name)
    if process_count == 0:
        print("Error!")
    elif process_count > 0:
        set_affinity(process_name, process_count)
        print(f"Setting Completed for {process_count} Instance(s).")
input("")