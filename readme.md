Thư mục [story-ai](file:///u:/comic-generation-ai/story-ai) là một **FastAPI HTTP microservice** chịu nhiệm tạo kịch bản phân cảnh truyện tranh (gồm tiêu đề, số khung tranh, nhân vật thoại, nội dung thoại bằng tiếng Việt và prompt mô tả ảnh bằng tiếng Anh) dựa trên cốt truyện tóm tắt và phong cách vẽ yêu cầu.

Dưới đây là cấu trúc source code và cách hoạt động của service này:

---

### 1. Cấu trúc thư mục chính

*   [src/config.py](file:///u:/comic-generation-ai/story-ai/src/config.py): Quản lý các biến môi trường cấu hình (Port chạy FastAPI, API key của OpenRouter/Ali MaaS, tên Model LLM).
*   [src/llm/](file:///u:/comic-generation-ai/story-ai/src/llm/):
    *   [prompt_template.py](file:///u:/comic-generation-ai/story-ai/src/llm/prompt_template.py): Chứa prompt hệ thống (System Prompt) hướng dẫn AI đóng vai biên kịch truyện tranh chuyên nghiệp và trả về kết quả theo cấu trúc JSON định sẵn với các giới hạn và quy định chặt chẽ cho `image_prompt`.
    *   [parser.py](file:///u:/comic-generation-ai/story-ai/src/llm/parser.py): Làm sạch phản hồi từ LLM và sử dụng `Pydantic` để kiểm tra độ chính xác của cấu trúc dữ liệu JSON trả về.
    *   [folklore.py](file:///u:/comic-generation-ai/story-ai/src/llm/folklore.py): Nhận diện cốt truyện cổ tích Việt Nam để cung cấp ngữ cảnh chuẩn xác.
*   [src/server.py](file:///u:/comic-generation-ai/story-ai/src/server.py): Điểm khởi chạy của FastAPI Server, thực hiện xử lý logic các request đến thông qua HTTP API.
*   [Dockerfile](file:///u:/comic-generation-ai/story-ai/Dockerfile): File build Docker image để chạy ứng dụng trong môi trường container hóa.
*   [test_run.py](file:///u:/comic-generation-ai/story-ai/test_run.py): Script để test gọi API cục bộ phục vụ cho việc phát triển và kiểm thử.

---

### 2. Cách hoạt động chi tiết của luồng `GenerateStory`

1.  **Tiếp nhận Request**: 
    *   Client gửi một HTTP POST request đến endpoint `/generate-story` chứa thông tin về cốt truyện muốn viết, phong cách hình ảnh mong muốn, số khung tranh cần tạo (mặc định là 4).
2.  **Chuẩn bị Prompt**:
    *   Hệ thống lấy thông tin đầu vào đưa vào các hàm định dạng prompt tại [prompt_template.py](file:///u:/comic-generation-ai/story-ai/src/llm/prompt_template.py). 
    *   System Prompt yêu cầu AI tạo ra dữ liệu cấu trúc dạng JSON chứa danh sách các panels, với `dialogue` và `speaker` bằng tiếng Việt, còn `image_prompt` (prompt vẽ hình tối đa 50-70 từ tiếng Anh, không chứa ký tự Midjourney như `--ar`) bằng tiếng Anh.
3.  **Gọi LLM (via OpenRouter/Ali MaaS)**:
    *   Nếu có API Key hợp lệ, Server gọi đến API bằng OpenAI Client được cấu hình thông qua `Config.BASE_URL` và `Config.MODEL_NAME`.
4.  **Parse & Validating**:
    *   Nhận kết quả thô dạng String từ LLM, chuyển qua bộ parser để lọc bỏ các thẻ suy nghĩ `<think>...</think>` (đối với mô hình như Qwen Reasoning) và các khối markdown (như ` ```json `), sau đó kiểm tra kiểu dữ liệu thông qua Pydantic schema để chắc chắn các trường bắt buộc (`panel_number`, `image_prompt`, `speaker`, `dialogue`) đều có đủ và đúng định dạng.
5.  **Cơ chế Fallback (Dự phòng)**:
    *   Trong trường hợp không cấu hình API Key hoặc có lỗi trong quá trình gọi LLM/parse dữ liệu, server sẽ tự động kích hoạt chế độ **Fallback** bằng cách sinh ra danh sách panel giả lập (Mock panels) từ các mẫu dựng sẵn để đảm bảo client vẫn nhận được phản hồi và không bị lỗi hệ thống.
6.  **Trả kết quả**:
    *   Server đóng gói dữ liệu đã chuẩn hóa vào object `GenerateStoryResponse` và gửi trả lại cho client thông qua HTTP response.