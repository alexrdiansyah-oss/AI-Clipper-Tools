# 🎬 AI Clipper Tools

An AI-powered video processing pipeline that automatically transforms long-form videos into short-form vertical content.

The project is designed to automate the process of:

**Long Video → Transcription → Clip Detection → Clip Ranking → Video Cutting → 9:16 Formatting → Subtitle Generation → Final Shorts**

---

## 🚀 Project Overview

Creating short-form content from long videos usually requires several repetitive tasks:

* Watching the entire video
* Finding interesting moments
* Cutting the video
* Formatting it for vertical platforms
* Creating subtitles
* Preparing the final video

**AI Clipper Tools** aims to automate this workflow using Python, Whisper, FFmpeg, and MoviePy.

The long-term goal is to build a reusable content-processing pipeline that can analyze long videos and generate short-form video candidates automatically.

---

## ✨ Current Features

### 🎙️ 1. Video Transcription

Uses OpenAI Whisper locally to transcribe the input video.

Features:

* Indonesian language transcription
* Word-level timestamps
* Local processing
* JSON transcript output

Output:

```text
transcript.json
```

Example structure:

```json
{
    "start": 326.92,
    "end": 330.15,
    "text": "Hari ini ada kabar buruk",
    "words": [
        {
            "word": "Hari",
            "start": 326.92,
            "end": 327.20
        }
    ]
}
```

---

### ✂️ 2. Clip Detection

The system identifies potential interesting moments from the transcript.

Potential signals include:

* Questions
* Problems
* Surprising statements
* Numbers
* Strong statements
* Curiosity
* Humor
* Interesting context

Output:

```text
clip_candidates.json
```

---

### 🏆 3. Clip Ranking

Candidate clips are scored and ranked based on several signals.

Example:

```text
Rank 1
Title    : Kenapa Subscriber Tiba-Tiba Turun?
Score    : 8
Duration : 39 seconds
```

The highest-ranked clips are saved to:

```text
top_clips.json
```

---

### 🎞️ 4. Automatic Video Cutting

The system automatically cuts selected sections from the original video.

Example:

```text
input/video.mp4
       ↓
clip_01.mp4
clip_02.mp4
clip_03.mp4
```

The project uses MoviePy for video processing.

---

### 📱 5. Shorts Formatting

Selected clips are converted into vertical:

```text
1080 × 1920
9:16
```

This format is suitable for short-form video platforms.

Output:

```text
output/shorts/
```

---

### 💬 6. Automatic Subtitle Generation

Subtitle timing is generated using Whisper word-level timestamps.

The system groups words into short subtitle blocks instead of displaying an entire transcript segment at once.

Example:

```text
Hari ini ada kabar

buruk tentang internet
```

The subtitle timing follows the actual timestamps detected by Whisper.

Output:

```text
output/subtitles/
```

---

### 🔥 7. Subtitle Burning

Subtitles are permanently rendered into the video using FFmpeg.

Final videos are stored in:

```text
output/final/
```

---

# 🧠 Processing Pipeline

```text
                    INPUT VIDEO
                         │
                         ▼
                ┌─────────────────┐
                │     Whisper     │
                │  Transcription  │
                └────────┬────────┘
                         │
                         ▼
                 transcript.json
                         │
                         ▼
                ┌─────────────────┐
                │ Clip Detection  │
                └────────┬────────┘
                         │
                         ▼
               clip_candidates.json
                         │
                         ▼
                ┌─────────────────┐
                │   Clip Ranking  │
                └────────┬────────┘
                         │
                         ▼
                  top_clips.json
                         │
                         ▼
                ┌─────────────────┐
                │  Video Cutting  │
                └────────┬────────┘
                         │
                         ▼
                    clip_01.mp4
                         │
                         ▼
                ┌─────────────────┐
                │ Shorts Formatter│
                └────────┬────────┘
                         │
                         ▼
                    1080 × 1920
                         │
                         ▼
                ┌─────────────────┐
                │    Subtitle     │
                │    Generator    │
                └────────┬────────┘
                         │
                         ▼
                     .srt files
                         │
                         ▼
                ┌─────────────────┐
                │ Subtitle Burner │
                └────────┬────────┘
                         │
                         ▼
                  FINAL SHORTS
```

---

# 📁 Project Structure

```text
AI-Clipper-Tools/
│
├── input/
│   └── video.mp4
│
├── output/
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   │
│   ├── shorts/
│   │   ├── clip_01.mp4
│   │   └── clip_02.mp4
│   │
│   ├── subtitles/
│   │   ├── clip_01.srt
│   │   └── clip_02.srt
│   │
│   └── final/
│       ├── clip_01.mp4
│       ├── clip_02.mp4
│       └── ...
│
├── src/
│   ├── config.py
│   ├── progress.py
│   ├── transcriber.py
│   ├── clip_detector.py
│   ├── clip-rank.py
│   ├── video_editor.py
│   ├── shorts_formatter.py
│   ├── subtitle_generator.py
│   └── subtitle_burner.py
│
├── transcript.json
├── clip_candidates.json
├── top_clips.json
│
├── AI_Tools.py
├── README.md
└── .ai-tools/
```

