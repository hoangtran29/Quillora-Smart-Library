# Quillora — Nền tảng đọc sách thông minh cho sinh viên

> **Cuộc thi**: Ngày hội đọc sách PTIT 2026
> **Nhóm phát triển**: Học viện Công nghệ Bưu chính Viễn thông (PTIT)

---

## 1. Tên đề tài / Sản phẩm

**Quillora — Nền tảng đọc sách thông minh ứng dụng AI cho sinh viên PTIT**

> *"Quillora"* được ghép từ **Quill** (ngòi bút — biểu tượng tri thức) và **Aurora** (bình minh — sự khai sáng), mang ý nghĩa: **từ mỗi trang sách, tri thức được khai sáng.**

---

## 2. Mô tả vấn đề thực tiễn

### 2.1. Thực trạng đọc sách tại Việt Nam — Những con số đáng báo động

Theo thống kê của Bộ Giáo dục và Đào tạo, **trung bình mỗi người Việt Nam đọc khoảng 4 cuốn sách/năm, nhưng 2,8 cuốn trong đó là sách giáo khoa** — tức chỉ khoảng **1,2 cuốn sách tự chọn/năm** *(Báo Giáo dục và Thời đại, 2024)*. Con số này thấp hơn rất nhiều so với mức trung bình **20 cuốn/năm** tại Israel, Phần Lan, Pháp, Nhật Bản, hay **14 cuốn/năm** tại Singapore, Malaysia, Thái Lan *(Báo Pháp Luật, 2024)*.

Đáng lo ngại hơn: **26% dân số Việt Nam không bao giờ đọc sách**, 44% thỉnh thoảng đọc, và chỉ 30% đọc thường xuyên *(Báo Đầu tư, 2024)*.

### 2.2. Thách thức cụ thể đối với sinh viên kỹ thuật

Tại PTIT — nơi **tuyển sinh khoảng 8.000 sinh viên/năm** *(ptit.edu.vn, 2026)* — sinh viên đối mặt với những rào cản đặc thù:

- **Giáo trình dày, thuật ngữ chuyên ngành phức tạp**: Các môn như Hệ điều hành, Mạng máy tính, Cơ sở dữ liệu… có giáo trình hàng trăm trang với mật độ kiến thức cao. Sinh viên mất nhiều thời gian đọc nhưng khó nắm bắt trọng tâm.

- **Thiếu công cụ hỗ trợ đọc chủ động**: Thư viện số hiện tại chỉ cung cấp file PDF tĩnh — sinh viên không thể tra cứu nhanh, đặt câu hỏi hay kiểm tra hiểu biết ngay trong quá trình đọc.

- **Ôn tập thiếu hiệu quả — Đường cong lãng quên Ebbinghaus**: Theo nghiên cứu kinh điển của Ebbinghaus (1885), con người **quên 56% kiến thức chỉ sau 1 giờ** và **lên đến 79% sau 31 ngày** nếu không ôn tập *(Ebbinghaus, 1885; Murre & Dros, 2015)*. Trước kỳ thi, sinh viên thường đọc lại toàn bộ giáo trình (passive review) — một phương pháp được chứng minh là kém hiệu quả hơn nhiều so với active recall.

- **Rào cản ngôn ngữ và cách diễn đạt**: Nhiều giáo trình viết bằng ngôn ngữ học thuật khô khan, khiến sinh viên — đặc biệt năm nhất — khó tiếp cận và nhanh mất hứng thú.

- **Thiếu tương tác và cá nhân hoá**: Mỗi sinh viên có nền tảng và tốc độ học khác nhau, nhưng tài liệu hiện tại là "một chiều" — không thể giải đáp thắc mắc cá nhân hay điều chỉnh cách trình bày.

### 2.3. Bối cảnh thị trường và cơ hội

