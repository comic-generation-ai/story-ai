

Thư mục [story-ai](file:///u:/comic-generation-ai/story-ai) là một **gRPC microservice** chịu trách nhiệm tạo kịch bản phân cảnh truyện tranh (gồm tiêu đề, số khung tranh, nhân vật thoại, nội dung thoại bằng tiếng Việt và prompt mô tả ảnh bằng tiếng Anh) dựa trên cốt truyện tóm tắt và phong cách vẽ yêu cầu.

Dưới đây là cấu trúc source code và cách hoạt động của service này:

---

### 1. Cấu trúc thư mục chính

*   [proto/story_generation.proto](file:///u:/comic-generation-ai/story-ai/proto/story_generation.proto): Định nghĩa hợp đồng API gRPC (`StoryGenerationService`) bao gồm:
    *   Hàm `GenerateStory`: Nhận vào tóm tắt cốt truyện (`summary`), phong cách (`style`), số khung hình (`num_panels`), ngôn ngữ (`language`) và trả về danh sách các panel.
    *   Hàm `CheckHealth`: Dùng để kiểm tra trạng thái hoạt động của service.
*   [scripts/generate_proto.py](file:///u:/comic-generation-ai/story-ai/scripts/generate_proto.py): Script tự động chạy để biên dịch file `.proto` ở trên thành các module python chứa trong `src/service/generated/`.
*   [src/config.py](file:///u:/comic-generation-ai/story-ai/src/config.py): Quản lý các biến môi trường cấu hình (Port chạy gRPC, API key của Alibaba DashScope, tên Model LLM Qwen).
*   [src/llm/](file:///u:/comic-generation-ai/story-ai/src/llm/):
    *   [prompt_template.py](file:///u:/comic-generation-ai/story-ai/src/llm/prompt_template.py): Chứa prompt hệ thống (System Prompt) hướng dẫn AI đóng vai biên kịch truyện tranh chuyên nghiệp và trả về kết quả theo cấu trúc JSON định sẵn.
    *   [parser.py](file:///u:/comic-generation-ai/story-ai/src/llm/parser.py): Làm sạch phản hồi từ LLM và sử dụng `Pydantic` để kiểm tra độ chính xác của cấu trúc dữ liệu JSON trả về.
*   [src/server.py](file:///u:/comic-generation-ai/story-ai/src/server.py): Điểm khởi chạy của gRPC Server, thực hiện xử lý logic các request đến.
*   [Dockerfile](file:///u:/comic-generation-ai/story-ai/Dockerfile): File build Docker image để chạy ứng dụng trong môi trường container hóa.

---

### 2. Cách hoạt động chi tiết của luồng `GenerateStory`

1.  **Tiếp nhận Request**: 
    *   Client (thường là Orchestrator service) gửi một gRPC request đến `story-ai` chứa thông tin về cốt truyện muốn viết, phong cách hình ảnh mong muốn, số khung tranh cần tạo (mặc định là 4).
2.  **Chuẩn bị Prompt**:
    *   Hệ thống lấy thông tin đầu vào đưa vào các hàm định dạng prompt tại [prompt_template.py](file:///u:/comic-generation-ai/story-ai/src/llm/prompt_template.py). 
    *   System Prompt sẽ yêu cầu AI tạo ra dữ liệu cấu trúc dạng JSON chứa danh sách các panels, với `dialogue` và `speaker` bằng tiếng Việt, còn `image_prompt` (prompt vẽ hình) bằng tiếng Anh.
3.  **Gọi LLM (Qwen via DashScope)**:
    *   Nếu có API Key hợp lệ, Server gọi đến API của Alibaba DashScope (sử dụng model Qwen) với tham số `response_format={"type": "json_object"}` để đảm bảo kết quả trả về là JSON thuần túy.
4.  **Parse & Validating**:
    *   Nhận kết quả thô dạng String từ LLM, chuyển qua bộ parser để lọc bỏ các khối markdown (như ` ```json `), sau đó kiểm tra kiểu dữ liệu thông qua Pydantic schema để chắc chắn các trường bắt buộc (`panel_number`, `image_prompt`, `speaker`, `dialogue`) đều có đủ và đúng định dạng.
5.  **Cơ chế Fallback (Dự phòng)**:
    *   Trong trường hợp không cấu hình API Key hoặc có lỗi trong quá trình gọi LLM/parse dữ liệu, server sẽ tự động kích hoạt chế độ **Fallback** bằng cách sinh ra danh sách panel giả lập (Mock panels) từ các mẫu dựng sẵn để đảm bảo client vẫn nhận được phản hồi và không bị lỗi hệ thống.
6.  **Trả kết quả**:
    *   Server đóng gói dữ liệu đã chuẩn hóa vào object `GenerateStoryResponse` và gửi trả lại cho client thông qua kết nối gRPC.