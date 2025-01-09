# MuMu_CPUAfiinity
for AMD 7950X3D\
set MuMu App Player's Cpu Affinity to CCD(0, 1, all) cores\
if no input within 3 seconds, then CCD0 will be selected

inputTimeout.py\
subprocess를 바탕으로 구현. input_script.py 파일을 만들고 subprocess로 실행하여 input을 받음. timeout 시간이 지나면 input_script를 실행하고 있는 process를 terminate하고 default를 반환.
input_script에서 전달할 때는 stderr 채널을 통해 전달받음. pycharm과 windows에서는 사용자에게 출력되지 않는 것을 확인. 다른 OS, 다른 환경에서는 어떨지 모름. 더불어 다른 stderr 출력이 있다면 오작동 충분히 할 수 있음.

추가적인 input이 있다면 input에서 EOFError가 발생할 수 있음.