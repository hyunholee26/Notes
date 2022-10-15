1. miniconda를 설치한다.

2. nvidia-smi명령어를 이용하여 설치된 CUDA driver 버전을 확인한다.
 - CUDA driver가 설치되어 있지 않으면, GPU에 맞는 드라이버를 설치 (GPU 카드 버전 - CUDA drvier 버전 - pytorch 버전 순으로 확인)
 - CUDA driver에 맞는 pytorch 버전을 설치 (https://pytorch.org/get-started/previous-versions/)

3. pytorch 프레임워크는 밑바닥부터 시작하는 딥러닝 3권을 보면 도움이 많이 됨

4. Dataset - Dataloader - Model - Optimizer 순으로 파악하면 됨, 
 - 파이토치 튜토리얼: https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
 - 튜토리얼 설명이 자세하지 않은 경우, 직접 코드를 확인하는 것이 도움이 많이 됨, 파이토치 깃허브: https://github.com/pytorch
