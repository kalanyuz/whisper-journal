import time
from pathlib import Path
from typing import Callable, Optional, Dict, List
import sounddevice as sd
import soundfile as sf
import numpy as np
from queue import Queue
import signal
from rich.console import Console
from rich.table import Table
from queue import Queue, Empty

console = Console()


class AudioRecorder:
    def __init__(self):
        self.audio_queue = Queue()
        self.is_recording = False
        self.samplerate = 44100
        self.channels = 1
        self._input_device = None

    @staticmethod
    def list_devices() -> List[Dict]:
        """Get a list of available audio input devices"""
        devices = []
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:  # Only input devices
                devices.append(
                    {
                        "id": i,
                        "name": dev["name"],
                        "channels": dev["max_input_channels"],
                        "default_samplerate": dev["default_samplerate"],
                    }
                )
        return devices

    def print_devices(self):
        """Print available audio input devices in a nice table"""
        devices = self.list_devices()

        table = Table(title="Available Input Devices")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Channels", justify="right")
        table.add_column("Sample Rate", justify="right")

        for dev in devices:
            table.add_row(
                str(dev["id"]),
                dev["name"],
                str(dev["channels"]),
                f"{dev['default_samplerate']:.0f} Hz",
            )

        console.print(table)

    def set_device(self, device_id: int = None):
        """Set the input device by ID"""
        devices = self.list_devices()

        # If no device_id specified, try to find default
        if device_id is None:
            try:
                device_id = sd.default.device[0]
            except:
                # If no default device, use the first available one
                if devices:
                    device_id = devices[0]["id"]
                else:
                    raise ValueError("No input devices found")

        # Validate device_id
        device_info = None
        for dev in devices:
            if dev["id"] == device_id:
                device_info = dev
                break

        if not device_info:
            raise ValueError(f"Device ID {device_id} not found")

        self._input_device = device_id
        self.samplerate = int(device_info["default_samplerate"])
        self.channels = min(device_info["channels"], 2)  # Use mono or stereo

        console.print(f"[green]Selected device: {device_info['name']}[/green]")
        console.print(
            f"[blue]Sample rate: {self.samplerate} Hz, Channels: {self.channels}[/blue]"
        )

    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream to collect data"""
        if status:
            console.print(f"[yellow]Status: {status}")
        self.audio_queue.put(indata.copy())

    def _handle_stop(self, signum, frame):
        """Signal handler for stopping recording"""
        self.is_recording = False
        console.print("\n[yellow]Stopping recording...[/yellow]")

    def record(self, output_path: Path, progress_callback: Optional[Callable] = None):
        """Record audio until stopped by Ctrl+C"""
        # Ensure device is selected
        if self._input_device is None:
            self.set_device()  # Use default device if none selected

        self.is_recording = True
        recorded_chunks = []

        # Set up signal handler for graceful exit
        signal.signal(signal.SIGINT, self._handle_stop)

        # Start recording stream
        with sd.InputStream(
            device=self._input_device,
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._audio_callback,
            dtype=np.float32,  # Changed to float32 for better compatibility with soundfile
        ):
            console.print("[cyan]Recording... Press Ctrl+C to stop[/cyan]")

            elapsed_time = 0
            while self.is_recording:
                try:
                    chunk = self.audio_queue.get_nowait()
                    recorded_chunks.append(chunk)
                except:
                    pass

                if progress_callback:
                    progress_callback()

                time.sleep(0.1)
                elapsed_time += 0.1

                if elapsed_time % 1 < 0.1:
                    console.print(
                        f"[cyan]Recording... {int(elapsed_time)}s elapsed[/cyan]",
                        end="\r",
                    )

        while not self.audio_queue.empty():
            try:
                chunk = self.audio_queue.get_nowait()
                recorded_chunks.append(chunk)
            except Empty:
                break

        if not recorded_chunks:
            raise ValueError("No audio was recorded")

        console.print("\n[green]Finalizing recording...[/green]")
        recording = np.concatenate(recorded_chunks, axis=0)

        console.print(recording.sum())
        console.print(output_path)
        # Write using soundfile - supports more formats and better quality
        sf.write(
            file=str(output_path),
            data=recording,
            samplerate=self.samplerate,
            subtype="PCM_16",  # 16-bit PCM format for good quality and compatibility
        )
