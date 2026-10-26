# KSCU Automatic Radio Recording Distribution System

A continuously running Python service that automates the recording and distribution of live radio broadcasts for [KSCU 103.3 FM](https://www.kscu.org), Santa Clara University's student-run radio station.

## What It Does

For every show on the broadcast schedule, the system automatically:
1. Records the live radio stream for the length of the show
2. Identifies which DJ is on air based on the schedule
3. Emails that DJ a download link to the recording (the link is valid for 7 days)
4. Stores a copy of the recording in cloud storage for archival

The service runs unattended 24/7. Each quarter a new schedule must be created to keep the DJ information accurate.

## How It Works

- **`CreateSchedule.py`** pulls the upcoming week of shows from the [Spinitron](https://spinitron.com) API, looks up each show's DJ name and email, and writes them to a local `schedule.json`.
- **`recording.py`** is the long-running service. It checks the schedule, and when a show starts it records the stream with `ffmpeg` (converted to MP3), uploads the file to AWS S3, and emails the DJ a presigned download link using `yagmail`. It then deletes the local copy.

A few behaviors worth knowing:
- Shows that start between 1 am and 7 am are not recorded.
- Shows with no matching DJ in the schedule are skipped.
- Shows hosted by the station's automation account are uploaded to S3 but not emailed.
- If the upload to S3 fails, no email is sent.

## Architecture

- **Recording service**: Python script hosted on an AWS EC2 instance, continuously capturing show audio
- **Distribution**: Automated email to the on-air DJ after each recording completes
- **Storage**: Recordings archived to AWS S3 for long-term retention and easy access

## Tech Stack

- **Python**: Core recording and scheduling logic
- **ffmpeg**: Captures and encodes the live stream
- **AWS EC2**: Cloud hosting for the always-on service
- **AWS S3**: Cloud storage for recorded audio files, and presigned download links
- **Spinitron API**: Source of the show schedule and DJ contact information
- **yagmail**: Automated distribution to DJs

## Setup

Requires Python 3.9 or newer and `ffmpeg` installed on the machine.

```bash
git clone https://github.com/colinfriedel/KSCU-Show-Recorder.git
cd KSCU-Show-Recorder
pip install -r requirements.txt
cp .env.example .env     # then fill in the values
```

Configuration lives in `.env` (see `.env.example`):

| Variable | Used for |
|---|---|
| `SPINITRON_API_KEY` | Reading the show schedule from Spinitron |
| `SPINITRON_STATION_ID` | Station to pull the schedule for (defaults to `KSCU`) |
| `EMAIL_ADDRESS`, `EMAIL_PASSWORD` | The account that sends recordings to DJs |

AWS access comes from the standard boto3 credential sources, such as an IAM role on the EC2 instance. The role needs permission to upload to and read from the S3 bucket, which is set by `S3_BUCKET` in `recording.py`.

## Running

```bash
python CreateSchedule.py   # builds schedule.json from Spinitron
python recording.py        # starts the recording service
```

`schedule.json` contains DJ names and email addresses, so it is ignored by git and should not be committed.

## Background

Built to solve a real problem at KSCU: A previous recording system had gone down and DJs were no longer receiving recordings of their shows. This system runs in production and successfully distributed recordings to 130+ active DJs and volunteers over several months before being integrated into a new station management system.

## Status

Core system completed and deployed. Recording and distribution logic has since been adopted and extended as part of a broader station management platform.
