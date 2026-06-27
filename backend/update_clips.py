from import_clips import buscar_clips
from database import get_streamers

DIAS = 3


def atualizar_clips():

    streamers = get_streamers()

    for plataforma, streamer in streamers:

        if plataforma == "twitch":

            print(f"Buscando clips de {streamer}...")

            total = buscar_clips(streamer, DIAS)

            print(f"{total} clips novos.")


if __name__ == "__main__":
    atualizar_clips()