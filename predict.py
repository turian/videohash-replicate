import shutil
import tempfile

from cog import BasePredictor, Input, Path
from videohash import VideoHash


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load any required resources into memory to make running multiple predictions efficient"""
        # No model loading required for VideoHash computation
        pass

    def predict(
        self,
        path: Path = Input(description="Path to the input video file", default=None),
        url: str = Input(
            description="URL of the input video file (for yt-dlp)", default=None
        ),
        download_worst: bool = Input(
            description="Download the worst quality video to conserve bandwidth",
            default=False,
        ),
        frame_interval: float = Input(
            description="Number of frames extracted per unit time", default=1.0
        ),
    ) -> dict:
        """Run a single prediction on the model"""
        # Validate inputs
        if path is None and url is None:
            raise ValueError("You must specify either a path or a URL of the video.")
        if path and url:
            raise ValueError("Specify either a path or a URL, not both.")

        tmpdir_object = tempfile.TemporaryDirectory()
        tmpdir = tmpdir_object.name
        if not tmpdir.endswith("/"):
            tmpdir = f"{tmpdir}/"
            # Computie VideoHash
            videohash = VideoHash(
                path=str(path) if path else None,
                url=url,
                download_worst=download_worst,
                frame_interval=frame_interval,
                storage_path=tmpdir,
            )

            # Prepare the response
            response = {
                "hash": videohash.hash,
                "hash_hex": videohash.hash_hex,
                "bits_in_hash": videohash.bits_in_hash,
                "video_duration": videohash.video_duration,
            }

            return response
