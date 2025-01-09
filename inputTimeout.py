import subprocess, os

# input_script.py 없으면 생성
if not os.path.exists("input_script.py"):
    command = "import sys\n\nuser_input = input("")  # 입력값 받기\nprint(user_input, file=sys.stderr, end='')"
    with open("input_script.py", "w", encoding="utf-8") as f:
        f.writelines(command)

def input_with_timeout(prompt : str, timeoutsec : int, default=None, timeout_alert = True):
    """
    Reads input from the user with a specified timeout. If the timeout is exceeded,
    a default value is returned, and an optional alert can be displayed.
    The function executes an external script (`input_script.py`) to handle user input.

    :param prompt: The input prompt displayed to the user.
    :type prompt: str
    :param timeoutsec: The number of seconds before input times out.
    :type timeoutsec: int
    :param default: The default value returned if a timeout occurs.
    :type default: Any
    :param timeout_alert: If True, a timeout alert message is printed.
    :type timeout_alert: bool
    :return: The user input if provided within the timeout period, or the default value.
    :rtype: Any
    """
    print(prompt, end='', flush=True)
    user_input = default

    user_input_process = subprocess.Popen(
        ["python", "input_script.py"],  # 실행할 하위 스크립트 명령
        # stdin=sys.stdin,
        stdout=subprocess.PIPE,  # 표준 출력을 캡처
        stderr=subprocess.PIPE,  # 표준 에러를 캡처 (필요시 사용)
        text=True,  # 문자열 모드 활성화
        encoding="utf-8"
    )

    try:
        stdout_data, stderr_data = user_input_process.communicate(timeout=timeoutsec)

        # 저장된 값을 변수에 할당
        user_input = stderr_data.strip()
        # print("Output from subprocess' stdout:", stdout_data.strip())
        # print("Output from subprocess' stderr:", stderr_data.strip())

    except subprocess.TimeoutExpired:
        user_input = default
        print(user_input)
        if timeout_alert:
            print("\nTimeout occurred. Default value chosen.")
        user_input_process.terminate()

    return user_input