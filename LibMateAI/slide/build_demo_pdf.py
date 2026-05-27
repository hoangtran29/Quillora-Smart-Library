"""Build Quillora Demo PDF v5 — Times New Roman 13pt, polished layout."""
import os
from fpdf import FPDF

SLIDE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SLIDE_DIR, "screenshots")
OUT = os.path.join(SLIDE_DIR, "Quillora_Demo_v5.pdf")

FONT = "C:/Windows/Fonts/times.ttf"
FONT_B = "C:/Windows/Fonts/timesbd.ttf"
FONT_I = "C:/Windows/Fonts/timesi.ttf"

RED = (190, 17, 40)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
LIGHT = (210, 210, 210)
PAGE_W = 210
MARGIN = 20
CONTENT_W = PAGE_W - 2 * MARGIN  # 170mm


class DemoPDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("T", "", FONT)
        self.add_font("T", "B", FONT_B)
        self.add_font("T", "I", FONT_I)
        self.set_auto_page_break(False)
        self._pg = 0
        self.total = 22

    def new_page(self):
        self._pg += 1
        self.add_page()
        # Top accent bar
        self.set_fill_color(*RED)
        self.rect(0, 0, 210, 3, "F")
        # Footer line
        self.set_draw_color(*LIGHT)
        self.set_line_width(0.2)
        self.line(MARGIN, 285, PAGE_W - MARGIN, 285)
        # Footer text
        self.set_font("T", "I", 9)
        self.set_text_color(*GRAY)
        self.text(MARGIN, 291, "Quillora — Nền tảng đọc sách thông minh cho sinh viên PTIT")
        self.text(PAGE_W - MARGIN - 8, 291, f"{self._pg}")
        self.set_text_color(*BLACK)
        return 12

    def tag(self, y, text):
        self.set_fill_color(255, 235, 238)
        self.set_font("T", "B", 10)
        w = self.get_string_width(text) + 12
        self.rect(MARGIN, y, w, 7, "F")
        self.set_text_color(*RED)
        self.text(MARGIN + 6, y + 5.2, text)
        self.set_text_color(*BLACK)
        return y + 12

    def h1(self, y, text):
        self.set_font("T", "B", 20)
        self.set_text_color(*BLACK)
        self.text(MARGIN, y, text)
        return y + 10

    def para(self, y, text):
        self.set_font("T", "", 13)
        self.set_text_color(*BLACK)
        self.set_xy(MARGIN, y)
        self.multi_cell(CONTENT_W, 10, text)  # 1.5 line spacing (~10mm for 13pt)
        return self.get_y() + 4

    def label(self, y, text):
        self.set_font("T", "B", 13)
        self.set_text_color(*BLACK)
        # Small red square accent
        self.set_fill_color(*RED)
        self.rect(MARGIN, y - 3.5, 3, 3, "F")
        self.text(MARGIN + 6, y, text)
        return y + 7

    def bullet_list(self, y, items):
        self.set_font("T", "", 13)
        self.set_text_color(*BLACK)
        for item in items:
            self.set_xy(MARGIN + 3, y)
            self.set_text_color(*RED)
            self.cell(5, 5, chr(8226))
            self.set_text_color(*BLACK)
            self.set_xy(MARGIN + 8, y)
            self.multi_cell(CONTENT_W - 10, 8, item)  # 1.5 line spacing
            y = self.get_y() + 3
        return y

    def screenshot(self, y, filename, max_h=115):
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            self.set_draw_color(*LIGHT)
            self.rect(MARGIN, y, CONTENT_W, 30, "D")
            self.set_font("T", "I", 11)
            self.set_text_color(*GRAY)
            self.text(MARGIN + 50, y + 17, f"[ {filename} ]")
            self.set_text_color(*BLACK)
            return y + 34

        from PIL import Image
        img = Image.open(path)
        ratio = img.height / img.width
        h = CONTENT_W * ratio
        if h > max_h:
            h = max_h

        # Shadow-like border
        self.set_draw_color(190, 190, 190)
        self.set_line_width(0.3)
        self.rect(MARGIN - 0.3, y - 0.3, CONTENT_W + 0.6, h + 0.6, "D")
        self.image(path, MARGIN, y, CONTENT_W, h)
        return y + h + 5

    def note(self, y, text):
        self.set_draw_color(*RED)
        self.set_line_width(0.6)
        self.line(MARGIN, y, MARGIN, y + 14)
        self.set_font("T", "I", 12)
        self.set_text_color(*BLACK)
        self.set_xy(MARGIN + 4, y)
        self.multi_cell(CONTENT_W - 6, 8, text)  # 1.5 line spacing
        return self.get_y() + 4


