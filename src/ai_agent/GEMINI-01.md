# AI Engineering Prompt: Recreate the Auralith Canvas Application

You are an expert AI software engineer specializing in Python, generative AI, and modern application architecture. Your task is to generate a complete, functional, and well-structured Python application based on the detailed requirements below. The application, named "Auralith Canvas," is a tool for creating animations from images and text prompts.

---

## 🎯 Primary Objective

Create a Python application that allows a user to generate an animated video from a single input image and a text prompt. The application must feature a web-based user interface and be built upon a modular, layered architecture.

---

## 🏗️ System Architecture

The application must be designed with a clear separation of concerns, following a layered architecture.

### 1. Web Interface Layer (`src/web/`)
-   **Technology:** Gradio
-   **File:** `app.py`
-   **Functionality:**
    -   Provide a user-friendly interface with the title "Auralith Canvas".
    -   Include input fields for:
        -   `Project Name` (Textbox)
        -   `Scene Prompt` (Textbox)
        -   `Upload Initial Image` (Image Upload)
    -   Display a "GENERATE" button to trigger the animation process.
    -   Show a "Console" tab with a textbox for real-time logging and a progress bar.
    -   Display the final generated video and a download link upon completion.
    -   Implement a "Clear Inputs" button to reset the form.
-   **Styling:**
    -   Use a custom dark theme. Create a `ui_theme.py` file to define the theme and CSS.

### 2. Service Layer (`src/services/`)
-   **File:** `animation_service.py`
-   **Class:** `AnimationService`
-   **Functionality:**
    -   Act as an orchestrator between the web UI and the AI engine.
    -   Define a method `generate_animation(config, log_stream)` that takes a configuration dictionary (containing the project name, prompt, and image path) and a log stream object.
    -   Manage the animation generation process in a separate thread to keep the UI responsive.
    -   Handle file I/O, creating an output directory (`outputs/animations`) and saving the final video with a unique name.
    -   Provide robust error handling and log every step of the process.

### 3. AI Engine Layer (`src/scripts/`)
-   **File:** `animate_breathing_loop.py`
-   **Functionality:**
    -   Define a core function `generate_animation_scene(prompt, input_image, output_path)`.
    -   This function will encapsulate the logic for the AI-powered animation generation.
    -   **Models to Use:**
        -   `AnimateDiffPipeline` from `diffusers`.
        -   Motion Adapter: `guoyww/animatediff-motion-adapter-v1-5-2`
        -   Base Model: `emilianJR/epiCRealism`
        -   IP-Adapter: `h94/IP-Adapter` with `ip-adapter_sd15.bin` weights.
    -   **Generation Parameters:**
        -   `num_frames`: 16
        -   `guidance_scale`: 7.5
        -   `num_inference_steps`: 30
        -   `width`: 1024
        -   `height`: 576
    -   **Optimizations:**
        -   Enable VAE slicing and model CPU offload for memory efficiency.
    -   The script should also include a helper function `export_to_video` that uses `opencv-python` to save the generated frames as an `.mp4` file.

### 4. Logging Utility (`src/web/`)
-   **File:** `log_stream.py`
-   **Class:** `LogStream`
-   **Functionality:**
    -   Create a class that can be used to stream log messages from the backend services to the Gradio UI in real-time.
    -   It should implement a generator (`stream_generator`) that yields log messages as they are added.

---

## ⚙️ Implementation Instructions

1.  **Create the Project Structure:**
    -   Set up the directories as defined in the architecture section.
    -   Create empty `__init__.py` files where necessary to define Python packages.

2.  **Implement the AI Engine (`animate_breathing_loop.py`):**
    -   Write the `generate_animation_scene` function, loading the specified models and setting the generation parameters.
    -   Implement the `export_to_video` helper function.

3.  **Implement the Service Layer (`animation_service.py`):**
    -   Create the `AnimationService` class.
    -   The `generate_animation` method should call the `generate_animation_scene` function from the AI engine.
    -   Use Python's `threading` module to run the generation in a background thread.

4.  **Implement the Web Interface (`app.py`):**
    -   Build the Gradio UI as specified.
    -   The "GENERATE" button's click handler should:
        -   Instantiate the `AnimationService`.
        -   Call the `generate_animation` method in a new thread.
        -   Update the UI with real-time logs and progress from the `LogStream`.
        -   Display the final video when the generation is complete.

5.  **Create the `requirements.txt` file:**
    -   Include all necessary libraries: `gradio`, `torch`, `diffusers`, `transformers`, `opencv-python`, `numpy`.

6.  **Create a `README.md` file:**
    -   Provide a clear and concise overview of the project, its architecture, and instructions on how to run it.

---

## 🔑 Key Requirements

-   **Modularity:** The code must be clean, well-commented, and organized into the specified layers.
-   **Functionality:** The final application must be fully functional and generate an animation as described.
-   **User Experience:** The web interface should be intuitive and provide feedback to the user during the generation process.
-   **Error Handling:** The application should handle potential errors gracefully (e.g., missing inputs, generation failures).

---

## 🚀 Final Output

Provide the complete, functional, and ready-to-use source code for the entire Auralith Canvas application, structured according to the specified architecture.
