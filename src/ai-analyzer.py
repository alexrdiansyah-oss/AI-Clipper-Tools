import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# LOAD TRANSCRIPT
# =========================

with open(
    "transcript.json",
    "r",
    encoding="utf-8"
) as file:

    segments = json.load(file)


transcript_text = ""

for segment in segments:

    transcript_text += (
        f"[{segment['start']:.2f} - "
        f"{segment['end']:.2f}] "
        f"{segment['text']}\n"
    )


# =========================
# AI PROMPT
# =========================

prompt = f"""
Kamu adalah AI video editor yang bertugas
mencari bagian menarik dari sebuah video panjang
untuk dijadikan short-form content.

Analisis transcript berikut:

{transcript_text}

Cari maksimal 5 bagian video yang berpotensi
menjadi short video.

Kriteria:

1. Memiliki hook yang menarik.
2. Memiliki informasi atau cerita yang jelas.
3. Sebisa mungkin memiliki konteks yang lengkap.
4. Hindari bagian yang terlalu bergantung pada
   konteks yang tidak ada di dalam clip.
5. Durasi ideal antara 20 sampai 60 detik.
6. Jangan mengubah timestamp yang tersedia.
7. Gunakan timestamp dari transcript.

Untuk setiap kandidat berikan:

- start
- end
- title
- hook
- reason
- score

Score berada antara 0 sampai 100.

Output HARUS berupa JSON array.
Jangan tambahkan markdown atau penjelasan lain.
"""


# =========================
# CALL AI
# =========================

response = client.responses.create(
    model="gpt-5.6-sol",
    input=prompt
)


result_text = response.output_text


print("\n=== AI RESULT ===")
print(result_text)


# =========================
# SAVE RESULT
# =========================

with open(
    "clip_candidates.json",
    "w",
    encoding="utf-8"
) as file:

    file.write(result_text)


print("\nHasil disimpan ke clip_candidates.json")