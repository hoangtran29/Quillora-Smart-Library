"""Thin Gemini wrapper for chat/summary/quiz/flashcards.

Uses google-genai (same SDK as p-inno voice_chat_service).
If GEMINI_API_KEY is missing we fall back to a deterministic mock so the
demo still loads without network/keys.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    if not settings.GEMINI_API_KEY:
        return None
    try:
        from google import genai

        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return _client
    except Exception as e:
        logger.warning("Gemini client init failed: %s", e)
        return None


def _generate(prompt: str, system: str | None = None, retries: int = 2) -> str:
    import time

    client = _get_client()
    if client is None:
        return _mock_reply(prompt, system)
    try:
        from google.genai import types
    except Exception as e:
        logger.warning("google.genai types import failed: %s", e)
        return _mock_reply(prompt, system)

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    cfg = types.GenerateContentConfig(
        system_instruction=system or "Bạn là Quillora, trợ lý đọc sách tiếng Việt.",
        temperature=0.4,
    )

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = client.models.generate_content(
                model=settings.LLM_MODEL, contents=contents, config=cfg
            )
            return (resp.text or "").strip()
        except Exception as e:
            last_err = e
            msg = str(e)
            transient = "503" in msg or "UNAVAILABLE" in msg or "429" in msg or "RESOURCE_EXHAUSTED" in msg
            if not transient or attempt == retries:
                break
            # Extract retry delay hint if present, else exponential backoff.
            m = re.search(r"retry in (\d+)", msg)
            delay = int(m.group(1)) + 1 if m else (3 + attempt * 4)
            delay = min(delay, 50)
            logger.info("Gemini transient error (%s), retry in %ds", msg[:80], delay)
            time.sleep(delay)

    logger.warning("Gemini generate failed after %d retries: %s", retries, last_err)
    return _mock_reply(prompt, system)


# ---------- public API ----------

def answer_with_context(question: str, context: str, book_title: str, *, history: list[dict] | None = None) -> str:
    system = (
        "Bạn là Quillora, trợ lý đọc sách thân thiện của thư viện PTIT. "
        "Hãy trả lời như một người bạn học giỏi đang giải thích cho bạn mình — "
        "tự nhiên, dễ hiểu, có cảm xúc, tránh giọng máy móc hoặc liệt kê khô khan.\n\n"
        "Quy tắc:\n"
        "1. Nếu ngữ cảnh đủ → trả lời bám sát, chèn [Chương · tr.X] sau các ý chính.\n"
        "2. Nếu ngữ cảnh KHÔNG đủ → nói thẳng 'Trong sách chưa đề cập phần này, "
        "nhưng mình biết thêm:' rồi bổ sung bằng kiến thức chung. KHÔNG chèn trích dẫn giả.\n"
        "3. Luôn dùng tiếng Việt tự nhiên. Có thể dùng ví dụ đời thường để giải thích "
        "khái niệm khó. Thi thoảng khích lệ người đọc.\n"
        "4. Nếu người đọc hỏi tiếp về chủ đề trước, hãy dựa vào lịch sử hội thoại "
        "để trả lời liền mạch, không lặp lại phần đã nói."
    )

    # Build conversation history into prompt
    history_text = ""
    if history:
        parts = []
        for msg in history:
            role_label = "Người đọc" if msg["role"] == "user" else "Quillora"
            parts.append(f"{role_label}: {msg['text']}")
        history_text = "\n".join(parts)

    prompt = f"Cuốn sách: {book_title}\n\n"
    if history_text:
        prompt += f"### Lịch sử hội thoại\n{history_text}\n\n"
    prompt += (
        f"### Ngữ cảnh lấy từ sách\n{context}\n\n"
        f"### Câu hỏi mới nhất\n{question}\n\n"
        f"### Trả lời"
    )
    return _generate(prompt, system)


def describe_book(title: str, context: str) -> str:
    """Generate a short 1–2 sentence human-friendly description for book card.
    Must NOT quote raw chunks — must paraphrase into clean marketing-style blurb."""
    system = (
        "Bạn là biên tập viên thư viện PTIT. Hãy diễn đạt lại (không trích "
        "nguyên văn) nội dung cuốn sách thành một đoạn ngắn gọn, mạch lạc, "
        "hấp dẫn người đọc. Dùng tiếng Việt tự nhiên."
    )
    prompt = (
        f"Cuốn sách: \"{title}\"\n\n"
        f"Dưới đây là một số đoạn trích để bạn tham khảo nội dung:\n"
        f"---\n{context[:3500]}\n---\n\n"
        f"Viết 1–2 câu (tối đa 45 từ) mô tả cuốn sách này nói về gì, "
        f"ai nên đọc. Không trích dẫn, không chép nguyên văn, không đánh số "
        f"mục lục, không viết 'Cuốn sách này...'. Chỉ trả về đoạn mô tả, "
        f"không kèm giải thích."
    )
    text = _generate(prompt, system).strip()
    # Strip wrapping quotes if any
    text = text.strip('"').strip("'").strip("`").strip()
    # Keep at most 2 sentences
    parts = re.split(r"(?<=[.!?])\s+", text)
    if len(parts) > 2:
        text = " ".join(parts[:2])
    return text


def summarize(context: str, book_title: str, length: str = "200 từ") -> str:
    system = "Bạn tóm tắt sách chính xác, bám sát ngữ cảnh, không bịa."
    prompt = (
        f"Tóm tắt cuốn '{book_title}' dựa trên các đoạn sau, độ dài khoảng {length}. "
        f"Kết bài bằng 3 ý chính để ghi nhớ.\n\n{context}"
    )
    return _generate(prompt, system)


def make_quiz(context: str, book_title: str, n: int = 5, topic: str | None = None) -> list[dict]:
    system = "Bạn sinh quiz trắc nghiệm chất lượng, bám ngữ cảnh, không đoán mò."
    topic_line = (
        f"Chủ đề trọng tâm: '{topic}'. Ưu tiên các câu liên quan tới chủ đề này.\n"
        if topic
        else ""
    )
    prompt = (
        f"Dựa trên nội dung cuốn '{book_title}' dưới đây, sinh {n} câu hỏi trắc nghiệm "
        f"(mỗi câu 4 lựa chọn, 1 đáp án đúng). {topic_line}"
        f'Chỉ trả JSON dạng: {{"questions":[{{"q":"...","choices":["...","...","...","..."],"answer":"A","explain":"..."}}]}} '
        f'trong đó "answer" là một trong A/B/C/D tương ứng với thứ tự lựa chọn. '
        f'Các phần tử "choices" KHÔNG cần kèm tiền tố "A." / "B.".\n\n'
        f"### Nội dung\n{context}"
    )
    raw = _generate(prompt, system)
    return _extract_json(raw).get("questions", [])


def make_flashcards(context: str, book_title: str, n: int = 6, topic: str | None = None) -> list[dict]:
    system = "Bạn sinh flashcard Term↔Definition rõ ràng, bám ngữ cảnh."
    topic_line = (
        f"Chủ đề trọng tâm: '{topic}'. Ưu tiên các thuật ngữ thuộc chủ đề này.\n"
        if topic
        else ""
    )
    prompt = (
        f"Từ nội dung cuốn '{book_title}', tạo {n} flashcard ngắn gọn. {topic_line}"
        f'Trả về JSON: {{"cards":[{{"term":"...","definition":"..."}}]}}\n\n{context}'
    )
    raw = _generate(prompt, system)
    return _extract_json(raw).get("cards", [])


IMAGE_PROMPT_PREFIX = "masterpiece, best quality, colorful, vibrant colors, "


def excerpt_to_image_prompt(excerpt: str) -> str:
    system = "Bạn chuyển đoạn văn thành prompt tiếng Anh cô đọng cho mô hình sinh ảnh."
    prompt = (
        "Viết 1 prompt ngắn (<= 40 từ) bằng tiếng Anh miêu tả cảnh trong đoạn văn sau "
        "theo phong cách minh hoạ sách thiếu nhi (children's book illustration, soft watercolor, "
        "vivid colors, whimsical, dreamy atmosphere, pastel tones). "
        "Không kèm chú thích.\n\n"
        f"{excerpt}"
    )
    raw = _generate(prompt, system).strip().strip('"')
    return IMAGE_PROMPT_PREFIX + raw


# ---------- helpers ----------

def _extract_json(text: str) -> dict[str, Any]:
    if not text:
        return {}
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def _mock_reply(prompt: str, system: str | None) -> str:
    """Deterministic fallback so demo loads without API key."""
    sysl = (system or "").lower()
    if "mcq" in prompt.lower() or "quiz" in prompt.lower():
        return json.dumps(
            {
                "questions": [
                    {
                        "q": "Cuốn sách thuộc chủ đề chính nào?",
                        "choices": ["A. Văn học", "B. Kỹ thuật", "C. Lịch sử", "D. Khác"],
                        "answer": "B",
                        "explain": "Đây là câu mock — hãy cấu hình GEMINI_API_KEY để có quiz thật.",
                    }
                ]
            },
            ensure_ascii=False,
        )
    if "flashcard" in prompt.lower():
        return json.dumps(
            {"cards": [{"term": "Demo term", "definition": "Cấu hình GEMINI_API_KEY để có flashcard thật."}]},
            ensure_ascii=False,
        )
    if "tóm tắt" in prompt.lower() or "summar" in sysl:
        return "Bản tóm tắt mock — vui lòng cấu hình GEMINI_API_KEY để Quillora tóm tắt thật từ nội dung sách."
    if "image prompt" in prompt.lower() or "phong cách minh hoạ" in prompt.lower() or "children's book" in prompt.lower():
        return "children's book illustration of a cozy library scene, soft watercolor, vivid colors, whimsical dreamy atmosphere, pastel tones, warm golden light"
    return (
        "(Demo mock) Tôi cần GEMINI_API_KEY để trả lời đầy đủ. "
        "Dưới đây là ngữ cảnh liên quan nhất mà tôi tìm được trong sách:\n\n"
        + prompt.split("### Ngữ cảnh")[-1].split("### Câu hỏi")[0][:600]
    )
