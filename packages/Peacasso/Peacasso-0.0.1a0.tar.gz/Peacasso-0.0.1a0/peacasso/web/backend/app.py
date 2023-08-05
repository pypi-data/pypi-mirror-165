 
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
import os  
from dotenv import load_dotenv
from peacasso.generator import PromptGenerator
from fastapi.middleware.cors import CORSMiddleware

from peacasso.datamodel import PromptConfig
import hashlib

# # load token from .env file
load_dotenv()


app = FastAPI()
# allow cross origin requests for testing on localhost:8000 only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api = FastAPI(root_path="/api")
app.mount("/api", api)


root_file_path = os.path.dirname(os.path.abspath(__file__))
static_folder_root = os.path.join(root_file_path, "build")
files_static_root = os.path.join(root_file_path, "files/")

os.makedirs(files_static_root, exist_ok=True)

if not os.path.exists(static_folder_root):
    assert False, "Static folder not found: {}. Ensure the front end is built".format(
        static_folder_root
    )

hf_token = os.environ.get("HF_API_TOKEN")
generator = PromptGenerator(token=hf_token)

# mount peacasso front end UI files
app.mount("/", StaticFiles(directory=static_folder_root, html=True), name="ui")

api.mount("/files", StaticFiles(directory=files_static_root, html=True), name="files")

@api.post("/generate")
def generate(prompt_config: PromptConfig) -> str:
    """Generate an image given some prompt"""
    result = generator.generate(prompt_config)
    slug = hashlib.sha256(str(prompt_config).encode("utf-8")).hexdigest() 
    image_list = []
    try:
        for i,image in enumerate(result["images"]):
            image_save_path = f"{slug}_{i}.png"
            image.save(os.path.join(files_static_root, "images",image_save_path))
            image_list.append(image_save_path)
        result = {"status": True, "status_message":"generation success", "images": image_list, "time": result["time"]}
    except Exception as e:
        result = {"status": False, "status_message":str(e)}
    return result

 