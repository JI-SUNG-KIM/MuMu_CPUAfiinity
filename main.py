'''
MuMu App Player Affinity Changer for 7950x3d
'''

import subprocess, threading, sys, time
import _thread
import ctypes

def count_process(name):
    # PowerShell 명령어에서 안전하게 인자를 전달
    command = [
        "powershell",
        "-Command",
        f"""
        try {{
            $process = Get-Process -Name '{name}' -ErrorAction Stop
            $process.Length
        }} catch {{
            0  # 프로세스가 없으면 0 반환
        }}
        """
    ]

    returned = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    # 명령어의 실행 성공 여부 확인
    if returned.returncode != 0:
        raise RuntimeError(f"PowerShell command failed: {returned.stderr}")

    try:
        # 결과를 정수로 변환
        return int(returned.stdout.strip())
    except ValueError:
        raise RuntimeError(f"Invalid output from PowerShell command: {returned.stdout}")

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

def input_with_timeout(prompt, timeout, default=None):
    user_input = default

    def _input():
        nonlocal user_input
        user_input = input(prompt)

    def ctype_async_raise(thread_obj, exception):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_obj.ident), ctypes.py_object(exception))
    
    thread = threading.Thread(target=_input, daemon=True)
    thread.start()

    thread.join(timeout)

    if thread.is_alive():
        ctype_async_raise(thread, SystemExit)
        print(default)
        print("Timeout! Automatically set to default.")
    return user_input


process_name_list = ["MuMuPlayer", "MuMuVMMHeadless"]
ccd_chosen = int(input_with_timeout("Choose CCD (0 for CCD0, 1 for CCD1, 2 for all) : ", 3, 0))

for process_name in process_name_list:
    print(f"\nWorking for {process_name}")
    process_count = count_process(process_name)

    if process_count == 0:
        print("No Such Process Found! Trying Next Process.")
    elif process_count > 0:
        set_affinity(process_name, process_count, ccd_chosen)
        print(f"Setting to ccd{ccd_chosen} Completed for {process_count} Instance(s).")

'''
thread에서 돌고 있는 input이 종료되지 않아서 다음 input이 있으면 thread input이 먼저 입력받고 그다음 여기 input이 입력됨.
multiprocessing은 생성한 프로세스에서 input 못 받음.
키보드 입력 구현은 포커스가 다른 창으로 넘어가면 문제 발생

'''

# a = input("\nhi?: ")
# print(f"at the end : {a}")

print("\nAll Process Completed! Terminal will close in 2 seconds.")
time.sleep(2)
sys.exit()
