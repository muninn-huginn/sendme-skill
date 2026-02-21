#!/usr/bin/env python3
"""PTY wrapper for sendme send — works in non-interactive environments.

sendme requires a TTY (it enables raw mode for interactive features).
This script provides a pseudo-terminal so sendme works in scripts,
Docker, CI, and agent environments.

Usage:
    python3 sendme_send.py <path>

Prints the ticket to stdout. The sendme process keeps running
until interrupted (Ctrl+C or SIGTERM).
"""

import os
import pty
import select
import signal
import sys


def sendme_send(path):
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("sendme", ["sendme", "send", path])
    else:
        output = b""
        ticket = None

        while True:
            ready, _, _ = select.select([fd], [], [], 0.5)
            if ready:
                try:
                    chunk = os.read(fd, 4096)
                    if not chunk:
                        break
                    output += chunk
                    text = output.decode(errors="replace")
                    for line in text.split("\n"):
                        if "sendme receive blob" in line:
                            ticket = line.strip().replace("sendme receive ", "")
                            print(ticket)
                            sys.stdout.flush()
                except OSError:
                    break
            elif ticket:
                # Ticket found, keep process alive for recipient to download
                try:
                    os.waitpid(pid, os.WNOHANG)
                except ChildProcessError:
                    break

        # Clean up
        try:
            os.kill(pid, signal.SIGTERM)
            os.waitpid(pid, 0)
        except (ProcessLookupError, ChildProcessError):
            pass

        return ticket


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path>", file=sys.stderr)
        sys.exit(1)
    sendme_send(sys.argv[1])
