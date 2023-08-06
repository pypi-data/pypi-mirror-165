# Peacasso

Peacasso is a UI tool to help you generate art (and experiment) with multimodal (text, image) AI models (stable diffusion).

![](docs/images/screenpc.png)

## Requirements and Installation

- Acccess to the diffusion model weights needs a HuggingFace model account and access token. Please create an account at [huggingface.co](https://huggingface.co/), get an [access token](https://huggingface.co/settings/tokens) and agree to the model terms [here](https://huggingface.co/CompVis/stable-diffusion-v1-4). Finally, create a `HF_API_TOKEN` environment variable containing your token.
- This library requires `python 3.9` or higher.
- Requires a GPU (6 GB of VRAM) with CUDA support.

Once requirements are met, run the following command to install the library:

```bash
pip install peacasso
```

## Usage - UI and Python API

You can use the library from the ui by running the following command:

```bash
peacasso ui   # or peacasso ui --port=8080
```

```python

import os
from dotenv import load_dotenv
from peacasso.generator import PromptGenerator
from peacasso.datamodel import PromptConfig

# load token from .env file
load_dotenv()

token = os.environ.get("HF_API_TOKEN")
gen = PromptGenerator(token=token)
prompt = "A sea lion wandering the streets of post apocalyptic London"

prompt_config = PromptConfig(
    prompt=prompt,
    num_images=3,
    width=512,
    height=512,
    guidance_scale=7.5,
    num_inference_steps=50,
)

result = gen.generate(prompt_config)
for i, image in enumerate(result["images"]):
    image.save(f"image_{i}.png")
```

## Features and Road Map

- [x] Command line interface
- [x] UI Features. Query models with multiple parametrs
  - [x] Text prompting
  - [ ] Image based prompting
  - [ ] Image inpainting (masking)
  - [ ] Latent space exploration
- [ ] Curation/sharing experiment results

## Acknowledgement

This work builds on the stable diffusion model and code is adapted from the HuggingFace [implementation](https://huggingface.co/blog/stable_diffusion).
