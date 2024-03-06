import os


def send_videomsg(bot, id, msg_id):
    video = open(f'db/video/{id}.mp4', 'rb')
    bot.delete_message(id, msg_id)
    bot.send_video(id, video, caption="Бот по загрузке видео -->@example12546_bot")
    video.close()
    os.remove(f"db/video/{id}.mp4")