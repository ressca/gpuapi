from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GPU(BaseModel):
    id: int
    manufacturer: str
    name: str
    memory_gb: int

gpus = [
    GPU(id=1, manufacturer="NVIDIA", name="RTX 3080", memory_gb=10),
    GPU(id=2, manufacturer="AMD", name="Radeon RX 6800", memory_gb=16),
    GPU(id=3, manufacturer="NVIDIA", name="RTX 3090", memory_gb=24),
    GPU(id=4, manufacturer="AMD", name="Radeon RX 6900 XT", memory_gb=16),
    GPU(id=5, manufacturer="NVIDIA", name="RTX 3070", memory_gb=8),
]

@app.get("/gpus",)
def get_gpus():
    return gpus


@app.get("/gpu/{gpu_id}")
def get_gpu(gpu_id: int):
    for gpu in gpus:
        if gpu.id == gpu_id:
            return gpu
    return {"error": "GPU not found"}


@app.post("/gpu")
def add_gpu(gpu: GPU):
    new_id = max(gpu.id for gpu in gpus) + 1 if gpus else 1

    gpu_data = gpu.model_dump(exclude={"id"})
    new_gpu = GPU(id=new_id, **gpu_data)
    gpus.append(new_gpu)


@app.put("/gpu/{gpu_id}")
def update_gpu(gpu_id: int, updated_gpu: GPU):
    for index, gpu in enumerate(gpus):
        if gpu.id == gpu_id:
            gpu_data = updated_gpu.model_dump(exclude={"id"})
            gpus[index] = GPU(id=gpu_id, **gpu_data)


@app.delete("/gpu/{gpu_id}")
def delete_gpu(gpu_id: int):
    for index, gpu in enumerate(gpus):
        if gpu.id == gpu_id:
            del gpus[index]