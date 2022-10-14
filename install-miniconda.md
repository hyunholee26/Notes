1. miniconda를 설치한다.
 - 다운로드 받아서 sftp로 올리고, 명령어를 실행
 - wget으로 받기
 - sudo apt 등등

2. source ~/.bashrc를 실행해서 설치한 miniconda를 프롬프트로 반영한다.

3. 가상환경을 생성한다.

conda create -n [가상환경이름] python=[버전]

4. 가상환경을 활성화한다

conda activate [가상환경이름]

5. conda install 등을 활용하여 설치한다. 

6. conda install python으로 파이썬 버전 추가 설치 가능함
