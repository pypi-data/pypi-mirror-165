from io import BytesIO
import io
import zipfile
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from peacasso.generator import PromptGenerator
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
static_folder_root = os.path.join(root_file_path, "ui")
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
    image_list = []
    try:
        result = generator.generate(prompt_config)
        slug = hashlib.sha256(str(prompt_config).encode("utf-8")).hexdigest()

        # for i, image in enumerate(result["images"]):
        #     image_save_path = f"{slug}_{i}.png"
        #     image.save(os.path.join(files_static_root, "images", image_save_path))
        #     image_list.append(image_save_path)
        # result = {
        #     "status": True,
        #     "status_message": "generation success",
        #     "images": image_list,
        #     "time": result["time"],
        # }
        zip_io = BytesIO()
        with zipfile.ZipFile(
            zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as temp_zip:
            for i, image in enumerate(result["images"]):
                zip_path = os.path.join("/", str(slug) + "_" + str(i) + ".png")
                # Add file, at correct path
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format="PNG")
                image.close()
                temp_zip.writestr(zip_path, img_byte_arr.getvalue())
        return StreamingResponse(
            iter([zip_io.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename=images.zip"},
        )
    except Exception as e:
        result = {"status": False, "status_message": str(e)}
    return result


@api.get("/test")
def test() -> str:
    files_dir = os.path.join(files_static_root, "images")
    files = os.listdir(files_dir)[:3]
    zip_io = BytesIO()
    with zipfile.ZipFile(
        zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as temp_zip:
        for fname in files:
            zip_path = os.path.join("/", fname)
            # Add file, at correct path
            temp_zip.write(os.path.join(files_dir, fname), zip_path)
    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=images.zip"},
    )
