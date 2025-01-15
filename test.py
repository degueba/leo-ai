from RealtimeSTT import AudioToTextRecorder
import pyaudio
import traceback
import os


def print_text(text):
    print(f"You said: {text}")
    return True


def main():
    # Set environment variables for multiprocessing
    os.environ["OMP_NUM_THREADS"] = "1"

    # Initialize PyAudio to find devices
    p = pyaudio.PyAudio()

    # Find USB microphone index
    usb_index = None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if "USB" in info["name"] and info["maxInputChannels"] > 0:
            usb_index = i
            print(f"Using USB microphone: {info['name']} (index {i})")
            break

    if usb_index is None:
        print("No USB microphone found!")
        return

    try:
        recorder = AudioToTextRecorder(
            model="tiny.en",
            language="en",
            input_device_index=usb_index,
            print_transcription_time=True,
            spinner=False,
            use_microphone=True,
            device="cpu",
            enable_realtime_transcription=True,
            realtime_processing_pause=0.1,
            on_recording_start=lambda: print("Recording started..."),
            on_recording_stop=lambda: print("Recording stopped"),
            on_vad_detect_start=lambda: print("Voice detected"),
            on_vad_detect_stop=lambda: print("Voice ended"),
        )

        print("🎤 Speak into your USB microphone... (press Ctrl+C to stop)")
        recorder.text(print_text)

    except KeyboardInterrupt:
        print("👋 Stopped recording")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Detailed traceback:")
        traceback.print_exc()
    finally:
        p.terminate()


if __name__ == "__main__":
    # Set multiprocessing start method
    import multiprocessing

    multiprocessing.set_start_method("spawn")
    main()