- **Thị trường AI trong giáo dục** toàn cầu đạt **7,5 tỷ USD năm 2025**, dự kiến tăng lên **42,5 tỷ USD vào 2030** với tốc độ tăng trưởng **40,9%/năm** *(GlobeNewsWire, 2026)*. Khu vực châu Á — Thái Bình Dương dẫn đầu tốc độ tăng trưởng với **CAGR 44,2%** *(Grand View Research, 2025)*.

- **Thị trường EdTech Việt Nam** đạt **1 tỷ USD năm 2024**, dự kiến tăng lên **3 tỷ USD vào 2033** *(IMARC Group, 2025)*. **50% cơ sở giáo dục đại học** tại Việt Nam đã triển khai chương trình học trực tuyến một phần hoặc toàn phần *(Austrade, 2025)*.

- **Hơn 2 triệu sinh viên đại học** tại Việt Nam trong năm 2024 *(Statista, 2025)* — một thị trường lớn đang thiếu công cụ đọc sách thông minh.

### 2.4. Nhu cầu thực tế

Sinh viên cần một nền tảng đọc sách **thông minh**, nơi họ có thể:

- Đặt câu hỏi trực tiếp về nội dung sách và nhận câu trả lời có trích dẫn trang/chương cụ thể.
- Tóm tắt nhanh nội dung để nắm bắt trọng tâm trước khi đọc sâu.
- Tự tạo quiz và flashcard từ nội dung sách để ôn tập chủ động.
- Tìm kiếm ngữ nghĩa xuyên suốt nhiều cuốn sách thay vì chỉ tìm từ khoá.
- Có trải nghiệm đọc sách sinh động, tương tác và cá nhân hoá.

---

## 3. Giải pháp ứng dụng AI

**Quillora** là một nền tảng web ứng dụng trí tuệ nhân tạo tạo sinh (Generative AI) kết hợp kỹ thuật RAG (Retrieval-Augmented Generation) để biến mỗi cuốn sách thành một **trợ lý học tập cá nhân**.

### 3.1. Kiến trúc RAG — Trả lời bám sát nội dung sách

> **Tại sao RAG?** Nghiên cứu cho thấy kỹ thuật RAG giúp **giảm tỷ lệ ảo giác (hallucination) của LLM xuống còn ~5,8%** với Self-reflective RAG *(ACL Anthology, 2024)*, và framework Dual-Pathway KG-RAG **giảm 18% hallucination** trong các bài toán hỏi đáp *(MDPI Electronics, 2025)*. Điều này đặc biệt quan trọng trong giáo dục — sinh viên cần câu trả lời chính xác, có nguồn gốc, không phải thông tin bịa đặt.

Thay vì để AI "tưởng tượng" câu trả lời, Quillora sử dụng quy trình RAG:

1. **Trích xuất & Chunking**: Khi sách được tải lên, hệ thống tự động trích xuất văn bản từ PDF, chia thành các đoạn (chunk) ~900–1100 ký tự với phần chồng lấp để giữ ngữ cảnh liên tục.

2. **Embedding**: Mỗi chunk được chuyển thành vector nhúng (embedding) bằng mô hình đa ngữ `paraphrase-multilingual-MiniLM-L12-v2`, cho phép tìm kiếm ngữ nghĩa tiếng Việt chính xác.

3. **Retrieval**: Khi người dùng đặt câu hỏi, hệ thống tìm top-K chunk liên quan nhất bằng cosine similarity, kèm thông tin chương và trang.

4. **Generation**: Các chunk được đưa vào prompt cùng lịch sử hội thoại, LLM sinh câu trả lời bám sát ngữ cảnh và chèn trích dẫn `[Chương · tr.X]`.

### 3.2. Hệ thống tính năng AI

