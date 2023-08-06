import subprocess
import os
import signal
import shlex

from typing import List


class ProcessManager:
    def __init__(self) -> None:
        self.proc = None

    def start(self, process_list: List[str]) -> None:
        # Kill existing process if anything is running
        if self.proc is not None:
            self.stop()

        self.proc = subprocess.Popen(
            process_list,
            preexec_fn=os.setsid,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def start_from_string(self, process_string: str):
        return self.start(shlex.split(process_string))

    def stop(self) -> None:
        if self.proc is None:
            return

        try:
            os.kill(self.proc.pid, signal.SIGINT)
        except OSError:
            pass

        self.proc = None

    def is_running(self) -> bool:
        if self.proc is None:
            return False
        else:
            if self.proc.poll() is None:
                return True
            else:
                return False

    def __del__(self) -> None:
        self.stop()  # Stop if class is destroyed
