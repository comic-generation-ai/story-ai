# Task cho story-ai — sau khi test thật với image-ai

Bối cảnh: test `image_prompt` sinh ra từ story-ai (truyện Tấm Cám, `test_result.json`) qua image-ai
(Stable Diffusion) thật thì ảnh ra xấu/lệch mô tả. Đã tìm ra nguyên nhân cụ thể bên dưới.

---

## 1. Sửa `image_prompt` cho khớp CLIP/Stable Diffusion (ưu tiên cao)

**File cần sửa:** `src/llm/prompt_template.py`, hàm `get_system_prompt()`, mục `IMAGE PROMPT RULES`.

### Vấn đề

Model sinh ảnh (Stable Diffusion) dùng CLIP text encoder — **giới hạn cứng ~77 token**
(khoảng 300-320 ký tự tiếng Anh), không phải do image-ai cấu hình mà là giới hạn kiến trúc
của chính model, không đổi được. Prompt dài hơn sẽ bị cắt mất, phần bị cắt không hiện trong
ảnh.

Panel 1 của truyện Tấm Cám hiện dài **422 ký tự**, đã vượt giới hạn ngay từ đầu:

```
"A beautiful Vietnamese village at dusk, warm golden hour lighting. Tấm, a gentle and
beautiful young woman wearing modest but elegant royal attire mixed with traditional áo
tứ thân, walks along a dirt path towards a traditional thatched-roof house. In the
background, a tall, slender areca palm tree sways in the wind. Melancholic yet peaceful
mood, wide shot, comic book style, vibrant colors, detailed line art --ar 16:9"
```

2 lỗi cụ thể trong system prompt hiện tại:

1. Dòng ví dụ cuối `IMAGE PROMPT RULES` đang có:
   `"comic book style, vibrant colors, detailed line art --ar 16:9"`
   → **`--ar 16:9` là cú pháp riêng của Midjourney**, Stable Diffusion/CLIP không hiểu,
   chỉ bị biến thành rác token, phí ngân sách 77 token quý giá. **Xoá hẳn `--ar 16:9`.**

2. Rule đang ghi `"Detailed English image prompt describing scene, characters, lighting,
   composition, and art style."` → khuyến khích viết dài, văn xuôi nhiều câu. Cần đổi thành
   yêu cầu **súc tích, dạng tag phân cách dấu phẩy**, không phải câu văn tường thuật.

### Cách sửa

- Giới hạn `image_prompt` còn khoảng **50-70 từ tiếng Anh (~250-300 ký tự)**.
- Dạng **tag/keyword phân cách dấu phẩy**, không viết câu văn xuôi nhiều mệnh đề.
- Mỗi panel chỉ mô tả **1 hành động/khoảnh khắc chính** (vì mỗi `image_prompt` render ra
  đúng 1 ảnh tĩnh — không nhồi cả chuỗi hành động "đi tới nhà → nhìn thấy → nói chuyện"
  vào 1 prompt).
- Mô tả cảm xúc/tường thuật chi tiết vẫn giữ nguyên trong `dialogue` (hiển thị cho người đọc)
  — không cần nhồi vào `image_prompt`.
- Bỏ hẳn mọi cú pháp Midjourney (`--ar`, `--v`, `--style raw`,...).

### Ví dụ before/after

```
Trước (422 ký tự, bị cắt mất phần lớn khi tới image-ai):
"A beautiful Vietnamese village at dusk, warm golden hour lighting. Tấm, a gentle and
beautiful young woman wearing modest but elegant royal attire mixed with traditional áo
tứ thân, walks along a dirt path towards a traditional thatched-roof house. In the
background, a tall, slender areca palm tree sways in the wind. Melancholic yet peaceful
mood, wide shot, comic book style, vibrant colors, detailed line art --ar 16:9"

Sau (~110 ký tự, giữ nguyên vẹn khi qua image-ai):
"young Vietnamese woman in áo tứ thân, walking on dirt path toward thatched house,
areca palm tree, golden hour, melancholic mood, wide shot"
```

> Phía image-ai đã tự vá tạm (ưu tiên giữ style suffix, cắt bớt phần mô tả dài, lọc `--ar`),
> nhưng vá ở đó vẫn mất phần lớn nội dung — sửa gốc ở story-ai mới thực sự tối ưu.

---

## Ghi chú thêm

- `readme.md` hiện tại của story-ai mô tả kiến trúc **gRPC + Alibaba DashScope/Qwen** — đã
  lỗi thời, code thật (`src/server.py`) đang dùng **FastAPI + OpenRouter**. Nên cập nhật lại
  README cho khớp thực tế, tránh nhầm lẫn khi người khác đọc.
