from RealtimeSTT import AudioToTextRecorder
from modules.assistant_config import get_config
from modules.typer_agent import TyperAgent
import typer
from typing import List
import traceback
from datetime import datetime
import multiprocessing
import os

app = typer.Typer()


@app.command()
def ping():
    print("pong")


@app.command()
def awaken(
    typer_file: str = typer.Option(...),
    scratchpad: str = typer.Option(...),
    context_files: List[str] = typer.Option([]),
    mode: str = typer.Option("default"),
):
    """Run STT interface that processes speech into typer commands"""

    # Set multiprocessing start method
    multiprocessing.set_start_method("spawn")

    # Set environment variables
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    assistant, typer_file, _ = TyperAgent.build_agent(typer_file, [scratchpad])

    print("🎤 Speak now... (press Ctrl+C to exit)")

    recorder = AudioToTextRecorder(
        model="tiny.en",
        language="en",
        print_transcription_time=True,
        spinner=False,
        device="cpu",
        enable_realtime_transcription=True,
        realtime_processing_pause=0.1,
        post_speech_silence_duration=1.5,
        compute_type="float32",
        beam_size=8,
        batch_size=25,
        on_recording_start=lambda: print("🎤 Recording started..."),
        on_recording_stop=lambda: print("🎤 Recording stopped"),
        on_vad_detect_start=lambda: print("🎤 Voice detected"),
        on_vad_detect_stop=lambda: print("🎤 Voice ended"),
    )

    def process_text(text):
        print(f"\n🎤 Heard: {text}")
        try:
            assistant_name = get_config("typer_assistant.assistant_name")
            if assistant_name.lower() not in text.lower():
                print(f"🤖 Not {assistant_name} - ignoring")
                return

            recorder.stop()
            print("🤖 Processing command...")
            output = assistant.process_text(
                text, typer_file, scratchpad, context_files, mode
            )
            print(f"🤖 Response:\n{output}")
            recorder.start()
        except Exception as e:
            # Create a visually distinct error block
            print("\n" + "❌" * 40)
            print("❌ ERROR DETECTED")
            print("❌" * 40)
            print(f"\nError Type: {type(e).__name__}")
            print(f"Error Message: {str(e)}")
            print("\n🧐 Context:")
            print(f"- Input Text: {text}")
            print(f"- Mode: {mode}")
            print(f"- Typer File: {typer_file}")
            print(f"- Scratchpad: {scratchpad}")
            print(f"- Context Files: {context_files}")

            # Print the traceback directly to console
            print("\n🔍 Full Traceback:")
            traceback.print_exc()

            # Still log to file for persistence
            with open("error_log.txt", "a") as f:
                f.write(f"\n\n[{datetime.now()}] ERROR DETAILS\n")
                f.write(f"Input Text: {text}\n")
                f.write(f"Error Type: {type(e).__name__}\n")
                f.write(f"Error Message: {str(e)}\n")
                f.write("Traceback:\n")
                traceback.print_exc(file=f)

            print("\n🤖 Attempting to restart recorder...")
            try:
                recorder.start()
            except Exception as restart_error:
                print(f"⚠️ Failed to restart recorder: {str(restart_error)}")
            print("\n" + "❌" * 40 + "\n")

    while True:
        recorder.text(process_text)


if __name__ == "__main__":
    app()
