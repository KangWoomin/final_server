import os
import django
from django import setup

django.setup()  # Django 설정 초기화
# streaming/views.py
from channels.generic.websocket import AsyncWebsocketConsumer
import ffmpeg
import subprocess
import asyncio  # asyncio를 import

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        stream_url = "http://10.0.66.137:81/stream"
        await self.send(stream_url)
        await self.accept()

    async def disconnect(self, code):
        await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "save_video":
            await self.save_streamed_video("http://10.0.66.137:81/stream", "output.mp4", duration=60)

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

        # Run the subprocess asynchronously
        process = await asyncio.create_subprocess_exec(*command)
        await process.wait()