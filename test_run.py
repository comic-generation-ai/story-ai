import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath("."))

from src.server import generate_story_endpoint, GenerateStoryRequest

def main():
    print("=== BẮT ĐẦU TEST TẠO TRUYỆN TRANH VỚI OPENROUTER ===")
    request = GenerateStoryRequest(
        job_id="test_tam_cam_01",
        summary="Nhân dịp giỗ cha, Tấm về thăm nhà. Mẹ kế lừa Tấm trèo lên cây cau để hái quả cúng giỗ, rồi lén chặt gốc cây khiến Tấm ngã xuống và qua đời. Sau đó, mẹ con Cám đưa Cám vào cung thay Tấm làm hoàng hậu. Linh hồn Tấm hóa thành chim Vàng Anh, mở đầu cho hành trình hóa thân và trở về đòi lại công lý.",
        num_panels=5,
        style="comic book style, vibrant colors",
        language="vi"
    )

    print(f"Job ID: {request.job_id}")
    print(f"Summary: {request.summary}")
    print("Đang gọi OpenRouter API...")

    response = generate_story_endpoint(request)

    print("\n=== KẾT QUẢ SINH RA (STRUCT Pydantic / JSON) ===")
    json_result = response.model_dump_json(indent=2)
    print(json_result)

    # Save to file for easy viewing
    output_file = "test_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_result)
    print(f"\n=> Đã lưu toàn bộ kết quả JSON vào file: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