---

# 🛠️ Technologies

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Main programming language             |
| Whisper    | Speech-to-text transcription          |
| MoviePy    | Video processing                      |
| FFmpeg     | Video encoding and subtitle rendering |
| JSON       | Intermediate data storage             |
| SRT        | Subtitle format                       |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Clipper-Tools
```

---

## 2. Create virtual environment

```bash
python -m venv .ai-tools
```

Activate it on Windows:

```bash
.ai-tools\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install openai-whisper
pip install moviepy
```

FFmpeg is also required.

Verify:

```bash
ffmpeg -version
```

---

# ▶️ Usage

Place your video inside:

```text
input/video.mp4
```

Then run:

```bash
python AI_Tools.py
```

The pipeline will process the video through each stage.

Expected flow:

```text
[1/7] Transcribing video
[2/7] Detecting clips
[3/7] Ranking clips
[4/7] Cutting videos
[5/7] Formatting Shorts
[6/7] Generating subtitles
[7/7] Burning subtitles
```

Final videos will be available in:

```text
output/final/
```

---

# 📊 Example Output

Example clip candidates generated by the system:

| Rank | Title                                     | Duration |
| ---- | ----------------------------------------- | -------: |
| 1    | Kenapa Subscriber Tiba-Tiba Turun?        |   39 sec |
| 2    | Realita Penghasilan Ngopang               |   51 sec |
| 3    | Internet Down, Nggak Ada Backup Plan      |   24 sec |
| 4    | Jangan Banding-Bandingkan Server          |   28 sec |
| 5    | Cinta Itu Butuh Waktu, Bahkan untuk Brand |   60 sec |

These candidates are then processed into vertical short-form videos.

---

# 🔬 Current Development Status

### Completed

* [x] Local Whisper transcription
* [x] Indonesian transcription
* [x] Word-level timestamps
* [x] Clip candidate detection
* [x] Clip ranking
* [x] Automatic video cutting
* [x] 9:16 video formatting
* [x] Automatic subtitle generation
* [x] Subtitle burning
* [x] Basic progress bar
* [x] Pipeline automation

### In Development

* [ ] Real-time transcription progress
* [ ] Better clip scoring
* [ ] AI-based clip analysis
* [ ] Better hook detection
* [ ] Face-aware 9:16 cropping
* [ ] Dynamic subtitle styling
* [ ] Automatic title generation
* [ ] Automatic description generation
* [ ] Automatic hashtag generation
* [ ] Web interface
* [ ] Batch video processing

---

# 🧠 Future AI Features

The next version will move beyond rule-based clip selection.

The planned scoring system will consider:

```text
Hook
  +
Curiosity
  +
Context
  +
Emotional intensity
  +
Humor
  +
Information value
  +
Standalone quality
  +
Duration
  ↓
Clip Score
```

The goal is to identify clips that can stand on their own without requiring the viewer to watch the entire original video.

---

# 🎯 Project Goals

The project has three main goals:

### 1. Automation

Reduce the manual work required to create short-form content from long videos.

### 2. AI Engineering Practice

Use this project to practice:

* Python
* Machine Learning
* Natural Language Processing
* Speech-to-text
* Video processing
* AI-assisted ranking
* Software engineering

### 3. Portfolio

This project demonstrates the ability to build an end-to-end AI application rather than isolated Python scripts.

---

# 📌 Roadmap

```text
Phase 1
Python + Video Processing
        ✓

Phase 2
Whisper Transcription
        ✓

Phase 3
Automatic Clip Detection
        ✓

Phase 4
Clip Ranking
        ✓

Phase 5
Shorts Formatting
        ✓

Phase 6
Subtitle Automation
        ✓

Phase 7
Pipeline Automation
        ✓

Phase 8
Real-time Progress
        → NEXT

Phase 9
AI Clip Analysis
        → NEXT

Phase 10
Advanced Video Editing
        → NEXT

Phase 11
Web Interface
        → FUTURE

Phase 12
Production-ready AI Content Pipeline
        → FUTURE
```

---

# ⚠️ Notes

Whisper transcription can be computationally intensive when running on CPU.

When using CPU, Whisper may display a warning about FP16. The project explicitly uses:

```python
fp16=False
```

for CPU compatibility.

For best performance, a compatible GPU can significantly improve transcription speed.

---

# 📜 License

This project is currently intended as a personal learning and portfolio project.

Before processing or publishing videos, make sure you have the appropriate rights or permission to use the source material.

---

# 👨‍💻 About

**AI Clipper Tools** is a personal AI engineering project focused on building an automated pipeline for transforming long-form video into short-form content.

The project is continuously evolving from a collection of Python scripts into a more complete AI-powered application.