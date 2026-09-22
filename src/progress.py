import sys


# ======================================
# PROGRESS BAR
# ======================================

def show_progress(
    current,
    total,
    prefix="Progress",
    bar_length=30
):
    """
    Menampilkan progress bar sederhana.

    current = posisi sekarang
    total   = total pekerjaan
    """

    if total <= 0:
        total = 1

    percent = current / total
    filled = int(bar_length * percent)

    bar = "█" * filled + "░" * (bar_length - filled)

    percentage = percent * 100

    sys.stdout.write(
        f"\r{prefix}: [{bar}] {percentage:6.2f}%"
    )

    sys.stdout.flush()

    if current >= total:
        print()


# ======================================
# TEST
# ======================================

if __name__ == "__main__":

    import time

    print()
    print("Testing progress bar...")
    print()

    total = 100

    for i in range(total + 1):

        show_progress(
            i,
            total,
            prefix="Processing"
        )

        time.sleep(0.03)

    print()
    print("✓ Progress selesai")