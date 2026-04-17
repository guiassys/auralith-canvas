# 🎧 Auralith Canvas

AI-powered Python tool to create stunning images from images and text prompts. Auralith Canvas is designed to be an intuitive platform for artists and creators to bring their static images to life.

---

# 🎯 Objective

To create an automated pipeline capable of:

1.  Generating images from a single image and a text prompt.
2.  Providing a simple, web-based interface for easy interaction.
3.  Structuring the system in a modular, layered architecture for scalability.
4.  Producing high-quality outputs ready for publishing.

---

# 🏗️ System Architecture

Auralith Canvas is built as a modular, AI-based multimedia generation pipeline.

## 🔹 System Layers

### 1. Generation Layer
The core AI engine (`src/scripts/ai_model_interface.py`), responsible for receiving prompts and configurations, interacting with generation models, and returning the raw generated image.

### 2. Service Layer
The business logic orchestrator (`src/services/image_generation_service.py`), which bridges the web interface and the generation layer. It handles file naming, directory creation, threading, and logging.

### 3. Web Interface Layer
The user-facing Gradio application (`src/web/app.py`). It provides a modern, DAW-inspired UI with real-time log streaming, progress tracking, and input validation.

### 4. Output Layer
The final destination for generated assets. It structures the outputs by saving generated images with timestamps and optional user-defined suffixes inside the designated output directory.

## 🔄 System Flow

1. **User Input:** The user provides a text prompt, an optional initial image, and configuration settings (e.g., strength, guidance scale, seed) via the Gradio UI.
2. **Service Request:** The UI triggers the `ImageGenerationService`, passing all the configurations.
3. **Execution:** The service locks the process to ensure single-threaded execution, formatting the expected output file path, and calls the `AIModelInterface`.
4. **Generation:** The AI Model generates the image, streaming status logs back to the UI in real-time.
5. **Completion:** The generated image is saved to disk, and the path is returned to the UI, which updates the view with the final image and success logs.

---

# ⚙️ How to Run the Project

## Developer Installation (WSL + Ubuntu)
```bash
cd ~/devtools/repos/auralith-canvas
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run_web.py
```

## Quick Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_web.py
```

## Via Web Interface (Gradio)
```bash
python src/web/app.py
```
Access the interface at: http://localhost:7860

**Web Interface:**
The interface provides three main tabs:
- **🎨 Image Generation:** For inputting your prompt and initial image.
- **⚙️ Settings:** To adjust generation parameters and output directories.
- **🖥️ Console:** To monitor the generation process via real-time logs and preview the final result.

## Result
The generated file will be saved in the `outputs` directory (or custom output directory defined in the settings).

---

# 📁 Project Structure

```
auralith-canvas/
├── src/
│   ├── ai_agent/         # AI configuration and prompts
│   │   └── GEMINI-01.md
│   ├── services/         # Application layer orchestrator
│   │   └── image_generation_service.py
│   ├── scripts/          # Generation pipeline (AI Model integration)
│   │   └── ai_model_interface.py
│   └── web/              # Web interface implementation
│       ├── app.py
│       ├── log_stream.py
│       ├── run_web.py
│       └── ui_theme.py
├── outputs/              # Default destination for generated files
├── .gitignore
├── requirements.txt      # Python dependencies
├── config.json           # Default user configuration file
├── temp_install.py       # Installation utilities
├── run_web.py            # Entry point for the Gradio application
└── README.md
```

---

# 📦 Requirements

- Python 3.10+
- A compatible GPU (NVIDIA recommended for optimal generation times)
- Dependencies listed in `requirements.txt` (including Gradio and Torch)

---

# 🚧 Project Status

Actively in development. Currently supporting static image generation from prompts and initial images with a functional Gradio interface.

---

# 🌌 Vision

To evolve into a comprehensive toolkit for AI-driven visual creation, eventually expanding to incorporate video generation, advanced style transfers, and seamless integration with other creative software ecosystems.

---

# 📄 License

This project is proprietary and confidential.  
All rights reserved.