| # | Tính năng | Mô tả | Công nghệ AI |
|---|-----------|-------|---------------|
| 1 | **Hỏi đáp thông minh** | Chat trực tiếp với từng cuốn sách, mọi câu trả lời kèm trích dẫn chương/trang | RAG + Gemini LLM |
| 2 | **Chatbot thư viện** | Trợ lý nổi (floating) hỏi đáp xuyên suốt toàn bộ thư viện, tìm kiếm đa sách | RAG đa sách + Gemini |
| 3 | **Tóm tắt sách** | Tóm tắt nội dung chính của sách trong ~200 từ | RAG + Gemini |
| 4 | **Tạo Quiz tự động** | Sinh 3–20 câu hỏi trắc nghiệm từ nội dung sách, hỗ trợ lọc theo chủ đề. Dựa trên **Testing Effect** — nghiên cứu của Roediger & Karpicke (2006, *Psychological Science*) chứng minh: **làm 1 bài test giữ kiến thức tương đương 5 lần đọc lại**, và active retrieval **cải thiện 50% khả năng ghi nhớ dài hạn** so với đọc thụ động *(Karpicke & Blunt, 2011, Science)* | RAG + Gemini |
| 5 | **Flashcard ôn tập** | Tạo thẻ thuật ngữ–định nghĩa từ nội dung sách. Áp dụng nguyên lý **Spaced Repetition** — meta-analysis trên 184 nghiên cứu cho thấy ôn tập phân tán **vượt trội 10–30%** so với học dồn *(Cepeda et al., 2006)*. Ôn tập trong 24 giờ đầu giúp **tăng 80% khả năng nhớ** *(Murre & Dros, 2015)* | RAG + Gemini |
| 6 | **Minh hoạ đoạn văn** | Chọn đoạn văn yêu thích → AI vẽ tranh minh hoạ phong cách watercolor | Gemini Image Generation |
| 7 | **Nhập liệu bằng giọng nói** | Nói tiếng Việt để đặt câu hỏi thay vì gõ phím | Web Speech API |
| 8 | **Trò chuyện bằng giọng nói** | Đàm thoại realtime với "linh hồn" cuốn sách qua WebSocket | Gemini Live Audio API |
| 9 | **Tìm kiếm ngữ nghĩa** | Tìm kiếm theo ý nghĩa thay vì từ khoá, xuyên suốt nhiều cuốn sách | Sentence Transformers + Cosine Similarity |
| 10 | **Lịch sử hội thoại** | AI nhớ ngữ cảnh cuộc trò chuyện, trả lời liền mạch khi hỏi tiếp | Context Window Management |

### 3.3. Phong cách trả lời

Quillora được thiết kế với giọng điệu **thân thiện, tự nhiên** — như một người bạn học giỏi đang giải thích cho bạn mình:

- Dùng ví dụ đời thường để giải thích khái niệm khó.
- Khích lệ người đọc khi họ đặt câu hỏi hay.
- Khi sách không đủ thông tin, nói thẳng và bổ sung kiến thức chung (không bịa trích dẫn).
- Trả lời liền mạch dựa trên lịch sử hội thoại, không lặp lại phần đã nói.

---

## 4. Công nghệ dự kiến sử dụng

### 4.1. Backend

| Thành phần | Công nghệ | Vai trò |
|------------|-----------|---------|
| Web Framework | **FastAPI** (Python) | API server hiệu năng cao, hỗ trợ async, WebSocket |
| LLM | **Google Gemini 2.5 Flash** | Sinh câu trả lời, tóm tắt, quiz, flashcard, image prompt |
| Image Generation | **Gemini Image Generation** | Sinh tranh minh hoạ từ đoạn văn |
| Embedding | **Sentence Transformers** (`paraphrase-multilingual-MiniLM-L12-v2`) | Vector hoá văn bản tiếng Việt cho tìm kiếm ngữ nghĩa |
| PDF Processing | **PyPDF** | Trích xuất văn bản từ file PDF |
| Voice Realtime | **Gemini Live Audio API** | Đàm thoại giọng nói realtime qua WebSocket |
| Authentication | **JWT Token** + **Auth0 (Microsoft OAuth)** | Xác thực sinh viên PTIT qua email @stu.ptit.edu.vn |
| Server | **Uvicorn** | ASGI server production-ready |

