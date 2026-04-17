import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from PIL import Image
import os
import cv2
import numpy as np
from typing import Optional, Dict, Any
from src.web.log_stream import LogStream

def export_to_video(frames, output_path, fps, log_stream: Optional[LogStream] = None):
    """Exports a list of PIL Images to a video file."""
    def _log(message):
        print(message)
        if log_stream:
            log_stream.log(message)

    _log(f"Exporting video to {output_path}...")
    if not frames:
        _log("No frames to export.")
        return

    first_frame = frames[0]
    width, height = first_frame.size
    # Video codecs often require even dimensions
    if width % 2 != 0: width -= 1
    if height % 2 != 0: height -= 1

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not writer.isOpened():
        raise IOError(f"Could not open video writer for path {output_path}.")

    for frame in frames:
        # Resize frame if it doesn't match the writer's dimensions
        if frame.size != (width, height):
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
        
        frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

    writer.release()
    _log("Video saved successfully.")

def generate_animation_scene(
    prompt: str,
    input_image: Optional[Image.Image],
    output_path: str,
    log_stream: Optional[LogStream] = None,
    animation_settings: Optional[Dict[str, Any]] = None,
    generator_settings: Optional[Dict[str, Any]] = None # Keep for future use
):
    """Generates a single animation scene using parameters passed from the service."""
    def _log(message):
        print(message)
        if log_stream:
            log_stream.log(message)

    # Use provided settings or default to an empty dict
    anim_config = animation_settings or {}

    # Extract parameters from the settings dictionary with default values
    total_frames = int(anim_config.get('total_frames', 160))
    frames_per_chunk = int(anim_config.get('frames_per_chunk', 16))
    guidance_scale = float(anim_config.get('guidance_scale', 7.5))
    num_inference_steps = int(anim_config.get('num_inference_steps', 40))
    width = int(anim_config.get('width', 1024))
    height = int(anim_config.get('height', 576))
    fps = int(anim_config.get('fps', 12))
    ip_adapter_scale = float(anim_config.get('ip_adapter_scale', 0.7))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    
    _log("Loading motion adapter...")
    adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=dtype)
    _log("Loading diffusion pipeline...")
    model_id = "emilianJR/epiCRealism"
    pipe = AnimateDiffPipeline.from_pretrained(model_id, motion_adapter=adapter, torch_dtype=dtype)
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, beta_schedule="linear", timestep_spacing="linspace")

    if input_image:
        _log("IP-Adapter enabled. Loading IP-Adapter weights...")
        pipe.load_ip_adapter("h94/IP-Adapter", subfolder="models", weight_name="ip-adapter_sd15.bin")
        pipe.set_ip_adapter_scale(ip_adapter_scale)
    else:
        _log("No initial image provided. IP-Adapter will be disabled.")

    pipe.enable_vae_slicing()
    if device == "cuda":
        pipe.enable_model_cpu_offload()

    negative_prompt = "bad quality, worse quality, low resolution, blurry, noisy, distorted, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face"

    _log(f"Generating animation with prompt: '{prompt}'")
    generator = torch.Generator("cpu" if device == "cuda" else device).manual_seed(42)
    
    all_frames = []
    current_image = input_image
    
    num_chunks = max(1, total_frames // frames_per_chunk)

    for i in range(num_chunks):
        _log(f"Generating chunk {i+1}/{num_chunks}...")
        
        pipe_kwargs = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_frames": frames_per_chunk,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
            "generator": generator,
            "width": width,
            "height": height,
        }

        if current_image:
            pipe_kwargs["ip_adapter_image"] = current_image

        output = pipe(**pipe_kwargs)
        chunk_frames = output.frames[0]
        all_frames.extend(chunk_frames)
        
        # Use the last frame of the current chunk as the starting image for the next
        if current_image:
            current_image = chunk_frames[-1]

    if all_frames:
        export_to_video(all_frames, output_path, fps=fps, log_stream=log_stream)
    else:
        _log("Warning: No frames were generated.")
