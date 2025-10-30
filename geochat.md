## Install
  1. Clone this repository and navigate to GeoChat folder
  ```
  git clone https://github.com/mbzuai-oryx/GeoChat.git
  cd GeoChat
  ```

  2. Install Package
  ```
  conda create -n geochat python=3.10 -y
  conda activate geochat
  pip install --upgrade pip  # enable PEP 660 support
  pip install -e .
  ```

  3. Install additional packages for training cases
  ```
  pip install ninja
  pip install flash-attn --no-build-isolation
  ```

  4. Upgrade to latest code base
  ```
  git pull
  pip uninstall transformers
  pip install -e .
  ```
  
  5. Model download
  ```
  pip install huggingface_hub
  huggingface-cli download MBZUAI/geochat-7B --local-dir .
  ```
