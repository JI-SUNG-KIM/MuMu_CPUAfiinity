'''
MuMu App Player Affinity Changer for 7950x3d
'''

import subprocess, threading, sys, io, time

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

def input_with_timeout(prompt, timeout, default=0):
    user_input = ""

    def _input():
        nonlocal user_input
        user_input = input(prompt)

    thread = threading.Thread(target=_input, daemon=True)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # sys.stdin = io.StringIO('')
        print()
        print()
        print("Timeout!")
        return default

    return user_input


process_name_list = ["MuMuPlayer", "MuMuVMMHeadless"]
ccd_chosen = input_with_timeout("Choose CCD (0 for CCD0, 1 for CCD1, 2 for all) : ", 3)

for process_name in process_name_list:
    print(f"Working for {process_name}")
    process_count = count_process(process_name)

    if process_count == 0:
        print("Error!")
    elif process_count > 0:
        set_affinity(process_name, process_count, ccd_chosen)
        print(f"Setting to ccd{ccd_chosen} Completed for {process_count} Instance(s).")

time.sleep(1)
sys.exit()
