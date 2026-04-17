# AI Engineering Prompt: Recreate the Auralith Canvas Application

You are an expert AI software engineer specializing in Python, generative AI, and modern application architecture. Your task is to generate a complete, functional, and well-structured Python application based on the detailed requirements below. The application, named "Auralith Canvas," is a tool for creating images from images and text prompts.

---

## 🎯 Primary Objective

Create a Python application that allows a user to generate an images (.png, .jpg, .gif) from a single input image and a text prompt. The application must feature a web-based user interface and be built upon a modular, layered architecture.

---

## 🏗️ System Architecture

The application must be designed with a clear separation of concerns, following a layered architecture.
The application must be secure and make use of designer patterns. Use SOLID whenever possible.

### 1. Web Interface Layer (`src/web/`)
-   **File:** `app.py`
-   **Framework:** Gradio
-   **Functionality:**
    -   Provide a user-friendly web interface for interacting with the image generation process.
    -   Allow users to upload a single input image file (e.g., PNG, JPG).
    -   Include a text input field for users to provide a descriptive prompt for the desired image.
    -   Display the generated image prominently after the process is complete.
    -   Implement a "Generate" button to initiate the image creation.
    -   Integrate with the `LogStream` utility to display real-time feedback and progress messages to the user during generation.

### 2. Service Layer (`src/services/`)
-   **File:** `image_generation_service.py`
-   **Class:** `ImageGenerationService`
-   **Functionality:**
    -   Act as an intermediary between the Web Interface Layer and the AI Engine Layer.
    -   Receive the input image and text prompt from the web interface.
    -   Validate inputs to ensure they meet the requirements for the AI model.
    -   Call the AI Engine Layer to perform the image generation.
    -   Handle the saving of the generated image to a specified output directory.
    -   Manage the state of the generation process (e.g., "pending," "generating," "completed," "failed").
    -   Provide methods for logging status updates and errors using the `LogStream`.

### 3. AI Engine Layer (`src/scripts/`)
-   **File:** `ai_model_interface.py`
-   **Class:** `AIModelInterface`
-   **Functionality:**
    -   Encapsulate all interactions with the chosen AI image generation model.
    -   Provide a method, `generate_image(input_image_path: str, prompt: str) -> str`, which takes the path to an input image and a text prompt, and returns the path to the newly generated image.
    -   This method should load the AI model (e.g., a Stable Diffusion variant or similar capable of image-to-image generation guided by text).
    -   Perform necessary pre-processing on the input image and prompt for the model.
    -   Execute the model inference to generate the new image.
    -   Handle post-processing of the generated image (e.g., converting tensor to PIL Image, saving to disk).
    -   Abstract away the specifics of the AI model, allowing for easier swapping of models in the future.

### 4. Logging Utility (`src/web/`)
-   **File:** `log_stream.py`
-   **Class:** `LogStream`
-   **Functionality:**
    -   Create a class that can be used to stream log messages from the backend services to the Gradio UI in real-time.
    -   It should implement a generator (`stream_generator`) that yields log messages as they are added.
    
---

## ⚙️ Implementation Instructions

-   **Dependencies:** Use `gradio` for the web interface. For AI image generation, consider using popular libraries like `diffusers` (Hugging Face) with a pre-trained model capable of image-to-image generation (e.g., Stable Diffusion img2img). `Pillow` (PIL) will be essential for image manipulation.
-   **Project Structure:** Adhere strictly to the specified layered architecture and file organization.
-   **AI Model Selection:** Choose an open-source AI model that excels at generating new images based on an existing image and a text prompt. The model should be able to blend elements from the input image with the concepts described in the prompt.
-   **Asynchronous Processing:** Implement asynchronous handling for the image generation process to prevent the web interface from freezing during long-running AI tasks. Gradio's `gr.Interface` can often handle this with appropriate function signatures.
-   **Error Handling:** Implement robust error handling in all layers, providing informative messages to the user via the `LogStream` and the UI.
-   **Output Management:** Generated images should be saved to a designated output directory (e.g., `output/`) with unique filenames.

---

## 🔑 Key Requirements

-   **Modularity:** The code must be clean, well-commented, and organized into the specified layers.
-   **Functionality:** The final application must be fully functional and generate an animation as described.
-   **User Experience:** The web interface should be intuitive and provide feedback to the user during the generation process.
-   **Error Handling:** The application should handle potential errors gracefully (e.g., missing inputs, generation failures).

---

## 🚀 Final Output

Provide the complete, functional, and ready-to-use source code for the entire Auralith Canvas application, structured according to the specified architecture.
