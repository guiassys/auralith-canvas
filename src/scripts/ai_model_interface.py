import torch
from diffusers import StableDiffusionPipeline, StableDiffusionInstructPix2PixPipeline
from PIL import Image
from typing import Optional
from src.web.log_stream import LogStream

class AIModelInterface:
    def __init__(self, log_stream: Optional[LogStream] = None):
        self.log_stream = log_stream
        self.txt2img_pipe = None
        self.img2img_pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.instruct_model_id = "timbrooks/instruct-pix2pix"

    def _log(self, message):
        print(message)
        if self.log_stream:
            self.log_stream.log(message)

    def _load_txt2img_model(self):
        if self.txt2img_pipe is None:
            self._log("Loading text-to-image pipeline...")
            self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=self.dtype)
            self._configure_pipe(self.txt2img_pipe)

    def _load_img2img_model(self):
        if self.img2img_pipe is None:
            self._log("Loading InstructPix2Pix pipeline...")
            self.img2img_pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(self.instruct_model_id, torch_dtype=self.dtype)
            self._configure_pipe(self.img2img_pipe)

    def _configure_pipe(self, pipe):
        pipe.enable_vae_slicing()
        if self.device == "cuda":
            pipe.enable_model_cpu_offload()
        else:
            pipe.to(self.device)
        pipe.enable_attention_slicing()

    def generate_image(self, prompt: Optional[str], input_image_path: Optional[str], output_path: str, strength: float = 0.75, guidance_scale: float = 7.5, seed: int = 42):
        self._log("Generating image...")
        
        # The generator should be on the CPU when using model offloading
        generator_device = "cpu" if self.device == "cuda" else self.device
        generator = torch.Generator(device=generator_device).manual_seed(seed)

        try:
            if input_image_path:
                self._load_img2img_model()
                # Image processing: resize down if it's too large to prevent OOM
                input_image = Image.open(input_image_path).convert("RGB")
                
                # Max dimension to avoid OOM
                max_dim = 1024
                if input_image.width > max_dim or input_image.height > max_dim:
                    ratio = min(max_dim / input_image.width, max_dim / input_image.height)
                    new_size = (int(input_image.width * ratio), int(input_image.height * ratio))
                    # Ensure dimensions are multiples of 8 (required by UNet)
                    new_size = (new_size[0] - new_size[0] % 8, new_size[1] - new_size[1] % 8)
                    input_image = input_image.resize(new_size, Image.Resampling.LANCZOS)
                    self._log(f"Resized image to {new_size} to save VRAM.")
                else:
                    # Even if not resizing down, enforce multiple of 8
                    new_size = (input_image.width - input_image.width % 8, input_image.height - input_image.height % 8)
                    if new_size != (input_image.width, input_image.height):
                        input_image = input_image.resize(new_size, Image.Resampling.LANCZOS)

                self._log(f"Generating image with prompt: '{prompt or 'Default'}' and input image.")
                
                image_guidance_scale = 1.5 
                
                with torch.no_grad():
                    # Clear cache before generation
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()

                    generated_image = self.img2img_pipe(
                        prompt=prompt,
                        image=input_image,
                        image_guidance_scale=image_guidance_scale,
                        guidance_scale=guidance_scale,
                        generator=generator
                    ).images[0]
            else:
                self._load_txt2img_model()
                self._log(f"Generating image with prompt: '{prompt}'")
                
                with torch.no_grad():
                    # Clear cache before generation
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()

                    generated_image = self.txt2img_pipe(
                        prompt=prompt,
                        guidance_scale=guidance_scale,
                        generator=generator
                    ).images[0]

            generated_image.save(output_path)
            self._log(f"Image saved successfully to {output_path}")
            return output_path
        except Exception as e:
            self._log(f"Error during image generation: {e}")
            raise
