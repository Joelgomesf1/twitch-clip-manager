from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import (
    get_pending_clips,
    delete_clip_by_id,
    update_clip_status,
    get_clip_by_id,
    delete_pending_clips_by_streamer,
    get_downloaded_clips,
    get_approved_clips,
    get_streamers,
    delete_streamer,
    add_streamer,
    streamer_existe
)

app = FastAPI()


@app.get("/api")
def home():
    return {"mensagem": "API funcionando!"}


@app.get("/clips")
def listar_clips():
    clips = get_pending_clips()

    resultado = []

    for clip in clips:
        resultado.append({
            "id": clip[0],
            "platform": clip[1],
            "streamer": clip[2],
            "clip_id": clip[3],
            "title": clip[4],
            "url": clip[5],
            "status": clip[6]
        })

    return resultado

@app.get("/clips/{clip_id}")
def obter_clip(clip_id: int):
    clips = get_pending_clips()

    for clip in clips:
        if clip[0] == clip_id:
            return {
                "id": clip[0],
                "platform": clip[1],
                "streamer": clip[2],
                "clip_id": clip[3],
                "title": clip[4],
                "url": clip[5],
                "status": clip[6]
            }

   

    
    return {"erro": "Clip não encontrado"}


@app.get("/downloaded")
def downloaded():

    clips = get_downloaded_clips()

    resultado = []

    for clip in clips:

        resultado.append({
            "id": clip[0],
            "platform": clip[1],
            "streamer": clip[2],
            "clip_id": clip[3],
            "title": clip[4],
            "url": clip[5],
            "vod_url": clip[6],
            "status": clip[7]
        })

    return resultado

@app.delete("/clips/{clip_id}")
def deletar_clip(clip_id: int):

    delete_clip_by_id(clip_id)

    return {
        "mensagem": "Clip removido com sucesso"
    }

@app.post("/update")
def atualizar():

    from update_clips import atualizar_clips

    atualizar_clips()

    return {"ok": True}

from pydantic import BaseModel


class Streamer(BaseModel):
    streamer: str


@app.post("/streamers")
def adicionar_streamer(dados: Streamer):

    streamer = dados.streamer.strip().lower()

    if "twitch.tv/" in streamer:

        streamer = streamer.split("twitch.tv/")[1]

        streamer = streamer.split("/")[0]

        streamer = streamer.split("?")[0]

    if streamer_existe(streamer):
        return {"mensagem": "Streamer já cadastrado"}

    add_streamer("twitch", streamer)

    return {"mensagem": "Streamer adicionado"}

# DEIXE AQUI

@app.post("/clips/{clip_id}/download")
def download_clip(clip_id: int):

    update_clip_status(clip_id, "approved")

    return {"ok": True}


@app.post("/clips/{clip_id}/reject")
def reject_clip(clip_id: int):

    update_clip_status(clip_id, "rejected")

    return {"ok": True}



@app.get("/approved")
def approved():

    clips = get_approved_clips()

    resultado = []

    for clip in clips:

        resultado.append({
            "id": clip[0],
            "platform": clip[1],
            "streamer": clip[2],
            "clip_id": clip[3],
            "title": clip[4],
            "url": clip[5],
            "vod_url": clip[6],
            "status": clip[7]
        })

    return resultado


@app.delete("/streamers/{streamer}")
def remover_streamer(streamer: str):

    delete_streamer(streamer)

    delete_pending_clips_by_streamer(streamer)  

    return {"ok": True}


@app.get("/streamers")
def listar_streamers():

    streamers = get_streamers()

    return [
        {
            "platform": s[0],
            "streamer": s[1]
        }
        for s in streamers
    ]


from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

