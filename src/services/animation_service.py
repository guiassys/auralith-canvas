"""Animation Service to encapsulate the business logic for video generation."""

import logging
import os
import threading
import time
from typing import Optional, Dict, Any

from src.scripts.animate import generate_animation_scene
from src.web.log_stream import LogStream
from PIL import Image

logger = logging.getLogger(__name__)

class AnimationService:
    """
    Service that encapsulates animation generation.
    Orchestrates the web interface and the AI engine.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._lock = threading.Lock()

    def generate_animation(
        self,
        config: Dict[str, Any],
        log_stream: Optional[LogStream] = None
    ) -> Dict[str, Any]:
        """
        Executes the animation generation pipeline with log streaming.
        Ensures only one animation is generated at a time.
        """
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[SERVICE] {message}")
            if log_stream:
                log_stream.log(message, level)

        with self._lock:
            start_time = time.time()
            try:
                # Extract base parameters
                project_name = config.get('name')
                prompt = config.get('prompt')
                image_path = config.get('image_path')
                
                # Extract nested settings with defaults
                animation_settings = config.get('animation_settings', {})
                generator_settings = config.get('generator_settings', {})
                output_dir_from_config = config.get('output_directory', self.output_dir)

                if not prompt:
                    raise ValueError("A prompt is required.")

                _log(f"Starting animation process for project: {project_name or 'Unnamed'}")
                _log(f"Using configuration: {config}")

                input_image = None
                if image_path:
                    input_image = Image.open(image_path).convert("RGB")
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                
                if project_name:
                    output_filename = f"{project_name}.mp4"
                else:
                    output_filename = f"{timestamp}_v01_gen.mp4"

                # Ensure the output directory from the UI exists
                os.makedirs(output_dir_from_config, exist_ok=True)
                output_path = os.path.join(output_dir_from_config, output_filename)

                # Pass all relevant settings to the animation script
                generate_animation_scene(
                    prompt=prompt,
                    input_image=input_image,
                    output_path=output_path,
                    log_stream=log_stream,
                    animation_settings=animation_settings,
                    generator_settings=generator_settings
                )

                end_time = time.time()
                processing_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))

                _log(f"Total processing time: {processing_time}")
                _log(f"Success! Animation saved to: {os.path.basename(output_path)}")

                return {
                    "success": True,
                    "file_path": output_path,
                    "error": None
                }

            except Exception as e:
                error_msg = f"Processing failure: {str(e)}"
                _log(error_msg, level="ERROR")
                logger.error(f"[SERVICE] {error_msg}", exc_info=True)

                return {
                    "success": False,
                    "file_path": None,
                    "error": error_msg
                }
