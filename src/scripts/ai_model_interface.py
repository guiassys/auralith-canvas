import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
from typing import Optional
from src.web.log_stream import LogStream

class AIModelInterface:
    def __init__(self, log_stream: Optional[LogStream] = None):
        self.log_stream = log_stream
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

    def _log(self, message):
        print(message)
        if self.log_stream:
            self.log_stream.log(message)

    def load_model(self):
        if self.pipe is None:
            self._log("Loading diffusion pipeline...")
            model_id = "runwayml/stable-diffusion-v1-5"
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=self.dtype)

            self.pipe.enable_vae_slicing()
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
            else:
                self.pipe.to(self.device)

            self.pipe.enable_attention_slicing()

    def generate_image(self, prompt: str, input_image_path: str, output_path: str, strength: float = 0.75, guidance_scale: float = 7.5):
        self._log("Generating image...")
        self.load_model()

        try:
            input_image = Image.open(input_image_path).convert("RGB")
            
            self._log(f"Generating image with prompt: '{prompt}'")
            
            # The generator should be on the CPU when using model offloading
            generator_device = "cpu" if self.device == "cuda" else self.device
            generator = torch.Generator(device=generator_device).manual_seed(42)

            with torch.no_grad():
                generated_image = self.pipe(
                    prompt=prompt,
                    image=input_image,
                    strength=strength,
                    guidance_scale=guidance_scale,
                    generator=generator
                ).images[0]

            generated_image.save(output_path)
            self._log(f"Image saved successfully to {output_path}")
            return output_path
        except Exception as e:
            self._log(f"Error during image generation: {e}")
            raise
