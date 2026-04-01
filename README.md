# KSCU Automatic Radio Recording Distribution System

A continuously running Python service that automates the recording and distribution of live radio broadcasts for [KSCU 103.3 FM](https://www.kscu.org), Santa Clara University's student-run radio station.

## What It Does

Every hour, the system automatically:
1. Records the live radio station output
2. Identifies which DJ is currently on air based on the broadcast schedule
3. Emails the recording directly to that DJ in an easily downloadable format
4. Stores a copy of the recording in cloud storage for archival

No manual intervention required during operation — the system runs unattended 24/7. Each quarter a new schedule must be created in order to keep information accurate. 

## Architecture

- **Recording service** — Python script hosted on an AWS EC2 instance, continuously capturing hourly audio output
- **Distribution** — Automated email delivery to the on-air DJ after each recording completes
- **Storage** — Recordings archived to AWS S3 for long-term retention and easy access

## Tech Stack

- **Python** — Core recording and scheduling logic
- **AWS EC2** — Cloud hosting for the always-on service
- **AWS S3** — Cloud storage for recorded audio files
- **yagmail** — Automated distribution to DJs

## Background

Built to solve a real problem at KSCU: A previous recording system had gone down and DJs were no longer receiving recordings of their shows. This system runs in production and successfully distributed recordings to 130+ active DJs and volunteers over several months before being integrated into a new station management system.

## Status

Core system completed and deployed. Recording and distribution logic has since been adopted and extended as part of a broader station management platform.