def build():
    pdf = DemoPDF()

    # ══════ 1. BÌA ══════
    y = pdf.new_page()
    pdf.set_font("T", "B", 12)
    pdf.set_text_color(*RED)
    pdf.text(MARGIN, 15, "NGÀY HỘI ĐỌC SÁCH PTIT 2026")
    pdf.set_font("T", "", 12)
    pdf.set_text_color(*BLACK)
    pdf.text(MARGIN, 22, "Học viện Công nghệ Bưu chính Viễn thông")

    pdf.set_font("T", "B", 40)
    pdf.set_text_color(*BLACK)
    pdf.text(MARGIN, 48, "Quillora")
    pdf.set_text_color(*RED)
    pdf.text(MARGIN + pdf.get_string_width("Quillora"), 48, ".")
    pdf.set_text_color(*BLACK)

    pdf.set_font("T", "", 16)
    pdf.text(MARGIN, 58, "Nền tảng đọc sách thông minh ứng dụng AI cho sinh viên PTIT")

    pdf.set_font("T", "I", 13)
    pdf.set_text_color(*RED)
    pdf.text(MARGIN, 67, '"Từ ngòi bút đến bình minh tri thức"')
    pdf.set_text_color(*BLACK)

    y = pdf.screenshot(75, "trangchu.png", max_h=115)
    pdf.note(y, "Giao diện trang chủ với hero section, kệ sách giáo trình PTIT, nút CTA vào thư viện. Responsive, hỗ trợ dark mode.")

    # ══════ 2. GIỚI THIỆU MỞ ĐẦU ══════
    y = pdf.new_page()
    y = pdf.tag(y, "GIỚI THIỆU")
    y = pdf.h1(y, "Quillora là gì?")
    y = pdf.para(y,
        "Quillora là nền tảng đọc sách thông minh ứng dụng trí tuệ nhân tạo tạo sinh (Generative AI) "
        "kết hợp kỹ thuật RAG (Retrieval-Augmented Generation), được phát triển dành riêng cho sinh viên "
        "Học viện Công nghệ Bưu chính Viễn thông (PTIT)."
    )
    y = pdf.para(y,
        "Tên gọi \"Quillora\" được ghép từ Quill (ngòi bút — biểu tượng tri thức) và Aurora "
        "(bình minh — sự khai sáng), mang ý nghĩa: từ mỗi trang sách, tri thức được khai sáng."
    )
    y = pdf.label(y, "Vấn đề Quillora giải quyết")
    y = pdf.para(y,
        "Theo thống kê của Bộ Giáo dục và Đào tạo, trung bình mỗi người Việt Nam đọc khoảng 4 cuốn sách/năm, "
        "nhưng 2,8 cuốn trong đó là sách giáo khoa — tức chỉ khoảng 1,2 cuốn sách tự chọn/năm. "
        "26% dân số không bao giờ đọc sách. Sinh viên kỹ thuật thì ngược lại — phải đọc hàng chục giáo trình "
        "dày đặc mỗi học kỳ nhưng thiếu công cụ hỗ trợ thông minh."
    )
    y = pdf.label(y, "Giải pháp")
    y = pdf.para(y,
        "Quillora biến mỗi cuốn sách thành một trợ lý học tập cá nhân. Sinh viên có thể hỏi đáp trực tiếp "
        "với nội dung sách (kèm trích dẫn chương/trang), tạo quiz và flashcard để ôn tập chủ động, "
        "tóm tắt nội dung, minh hoạ đoạn văn bằng AI, và trò chuyện bằng giọng nói — tất cả trong một giao diện web duy nhất."
    )
    y = pdf.label(y, "Tài liệu này trình bày")
    y = pdf.bullet_list(y, [
        "Toàn bộ giao diện và chức năng của Quillora thông qua ảnh chụp màn hình thực tế.",
        "Mô tả chi tiết cách hoạt động của từng tính năng.",
        "Công nghệ sử dụng và cơ sở khoa học đằng sau các quyết định thiết kế.",
    ])

    # ══════ 3. THƯ VIỆN ══════
    y = pdf.new_page()
    y = pdf.tag(y, "THƯ VIỆN SÁCH")
    y = pdf.h1(y, "Kệ sách giáo trình PTIT")
    y = pdf.para(y, "Hiển thị tất cả giáo trình dưới dạng grid card. Mỗi card có: bìa sách (Google Books), tóm tắt AI, danh mục, mức độ khó, nút yêu thích. Click vào bất kỳ sách nào để mở reader.")
    y = pdf.screenshot(y, "thuvien.png", max_h=110)
    y = pdf.bullet_list(y, [
        "10 giáo trình PTIT sẵn có: Mạng máy tính, Hệ điều hành, CTDL, Java, CNPM, Đồ hoạ, ATTT, Kho DL, Toán rời rạc, AI.",
        "Bìa sách thật từ Google Books API. Tóm tắt AI tự động.",
        "Đánh dấu yêu thích — lưu vào trang cá nhân.",
        "Upload thêm PDF: kéo thả → trích xuất → embedding → sẵn sàng chat trong vài giây.",
    ])

    # ══════ 3. ĐĂNG NHẬP ══════
    y = pdf.new_page()
    y = pdf.tag(y, "XÁC THỰC")
    y = pdf.h1(y, "Đăng nhập & Đăng ký")
    y = pdf.para(y, "Hai phương thức: email/password hoặc Microsoft OAuth qua Auth0. Sinh viên PTIT đăng nhập 1-click bằng email @stu.ptit.edu.vn — không cần tạo tài khoản riêng.")
    y = pdf.label(y, "Modal đăng nhập")
    y = pdf.screenshot(y, "dangnhap.png", max_h=100)
    # Page break for second image
    y = pdf.new_page()
    y = pdf.tag(y, "XÁC THỰC")
    y = pdf.label(y + 2, "Modal đăng ký — thông tin cơ bản")
    y = pdf.screenshot(y, "dangki.png", max_h=100)

    # Page break for third image
    y = pdf.new_page()
    y = pdf.tag(y, "XÁC THỰC")
    y = pdf.label(y + 2, "Modal đăng ký — hoàn thiện hồ sơ (MSV, ngành, ngày sinh)")
    y = pdf.screenshot(y, "dangki2.png", max_h=100)
    y = pdf.bullet_list(y, [
        "Email/password: đăng ký với MSV, ngành học, ngày sinh. JWT token 7 ngày.",
        "Microsoft OAuth: Auth0 → xác thực email @ptit.edu.vn / @stu.ptit.edu.vn tự động.",
        "Auto-verify token: reload trang vẫn giữ phiên đăng nhập.",
    ])

    # ══════ 4. ĐỌC SÁCH ══════
    y = pdf.new_page()
    y = pdf.tag(y, "ĐỌC SÁCH PDF")
    y = pdf.h1(y, "PDF Reader trên trình duyệt")
    y = pdf.para(y, "Đọc giáo trình trực tiếp trên web với PDF.js — zoom, cuộn trang, lazy loading. Không cần tải về hay cài phần mềm.")
    y = pdf.screenshot(y, "docsach.png", max_h=120)
    y = pdf.bullet_list(y, [
        "PDF.js (Mozilla): render PDF client-side, lazy load từng trang khi scroll.",
        "Zoom: 43% → 214%. Download PDF gốc với tên file tiếng Việt có dấu.",
        "Tab navigation: Đọc sách / Hỏi đáp / Tóm tắt / Quiz / Flashcard / Minh hoạ / Nghe sách.",
    ])

    # ══════ 5. HỎI ĐÁP (câu hỏi đầu tiên) ══════
    y = pdf.new_page()
    y = pdf.tag(y, "HỎI ĐÁP AI")
    y = pdf.h1(y, "Chat trực tiếp với sách")
    y = pdf.para(y, "Đặt câu hỏi bằng tiếng Việt tự nhiên. Quillora tìm đúng đoạn liên quan trong sách (RAG), sinh câu trả lời kèm trích dẫn [Chương · tr.X]. Hỗ trợ lịch sử hội thoại liền mạch.")
    y = pdf.label(y, "Câu hỏi đầu tiên")
    y = pdf.screenshot(y, "hoidap.png", max_h=120)

    # ══════ 6. HỎI ĐÁP (tiếp) ══════
    y = pdf.new_page()
    y = pdf.tag(y, "HỎI ĐÁP AI")
    y = pdf.label(y + 2, "Hỏi tiếp — AI nhớ ngữ cảnh (chat history)")
    y = pdf.screenshot(y, "hoidap2.png", max_h=100)
    y = pdf.label(y, "Câu trả lời format Markdown (bold, danh sách, trích dẫn)")
    y = pdf.screenshot(y, "hoidap3.png", max_h=100)

    # ══════ 7. TÓM TẮT ══════
    y = pdf.new_page()
    y = pdf.tag(y, "TÓM TẮT SÁCH")
    y = pdf.h1(y, "Tóm tắt nội dung bằng AI")
    y = pdf.para(y, "Một nút bấm — có ngay bản tóm tắt ~200 từ giúp nắm bắt trọng tâm cuốn sách trước khi đọc sâu. RAG truy hồi các đoạn quan trọng nhất, Gemini 2.5 Flash sinh tóm tắt.")
    y = pdf.label(y, "Kết quả tóm tắt")
    y = pdf.screenshot(y, "tomtat.png", max_h=130)

    # ══════ 8. QUIZ ══════
    y = pdf.new_page()
    y = pdf.tag(y, "QUIZ TỰ ĐỘNG")
    y = pdf.h1(y, "Ôn tập bằng trắc nghiệm AI")
    y = pdf.para(y, "Sinh 3–20 câu hỏi trắc nghiệm theo chủ đề tuỳ chọn từ nội dung sách gốc. Chấm điểm tức thì, giải thích đáp án chi tiết. Làm quiz giúp nhớ gấp 5x so với đọc lại (Roediger, 2006).")
    y = pdf.label(y, "Tạo quiz theo chủ đề")
    y = pdf.screenshot(y, "sinhquiz.png", max_h=120)

    # Quiz page 2
    y = pdf.new_page()
    y = pdf.tag(y, "QUIZ TỰ ĐỘNG")
    y = pdf.label(y + 2, "Kết quả chấm điểm — highlight đúng/sai + giải thích")
    y = pdf.screenshot(y, "sinhquiz2.png", max_h=120)
    y = pdf.bullet_list(y, [
        "4 đáp án A/B/C/D, 1 đáp án đúng, giải thích chi tiết cho từng câu.",
        "Lưu lịch sử quiz vào trang cá nhân: book, score, topic, thời gian.",
    ])

    # ══════ 9. FLASHCARD ══════
    y = pdf.new_page()
    y = pdf.tag(y, "FLASHCARD")
    y = pdf.h1(y, "Flashcard ôn tập nhanh")
    y = pdf.para(y, "Tạo 3–20 thẻ thuật ngữ – định nghĩa từ nội dung sách. Click lật thẻ. Ôn tập trong 24h đầu tăng 80% ghi nhớ (Murre & Dros, 2015).")
    y = pdf.label(y, "Mặt trước (thuật ngữ)")
    y = pdf.screenshot(y, "flashcard.png", max_h=100)

    # Flashcard page 2
    y = pdf.new_page()
    y = pdf.tag(y, "FLASHCARD")
    y = pdf.label(y + 2, "Mặt sau (lật thẻ — định nghĩa)")
    y = pdf.screenshot(y, "flashcard2.png", max_h=120)

    # ══════ 10. MINH HOẠ ══════
    y = pdf.new_page()
    y = pdf.tag(y, "MINH HOẠ ĐOẠN VĂN")
    y = pdf.h1(y, "AI vẽ tranh từ đoạn văn")
    y = pdf.para(y, "Chọn đoạn văn yêu thích → AI chuyển thành prompt tiếng Anh → Gemini Image Generation vẽ tranh phong cách watercolor / children's book illustration. Ảnh lưu vào Tường tranh cá nhân.")
    y = pdf.label(y, "Nhập đoạn văn & sinh ảnh")
    y = pdf.screenshot(y, "minhhoaanh.png", max_h=100)

    # Minh hoa page 2
    y = pdf.new_page()
    y = pdf.tag(y, "MINH HOẠ ĐOẠN VĂN")
    y = pdf.label(y + 2, "Kết quả minh hoạ AI")
    y = pdf.screenshot(y, "minhhoa2.png", max_h=120)
    y = pdf.note(y, "Phong cách: masterpiece, best quality, colorful, vibrant colors, children's book illustration, soft watercolor.")

    # ══════ 11. TƯỜNG TRANH ══════
    y = pdf.new_page()
    y = pdf.tag(y, "TƯỜNG TRANH")
    y = pdf.h1(y, "Gallery minh hoạ cá nhân")
    y = pdf.para(y, "Mỗi user có tường tranh riêng — lưu lại tất cả ảnh AI đã gen. Đăng nhập khác → tường tranh khác. Lưu trữ vĩnh viễn trên server.")
    y = pdf.label(y, "Tường tranh /wall")
    y = pdf.screenshot(y, "tuongtranh.png", max_h=130)

    # ══════ 12. CHATBOT ══════
    y = pdf.new_page()
    y = pdf.tag(y, "CHATBOT THƯ VIỆN")
    y = pdf.h1(y, "Trợ lý nổi — hỏi đáp đa sách")
    y = pdf.para(y, "FAB góc phải dưới, luôn hiện ở mọi trang. Tìm kiếm ngữ nghĩa xuyên suốt toàn bộ thư viện, trích dẫn từ nhiều sách.")
    y = pdf.label(y, "Chatbot nổi")
    y = pdf.screenshot(y, "chatbot.png", max_h=120)
    y = pdf.bullet_list(y, [
        "Cross-book RAG: hỏi 1 câu → tìm trong TẤT CẢ sách cùng lúc.",
        "Gợi ý câu hỏi mẫu, lịch sử hội thoại liền mạch.",
    ])

    # ══════ 13. UPLOAD ══════
    y = pdf.new_page()
    y = pdf.tag(y, "TẢI TÀI LIỆU")
    y = pdf.h1(y, "Upload PDF — sẵn sàng chat vài giây")
    y = pdf.para(y, "Kéo thả PDF (max 20MB) → tự động trích xuất text, chunking, embedding, sinh tóm tắt AI → sẵn sàng hỏi đáp & ôn tập.")
    y = pdf.label(y, "Modal upload tài liệu")
    y = pdf.screenshot(y, "upload.png", max_h=130)

    # ══════ 14. TRANG CÁ NHÂN ══════
    y = pdf.new_page()
    y = pdf.tag(y, "TRANG CÁ NHÂN")
    y = pdf.h1(y, "Dashboard học tập cá nhân")
    y = pdf.para(y, "Thống kê sách đã đọc, điểm quiz trung bình, sách yêu thích, lịch sử ôn tập — theo dõi tiến bộ qua thời gian.")
    y = pdf.label(y, "Thống kê & sách yêu thích")
    y = pdf.screenshot(y, "trangcanhan.png", max_h=100)

    # Page 2
    y = pdf.new_page()
    y = pdf.tag(y, "TRANG CÁ NHÂN")
    y = pdf.label(y + 2, "Lịch sử đọc & Quiz history")
    y = pdf.screenshot(y, "trangcanhan2.png", max_h=120)

    # ══════ 15. GIỚI THIỆU ══════
    y = pdf.new_page()
    y = pdf.tag(y, "GIỚI THIỆU")
    y = pdf.h1(y, "Trang About — 4 tính năng nổi bật")
    y = pdf.para(y, "Trang /about trình bày 4 tính năng cốt lõi với mô tả cuốn hút, số liệu khoa học — thuyết phục người dùng ngay từ lần đầu truy cập.")
    y = pdf.label(y, "Giao diện trang giới thiệu")
    y = pdf.screenshot(y, "tranggioithieu.png", max_h=120)
    y = pdf.bullet_list(y, [
        "Hỏi là có, trích dẫn luôn trang sách — RAG giảm 94% câu trả lời sai.",
        "Ôn thi 10 phút thay 10 tiếng — Quiz nhớ gấp 5x, Flashcard +80% ghi nhớ.",
        "Nói chuyện với sách bằng giọng nói thật — gia sư cá nhân realtime.",
        "Đọc đến đâu, vẽ tranh đến đó — hình ảnh giúp nhớ sâu hơn 65%.",
    ])

    pdf.total = pdf._pg  # update total
    pdf.output(OUT)
    print(f"Saved: {OUT}")
    print(f"Pages: {pdf._pg}")


if __name__ == "__main__":
    build()