### 4.2. Frontend

| Thành phần | Công nghệ | Vai trò |
|------------|-----------|---------|
| UI | **Vanilla JavaScript** (SPA) | Giao diện đơn trang, nhẹ, không phụ thuộc framework |
| PDF Viewer | **PDF.js** (Mozilla) | Hiển thị PDF trực tiếp trên trình duyệt |
| Voice Input | **Web Speech API** | Nhận dạng giọng nói tiếng Việt |
| Typography | **Google Fonts** (Be Vietnam Pro, Plus Jakarta Sans) | Font tiếng Việt tối ưu cho đọc sách |
| Styling | **CSS thuần** | Responsive, hỗ trợ dark mode, thiết kế hiện đại |

### 4.3. Hạ tầng & Triển khai

| Thành phần | Công nghệ | Vai trò |
|------------|-----------|---------|
| Container | **Docker** + **Docker Compose** | Đóng gói ứng dụng, triển khai nhất quán |
| Storage | **JSON file-based** (demo) → có thể mở rộng sang PostgreSQL + Milvus | Lưu trữ sách, chunk, embedding, user data |
| OAuth Provider | **Auth0** | Quản lý đăng nhập Microsoft cho sinh viên PTIT |

---

## 5. Điểm nổi bật và khả năng triển khai

### 5.1. Điểm nổi bật

#### a) Biến sách thành trợ lý cá nhân

Quillora không chỉ là thư viện số — mỗi cuốn sách trở thành một **trợ lý AI riêng** mà sinh viên có thể hỏi đáp, tranh luận và ôn tập. Câu trả lời luôn kèm trích dẫn chương/trang, giúp sinh viên dễ dàng tra cứu lại trong sách gốc.

#### b) Ôn tập chủ động với Quiz & Flashcard

Thay vì đọc lại toàn bộ giáo trình, sinh viên có thể:

- **Quiz**: Tạo 3–20 câu hỏi trắc nghiệm theo chủ đề tùy chọn. Hệ thống chấm điểm ngay lập tức, hiển thị giải thích chi tiết cho từng câu. Kết quả được lưu lại trong lịch sử cá nhân.
- **Flashcard**: Tạo thẻ thuật ngữ–định nghĩa, lật để ôn tập. Tập trung vào khái niệm cốt lõi thay vì chi tiết thừa.

#### c) Tìm kiếm ngữ nghĩa đa sách

Sinh viên không cần nhớ chính xác từ khoá — chỉ cần diễn đạt ý cần tìm bằng ngôn ngữ tự nhiên. Hệ thống tìm kiếm xuyên suốt toàn bộ thư viện và trả về kết quả liên quan nhất kèm trích dẫn nguồn.

#### d) Minh hoạ trực quan

Tính năng độc đáo: chọn một đoạn văn trong sách và để AI vẽ lại thành tranh minh hoạ phong cách watercolor/children's book. Ảnh được lưu lại trong **Tường tranh** — tạo động lực đọc sách và chia sẻ.

#### e) Tương tác đa phương thức

- **Gõ phím**: Chat truyền thống.
- **Giọng nói**: Nói tiếng Việt để đặt câu hỏi (Web Speech API).
- **Đàm thoại realtime**: Trò chuyện bằng giọng nói trực tiếp với "linh hồn" cuốn sách qua WebSocket — trải nghiệm như đang nói chuyện với tác giả.

#### f) Cá nhân hoá trải nghiệm

- **Lịch sử đọc sách**: Theo dõi sách đã mở, tab đã xem, tiếp tục đọc nhanh.
- **Sách yêu thích**: Đánh dấu sách hay để quay lại.
- **Thống kê ôn tập**: Xem điểm quiz trung bình, số lượt ôn, theo dõi tiến bộ.
- **Lịch sử hội thoại**: AI nhớ ngữ cảnh, trả lời liền mạch khi hỏi tiếp.

