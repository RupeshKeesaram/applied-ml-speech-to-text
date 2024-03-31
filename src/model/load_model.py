import os
import zipfile
import whisper
from src.logger import ProjectLogger

logger = ProjectLogger().get_logger()


class WhisperModelManager:
    def __init__(self):
        """Initialize the WhisperModelManager."""
        pass

    def load_model(self, model_name):
        """
        Load or download a Whisper model.

        Parameters:
        - model_name (str): The name of the Whisper model.

        Returns:
        - whisper.WhisperForConditionalGeneration: The loaded or downloaded Whisper model, or None if there is an error.
        """

        logger.info(f"Entered load_model() in {self.__class__.__name__}")

        model_folder_path = f"models/{model_name}"

        # Check if the model files exist in the specified folder
        if not os.path.exists(model_folder_path):
            try:
                # Download the model

                logger.info("Downloading from remote")
                model = whisper.load_model("base")  # download_root=model_folder_path

                try:
                    # Save the downloaded model as a zip file
                    self.save_model_as_zip(model, model_name, model_folder_path)
                except Exception as e:
                    logger.exception("Failed to save model", e)

                logger.info(f"Model '{model_name}' downloaded successfully.")
                return model
            except Exception as e:
                logger.info(f"Error downloading model '{model_name}': {e}")
                return None
        else:
            # Load the model from the specified folder
            model_zip_path = os.path.join(model_folder_path, f"{model_name}_model.zip")
            model_extracted_path = model_folder_path + "/extracted"
            if os.path.exists(model_extracted_path):
                try:
                    logger.info("Loading model from extracted files")
                    model = whisper.load_model(
                        model_extracted_path + f"/{model_name}.pt"
                    )
                    logger.info("Model Loaded Successfully!!!")
                    return model
                except Exception as e:
                    logger.exception("Error occurred ",e)
            else:
                logger.info("unzipping & loading model")
                if os.path.exists(model_zip_path):
                    # Load the model from the zip file
                    model = self.load_model_from_zip(
                        model_zip_path, model_extracted_path
                    )
                    logger.info(f"Model '{model_name}' loaded from local zip file.")
                    return model

    def save_model_as_zip(self, model, model_name, model_folder_path):
        """Save the downloaded model as a zip file."""

        model_zip_path = model_folder_path + f"/{model_name}_model.zip"
        # model_zip_path = "../../models/"
        try:
            with zipfile.ZipFile(model_zip_path, "w") as zipf:
                logger.info("Opening zip file")
                # Add all files in the model folder to the zip file
                for root, _, files in os.walk(model_folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, model_folder_path)
                        zipf.write(file_path, arcname=arc_name)
        except Exception as e:
            logger.exception("Failed to save model", e)

    def load_model_from_zip(self, model_zip_path, model_extracted_path):
        """Load the model from the zip file."""
        logger.info("About to load model using zip")

        with zipfile.ZipFile(model_zip_path, "r") as zipf:
            logger.info("Extracting the model from zip")
            # Extract the zip file to a temporary directory
            zipf.extractall(model_extracted_path)

            # Load the model from the temporary directory
            model = whisper.load_model("base", download_root=model_extracted_path)

            return model
