"""
Professional Web Interface for Auralite using Gradio with a DAW-inspired,
dark-themed layout and real-time log streaming.
"""
import gradio as gr
import logging
import os
import threading
import time
import base64
import json
from src.services.image_generation_service import ImageGenerationService
from src.web.log_stream import LogStream
from src.web.ui_theme import auralite_theme, custom_css

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Load Configuration ---
def load_config():
    """Loads the application configuration from config.json."""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("config.json not found. Using default settings.")
        return {
            "image_settings": {
                "strength": 0.75,
                "guidance_scale": 7.5,
                "seed": 42
            },
            "output_directory": "outputs/images",
            "output_filename_suffix": "",
            "web_settings": {
                "server_port": 7860
            }
        }

config = load_config()
output_dir = config.get("output_directory", "outputs/images")
server_port = config.get("web_settings", {}).get("server_port", 7860)
server_host = config.get("web_settings", {}).get("server_host", "0.0.0.0")

# --- Service Initialization ---
image_generation_service = ImageGenerationService(output_dir=output_dir)

# --- Helper Functions ---
def get_image_html(image_path):
    """Encodes image to Base64 and returns an HTML image tag."""
    if not os.path.exists(image_path):
        return "<div>Image not found.</div>"
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    return f'<img src="data:image/png;base64,{encoded_string}" style="width:100%; height:auto;">'