#### g) Đăng nhập bằng tài khoản Microsoft PTIT

Sinh viên đăng nhập nhanh bằng email `@stu.ptit.edu.vn` hoặc `@ptit.edu.vn` thông qua Microsoft OAuth — không cần tạo tài khoản riêng, xác thực danh tính sinh viên tự động.

#### h) Tải lên tài liệu riêng

Sinh viên có thể tải lên giáo trình hoặc tài liệu PDF của riêng mình. Hệ thống tự động:
- Trích xuất văn bản
- Chia chunk và tạo embedding
- Sinh tóm tắt AI cho bìa sách
- Sẵn sàng chat và ôn tập trong vài giây

### 5.2. Khả năng triển khai

#### a) Triển khai nhanh

- **Docker hoá hoàn chỉnh**: Chỉ cần `docker compose up` là có thể chạy toàn bộ hệ thống.
- **Cấu hình đơn giản**: Chỉ cần 1 API key (Gemini) là đủ cho mọi tính năng AI.
- **Không phụ thuộc GPU**: Tất cả inference qua API cloud, server chỉ cần CPU.

#### b) Chi phí vận hành thấp

- **Gemini API**: Có gói miễn phí với quota đủ cho demo và pilot.
- **Frontend tĩnh**: Không cần Node.js build, giảm phức tạp triển khai.
- **Storage file-based**: Phù hợp cho pilot 50–100 sinh viên, không cần database server.

#### c) Khả năng mở rộng

| Giai đoạn | Quy mô | Hạ tầng |
|-----------|--------|---------|
| Demo / Pilot | 50–100 sinh viên | JSON file storage, 1 container |
| Production | 500–2000 sinh viên | PostgreSQL + Milvus vector DB, load balancer |
| Mở rộng | Toàn trường / đa trường | Kubernetes, CDN cho PDF, cache Redis |

#### d) Lộ trình phát triển

| Mốc | Nội dung |
|-----|---------|
| **Hiện tại** | Web demo đầy đủ tính năng, sẵn sàng cho cuộc thi |
| **Ngắn hạn** | Tích hợp kho giáo trình PTIT, thêm sách giáo trình các khoa |
| **Trung hạn** | Chuyển sang PostgreSQL + Milvus, hỗ trợ đa ngôn ngữ, mobile app |
| **Dài hạn** | Hệ thống gợi ý sách cá nhân, phân tích tiến độ học tập, mở rộng đa trường |

---

## 6. Tổng kết

**Quillora** giải quyết bài toán thực tế: sinh viên kỹ thuật cần đọc nhiều giáo trình phức tạp nhưng thiếu công cụ hỗ trợ thông minh. Bằng cách kết hợp **RAG + Generative AI + đa phương thức**, Quillora biến mỗi cuốn sách thành một trợ lý cá nhân — giúp sinh viên đọc ít hiểu nhiều, ôn nhanh nhớ lâu.

| Chỉ số | Giá trị |
|--------|---------|
| Tổng tính năng AI | 10 tính năng chính |
| Tổng tính năng người dùng | 80+ tính năng chi tiết |
| Mô hình AI sử dụng | Gemini 2.5 Flash (LLM + Image + Voice) |
| Ngôn ngữ hỗ trợ | Tiếng Việt (giao diện + giọng nói + nội dung) |
| Thời gian triển khai | Sẵn sàng demo ngay |

---

## 7. Tài liệu tham khảo

### Nghiên cứu khoa học

