"""Image Generation Service to encapsulate the business logic for image creation."""

import logging
import os
import threading
import time
from typing import Optional, Dict, Any

from src.scripts.ai_model_interface import AIModelInterface
from src.web.log_stream import LogStream

logger = logging.getLogger(__name__)

class ImageGenerationService:
    """
    Service that encapsulates image generation.
    Orchestrates the web interface and the AI engine.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._lock = threading.Lock()
        self.ai_model = None

    def _get_model(self, log_stream: Optional[LogStream] = None) -> AIModelInterface:
        if self.ai_model is None:
            self.ai_model = AIModelInterface(log_stream=log_stream)
        return self.ai_model

    def generate_image(
        self,
        config: Dict[str, Any],
        log_stream: Optional[LogStream] = None
    ) -> Dict[str, Any]:
        """
        Executes the image generation pipeline with log streaming.
        Ensures only one image is generated at a time.
        """
        def _log(message: str, level: str = "INFO"):
            logger.info(f"[SERVICE] {message}")
            if log_stream:
                log_stream.log(message, level)

        with self._lock:
            start_time = time.time()
            try:
                prompt = config.get('prompt')
                image_path = config.get('image_path')
                output_dir_from_config = config.get('output_directory', self.output_dir)

                if not prompt and not image_path:
                    raise ValueError("A prompt or an input image is required.")

                _log(f"Starting image generation process...")
                _log(f"Using configuration: {config}")

                ai_model = self._get_model(log_stream)

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_filename = f"{timestamp}_generated_image.png"
                
                os.makedirs(output_dir_from_config, exist_ok=True)
                output_path = os.path.join(output_dir_from_config, output_filename)

                generated_image_path = ai_model.generate_image(
                    prompt=prompt,
                    input_image_path=image_path,
                    output_path=output_path,
                    strength=config.get('strength', 0.75),
                    guidance_scale=config.get('guidance_scale', 7.5),
                    seed=config.get('seed', 42)
                )

                end_time = time.time()
                processing_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))

                _log(f"Total processing time: {processing_time}")
                _log(f"Success! Image saved to: {os.path.basename(generated_image_path)}")

                return {
                    "success": True,
                    "file_path": generated_image_path,
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
