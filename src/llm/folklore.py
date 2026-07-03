import re
import unicodedata
from typing import Dict, Optional

# A robust Vietnamese text normalization function to match queries with/without accents
def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Normalize unicode to decompose accents
    text = unicodedata.normalize('NFKD', text)
    # Remove accent marks
    text = "".join([c for c in text if not unicodedata.combining(c)])
    # Replace special characters and extra spaces
    text = re.sub(r'[đĐ]', 'd', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Folklore database containing details for popular Vietnamese stories
FOLKLORE_DATABASE = {
    "thach_sanh": {
        "canonical_title": "Thạch Sanh",
        "keywords": ["thach sanh", "ly thong", "chan tinh", "dai bang tinh", "nieu com than", "dan than"],
        "context": """
- Bối cảnh: Việt Nam thời cổ đại.
- Nhân vật chính:
  + Thạch Sanh: Chàng tiều phu nghèo khổ nhưng khoẻ mạnh, thật thà, tốt bụng, dũng cảm và có võ nghệ cao cường. Chàng dùng rìu đá (búa thần), cung tên vàng (cung thần), niêu cơm thần (luôn đầy cơm) và đàn thần (tiếng đàn cảm hoá quân sĩ, giải oan).
  + Lý Thông: Người anh kết nghĩa của Thạch Sanh. Tính cách quỷ quyệt, xảo quyệt, tham lam và tàn nhẫn, luôn tìm cách cướp công của Thạch Sanh.
  + Chằn Tinh: Con quái vật nửa người nửa thú (ogre/monster) hung ác tàn bạo chuyên ăn thịt người.
  + Đại Bàng Tinh: Con quái vật chim khổng lồ bắt cóc Công chúa Quỳnh Nga.
  + Công chúa Quỳnh Nga: Công chúa hiền dịu, bị Đại Bàng bắt đi và được Thạch Sanh giải cứu.
- Cốt truyện truyền thống:
  1. Thạch Sanh kết nghĩa anh em với Lý Thông, bị Lý Thông lừa đi canh miếu thờ để thế mạng cho hắn trước Chằn Tinh. Thạch Sanh chiến đấu dũng cảm, diệt Chằn Tinh, lấy được bộ cung tên vàng. Lý Thông cướp công.
  2. Đại Bàng Tinh bắt công chúa. Thạch Sanh bắn thương đại bàng, tìm đến hang của nó, xuống hang cứu công chúa lên. Lý Thông ở trên lấp cửa hang để hại Thạch Sanh và cướp công chúa về hoàng cung đòi công.
  3. Thạch Sanh giết đại bàng tinh và cứu con vua Thủy Tề, được tặng cây đàn thần.
  4. Thạch Sanh bị vu oan và giam vào ngục tối. Tiếng đàn thần của chàng vang lên khiến công chúa hết câm, giải oan cho chàng và vạch mặt mẹ con Lý Thông.
  5. Khi các nước chư hầu đem quân xâm lược, Thạch Sanh gảy đàn thần làm quân địch nản lòng quy hàng, dùng niêu cơm thần ăn mãi không hết thiết đãi hàng vạn quân sĩ chư hầu, khiến họ kính phục rút quân.
- Hướng dẫn lời thoại và tạo ảnh:
  + Không bao giờ mô tả Thạch Sanh đánh quái vật "vì đói". Thạch Sanh hành hiệp trượng nghĩa vì lòng dũng cảm và bảo vệ dân lành.
  + Lời thoại của Thạch Sanh cần thể hiện sự khiêm tốn, thật thà nhưng cương nghị, anh dũng.
  + Lời thoại của Lý Thông nịnh bợ, ngọt ngào trước mặt nhưng mưu mô sau lưng.
  + Vũ khí của Thạch Sanh là chiếc rìu đá/thần hoặc cung tên vàng, không dùng búa sắt của tiều phu hiện đại.
"""
    },
    "tam_cam": {
        "canonical_title": "Tấm Cám",
        "keywords": ["tam cam", "di ghe", "ca bong", "chim vang anh", "cay xoan dao", "khung cui", "qua thi"],
        "context": """
- Bối cảnh: Làng quê Việt Nam cổ xưa.
- Nhân vật chính:
  + Tấm: Cô gái hiền lành, siêng năng, xinh đẹp nhưng chịu nhiều bất hạnh và bị dì ghẻ, em gái ngược đãi. Tấm trải qua nhiều lần hóa kiếp (chim vàng anh, cây xoan đào, khung cửi, quả thị) trước khi sum họp với vua.
  + Cám và Mụ Dì Ghẻ: Hai mẹ con độc ác, lười biếng, đố kỵ, luôn tìm mọi cách hại Tấm để giành giật hạnh phúc và ngôi hoàng hậu.
  + Vua: Yêu thương Tấm chân thành, nhận ra Tấm qua các hóa thân và miếng trầu têm cánh phượng.
  + Bụt: Đấng thần tiên hiền từ luôn xuất hiện giúp đỡ Tấm mỗi khi cô khóc (qua cá bống, đôi giày thêu).
- Cốt truyện truyền thống:
  1. Tấm bị Cám lừa trút hết giỏ tép để đoạt yếm đỏ. Bụt hiện lên cho Tấm con cá bống làm bạn. Mẹ con Cám lừa giết bống ăn thịt.
  2. Ngày hội, dì ghẻ trộn gạo lẫn thóc bắt Tấm nhặt. Bụt sai chim sẻ nhặt giúp, cho Tấm quần áo đẹp và giày thêu đi trẩy hội. Tấm đánh rơi giày, Vua nhặt được và cưới Tấm làm Hoàng hậu.
  3. Tấm về giỗ cha, bị dì ghẻ lừa trèo cây cau rồi chặt gốc khiến Tấm ngã chết. Cám vào cung thế chỗ.
  4. Tấm hóa thân thành Chim Vàng Anh, Cây Xoan Đào, Khung Cửi. Lần nào cũng bị mẹ con Cám tiêu hủy.
  5. Cuối cùng, Tấm hóa thành Quả Thị thơm ngát rơi vào bị của bà lão hàng nước. Tấm bước ra từ quả thị giúp bà dọn dẹp. Vua đi tuần ghé quán nước, nhận ra trầu cánh phượng Tấm têm và đón cô về cung. Mẹ con Cám bị trừng trị thích đáng.
- Lời thoại và tạo ảnh:
  + Tấm có giọng nói dịu dàng, u sầu nhưng kiên cường. Dì ghẻ và Cám đanh đá, chua ngoa.
  + Khung cảnh mang đậm nét làng quê Việt Nam: giếng nước, gốc cau, hội làng, quán nước mái lá tranh nghèo, quả thị vàng thơm.
"""
    },
    "thanh_giong": {
        "canonical_title": "Thánh Gióng",
        "keywords": ["thanh giong", "phu dong", "roi sat", "ngua sat", "giap sat", "tre dang nga", "giac an"],
        "context": """
- Bối cảnh: Đời Hùng Vương thứ sáu.
- Nhân vật chính:
  + Gióng (Thánh Gióng): Đứa trẻ lên ba không biết nói biết cười, nhưng khi giặc Ân xâm lược, nghe tiếng loa sứ giả liền cất tiếng đòi đi đánh giặc. Gióng ăn khỏe như thổi, lớn nhanh như thổi, cưỡi ngựa sắt phun lửa, mặc giáp sắt, cầm roi sắt phá tan quân thù.
  + Người mẹ: Người phụ nữ nông dân nghèo khổ, mang thai Gióng sau khi ướm chân vào một vết chân khổng lồ ngoài đồng.
  + Sứ giả: Sứ giả nhà vua đi tìm người tài cứu nước.
- Cốt truyện truyền thống:
  1. Gióng lên ba không biết nói cười. Khi giặc Ân đến bờ cõi, sứ giả đi tìm người tài, Gióng bỗng nói được, yêu cầu đúc ngựa sắt, roi sắt, giáp sắt.
  2. Cả làng góp gạo nuôi Gióng lớn nhanh như thổi để đi đánh giặc.
  3. Khi giặc đến, Gióng vươn vai biến thành tráng sĩ oai phong lẫm liệt, mặc giáp, cầm roi, cưỡi ngựa sắt phun lửa xông trận đánh tan quân giặc. Khi roi sắt gãy, Gióng nhổ những bụi tre đằng ngà bên đường làm vũ khí quật ngã quân thù.
  4. Giặc tan, Gióng cưỡi ngựa bay lên đỉnh núi Sóc Sơn rồi bay về trời, không nhận bổng lộc triều đình.
- Lời thoại và tạo ảnh:
  + Tránh lời thoại dài dòng cho Gióng. Tiếng nói đầu tiên của Gióng là dành cho vận mệnh đất nước ("Mẹ ra mời sứ giả vào đây cho con"). Gióng chiến đấu trong im lặng oai hùng.
  + Ảnh minh họa cần cực kỳ hoành tráng, hùng vĩ: ngựa sắt phun lửa, roi sắt sáng loáng, lũy tre vàng óng (tre đằng ngà) bị nhổ tận gốc quật giặc.
"""
    },
    "son_tinh_thuy_tinh": {
        "canonical_title": "Sơn Tinh Thủy Tinh",
        "keywords": ["son tinh", "thuy tinh", "hung vuong", "my nuong", "chin nga", "chin cua", "chin hong mao"],
        "context": """
- Bối cảnh: Đời Hùng Vương thứ mười tám.
- Nhân vật chính:
  + Sơn Tinh: Thần Núi Ba Vì. Người hiền hòa, có tài vẫy tay nổi cồn bãi, dâng đồi núi cao chống lại dòng nước. Đại diện cho sức mạnh chế ngự thiên tai của người Việt cổ.
  + Thủy Tinh: Thần Nước. Người kiêu ngạo, nóng nảy, có tài gọi gió, làm mưa, dâng nước lụt dìm chết mọi thứ.
  + Hùng Vương XVIII: Vua nước Văn Lang, muốn tìm rể hiền cho con gái.
  + Mỵ Nương: Công chúa xinh đẹp nết na.
- Cốt truyện truyền thống:
  1. Hùng Vương kén rể, Sơn Tinh và Thủy Tinh cùng đến cầu hôn. Cả hai đều tài giỏi ngang nhau.
  2. Vua thách cưới bằng sính lễ đặc biệt: "Một trăm ván cơm nếp, một trăm tiệp bánh chưng, voi chín ngà, gà chín cựa, ngựa chín hồng mao, mỗi thứ một đôi", ai đem đến trước thì được cưới Mỵ Nương.
  3. Sơn Tinh dâng lễ trước, đón Mỵ Nương về núi. Thủy Tinh đến sau, nổi giận đùng đùng, dâng nước lụt đuổi theo đòi cướp công chúa.
  4. Hai bên giao chiến dữ dội. Thủy Tinh dâng nước cao bao nhiêu, Sơn Tinh dâng núi cao bấy nhiêu. Cuối cùng Thủy Tinh kiệt sức rút quân. Hằng năm, Thủy Tinh vẫn dâng nước đánh Sơn Tinh nhưng đều thất bại.
- Lời thoại và tạo ảnh:
  + Lời thoại của Sơn Tinh điềm tĩnh, dứt khoát. Thủy Tinh dữ dội, giận dữ gào thét.
  + Sính lễ thuần Việt cổ truyền: cơm nếp, bánh chưng bánh giầy, sinh vật huyền thoại (voi 9 ngà, gà 9 cựa, ngựa 9 hồng mao).
"""
    },
    "su_tich_ho_guom": {
        "canonical_title": "Sự tích Hồ Gươm",
        "keywords": ["ho guom", "le loi", "le than", "rua vang", "kim quy", "thuan thien", "giac minh"],
        "context": """
- Bối cảnh: Cuộc khởi nghĩa Lam Sơn chống giặc Minh xâm lược dưới sự lãnh đạo của Lê Lợi.
- Nhân vật chính:
  + Lê Lợi: Chủ tướng nghĩa quân Lam Sơn hiền tài, dũng cảm, được lòng dân.
  + Lê Thận: Người đánh cá tham gia nghĩa quân, vớt được lưỡi gươm dưới nước.
  + Rùa Vàng (Kim Quy): Sứ giả của Long Quân đòi lại gươm thần sau khi giặc tan.
- Cốt truyện truyền thống:
  1. Nước ta bị giặc Minh đô hộ. Long Quân quyết định cho nghĩa quân Lam Sơn mượn thanh gươm thần Thuận Thiên.
  2. Lê Thận kéo lưới vớt được lưỡi gươm khắc chữ "Thuận Thiên". Sau đó, Lê Lợi chạy giặc trong rừng thấy chuôi gươm nạm ngọc trên ngọn cây đa. Đem lắp lưỡi vào chuôi thì vừa khít, thanh gươm phát sáng tựa như sức mạnh trời ban.
  3. Từ khi có gươm thần, nhuệ khí nghĩa quân tăng cao, đánh tan quân Minh giải phóng đất nước. Lê Lợi lên ngôi vua.
  4. Một năm sau, khi vua cưỡi thuyền rồng dạo chơi trên hồ Tả Vọng (Hồ Gươm), Rùa Vàng nổi lên đòi lại gươm thần cho Long Quân. Vua trả gươm, hồ đổi tên thành Hồ Gươm (Hồ Hoàn Kiếm).
- Lời thoại và tạo ảnh:
  + Lời thoại trang nghiêm, yêu nước, mang tính hào hùng dân tộc.
  + Thanh gươm thần nạm ngọc sáng chói, biểu tượng của sự đồng lòng toàn dân tộc và thiên mệnh.
"""
    }
}

def get_folklore_context(summary: str) -> Optional[dict]:
    """
    Checks if the user request summary matches any popular Vietnamese folktale.
    Returns the folklore details dictionary if matched, or None.
    """
    normalized_summary = normalize_text(summary)
    
    for key, data in FOLKLORE_DATABASE.items():
        # Check if any keyword matches
        for kw in data["keywords"]:
            normalized_kw = normalize_text(kw)
            if normalized_kw in normalized_summary:
                return data
                
    return None
