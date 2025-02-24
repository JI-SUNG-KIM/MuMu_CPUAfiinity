'''
MuMu App Player Affinity Changer for 7950x3d
'''
import subprocess, sys, time
import inputTimeout as it

def set_affinity(name, ccd):
    #             2^16-1, 2^32-2^16, 2^32-1
    ccd_to_num = [65535, 4294901760, 4294967295]
    command = f"Get-Process {name} | ForEach-Object {{$_.ProcessorAffinity={ccd_to_num[ccd]}}}"

    subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )

process_name_list = ["MuMuPlayer", "MuMuVMMHeadless", 'MuMuVMMSVC']
ccd_chosen = int(it.input_with_timeout("Choose CCD (0 for CCD0, 1 for CCD1, 2 for all) : ", 3, 0, True))

for process_name in process_name_list:
    print(f"\nWorking for {process_name}")

    set_affinity(process_name, ccd_chosen)
    print(f"Setting to {'all ' if ccd_chosen == 2 else ''}ccd{ccd_chosen if ccd_chosen != 2 else 's'}.")

print("\nAll Process Completed! Terminal will close in 2 seconds.")
time.sleep(2)
sys.exit(1)
