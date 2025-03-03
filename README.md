# MineGuide
It is a guide for Minecraft.
Based on the fear that humans have of the unknown, I created a guide that generates an overview of what we see in our field of vision.

人間が未知のものに抱く恐怖から、視界に映るものについて概要を生成するガイドを作成。

Minecraft was chosen because it utilizes a virtual world to conduct experiments and then uses the results to solve real-world problems.

仮想世界を活用して実験を行い、その成果を現実世界の課題解決に役立てることからマインクラフトを選択。

This project was produced in class and used AzureOpenAI provided for the LLM.

このプロジェクトは授業の中で製作したためLLMには提供された AzureOpenAI を使用。

![demo](./demo/demo.png)

## Initialize
**Installation**
```bash
python -m venv .venv
.venv/Scripts/activate
git clone https://github.com/mai-Den06/MineGuide.git
python -m pip install -U pip
pip install -r requirements.txt
```

**Get your minecraft window name**
```bash
python show_window_names.py
```

**Create .env**
```python
API_KEY='your_api_key'
ENDPOINT='your_endpoint'
```

**Set config/setting.py**
```
# guide
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
API_VERSION = 'your_api_version'
MODEL = "gpt-4o"

# window capture
WINDOW_NAME = 'your_minecraft_window_name'
```

**Create database**
```bash
python db_init.py
```

## Usage
**Launch**
```bash
python main.py
```
**Stop**
```
click "⛔" in overlay
```

## About Object Detection Model
The object detection model was trained using [YOLOv11](https://github.com/ultralytics/ultralytics "github").
This model is only available for ore.
This model only supports default textures.

物体検出モデルの学習に[YOLOv11](https://github.com/ultralytics/ultralytics "github")を使用。
このモデルは鉱石にのみ使用可能。
このモデルはデフォルトのテクスチャにのみ対応。

### About Dataset
The dataset used for the training is [here](https://universe.roboflow.com/mineguide/minecraft-ore-detection "roboflow").

学習に用いたデータセットは[こちら](https://universe.roboflow.com/mineguide/minecraft-ore-detection "roboflow")。

## Notes  
Since this project uses an LLM without frameworks like LangChain, there is a risk of generating hallucinations.  

このプロジェクトはLLMを使用しているが、LangChainのようなフレームワークを使用していないため、ハルシネーションを生成するリスクがある。
