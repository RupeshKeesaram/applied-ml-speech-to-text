import pytube
from src.logger import ProjectLogger
from pytubefix import YouTube
from pytubefix.cli import on_progress

logger = ProjectLogger().get_logger()


class YouTubeAudioExtractor:
    def __init__(self):
        """
        Initialize the YouTubeAudioExtractor.
        """
        self.data = None
        self.audio = None

    def extract_audio(self, url):
        """
        Extract audio from a YouTube video and save it as an MP4 file.

        Parameters:
        - url (str): The URL of the YouTube video.

        Raises:
        - Exception: If there is an error during the extraction process.
        """
        logger.info(f"Entered extract_audio() in {self.__class__.__name__} class")
        try:
            # self.data = pytube.YouTube(url)
            # ys = yt.streams.get_audio_only()
            # ys.download(mp3=True)
            self.data = YouTube(url)
            if self.data:
                self.audio = self.data.streams.get_audio_only()
                if self.audio:
                    # Download the audio and save as MP4
                    self.audio.download(filename="data/uploaded/youtube_audio.mp4")
                else:
                    logger.error("Failed to save file")
            else:
                logger.error("Failed to extract audio from YouTube Video")
        except Exception as e:
            logger.exception(e)
        logger.info("Exiting extract_audio()")
