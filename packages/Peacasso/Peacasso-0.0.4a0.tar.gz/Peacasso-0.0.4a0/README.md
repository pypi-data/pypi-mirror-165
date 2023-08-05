# Peacasso

Peacasso is an experimental UI interface that makes it easy to generate interesting images with multimodal (text, image) models (stable diffusion).

![](docs/images/screenpc.png)

## Installation

Acccess to the model weights needs a HuggingFace model account and access token. Please create an account at [huggingface.co](https://huggingface.co/), get an [access token](https://huggingface.co/settings/tokens) and agree to the model terms [here](https://huggingface.co/CompVis/stable-diffusion-v1-4). Finally, create a `HF_API_TOKEN` environment variable containing your token.

```bash
pip install peacasso
```

once installed, run the ui with the following command:

```bash
peacasso ui   # or peacasso ui --port=8080
```

Note that you will need to run this on a machine that meets the requirements for the stable diffusion model (cuda).

## Implementation Plan

- [x] Command line interface
- [x] UI interface with controls for changing the model parameters
- [ ] Enable curation of galleries
- [ ] Image inpainting
- [ ] Latent space visualization

## Acknowledgement

This work builds on the stable diffusion model and code is adapted from the HuggingFace [implementation](https://huggingface.co/blog/stable_diffusion).
