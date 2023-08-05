from torch import autocast
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionPipeline
import os
import torch
import time

from peacasso.datamodel import PromptConfig


class PromptGenerator:
    """Generate image from prompt"""

    def __init__(
        self,
        token: str = os.environ.get("HF_API_TOKEN"),
    ) -> None:
        assert token is not None, "HF_API_TOKEN must be provided or set in .env file"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=token,
        ).to(self.device)

    def generate(self, config: PromptConfig) -> Image:
        """Generate image from prompt"""
        prompt = [config.prompt] * config.num_images
        start_time = time.time()
        with autocast(self.device):
            images = self.pipe(
                prompt,
                width=config.width,
                height=config.height,
                guidance_scale=config.guidance_scale,
                num_inference_steps=config.num_inference_steps,
            )["sample"]
        elapsed_time = time.time() - start_time
        return {"images": images, "time": elapsed_time}