1. **Ebbinghaus, H.** (1885). *Über das Gedächtnis*. Đường cong lãng quên: con người quên 56% sau 1 giờ, 79% sau 31 ngày nếu không ôn tập.
2. **Roediger, H. L., & Karpicke, J. D.** (2006). Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. *Psychological Science*, 17(3), 249–255. — Làm 1 bài test hiệu quả bằng 5 lần đọc lại. [PubMed](https://pubmed.ncbi.nlm.nih.gov/16507066/)
3. **Karpicke, J. D., & Blunt, J. R.** (2011). Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping. *Science*, 331(6018), 772–775. — Active retrieval cải thiện 50% khả năng ghi nhớ.
4. **Cepeda, N. J., et al.** (2006). Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis. *Psychological Bulletin*, 132(3), 354–380. — Meta-analysis 184 nghiên cứu: spaced repetition vượt trội 10–30%.
5. **Murre, J. M. J., & Dros, J.** (2015). Replication and Analysis of Ebbinghaus' Forgetting Curve. *PLOS ONE*. — Ôn tập trong 24h đầu tăng 80% khả năng nhớ.
6. **Roediger, H. L., et al.** (2011). Test-Enhanced Learning in the Classroom. *Journal of Educational Psychology*. — Kiểm tra thường xuyên trong lớp cải thiện điểm số cuối kỳ. [PDF](https://pdf.retrievalpractice.org/guide/Roediger_Agarwal_etal_2011_JEPA.pdf)

### RAG & AI

7. **Lewis, P., et al.** (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*. — Bài báo gốc giới thiệu kiến trúc RAG.
8. **Self-reflective RAG** (2024). Giảm hallucination xuống 5,8%. [ACL Anthology](https://aclanthology.org/2024.naacl-industry.19/)
9. **MEGA-RAG** (2025). Multi-evidence guided answer refinement giảm ảo giác trong y tế công cộng. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348/)
10. **Dual-Pathway KG-RAG** (2025). Giảm 18% hallucination trong hỏi đáp y sinh. [MDPI](https://www.mdpi.com/2079-9292/14/21/4227)

### Thống kê thị trường

11. **Báo Giáo dục và Thời đại** (2024). Người Việt đọc trung bình 4 quyển sách/năm nhưng 2,8 quyển là sách giáo khoa. [Link](https://giaoducthoidai.vn/nguoi-viet-doc-trung-binh-4-quyen-sachnam-nhung-28-quyen-da-la-sach-giao-khoa-post703257.html)
12. **VOV** (2024). 5 năm Ngày sách Việt Nam: Người Việt đọc 4 hay 1 cuốn sách mỗi năm? [Link](https://vov.vn/van-hoa/van-hoc/5-nam-ngay-sach-viet-nam-nguoi-viet-doc-4-hay-1-cuon-sach-moi-nam-897994.vov)
13. **GlobeNewsWire** (2026). Global AI in Education Market: $10.6B in 2026, projected $42.48B by 2030 (CAGR 40.9%). [Link](https://www.globenewswire.com/news-release/2026/04/07/3269515/0/en/Global-10-6B-AI-in-Education-Market-2026-Total-Revenue-Set-to-Quadruple-During-2026-2030-Reaching-42-48-Billion.html)
14. **Grand View Research** (2025). AI in Education Market — Asia-Pacific CAGR 44.2%. [Link](https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-education-market-report)
15. **IMARC Group** (2025). Vietnam EdTech Market: $1B (2024) → $3B (2033), CAGR 12.96%. [Link](https://www.imarcgroup.com/vietnam-edtech-market)
16. **Austrade** (2025). Vietnam's next frontier: Edtech and the digital education economy. [Link](https://www.austrade.gov.au/en/news-and-analysis/news/vietnams-next-frontier-edtech-and-the-digital-education-economy)
17. **PTIT** (2026). Học viện dự kiến tuyển sinh khoảng 8.000 sinh viên năm 2026. [Link](https://ptit.edu.vn/tin-tuc/hoc-vien-cong-nghe-buu-chinh-vien-thong-du-kien-tuyen-sinh-khoang-8-000-sinh-vien-nam-2026)

---

*Quillora — Từ ngòi bút đến bình minh tri thức.*
