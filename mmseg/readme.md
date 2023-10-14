### mmsegmentation v1.0을 바탕으로 custom dataset을 적용하기 위한 삽질 정리기

### 환경설정 및 설치하기 주요 명령어
- miniconda 설치
- conda create --name [가상환경이름] python=3.9 -y // 가상환경 with python
- pip install torch==1.8.1+cu101 torchvision==0.9.1+cu101 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html // 파이토치설치, 버전확인 필요!
- pip install -U openmim
- mim install mmengine
- mim install "mmcv>=2.0.0"
- mim install mmdet
- git clone -b main https://github.com/open-mmlab/mmsegmentation.git // 소스 코드를 일부 고쳐야하므로, mim install을 하지 않고 소스로 설치하고 소스 수정!
- cd mmsegmentation
- pip install -v -e .

### 소스 수정해야할 부분
- 기본적으로 custom기능을 추가하기 위해서 tutorial을 참고해야함
- dataset: cityscapes와 같이 기존 dataset소스코드를 참고하여, 파일을 만들고, __init__.py에 등록
- transform: 역시 유사하게 기존 파일을 참고하여, 파일을 만들고, __init__.py에 등록
- 참고사항1. dataset->transform이후에 transform마지막 단계에서 특이하게 PackSegInputs이라는 방식으로 데이터가 묶임. 자세한 내용은 tutorial 참고
- PackSegInputs로 묶인 것을 model의 입력으로 처리하기 위해 data_preprocessor를 통과함. base, img, seg 세가지가 있는데, custome data에 적합하지 않은 경우가 있어, 기존 소스코드를 참고하여 customed data_preprocessor를 추가함
- loss계산시 모델의 예측값을 post processing하는 모듈이 있는데, 역시 custom dataset에 맞지 않는 부분을 수정해야함, 나의 경우 resize()함수를 주석처리함
- ignore_index를 주의 깊게 확인해야함
