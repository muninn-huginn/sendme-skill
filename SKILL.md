---
name: sendme
description: >-
  Send and receive files peer-to-peer using the sendme protocol from iroh.computer.
  Use when the user wants to share files, transfer files between machines, send
  files to someone, or receive files using a sendme ticket. Supports files and
  folders of any size with resumable downloads, integrity verification, and
  direct peer-to-peer connections without servers.
metadata:
  openclaw:
    requires:
      anyBins: [sendme]
    install:
      - kind: brew
        formula: sendme
        bins: [sendme]
---

# Sendme

Peer-to-peer file transfer using [iroh](https://www.iroh.computer/sendme). No server uploads — files stream directly between machines via encrypted connections with automatic NAT traversal.

## Installation

If `sendme` is not installed:

```bash
brew install sendme
```

Alternatively, install via Cargo: `cargo install sendme`

## Sending Files

```bash
sendme send <path>
```

- Accepts a file or directory path
- Outputs a **ticket** — a long base32-encoded string the recipient needs
- The process stays running until interrupted with Ctrl+C — the sender must remain online for the recipient to download
- Present the ticket to the user and instruct them to share it with their recipient

Example:

```bash
sendme send ~/Documents/report.pdf
# Outputs: sendme receive blobaa...  (the ticket)
```

For directories, sendme bundles the entire folder recursively.

## Receiving Files

```bash
sendme receive <ticket>
```

- Downloads the file/folder to the current directory
- Uses temporary `.sendme-*` directories during download, then moves atomically
- Automatically verifies integrity via blake3 hashing
- Resumes interrupted downloads automatically

Example:

```bash
sendme receive blobaafy...
```

## Key Details

- **Connection**: Direct peer-to-peer with TLS encryption. Falls back to relay servers if direct connection fails.
- **Resumable**: Interrupted downloads continue from where they left off.
- **Integrity**: All data is blake3-verified during streaming.
- **Speed**: Saturates connections up to 4Gbps.
- **No size limit**: Works with files and folders of any size.
- **Sender must stay online**: The `sendme send` process must keep running until the recipient completes the download.
