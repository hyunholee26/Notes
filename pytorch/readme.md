### 파이토치 설치 및 구조 파악 팁

1. miniconda를 설치한다.

2. nvidia-smi명령어를 이용하여 설치된 CUDA driver 버전을 확인한다.
 - CUDA driver가 설치되어 있지 않으면, GPU에 맞는 드라이버를 설치 (GPU 카드 버전 - CUDA drvier 버전 - pytorch 버전 순으로 확인)
 - CUDA driver에 맞는 pytorch 버전을 설치 (https://pytorch.org/get-started/previous-versions/)


conda install python=3.6

- 파이토치: pip install torch==1.8.1+cu101 torchvision==0.9.1+cu101 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

- gdal: conda install -c conda-forge gdal

- esda: pip install esda

3. pytorch 프레임워크는 밑바닥부터 시작하는 딥러닝 3권을 보면 도움이 많이 됨

4. Dataset - Dataloader - Model - train.py 순으로 파악하면 됨, 
 - preprocressing, 결측치 처리, normalization 등 검토 필요
 - 파이토치 튜토리얼: https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
 - 튜토리얼 설명이 자세하지 않은 경우, 직접 코드를 확인하는 것이 도움이 많이 됨, 파이토치 깃허브: https://github.com/pytorch
 
 ### 리눅스 명령어 모음
 
 - GPU 체크 : nvidia-smi
 - GPU 프로세스 kill : nvidia-smi | grep 'python' | awk '{ print $3 }' | xargs -n1 kill -9

 - 텐서보드 실행: tensorboard --logdir=./outputs
 - 텐서보드 종료: kill $(ps -e | grep 'tensorboard' | awk '{print $1}')

 - 파이썬 백그라운드 : nohup python -u run_experiment.py > log-HSV-validx-DiceBCELoss-512.out &
 - 백그라운드 파이썬 종료 : kill $(ps -ef | grep 'run_experiment.py' | awk '{print $2}')
 - 백그라운드 파이썬 조회 : select : ps -ef | grep 'run_experiment.py'
 - 백그라운드 파이썬 출력 : tail -f 파일명
 - 스토리지 용량 : du -h --max-depth=1
 - 기타
   - show user PID regarding GPU : fuser -v /dev/nvidia*
   - kill PID :kill -9 PID

### conda 명령어
복제
conda create -n py39_test_clone --clone py39

삭제
conda info --envs
conda remove --name [가상환경명] --all

