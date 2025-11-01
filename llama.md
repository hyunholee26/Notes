conda create -n llama python=3.10 -y
conda activate llama

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install huggingface_hub 

