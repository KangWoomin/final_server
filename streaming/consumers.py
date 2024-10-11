import os
import django
from django import setup

django.setup()  

from channels.generic.websocket import AsyncWebsocketConsumer
import ffmpeg
import subprocess
import asyncio  # asyncio를 import

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        stream_url = "http://10.0.66.136:81/stream"
        await self.send(stream_url)
        

    async def disconnect(self, code):
        await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "save_video":
            await self.save_streamed_video("http://10.0.66.136:81/stream", "output.mp4", duration=60)

    async def save_streamed_video(self, url, output_file, duration=60):
        await self.run_ffmpeg(url, output_file, duration)

    async def run_ffmpeg(self, url, output_file, duration):
        command = [
            'ffmpeg',
            '-i', url,
            '-t', str(duration),
            '-c:v', 'copy',
            output_file
        ]

        try:
            process = await asyncio.create_subprocess_exec(*command)
            await process.wait()

            if process.returncode == 0:
                await self.send("비디오 저장 성공!!!!")
            else:
                await self.send("비디오 저장중 오류..")
                await self.close()
        except Exception as e:
            await self.send(f"error: {str(e)}")
            await self.close()
