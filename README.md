# sendme

An OpenClaw skill for peer-to-peer file transfer using the [sendme](https://www.iroh.computer/sendme) protocol from iroh.computer.

## What it does

Enables Claude to send and receive files directly between machines — no server uploads needed. Files stream over encrypted peer-to-peer connections with automatic NAT traversal, integrity verification, and resumable downloads.

## Install

Import this skill via [ClewHub](https://clawhub.ai/import) from this GitHub repository.

### Prerequisites

Install the `sendme` CLI:

```bash
brew install sendme
```

## Usage

Once installed, ask Claude to:

- **Send files**: "Send this file using sendme" — runs `sendme send <path>` and gives you a ticket to share
- **Receive files**: "Receive this sendme ticket: blobaaf..." — runs `sendme receive <ticket>` to download
