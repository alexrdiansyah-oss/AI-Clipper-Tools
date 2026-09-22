import subprocess
import sys
import os
import time


# ======================================
# CONFIGURATION
# ======================================

STEPS = [
    ("Transcribing video", "src/transcriber.py"),
    ("Detecting clips", "src/clip_detector.py"),
    ("Ranking clips", "src/clip-rank.py"),
    ("Cutting videos", "src/video_editor.py"),
    ("Formatting Shorts", "src/shorts_formatter.py"),
    ("Generating subtitles", "src/subtitle_generator.py"),
    ("Burning subtitles", "src/subtitle_burner.py"),
]


# ======================================
# PROGRESS
# ======================================

def show_progress(current, total, prefix="Progress"):

    bar_length = 30

    percent = current / total

    filled = int(
        bar_length * percent
    )

    bar = (
        "█" * filled
        + "░" * (bar_length - filled)
    )

    percentage = percent * 100

    print(
        f"{prefix}: [{bar}] "
        f"{percentage:.0f}%"
    )


# ======================================
# RUN STEP
# ======================================

def run_step(step_number, total_steps, name, script):

    print()
    print("=" * 60)
    print(
        f"[{step_number}/{total_steps}] "
        f"{name}"
    )
    print("=" * 60)
    print()

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, script]
    )

    elapsed = time.time() - start_time

    if result.returncode != 0:

        print()
        print("=" * 60)
        print(f"✗ FAILED: {name}")
        print("=" * 60)

        return False

    print()
    print(f"✓ {name} selesai")
    print(
        f"Time: {elapsed:.1f} seconds"
    )

    return True


# ======================================
# MAIN
# ======================================

def main():

    print()
    print("=" * 60)
    print("              AI CLIPPER TOOLS")
    print("=" * 60)

    print()
    print("Starting pipeline...")
    print()

    total_steps = len(STEPS)

    overall_start = time.time()


    # ==================================
    # RUN PIPELINE
    # ==================================

    for index, (name, script) in enumerate(
        STEPS,
        start=1
    ):

        success = run_step(
            index,
            total_steps,
            name,
            script
        )

        if not success:

            print()
            print("=" * 60)
            print("PIPELINE STOPPED")
            print("=" * 60)

            sys.exit(1)


        # Progress pipeline
        show_progress(
            index,
            total_steps,
            prefix="Pipeline"
        )


    # ==================================
    # CALCULATE RESULT
    # ==================================

    total_time = (
        time.time()
        - overall_start
    )


    final_folder = "output/final"


    if os.path.exists(final_folder):

        final_videos = [
            file
            for file in os.listdir(
                final_folder
            )
            if file.endswith(".mp4")
        ]

    else:

        final_videos = []


    # ==================================
    # FINAL MESSAGE
    # ==================================

    print()
    print("=" * 60)
    print("              PROCESS COMPLETE")
    print("=" * 60)
    print()

    print(
        f"Generated clips : "
        f"{len(final_videos)}"
    )

    print(
        f"Output folder   : "
        f"{final_folder}"
    )

    print(
        f"Total time      : "
        f"{total_time / 60:.1f} minutes"
    )

    print()
    print("Generated files:")

    for video in final_videos:

        print(
            f"  ✓ {video}"
        )

    print()
    print("=" * 60)


# ======================================
# START PROGRAM
# ======================================

if __name__ == "__main__":
    main()