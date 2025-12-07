import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import speech_recognition as sr
import openai
import os
import io

class WhisperASRNode(Node):
    def __init__(self):
        super().__init__('whisper_asr_node')
        self.publisher_ = self.create_publisher(String, 'voice_command_text', 10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Create a timer to continuously listen for audio
        self.timer = self.create_timer(5.0, self.listen_callback) # Listen every 5 seconds

        self.get_logger().info('Whisper ASR Node started. Listening for voice commands...')
        if not os.environ.get("OPENAI_API_KEY"):
            self.get_logger().error("OPENAI_API_KEY environment variable not set. Transcription will fail.")

    def listen_callback(self):
        try:
            with self.microphone as source:
                self.get_logger().info("Say something!")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, phrase_time_limit=4) # Listen for up to 4 seconds
            
            # Use OpenAI Whisper API for transcription
            audio_data = io.BytesIO(audio.get_wav_data())
            audio_data.name = 'audio.wav' # OpenAI API expects a file-like object with a name

            response = self.openai_client.audio.transcriptions.create(
                model="whisper-1", # or "base", "small" if running locally
                file=audio_data,
                response_format="text"
            )
            
            transcribed_text = response.strip()
            if transcribed_text:
                msg = String()
                msg.data = transcribed_text
                self.publisher_.publish(msg)
                self.get_logger().info(f'Transcribed: "{transcribed_text}"')

        except sr.UnknownValueError:
            self.get_logger().warn("Whisper could not understand audio")
        except sr.RequestError as e:
            self.get_logger().error(f"Could not request results from Whisper service; {e}")
        except Exception as e:
            self.get_logger().error(f"An unexpected error occurred: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = WhisperASRNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
