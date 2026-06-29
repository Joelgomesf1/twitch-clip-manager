from twitch import get_user_id, get_clips
from database import add_clip, clip_existe, add_streamer


def buscar_clips(streamer, dias):

    add_streamer("twitch", streamer)

    user_data = get_user_id(streamer)

    if not user_data["data"]:
        return 0

    user_id = user_data["data"][0]["id"]

    clips = get_clips(user_id, dias)

    print(f"Streamer: {streamer}")
    print(clips)
    print(f"Quantidade de clips recebidos: {len(clips.get('data', []))}")

    total = 0

    for clip in clips["data"]:

        print(f"Clip: {clip['id']} - {clip['title']}")

        if clip_existe(clip["id"]):
            continue

        add_clip(
            platform="twitch",
            streamer=streamer,
            clip_id=clip["id"],
            title=clip["title"],
            url=clip["url"],
            vod_url=clip["video_id"]
        )

        print(f"Novo clip salvo: {clip['title']}")
    
        total += 1

    return total