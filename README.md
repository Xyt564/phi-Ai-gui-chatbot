# Phi-2 Chatbot GUI

A **lightweight, CPU-optimized AI chatbot GUI** built with **CustomTkinter**, designed to run **locally on modest hardware**.

This app uses the **Phi-2 model (`phi-2.Q4_K_M.gguf`)**, optimized for my hardware:

* **CPU:** 12th Gen Intel i3-1215U (8 threads, up to 4.4 GHz)
* **GPU:** Integrated Intel UHD Graphics (CPU inference only)
* **RAM:** 8 GB DDR4

> Due to these hardware limits, the code is optimized to run mainly on CPU, with smaller context, fewer tokens, and conservative parameters. If you have a stronger system, you can use bigger models by changing the model name and adjusting parameters.

---

## Features

* **Interactive chat GUI** with timestamped messages.
* **Lightweight and optimized** for CPU-only systems.
* **History tracking** with adjustable length.
* **Clear and save chat** functionality.
* **Dark mode UI** using CustomTkinter.
* **Model-agnostic**: replace the `.gguf` model with other compatible LLaMA-like GGUF models.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/Xyt564/phi-Ai-gui-chatbot.git
cd phi-Ai-gui-chatbot
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

> The `requirements.txt` includes:
>
> * `customtkinter` — for the modern GUI
> * `llama-cpp-python` — for local model inference

3. **Download the Phi-2 model**:

The Phi-2 model (`phi-2.Q4_K_M.gguf`, ~1.8 GB) **cannot be included** in the repo because of GitHub size limits.
Download it here:

**[Phi-2 Q4_K_M GGUF Model on Hugging Face](https://huggingface.co/codegood/phi-2-Q4_K_M-GGUF/tree/main)**

Save the `.gguf` file in a folder of your choice (e.g., `models/`).

4. **Update the model path in the code**:

Open `chatbot.py` and set:

```python
MODELS_DIR = Path("YOUR_MODELS_FOLDER")  # Folder containing the model
MODEL_FILE = "phi-2.Q4_K_M.gguf"        # Model file name
```

Example:

```python
# Windows
MODELS_DIR = Path("C:/Users/YourName/Downloads/models")

# macOS/Linux
MODELS_DIR = Path("/Users/yourname/Downloads/models")
```

> Make sure the folder exists and contains the `.gguf` model file. The app will automatically locate it using `find_model_file()`.

5. **Run the chatbot**:

```bash
python chatbot.py
```

The app will load the model (this may take a minute) and launch the GUI.

---

## Usage

1. Type your message in the input field and press **Enter** or click **Send**.
2. The AI response will appear with a timestamp.
3. **Clear Chat** resets the conversation.
4. **Save Chat** exports the conversation as a `.txt` file.
5. Adjust parameters like `MAX_TOKENS`, `HISTORY_LENGTH`, or `TEMPERATURE` in `chatbot.py` for different performance or response length.

---

## Using Bigger Models

If you have better hardware than mine (more RAM, stronger CPU/GPU):

1. Download a larger AI model such as an 8b or 12b one.
2. Place it in the models folder.
3. Update `MODEL_FILE` and `MODELS_DIR` in `chatbot.py` so the python code can get to the AI.
4. Optionally increase `MAX_TOKENS` and `HISTORY_LENGTH` for longer, more detailed conversations (If your hardware can take it).

> On my 8GB i3 setup, these settings are deliberately reduced for stability and CPU efficiency. Bigger models may require more RAM and stronger CPUs.

---

## File Structure

```
phi-Ai-gui-chatbot/
├── chatbot.py           # Main application script
├── requirements.txt     # Dependencies
└── models/              # Folder for Phi-2 .gguf model (Or whatever model you chose)
```

---

## License

This project is licensed under the **MIT License**, one of the most permissive and widely used open-source licenses. Below is the full text:

```
MIT License

Copyright (c) 2026 Xyt564

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> In short: You can use, modify, and redistribute the software freely, but you must include this copyright and license notice. The software is provided “as-is,” without warranty.

---