# --- UI DEFINITION ---
def create_ui():
    """Builds the Gradio Blocks UI for Auralite Canvas."""
    with gr.Blocks(
            title="Auralite Canvas",
            theme=auralite_theme,
            css=custom_css
    ) as demo:
        # --- Header ---
        with gr.Row(elem_classes=["header"]):
            gr.Markdown("## 🎨 Auralite Canvas", elem_id="logo")
            with gr.Column(scale=3):
                progress_bar = gr.Slider(label="Rendering Progress", value=0, interactive=False, elem_classes=["glowing-progress"])
        
        with gr.Row():
            # --- Main Workspace ---
            with gr.Column(scale=5):
                with gr.Tabs() as tabs:
                    # --- Tab 1: Image Generation ---
                    with gr.TabItem("🎨 Image Generation", id=0):
                        with gr.Group():
                            prompt_input = gr.Textbox(label="Scene Prompt", placeholder="e.g., A beautiful angel flying through the clouds", lines=3)
                            image_upload = gr.Image(label="Upload Initial Image", type="filepath")

                    # --- Tab 2: Settings ---
                    with gr.TabItem("⚙️ Settings", id=1):
                        gr.Markdown("### Image Settings")
                        with gr.Row():
                            strength = gr.Slider(label="Strength", minimum=0, maximum=1, step=0.05, value=config.get("image_settings", {}).get("strength", 0.75))
                            guidance_scale = gr.Slider(label="Guidance Scale", minimum=1, maximum=20, step=0.5, value=config.get("image_settings", {}).get("guidance_scale", 7.5))
                            seed_input = gr.Number(label="Seed", value=config.get("image_settings", {}).get("seed", 42), precision=0, minimum=-1)

                        gr.Markdown("### Output Settings")
                        output_directory_input = gr.Textbox(label="Output Directory", value=config.get("output_directory", "outputs"))
                        output_suffix_input = gr.Textbox(label="Output Filename Suffix", value=config.get("output_filename_suffix", ""))


                    # --- Tab 3: Console & Output ---
                    with gr.TabItem("🖥️ Console", id=2):
                        status_output = gr.Textbox(label="AI Engine Status", lines=15, interactive=False, elem_classes=["terminal-box"])
                        with gr.Row():
                            file_output = gr.File(label="Download Image", visible=False)
                            image_preview = gr.HTML(label="Image Preview", visible=False)

            # --- Sidebar ---
            with gr.Column(scale=1, min_width=100):
                # --- Global Action Buttons Moved Here ---
                gr.Markdown("### 🚀 Actions")
                clear_btn = gr.Button("🗑️ Clear Inputs")
                generate_btn = gr.Button("🚀 GENERATE", variant="primary")


        # --- Event Handling & Logic ---
        def run_generation(prompt, image, 
                           # Image Settings
                           strength_val, guidance_val, seed_val,
                           # Output Settings
                           output_dir_ui, output_suffix_ui):
            """Handles the image generation process and UI updates."""
            if not prompt and not image:
                gr.Warning("A prompt or an initial image is required to generate an image.")
                yield {
                    tabs: gr.update(selected=0),
                    status_output: "Error: A prompt or an initial image is required.",
                    generate_btn: gr.update(interactive=True),
                    clear_btn: gr.update(interactive=True),
                }
                return

            # Switch to console tab and lock UI
            yield {
                tabs: gr.update(selected=2),
                status_output: "Initializing image generation...",
                generate_btn: gr.update(interactive=False, value="Generating..."),
                clear_btn: gr.update(interactive=False),
                progress_bar: gr.update(value=0, label="Rendering... 0%")
            }

            log_stream = LogStream()
            log_history = []
            
            # Assemble config from UI inputs
            gen_config = {
                "prompt": prompt, 
                "image_path": image,
                "strength": strength_val,
                "guidance_scale": guidance_val,
                "seed": int(seed_val),
                "output_directory": output_dir_ui,
                "output_filename_suffix": output_suffix_ui
            }

            # Update service's output directory if it has changed
            image_generation_service.output_dir = output_dir_ui

            generation_task_result = {"result": None}
            def generation_task():
                try:
                    result = image_generation_service.generate_image(config=gen_config, log_stream=log_stream)
                    generation_task_result["result"] = result
                finally:
                    log_stream.end()

            thread = threading.Thread(target=generation_task)
            thread.start()

            # Stream logs and update progress
            for i, log_message in enumerate(log_stream.stream_generator()):
                log_history.append(log_message)
                progress_val = min(0.95, (i + 1) / 20) # Simplified progress
                progress_label = f"Rendering... {int(progress_val * 100)}%"
                yield {
                    status_output: "\n".join(log_history),
                    progress_bar: gr.update(value=progress_val, label=progress_label)
                }
                time.sleep(0.1)

            thread.join()
            result = generation_task_result["result"]

            # Final UI update
            if result and result["success"]:
                image_html = get_image_html(result["file_path"])
                log_history.append(f"✅ Generation successful! Output: {result['file_path']}")
                yield {
                    tabs: gr.update(selected=2),
                    status_output: "\n".join(log_history),
                    file_output: gr.update(value=result["file_path"], visible=True),
                    image_preview: gr.update(value=image_html, visible=True),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=1, label="Rendering Complete")
                }
            else:
                error_msg = result.get('error', "An unknown error occurred.") if result else "An unknown error occurred."
                log_history.append(f"❌ ERROR: {error_msg}")
                gr.Error(f"Generation Failed: {error_msg}")
                yield {
                    tabs: gr.update(selected=2),
                    status_output: "\n".join(log_history),
                    generate_btn: gr.update(interactive=True, value="🚀 GENERATE"),
                    clear_btn: gr.update(interactive=True),
                    progress_bar: gr.update(value=0, label="Rendering Failed")
                }
        
        # List of all setting components
        setting_inputs = [
            strength, guidance_scale, seed_input,
            output_directory_input, output_suffix_input
        ]

        generate_btn.click(
            fn=run_generation,
            inputs=[prompt_input, image_upload] + setting_inputs,
            outputs=[tabs, status_output, generate_btn, clear_btn, progress_bar, file_output, image_preview]
        )

        def clear_form():
            """Resets all input fields to their default state."""
            return {
                prompt_input: "",
                image_upload: None,
                status_output: "",
                file_output: gr.update(visible=False),
                image_preview: gr.update(value=None, visible=False),
                progress_bar: gr.update(value=0, label="Rendering Progress"),
            }

        clear_btn.click(fn=clear_form, outputs=[
            prompt_input, image_upload, status_output, file_output, image_preview, progress_bar
        ])

    return demo

# --- Main Execution ---
interface = create_ui()

if __name__ == "__main__":
    interface.launch(
        server_name=server_host,
        server_port=server_port,
        show_error=True
    )
