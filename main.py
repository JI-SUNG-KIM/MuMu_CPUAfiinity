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

def set_affinity(name, count, ccd):
    #             2^16-1, 2^32-2^16, 2^32-1
    ccd_to_num = [65535, 4294901760, 4294967295]
    command = f"""
    $process = Get-Process {name}
    """
    for i in range(count):
        command += f"\n$process[{i}].ProcessorAffinity = {ccd_to_num[ccd]}"

    subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )


process_name_list = ["MuMuPlayer", "MuMuVMMHeadless"]
ccd_chosen = -1

for process_name in process_name_list:
    print(f"Working for {process_name}")
    process_count = count_process(process_name)

    if process_count == 0:
        print("Error!")
    elif process_count > 0:
        ccd_chosen = int(input("0 for CCD0, 1 for CCD1, 2 for all : ")) if ccd_chosen == -1 else ccd_chosen
        set_affinity(process_name, process_count, ccd_chosen)
        print(f"Setting to ccd{ccd_chosen} Completed for {process_count} Instance(s).")

input("")