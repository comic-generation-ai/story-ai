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
    },
    "rua_va_tho": {
        "canonical_title": "Rùa và Thỏ",
        "keywords": ["rua va tho", "rua va tho chay dua", "tho kiêu ngao", "rua kien tri"],
        "context": """
- Bối cảnh: Khu rừng xanh yên bình.
- Nhân vật chính:
  + Thỏ: Nhanh nhẹn, tự phụ, kiêu ngạo, coi thường người khác.
  + Rùa: Chậm chạp nhưng kiên trì, chăm chỉ, không nản lòng trước khó khăn.
- Cốt truyện:
  1. Thỏ mỉa mai, chê bai Rùa chậm chạp. Rùa thách Thỏ chạy đua với mình.
  2. Thỏ đồng ý ngay vì tự tin vào tốc độ vượt trội. Khi bắt đầu cuộc đua, Thỏ nhanh chóng bỏ xa Rùa.
  3. Nghĩ rằng chiến thắng quá dễ dàng, Thỏ dừng lại nhởn nhơ chơi đùa và nằm ngủ dưới một gốc cây.
  4. Trong khi Thỏ ngủ say, Rùa vẫn kiên trì từng bước một, không ngừng nghỉ, vượt qua Thỏ và tiến về đích.
  5. Thỏ giật mình tỉnh giấc thì Rùa đã gần chạm vạch đích. Thỏ cố sức chạy nhưng không kịp nữa. Rùa giành chiến thắng.
- Lời thoại và tạo ảnh:
  + Giọng Thỏ kiêu căng, chế giễu. Giọng Rùa điềm đạm, khiêm tốn nhưng quyết tâm.
  + Hình ảnh minh họa: Rùa miệt mài bò từng bước, Thỏ nằm ngủ lười biếng dưới bóng cây cổ thụ, vạch đích náo nhiệt với sự cổ vũ của muông thú.
"""
    },
    "cay_tre_tram_dot": {
        "canonical_title": "Cây Tre Trăm Đốt",
        "keywords": ["cay tre tram dot", "khoai", "khac nhap khac xuat", "lao dia chu"],
        "context": """
- Bối cảnh: Làng quê Việt Nam xưa.
- Nhân vật chính:
  + Khoai: Chàng trai cày hiền lành, khỏe mạnh, chất phác, chăm chỉ chịu khó.
  + Lão địa chủ (Phú ông): Tham lam, xảo quyệt, nuốt lời hứa gả con gái cho Khoai để bóc lột sức lao động của anh.
  + Bụt: Hiện lên giúp đỡ chàng Khoai lúc khó khăn, ban cho câu thần chú.
- Cốt truyện truyền thống:
  1. Lão địa chủ hứa gả con gái cho Khoai nếu anh làm lụng chăm chỉ trong ba năm.
  2. Sau ba năm, lão địa chủ trở mặt, lừa Khoai đi tìm "cây tre trăm đốt" trên rừng mang về thì mới gả con gái, mục đích để gả con cho một nhà giàu khác.
  3. Khoai vào rừng tìm kiếm vô vọng và khóc. Bụt hiện lên, bảo anh chặt đủ một trăm đốt tre riêng lẻ, rồi dạy câu thần chú "Khắc nhập, khắc nhập" để gắn chúng lại thành một cây tre dài trăm đốt, và câu "Khắc xuất, khắc xuất" để tách rời ra như cũ để dễ gánh về.
  4. Về đến nhà, thấy đám cưới đang chuẩn bị cho người khác, Khoai liền đọc câu thần chú "Khắc nhập, khắc nhập" khiến lão địa chủ và những kẻ đồng lõa bị dính chặt vào cây tre.
  5. Lão địa chủ xin tha và hứa thực hiện lời hứa. Khoai đọc "Khắc xuất, khắc xuất" để giải thoát cho họ, rồi cưới con gái phú ông.
- Lời thoại và tạo ảnh:
  + Lời thoại phú ông lươn lẹo, ngọt nhạt lúc cần bóc lột nhưng ác độc sau lưng. Khoai thật thà, chất phác.
  + Câu thần chú thần kỳ "Khắc nhập, khắc nhập" và "Khắc xuất, khắc xuất" phải xuất hiện rõ ràng.
  + Hình ảnh lũy tre làng xanh mướt, đốt tre xếp chồng lấp lánh phép thuật.
"""
    },
    "sutich_traucau": {
        "canonical_title": "Sự tích Trầu Cau",
        "keywords": ["trau cau", "cao tan", "cao lan", "vo chong", "cay cau", "la trau", "da voi"],
        "context": """
- Bối cảnh: Đời Hùng Vương vương triều xa xưa.
- Nhân vật chính:
  + Cao Tân (anh) và Cao Lan (em): Hai anh em sinh đôi giống nhau như đúc, rất mực yêu thương nhau.
  + Người vợ (con gái thầy Lưu): Người vợ hiền thảo, yêu thương chồng.
- Cốt truyện truyền thống:
  1. Hai anh em Tân và Lan học nhà thầy Lưu. Thầy yêu quý gả con gái cho người anh (Tân).
  2. Sau khi kết hôn, người anh bận bịu gia đình, không còn quan tâm chu đáo đến em như trước. Một hôm đi làm đồng về, người vợ nhầm lẫn ôm chầm lấy người em (Lan). Người anh nhìn thấy, nảy sinh hiểu lầm, lạnh nhạt và nghi ngờ em.
  3. Người em đau khổ, bỏ nhà ra đi, đến một bờ sông cạn thì kiệt sức, hóa thành một tảng đá vôi.
  4. Người anh hối hận đi tìm em, đến bờ sông cũng kiệt sức hóa thành cây cau thẳng đứng bên cạnh tảng đá.
  5. Người vợ đi tìm chồng, cũng chết bên gốc cau hóa thành dây trầu không quấn chặt thân cau.
  6. Vua Hùng đi tuần qua, nghe kể lại câu chuyện tình nghĩa anh em vợ chồng thủy chung liền sai người hái lá trầu quả cau nhai thử cùng đá vôi, nhổ ra thấy nước đỏ tươi như máu. Vua ban lệnh trồng hai loại cây này khắp nơi và tục ăn trầu bắt đầu từ đó.
- Lời thoại và tạo ảnh:
  + Lời thoại buồn bã, day dứt, thể hiện sự thủy chung, tình nghĩa sâu nặng.
  + Hình ảnh cây cau thẳng đứng, dây trầu leo quanh và tảng đá vôi xám dưới chân mang tính biểu tượng văn hóa sâu sắc.
"""
    },
    "chu_dong_tu": {
        "canonical_title": "Chử Đồng Tử",
        "keywords": ["chu dong tu", "tien dung", "nhat da trach", "dam nhat ja", "gay non than"],
        "context": """
- Bối cảnh: Thời Hùng Vương thứ mười tám.
- Nhân vật chính:
  + Chử Đồng Tử: Chàng trai nghèo khó, hiếu thảo. Khi cha mất, chàng nhường chiếc khố duy nhất để liệm cho cha, còn bản thân chịu trần truồng kiếm sống bên sông.
  + Công chúa Tiên Dung: Con gái vua Hùng, xinh đẹp, thích ngao du sơn thủy, không muốn lấy chồng.
- Cốt truyện truyền thống:
  1. Tiên Dung du ngoạn trên sông, sai vây màn tắm trên bãi cát đúng nơi Chử Đồng Tử đang vùi mình tránh người. Nước dội làm trôi cát, lộ ra Chử Đồng Tử. Tiên Dung cho đó là duyên trời định nên kết hôn với chàng ngay trên bãi sông.
  2. Vua Hùng giận dữ không nhận con gái. Hai vợ chồng ở lại bãi sông làm ăn buôn bán. Chử Đồng Tử đi tìm thầy học đạo, được ban một cây gậy và một chiếc nón thần.
  3. Một đêm đi đường muộn, Chử Đồng Tử cắm gậy úp nón lên để nghỉ. Hóa phép ra một thành quách, đền đài tráng lệ và đầy rẫy người hầu lính tráng.
  4. Vua Hùng tưởng con làm phản, sai quân đi đánh. Đêm đó giông bão nổi lên, cả thành trì và hai vợ chồng bay về trời. Chỗ thành quách cũ sụt xuống thành đầm nước lớn gọi là Đầm Nhất Dạ (đầm một đêm).
- Lời thoại và tạo ảnh:
  + Giọng điệu tôn kính, giàu tính huyền thoại và lãng mạn.
  + Cảnh tắm trên cát lộ người và cảnh đầm Nhất Dạ rực sáng lấp lánh lúc thành trì bay lên trời.
"""
    },
    "sutich_banhchung_banhgiay": {
        "canonical_title": "Sự tích Bánh Chưng, Bánh Giầy",
        "keywords": ["banh chung banh giay", "lang lieu", "nep", "nhan dau xanh", "la dong", "khoi"],
        "context": """
- Bối cảnh: Thời Hùng Vương thứ sáu về già.
- Nhân vật chính:
  + Lang Liêu: Người con trai thứ mười tám của Vua Hùng. Chàng mất mẹ sớm, sống cuộc đời nghèo khó, tự cày ruộng nuôi thân, tính tình hiền lành, hiếu thảo.
  + Hùng Vương: Mong muốn tìm người con hiền tài nối ngôi báu.
  + Vị thần: Hiện ra trong giấc mộng chỉ dẫn Lang Liêu cách làm bánh.
- Cốt truyện truyền thống:
  1. Vua Hùng họp các con lại, tuyên bố ai dâng được lễ vật cúng tổ tiên ý nghĩa và ngon nhất sẽ được truyền ngôi. Các lang khác thi nhau đi tìm sơn hào hải vị.
  2. Lang Liêu lo lắng vì nhà nghèo. Một đêm, thần báo mộng: "Trong trời đất không gì quý bằng hạt gạo... Hãy lấy gạo nếp làm bánh hình tròn tượng trưng cho Trời, hình vuông tượng trưng cho Đất, ruột bánh là thịt mỡ và đậu xanh".
  3. Lang Liêu làm theo lời thần dạy, gói bánh chưng hình vuông bằng lá dong xanh, giã bánh giầy hình tròn trắng mịn.
  4. Đến ngày dâng lễ, Vua Hùng nếm thử, khen ngợi vị bánh ngon và ý nghĩa sâu sắc kính trời đất, cha mẹ của hai thứ bánh này. Vua quyết định truyền ngôi cho Lang Liêu.
- Lời thoại và tạo ảnh:
  + Thể hiện sự mộc mạc, tôn kính của Lang Liêu đối với tổ tiên và vua cha.
  + Cảnh gói bánh chưng bên bếp lửa bập bùng, những chiếc bánh giầy trắng tròn và bánh chưng vuông xanh mướt.
"""
    },
    "sutich_qua_dua_hau": {
        "canonical_title": "Sự tích Quả dưa hấu",
        "keywords": ["dua hau", "mai an tiem", "dao hoang", "hat den", "chim an gieo hat"],
        "context": """
- Bối cảnh: Đời Hùng Vương vương triều cổ đại.
- Nhân vật chính:
  + Mai An Tiêm: Con nuôi vua Hùng, chăm chỉ, tài giỏi nhưng tự trọng và thẳng thắn. Chàng nổi tiếng với câu nói: "Của biếu là của lo, của cho là của nợ", "Biết tay ta làm nên".
  + Vua Hùng: Do nghe lời gièm pha của bọn nịnh thần đã đày An Tiêm ra đảo hoang ngoài khơi xa.
- Cốt truyện truyền thống:
  1. Mai An Tiêm bị đày ra đảo hoang cùng vợ con. Chàng không nản chí, dựng lều và tự tìm cách sinh tồn.
  2. Một ngày nọ, An Tiêm phát hiện đàn chim biển từ phương Nam bay đến ăn một loại quả lạ, nhả hạt đen trên bãi cát. Chàng nghĩ chim ăn được người cũng ăn được nên gieo trồng hạt đó.
  3. Cây lớn nhanh, cho quả vỏ xanh, ruột đỏ, hạt đen, vị ngọt mát. An Tiêm đặt tên là dưa đỏ (sau này gọi là dưa hấu).
  4. An Tiêm khắc tên mình lên vỏ dưa thả trôi sông/biển. Thuyền buôn vớt được mang vào đất liền trao đổi. Đảo hoang dần trở nên đông vui.
  5. Vua Hùng biết chuyện, phục tài đức và ý chí của An Tiêm, sai người đón gia đình chàng về phong lại chức vị cũ.
- Lời thoại và tạo ảnh:
  + Thể hiện ý chí kiên cường, tự lực cánh sinh của Mai An Tiêm.
  + Cảnh đảo hoang đầy cát trắng, sóng vỗ và những quả dưa hấu xanh mướt được bổ đôi lộ ruột đỏ thắm.
"""
    },
    "con_rong_chau_tien": {
        "canonical_title": "Con Rồng Cháu Tiên",
        "keywords": ["con rong chau tien", "lac long quan", "au co", "boc tram trung", "lam vua", "hung vuong"],
        "context": """
- Bối cảnh: Thời kỳ sơ khai lập nước Việt Nam.
- Nhân vật chính:
  + Lạc Long Quân: Con thần Sùng Lãm, dòng dõi Rồng, có sức khỏe vô địch, nhiều phép lạ, giúp dân trừ yêu quái.
  + Âu Cơ: Dòng dõi Tiên, con gái Đế Lai, xinh đẹp tuyệt trần, sống ở vùng núi cao.
- Cốt truyện truyền thống:
  1. Lạc Long Quân kết duyên cùng Âu Cơ. Sau đó, Âu Cơ mang thai và sinh ra một bọc trăm trứng, nở ra một trăm người con trai hồng hào, khôi ngô tuấn tú.
  2. Do nếp sống khác nhau (Rồng ở nước, Tiên ở núi), Lạc Long Quân bàn với Âu Cơ chia con ra: 50 người con theo cha xuống biển, 50 người con theo mẹ lên núi, hẹn khi gặp hoạn nạn sẽ giúp đỡ lẫn nhau.
  3. Người con trưởng theo Âu Cơ lên vùng Phong Châu được tôn làm vua, lấy hiệu là Hùng Vương, lập ra nước Văn Lang. Từ đó, người Việt thường tự hào xưng là "Con Rồng Cháu Tiên".
- Lời thoại và tạo ảnh:
  + Giọng nói mang tính sử thi oai hùng, uy nghiêm.
  + Hình ảnh bọc trăm trứng phát sáng, Lạc Long Quân hóa rồng oai vệ và Âu Cơ bay lượn nhẹ nhàng thanh thoát như tiên nữ.
"""
    },
    "sutich_con_da_trang": {
        "canonical_title": "Sự tích con dã tràng",
        "keywords": ["da trang", "se cat", "vien ngoc", "ran ho mang", "tieng muong thu", "mat ngoc"],
        "context": """
- Bối cảnh: Đời sống dân gian thuở xưa.
- Nhân vật chính:
  + Dã Tràng: Người nông dân hiền lành, nghèo khổ.
  + Rắn hổ mang (rắn thần): Được Dã Tràng cứu mạng, trả ơn bằng một viên ngọc quý giúp nghe và hiểu tiếng của muông thú.
  + Vợ Dã Tràng: Người vợ vô tình làm mất viên ngọc thần.
- Cốt truyện truyền thống:
  1. Dã Tràng cứu sống rắn hổ mang. Rắn đền ơn bằng viên ngọc thần. Nhờ ngọc, Dã Tràng nghe tiếng chim quạ biết chỗ chôn vàng, cứu đàn kiến khỏi lụt. Đàn kiến trả ơn bằng cách báo trước các tin tức cần thiết.
  2. Một lần đi thuyền dạo chơi trên biển, vợ Dã Tràng cầm viên ngọc ngậm trong miệng để tránh làm rơi, nhưng không may vô tình nuốt mất (hoặc ngọc rơi xuống biển sâu).
  3. Mất ngọc thần, Dã Tràng vô cùng đau đớn và tiếc nuối. Chàng quyết tâm se cát lấp biển để tìm lại ngọc.
  4. Chàng làm việc ngày đêm không nghỉ cho đến khi kiệt sức chết hóa thành con dã tràng tiếp tục se cát bên bờ biển.
- Lời thoại và tạo ảnh:
  + Lời thoại buồn bã, thể hiện sự bất lực và nỗ lực vô vọng của Dã Tràng.
  + Hình ảnh con dã tràng nhỏ bé miệt mài vê từng viên cát tròn bên bờ sóng biển xô bồ.
"""
    },
    "coc_kien_troi": {
        "canonical_title": "Cóc kiện trời",
        "keywords": ["coc kien troi", "ong", "cua", "gau", "cop", "thien loi", "ngoc hoang", "nghien rang"],
        "context": """
- Bối cảnh: Trần gian gặp nạn đại hạn hán lâu ngày, vạn vật khô héo.
- Nhân vật chính:
  + Cóc: Con vật nhỏ bé nhưng gan dạ, thông minh, lãnh đạo muông thú đi đòi công lý.
  + Các bạn đồng hành: Cua, Gấu, Cọp (Hổ), Ong.
  + Ngọc Hoàng và Thiên Lôi: Thần linh cai quản mưa gió trên Thiên đình.
- Cốt truyện truyền thống:
  1. Nắng hạn kéo dài, Cóc quyết định lên thiên đình kiện Ngọc Hoàng. Dọc đường đi, Cóc rủ thêm Cua, Gấu, Cọp và Ong đi cùng.
  2. Đến cổng trời, Cóc sắp xếp đội hình: Cua nằm trong chum nước, Ong núp sau cửa, Gấu và Cọp ở hai bên cổng chờ sẵn. Cóc một mình vào đánh trống đòi kiện Ngọc Hoàng.
  3. Ngọc Hoàng nổi giận sai gà rừng, chó, rồi Thiên Lôi ra trị Cóc. Tất cả đều bị Cóc và nhóm bạn phối hợp đánh bại thảm hại (gà bị cọp bắt, Thiên Lôi bị ong châm chui vào chum nước bị cua kẹp, gấu đuổi).
  4. Ngọc Hoàng buộc phải xuống nước tiếp kiến Cóc, hứa sẽ làm mưa ngay xuống trần gian. Ngọc Hoàng dặn: "Hễ khi nào nắng hạn, ngươi cứ nghiến răng báo hiệu, ta sẽ cho mưa".
- Lời thoại và tạo ảnh:
  + Tiếng Cóc nghiến răng ken két vang dội. Giọng Cóc đanh thép đòi công lý cho muôn loài.
  + Cảnh Cóc nhỏ bé đứng trên trống chầu gõ trống oai phong lẫm liệt trước Ngọc Hoàng quyền uy.
"""
    },
    "sutich_cay_khe": {
        "canonical_title": "Sự tích cây khế",
        "keywords": ["cay khe", "tui ba gang", "nguoi em", "nguoi anh", "phuong hoang", "an mot qua tra cuc vang"],
        "context": """
- Bối cảnh: Làng quê Việt Nam cổ xưa.
- Nhân vật chính:
  + Người em: Thật thà, hiền lành, chăm chỉ, cam chịu, được chia một gian nhà tranh và cây khế.
  + Người anh và vợ người anh: Tham lam, ích kỷ, lấy hết gia sản cha mẹ để lại.
  + Chim Phượng Hoàng: Con chim khổng lồ biết nói, ăn khế trả vàng.
- Cốt truyện truyền thống:
  1. Cha mẹ mất, người anh chia hết gia tài chỉ cho người em cây khế ngọt. Người em chăm sóc cây chu đáo.
  2. Phượng Hoàng đến ăn khế chín. Người em khóc than quả khế là nguồn sống duy nhất. Chim đáp: "Ăn một quả, trả cục vàng, may túi ba gang, mang đi mà đựng".
  3. Chim chở người em ra đảo vàng ngoài khơi. Người em lấy vừa đủ túi ba gang rồi về, trở nên giàu có.
  4. Người anh biết chuyện đòi đổi toàn bộ gia tài lấy cây khế. Người anh cũng chờ chim đến ăn và hứa trả vàng. Nhưng do tham lam, người anh may túi tận chín gang và nhét đầy vàng vào người.
  5. Trên đường bay về, do sức nặng quá tải cộng với gió lớn, chim kiệt sức chao cánh khiến người anh rơi xuống biển sâu chết chìm cùng túi vàng.
- Lời thoại và tạo ảnh:
  + Lời thoại của người anh tham lam, quát tháo; người em nhỏ nhẹ, thật thà. Câu nói nổi tiếng của chim: "Ăn một quả, trả cục vàng, may túi ba gang, mang đi mà đựng".
  + Hình ảnh chim Phượng Hoàng khổng lồ lông ngũ sắc sặc sỡ đáp xuống cây khế trĩu quả vàng.
"""
    },
    "sutich_chu_cuoi_cung_trang": {
        "canonical_title": "Sự tích chú Cuội cung trăng",
        "keywords": ["chu cuoi", "cuoi cung trang", "cay da than", "la da cuu nguoi", "vo cuoi", "nuoc ban"],
        "context": """
- Bối cảnh: Làng quê nông thôn thanh bình.
- Nhân vật chính:
  + Cuội: Chàng tiều phu nghèo làm nghề đốn củi. Tính tình thật thà, thích cứu giúp người khác.
  + Cây đa thần: Cây có lá thần kỳ cải tử hoàn sinh.
  + Vợ Cuội: Tính tình hay quên, vô tình làm hại cây đa.
- Cốt truyện truyền thống:
  1. Cuội đi rừng phát hiện cọp mẹ dùng lá cây đa cứu cọp con sống lại. Cuội biết là cây quý bèn bứng về trồng ở góc sân nhà, dùng lá cứu sống nhiều người chết.
  2. Cuội dặn vợ: "Tưới nước cho cây thì tưới nước sạch, chớ tưới nước bẩn mà cây bay lên trời".
  3. Một ngày Cuội đi vắng, người vợ hay quên đã lấy nước bẩn tưới vào gốc cây. Đất đá dưới gốc cây rùng rùng chuyển động, cây đa rứt rễ bay lên trời.
  4. Cuội về vừa lúc cây cất cánh, vội nhảy lên níu giữ nhưng không cản nổi. Cuội bám vào rễ cây và bị kéo bay thẳng lên tận Cung Trăng.
- Lời thoại và tạo ảnh:
  + Hình ảnh chú Cuội ngồi dưới gốc cây đa thần trên mặt trăng sáng tỏ vào những đêm rằm.
  + Lời thoại mộc mạc, dân dã, biểu lộ sự hoảng hốt khi cây đa bay lên.
"""
    },
    "an_duong_vuong_mi_chau_trong_thuy": {
        "canonical_title": "An Dương Vương và Mị Châu - Trọng Thủy",
        "keywords": ["an duong vuong", "mi chau", "trong thuy", "no than", "mong rua", "trieu da", "long ngong", "co loa"],
        "context": """
- Bối cảnh: Nước Âu Lạc thời An Dương Vương đóng đô ở thành Cổ Loa.
- Nhân vật chính:
  + An Dương Vương (Thục Phán): Vua nước Âu Lạc, được thần Kim Quy giúp xây thành Cổ Loa và tặng móng làm nỏ thần đánh giặc.
  + Mị Châu: Công chúa nết na, cả tin, yêu chồng hết mực.
  + Trọng Thủy: Con trai Triệu Đà, làm rể Âu Lạc, lợi dụng tình cảm của Mị Châu để đánh cắp bí mật quốc gia.
- Cốt truyện truyền thống:
  1. An Dương Vương có nỏ thần bắn một phát ra hàng vạn mũi tên khiến giặc Triệu Đà khiếp sợ. Triệu Đà xin hòa, cho con trai Trọng Thủy sang làm rể và ở rể thành Cổ Loa.
  2. Trọng Thủy dỗ dành Mị Châu cho xem nỏ thần rồi lén tráo móng rùa thần bằng móng giả. Lấy được bí mật, Trọng Thủy xin về nước báo tin. Trước khi đi, hai người ước hẹn nếu có chiến tranh, Mị Châu sẽ rải lông ngỗng dọc đường chạy nạn để Trọng Thủy tìm theo.
  3. Triệu Đà đem quân đánh Âu Lạc. An Dương Vương chủ quan dùng nỏ thần bắn nhưng không còn phép màu, đành chở Mị Châu chạy về phương Nam.
  4. Đến bờ biển cạn, không còn lối thoát, Vua cầu cứu thần Kim Quy. Rùa Vàng nổi lên chỉ rõ: "Kẻ ngồi sau lưng chính là giặc đó!". An Dương Vương hiểu ra, rút gươm chém Mị Châu rồi đi xuống biển.
  5. Trọng Thủy theo dấu lông ngỗng tìm đến xác vợ khóc thương mang về chôn cất, sau đó nhảy xuống giếng trong thành Cổ Loa tự tử. Máu Mị Châu rơi xuống biển thành ngọc trai, mang ngọc rửa bằng nước giếng Trọng Thủy thì ngọc sáng vô cùng.
- Lời thoại và tạo ảnh:
  + Lời thoại mang âm hưởng bi kịch, cảnh báo sâu sắc về lòng tin và vận mệnh đất nước.
  + Chiếc nỏ thần Liên Châu, chiếc áo lông ngỗng của Mị Châu rải dọc đường chạy nạn, và giếng Loa Thành.
"""
    },
    "tri_khon_cua_ta_day": {
        "canonical_title": "Trí khôn của ta đây",
        "keywords": ["tri khon cua ta day", "cop", "trau", "bac nong dan", "rom dot", "bi chay xam"],
        "context": """
- Bối cảnh: Cánh đồng làng quê Việt Nam xưa.
- Nhân vật chính:
  + Bác nông dân: Thông minh, nhanh trí, đối đối bản lĩnh trước ác thú.
  + Con Cọp (Hổ): To khỏe, tò mò, kiêu ngạo nhưng ngốc nghếch.
  + Con Trâu: Chăm chỉ cày ruộng, cam chịu số phận.
- Cốt truyện truyền thống:
  1. Cọp thấy Trâu to khỏe bị bác nông dân quất roi cày ruộng. Cọp hỏi Trâu sao lại để sinh vật bé nhỏ kia sai khiến. Trâu trả lời vì con người có "trí khôn".
  2. Cọp đến hỏi bác nông dân: "Trí khôn của bác đâu, cho tôi xem một tí?". Bác nông dân trả lời: "Trí khôn tôi để ở nhà. Để tôi về lấy cho xem. Nhưng sợ lúc tôi đi vắng, cọp ăn mất trâu của tôi, nên để tôi trói cọp lại vào gốc cây".
  3. Cọp muốn xem trí khôn nên đồng ý chịu trói. Bác nông dân lấy dây thừng trói chặt Cọp vào gốc cây đa.
  4. Trói xong, bác nông dân chất rơm xung quanh Cọp rồi châm lửa đốt, vừa quật roi vừa hét lớn: "Trí khôn của ta đây! Trí khôn của ta đây!".
  5. Trâu thấy cọp bị đốt thì cười bò lăn ra đất, va răng vào đá gãy hết hàm răng trên. Cọp bị cháy sém lông thành những vằn đen đen, đứt dây trói chạy thẳng vào rừng sâu. Từ đó cọp có vằn đen và trâu không có răng hàm trên.
- Lời thoại và tạo ảnh:
  + Lời thoại vui nhộn, mang tính ngụ ngôn răn dạy. Câu nói nổi tiếng: "Trí khôn của ta đây!".
  + Cảnh cọp bị trói chặt xung quanh lửa rơm bùng cháy, trâu cười nghiêng ngả gãy răng.
"""
    },
    "em_be_thong_minh": {
        "canonical_title": "Em bé thông minh",
        "keywords": ["em be thong minh", "cau do", "xỏ chi vo oc", "kien cang", "chim se ba mam co", "trau duc de con"],
        "context": """
- Bối cảnh: Đất nước Việt Nam thời phong kiến xưa.
- Nhân vật chính:
  + Em bé: Con một nhà nông dân nghèo, rất thông minh, lém lỉnh, ứng biến nhanh nhạy trước các câu đố hiểm hóc.
  + Viên quan và Nhà vua: Luôn đi tìm kiếm nhân tài và thử thách dân chúng bằng các câu đố kỳ lạ.
  + Sứ giả nước láng giềng: Mang câu đố sang thử thách với ý đồ dò xét thực lực nước ta.
- Cốt truyện truyền thống:
  1. Quan đi tìm hiền tài, gặp hai cha con cày ruộng, hỏi trâu cày một ngày đi được mấy đường. Em bé hỏi vặn lại ngựa của quan đi một ngày được mấy bước khiến quan phục tài về tâu vua.
  2. Vua thử thách lần một: Cho làng của em bé ba thúng nếp và ba con trâu đực, bắt nuôi sao cho trâu đẻ con. Em bé lừa vua tự thừa nhận trâu đực không đẻ được bằng cách bắt bố khóc đòi đẻ em bé.
  3. Vua thử thách lần hai: Đưa một con chim sẻ bắt dọn thành ba mâm cỗ. Em bé đưa cây kim khâu nhờ vua rèn hộ thành con dao xẻ thịt chim. Vua nể phục khâm phục tài trí.
  4. Thử thách lần ba: Sứ giả nước láng giềng mang vỏ ốc vặn rất dài và rỗng hai đầu, đố xỏ chỉ qua ruột ốc. Cả triều đình bó tay. Em bé vừa hát đồng dao vừa bày kế: buộc chỉ vào chân con kiến càng, bôi mỡ ở đầu bên kia vỏ ốc để kiến ngửi mùi bò qua kéo sợi chỉ theo. Nước láng giềng kính phục từ bỏ ý định xâm lược, em bé được phong làm Trạng nguyên.
- Lời thoại và tạo ảnh:
  + Giọng em bé thông minh, tự tin, hóm hỉnh.
  + Cảnh em bé hát đồng dao xỏ chỉ vỏ ốc bằng kiến càng trước sự ngỡ ngàng của quan quân.
"""
    },
    "thay_boi_xem_voi": {
        "canonical_title": "Thầy bói xem voi",
        "keywords": ["thay boi xem voi", "mu", "so voi", "con dia", "don xoc", "quat thoc", "cot dinh", "choi se cun"],
        "context": """
- Bối cảnh: Phiên chợ quê náo nhiệt.
- Nhân vật chính:
  + Năm ông thầy bói mù: Mỗi người tò mò muốn biết hình thù con voi thế nào nên chung tiền cho quản tượng để được sờ voi.
- Cốt truyện truyền thống:
  1. Năm thầy mù tụ họp cùng nhau xem voi. Vì mù nên mỗi thầy chỉ sờ được một bộ phận của con voi.
  2. Thầy sờ vòi bảo: "Tưởng con voi thế nào, hóa ra nó sun sun như con đỉa".
  3. Thầy sờ ngà bảo: "Không phải, nó chành chành như cái đòn xóc".
  4. Thầy sờ tai bảo: "Đâu có! Nó bè bè như cái quạt thóc".
  5. Thầy sờ chân bảo: "Ai bảo! Nó sừng sững như cái cột đình".
  6. Thầy sờ đuôi bảo: "Các thầy nói sai cả. Nó tua tủa như cái chổi sể cùn".
  7. Năm thầy không ai chịu ai, cãi nhau kịch liệt rồi dẫn đến xô xát, đánh nhau toác đầu chảy máu.
- Lời thoại và tạo ảnh:
  + Lời thoại mang tính châm biếm sâu cay về thói phiến diện, quy chụp của con người.
  + Hình ảnh năm ông thầy mù vẻ mặt quả quyết, mỗi người ôm sờ một phần của con voi khổng lồ.
"""
    },
    "truyen_trang_quynh": {
        "canonical_title": "Truyện Trạng Quỳnh",
        "keywords": ["trang quynh", "mam da", "chua trinh", "trao phung", "dat nut con bo hung", "trang chet chua bang ha"],
        "context": """
- Bối cảnh: Xã hội Việt Nam thời vua Lê chúa Trịnh suy thoái.
- Nhân vật chính:
  + Trạng Quỳnh (Nguyễn Quỳnh): Nhân vật dân gian thông minh, giỏi chữ nghĩa văn thơ, dùng tài trí châm biếm chúa Trịnh kiêu căng, các quan lại tham lam, hống hách để bênh vực dân nghèo.
- Cốt truyện truyền thống:
  - Gồm các giai thoại trào phúng nổi tiếng:
    1. "Món ăn mầm đá": Chúa Trịnh kén ăn, Quỳnh bảo có món mầm đá rất ngon nhưng phải ninh lâu. Quỳnh bắt chúa chờ đói lả người, rồi dâng tương và rau luộc lên ăn ngon lành.
    2. "Đất nứt con bọ hung": Trêu chọc chúa khi chúa ra vế đối hống hách tự đắc.
    3. "Vẽ rồng đất": Vẽ cực nhanh bằng cách nhúng các ngón tay vào mực rồi quệt.
    4. "Trạng chết Chúa cũng băng hà": Quỳnh biết chúa Trịnh muốn đầu độc mình, trước khi ăn bát canh độc đã dặn dò gia nhân lo liệu, quả nhiên khi Quỳnh chết thì chúa Trịnh cũng chết theo do uống thuốc độc từ trước.
- Lời thoại và tạo ảnh:
  + Lời thoại thâm thúy, thông minh, sâu cay, châm biếm sâu sắc.
  + Hình ảnh Trạng Quỳnh mặc áo vải dân dã nhưng nét mặt thông tuệ, tự tin đối đầu chúa Trịnh đầy quan cách xa hoa.
"""
    },
    "truyen_trang_lon": {
        "canonical_title": "Truyện Trạng Lợn",
        "keywords": ["trang lon", "chung", "doan mo", "may man", "long dong duoi giac"],
        "context": """
- Bối cảnh: Làng quê phong kiến Việt Nam xưa.
- Nhân vật chính:
  + Trạng Lợn (tên thật là Chung): Con một nhà mổ lợn, lười học, dốt nát nhưng có tài đoán mò và cực kỳ may mắn, về sau đỗ Trạng nguyên.
- Cốt truyện truyền thống:
  - Gồm chuỗi sự kiện ngẫu nhiên giúp Chung được tôn làm thần bói toán và Trạng nguyên:
    1. Đoán hướng tìm lợn lạc trùng khớp 100% nhờ sự ngẫu nhiên.
    2. Đi thi đỗ Trạng nguyên nhờ gặp các tình huống trùng lặp kỳ lạ giúp đoán trúng đề bài và giải mã thành công câu hỏi hóc búa của sứ thần.
    3. Dẹp giặc giã bằng cách hoảng hốt khua chiêng gõ trống vô tình khiến địch tưởng có mai phục lớn mà hoảng loạn rút quân.
- Lời thoại và tạo ảnh:
  + Mang tiếng cười hóm hỉnh, trào phúng, châm biếm thói mê tín và thi cử ngày xưa.
  + Hình ảnh chàng Trạng Lợn béo tròn, nét mặt ngây ngô nhưng luôn gặp may mắn tột đỉnh trong mọi hoàn cảnh.
"""
    },
    "co_be_ban_diem": {
        "canonical_title": "Cô bé bán diêm",
        "keywords": ["co be ban diem", "quet diem", "ao anh", "dem giao thua", "ba ngoai", "chet ret"],
        "context": """
- Bối cảnh: Đêm giao thừa tuyết rơi buốt giá ở một thành phố châu Âu thời xưa.
- Nhân vật chính:
  + Cô bé bán diêm: Cô bé mồ côi mẹ, nhà nghèo khổ, đi chân đất bán diêm giữa trời đông giá rét. Cô bé rất sợ người cha bạo hành nếu không mang tiền về.
  + Bà ngoại: Người bà hiền từ đã qua đời, hiện ra trong ảo ảnh mang lại tình thương yêu duy nhất cho cô bé.
- Cốt truyện truyền thống:
  1. Đêm giao thừa rét mướt, cô bé đi bán diêm nhưng không ai mua. Sợ cha đánh nên không dám về nhà. Cô bé ngồi nép vào góc tường lạnh lẽo giữa hai ngôi nhà.
  2. Cô bé quẹt que diêm thứ nhất để sưởi ấm, hiện ra lò sưởi bằng đồng ấm áp. Diêm tắt, lò sưởi biến mất.
  3. Quẹt que thứ hai, hiện ra bàn ăn thịnh soạn với ngỗng quay vàng rực đi trên bàn. Diêm tắt, bàn ăn biến mất.
  4. Quẹt que thứ ba, hiện ra cây thông Noel lộng lẫy cùng hàng ngàn ngọn nến sáng lung linh.
  5. Quẹt que thứ tư, cô bé nhìn thấy người bà hiền dịu mỉm cười. Để giữ bà lại, cô bé vội quẹt tất cả số diêm còn lại trong bao. Bà ôm lấy cô bé và cả hai bay lên trời, về với Chúa nơi không còn đói rét, đau khổ.
  6. Sáng hôm sau, người ta tìm thấy cô bé chết rét ở xó tường với đôi má hồng và nụ cười trên môi.
- Lời thoại và tạo ảnh:
  + Lời thoại buồn bã, chứa đựng niềm tin ngây thơ, khát khao tình yêu thương và sự ấm áp.
  + Hình ảnh tương phản gay gắt giữa ánh sáng lung linh của que diêm và màn đêm tuyết rơi đen tối, lạnh buốt.
"""
    },
    "lo_lem": {
        "canonical_title": "Lọ Lem",
        "keywords": ["lo lem", "giay thuy tinh", "ba tien do dau", "bi ngo", "xe ngua", "hoang tu", "me ke"],
        "context": """
- Bối cảnh: Vương quốc cổ tích xa xưa.
- Nhân vật chính:
  + Lọ Lem (Cinderella): Cô gái hiền lành, xinh đẹp, chịu thương chịu khó nhưng bị mẹ kế và hai cô chị hành hạ dã man.
  + Mẹ kế và hai chị riêng: Độc ác, đố kỵ, kiêu ngạo, bắt Lọ Lem làm việc quần quật suốt ngày.
  + Bà tiên đỡ đầu: Thần tiên nhân từ hóa phép giúp đỡ Lọ Lem đi trẩy hội.
  + Hoàng tử: Chàng hoàng tử vương quốc, say đắm vẻ đẹp và sự thanh khiết của Lọ Lem.
- Cốt truyện truyền thống:
  1. Hoàng cung mở tiệc khiêu vũ kén vợ cho hoàng tử. Mẹ kế không cho Lọ Lem đi, bắt cô nhặt đậu và dọn dẹp nhà cửa.
  2. Bà tiên đỡ đầu hiện ra, dùng gậy thần hóa quả bí ngô thành cỗ xe vàng, chuột thành ngựa, rách rưới thành váy dạ hội lộng lẫy và đôi giày thủy tinh lấp lánh. Bà dặn Lọ Lem phải rời tiệc trước 12 giờ đêm vì phép thuật sẽ biến mất.
  3. Lọ Lem đến dạ tiệc, nhảy cùng hoàng tử và làm say đắm tất cả mọi người. Đúng 12 giờ đêm, cô vội vã chạy đi, đánh rơi một chiếc giày thủy tinh trên bậc thềm hoàng cung.
  4. Hoàng tử sai quân lính mang giày thủy tinh đi khắp vương quốc thử chân các cô gái, ai đi vừa sẽ cưới làm vợ.
  5. Mặc cho các cô chị cố gắng ních chân vào, chỉ có Lọ Lem đi vừa khít. Cô mặc lại chiếc váy dạ hội lộng lẫy, kết hôn cùng hoàng tử và sống hạnh phúc.
- Lời thoại và tạo ảnh:
  + Giọng Lọ Lem dịu dàng, nhẫn nhịn. Giọng mẹ kế chua ngoa, hách dịch.
  + Cảnh biến đổi kỳ diệu từ quả bí ngô thành cỗ xe vàng lấp lánh phép thuật, đôi giày thủy tinh lung linh dưới ánh đèn cung điện.
"""
    },
    "cong_chua_ngu_trong_rung": {
        "canonical_title": "Công chúa ngủ trong rừng",
        "keywords": ["cong chua ngu trong rung", "aurora", "mui soi", "nguyen rua", "nu hon", "hoang tu", "maleficent"],
        "context": """
- Bối cảnh: Vương quốc thần tiên cổ xưa.
- Nhân vật chính:
  + Công chúa Aurora (Hồng Hoa): Xinh đẹp, thuần khiết, bị dính lời nguyền ngủ trăm năm.
  + Mụ phù thủy độc ác (Maleficent): Tức giận vì không được mời dự tiệc đầy tháng công chúa nên đã ban lời nguyền độc địa.
  + Các bà tiên tốt bụng: Giảm nhẹ lời nguyền từ cái chết thành giấc ngủ trăm năm.
  + Hoàng tử: Người anh hùng dũng cảm vượt rừng gai, đánh thức công chúa bằng nụ hôn chân tình.
- Cốt truyện truyền thống:
  1. Lễ đầy tháng công chúa, phù thủy độc ác nguyền rằng khi tròn 16 tuổi, công chúa sẽ bị mũi sợi của máy quay sợi đâm vào tay và chết. Bà tiên tốt hóa giải thành giấc ngủ sâu 100 năm và sẽ tỉnh lại nhờ nụ hôn của tình yêu đích thực.
  2. Nhà vua ra lệnh tiêu hủy mọi máy quay sợi trong nước. Đến tuổi 16, công chúa tò mò chạm vào chiếc máy quay sợi cũ giấu trên đỉnh tháp và chìm vào giấc ngủ. Cả lâu đài cũng chìm vào giấc ngủ sâu cùng nàng.
  3. Rừng gai mọc dày đặc bao phủ toàn bộ lâu đài cô tịch.
  4. Trăm năm sau, một hoàng tử dũng cảm tìm đến vượt qua rừng gai hiểm trở, tìm thấy công chúa đang ngủ và trao cho nàng nụ hôn. Lời nguyền bị phá bỏ, công chúa và toàn vương quốc tỉnh giấc vui mừng.
- Lời thoại và tạo ảnh:
  + Giọng phù thủy đe dọa, giận dữ; các bà tiên nhân hậu, nhẹ nhàng.
  + Hình ảnh lâu đài cổ kính bị bao phủ bởi rừng gai rậm rạp, công chúa ngủ xinh đẹp lộng lẫy trên giường phủ hoa.
"""
    },
    "bach_tuyet_va_bay_chu_lun": {
        "canonical_title": "Nàng Bạch Tuyết và bảy chú lùn",
        "keywords": ["bach tuyet", "bay chu lun", "guong than", "tao doc", "hoang hau", "quan tai thuy tinh", "me ke"],
        "context": """
- Bối cảnh: Khu rừng cổ tích và lâu đài hoàng gia.
- Nhân vật chính:
  + Nàng Bạch Tuyết: Xinh đẹp "da trắng như tuyết, môi đỏ như son, tóc đen như gỗ mun", hiền lành, tốt bụng.
  + Hoàng hậu độc ác: Mẹ kế của Bạch Tuyết, ghen ghét sắc đẹp của nàng, sở hữu chiếc gương thần biết nói.
  + Bảy chú lùn: Sống trong rừng sâu, làm nghề đào mỏ, bảo bọc che chở cho Bạch Tuyết.
  + Hoàng tử: Say đắm nàng Bạch Tuyết, giúp giải cứu nàng khỏi độc tố.
- Cốt truyện truyền thống:
  1. Hoàng hậu có gương thần luôn hỏi ai đẹp nhất trần gian. Khi Bạch Tuyết lớn lên, gương thần bảo Bạch Tuyết đẹp nhất. Hoàng hậu tức giận sai thợ săn mang Bạch Tuyết vào rừng giết hại. Người thợ săn thương tình thả nàng đi.
  2. Bạch Tuyết chạy trốn vào rừng, tìm thấy ngôi nhà nhỏ của bảy chú lùn và được họ đồng ý cho ở lại chăm sóc nhà cửa.
  3. Hoàng hậu biết được qua gương thần, ba lần giả dạng tìm đến hãm hại nàng (bằng dây buộc ngực, lược độc, và quả táo độc). Bạch Tuyết ăn nửa quả táo độc rồi ngã xuống chết lâm sàng.
  4. Bảy chú lùn khóc thương, đặt nàng vào chiếc quan tài thủy tinh trong suốt.
  5. Hoàng tử đi qua nhìn thấy yêu mến nàng, xin đưa quan tài về cung. Trên đường đi, quân lính khênh quan tài vấp ngã làm quả táo độc văng khỏi cổ họng Bạch Tuyết. Nàng tỉnh dậy và kết duyên cùng hoàng tử.
- Lời thoại và tạo ảnh:
  + Câu nói nổi tiếng của Hoàng hậu: "Gương kia ngự ở trên tường, thế gian ai đẹp dường như ta?".
  + Hình ảnh Bạch Tuyết nằm trong quan tài thủy tinh rực rỡ, xung quanh là bảy chú lùn nhỏ bé khóc thương sụt sùi trong rừng sâu.
"""
    },
    "co_be_quang_khan_do": {
        "canonical_title": "Cô bé quàng khăn đỏ",
        "keywords": ["co be quang khan do", "khan do", "cho soi", "ba ngoai", "tho san", "nuot chung", "banh"],
        "context": """
- Bối cảnh: Con đường xuyên rừng xanh âm u.
- Nhân vật chính:
  + Khăn Đỏ: Cô bé ngây thơ, ham chơi, mặc chiếc áo choàng màu đỏ nổi bật.
  + Con Sói: Gian manh, xảo quyệt, thích ăn thịt người.
  + Bà ngoại: Sống cô đơn trong ngôi nhà sâu trong rừng.
  + Bác thợ săn (hoặc bác tiều phu): Người anh hùng giải cứu hai bà cháu.
- Cốt truyện truyền thống:
  1. Mẹ bảo Khăn Đỏ mang bánh sang thăm bà ngoại bị ốm, dặn đi đường thẳng, không được la cà.
  2. Dọc đường rừng, Khăn Đỏ gặp Sói. Sói ngon ngọt dụ dỗ cô bé đi hái hoa bắt bướm, còn mình chạy tắt đến nhà bà ngoại.
  3. Sói đến nhà bà ngoại, giả giọng Khăn Đỏ vào phòng rồi nuốt chửng bà ngoại. Sau đó Sói mặc quần áo của bà, đội mũ nằm trên giường đợi Khăn Đỏ.
  4. Khăn Đỏ đến nơi, ngạc nhiên hỏi về đôi tai to, mắt to, tay to, miệng to của Sói. Sói chồm dậy nuốt chửng luôn cô bé rồi nằm ngủ ngáy o o.
  5. Bác thợ săn đi qua nghe tiếng ngáy lạ, vào nhà thấy sói. Bác lấy kéo rạch bụng sói, cứu sống Khăn Đỏ và bà ngoại ra an toàn. Bác nhét đá đầy bụng sói khiến sói chết.
- Lời thoại và tạo ảnh:
  + Lời thoại đối đáp kinh điển giữa Khăn Đỏ và Sói giả dạng bà ngoại ("Bà ơi, sao tai bà to thế?...").
  + Hình ảnh cô bé quàng khăn đỏ nổi bật giữa rừng xanh rậm rạp và con sói to lớn ranh mãnh nấp sau cây.
"""
    },
    "chu_linh_chi_dung_cam": {
        "canonical_title": "Chú lính chì dũng cảm",
        "keywords": ["chu linh chi", "mot chan", "co vu nu", "thuyen giay", "lo suoi", "trai tim chi"],
        "context": """
- Bối cảnh: Căn phòng đồ chơi của trẻ em và hành trình trôi nổi ngoài cống rãnh.
- Nhân vật chính:
  + Chú lính chì: Chú lính đồ chơi làm bằng chì, bị thiếu một chân do đúc sau cùng thiếu nguyên liệu. Chú dũng cảm, trung kiên và có tình yêu chung thủy.
  + Cô vũ nữ bằng giấy: Xinh đẹp, đứng kiễng một chân làm chú lính chì tưởng nàng cũng giống mình.
  + Con sói đen/quỷ trong hộp lò xo: Kẻ đố kỵ luôn tìm cách hại chú lính chì.
- Cốt truyện truyền thống:
  1. Chú lính chì thầm yêu cô vũ nữ giấy xinh đẹp. Đêm đến, con quỷ trong hộp lò xo đe dọa chú không được mơ tưởng đến cô vũ nữ.
  2. Hôm sau, chú lính chì vô tình rơi từ cửa sổ xuống đường phố. Hai đứa trẻ nhặt được đặt chú lên thuyền giấy thả trôi theo dòng nước cống rãnh.
  3. Chú trôi ra sông và bị một con cá lớn nuốt chửng. Con cá sau đó bị đánh bắt đem bán vào đúng ngôi nhà cũ. Người đầu bếp mổ cá tìm thấy chú lính chì mang đặt lại phòng chơi đồ chơi.
  4. Một đứa trẻ không rõ lý do đột ngột ném chú lính chì vào lò sưởi đang cháy đỏ. Đúng lúc đó, gió lùa mạnh thổi bay cô vũ nữ giấy rơi thẳng vào lò sưởi cùng chú. Cả hai cùng cháy rụi.
  5. Hôm sau, khi dọn lò sưởi, người ta tìm thấy một miếng chì nhỏ hình trái tim và chiếc kim sa bằng đồng bị cháy sém của cô vũ nữ.
- Lời thoại và tạo ảnh:
  + Sự kiên cường, bất khuất của chú lính chì trước giông bão cuộc đời.
  + Hình ảnh chú lính chì đứng thẳng chỉ bằng một chân, cầm súng trên chiếc thuyền giấy trôi giữa dòng nước tối tăm.
"""
    },
    "vit_con_xau_xi": {
        "canonical_title": "Vịt con xấu xí",
        "keywords": ["vit con xau xi", "thien nga", "xao xit", "mat tong", "trang trai"],
        "context": """
- Bối cảnh: Trang trại làng quê thanh bình và đầm nước mùa đông hoang vắng.
- Nhân vật chính:
  + Vịt con xấu xí: Quả trứng to nhất nở muộn nhất, lông xám xịt, to lớn và thô kệch khác thường, chịu sự ghẻ lạnh của đồng loại nhưng thực chất mang dòng máu thiên nga.
- Cốt truyện truyền thống:
  1. Mẹ Vịt ấp trứng nở ra đàn con xinh đẹp riêng quả trứng cuối nở ra chú vịt con xám xịt, xấu xí. Chú bị anh chị em chê cười, đàn gà vịt trong trang trại mổ và bắt nạt.
  2. Quá buồn tủi, vịt con bỏ trang trại ra đi. Chú lang thang khắp nơi, trải qua một mùa đông lạnh giá cô độc, suýt chết cóng trong đầm nước nếu không được bác nông dân cứu giúp.
  3. Mùa xuân ấm áp trở về, cánh vịt con cứng cáp hơn. Chú bay đến một hồ nước lớn thấy đàn thiên nga trắng muốt xinh đẹp bơi lội.
  4. Chú vịt con tự ti cúi đầu xuống mặt nước chờ bị xua đuổi, nhưng bất ngờ nhìn thấy hình bóng phản chiếu của mình: Chú không còn là con vịt xám xấu xí nữa mà đã hóa thành một chú thiên nga trắng tuyệt đẹp, kiêu sa. Đàn thiên nga chào đón chú gia nhập đàn.
- Lời thoại và tạo ảnh:
  + Thể hiện nỗi buồn sâu thẳm của sự khác biệt và niềm hạnh phúc vỡ òa khi tìm thấy bản thân thật sự.
  + Hình ảnh vịt con xơ xác đi dưới mưa tuyết mùa đông và hình ảnh thiên nga trắng muốt kiêu sa soi bóng trên mặt hồ xuân trong vắt.
"""
    },
    "bo_quan_ao_moi_cua_hoang_de": {
        "canonical_title": "Bộ quần áo mới của hoàng đế",
        "keywords": ["bo quan ao moi", "hoang de", "tang hinh", "lua dao", "dua tre", "kieu ngao"],
        "context": """
- Bối cảnh: Vương quốc xa hoa thời xưa.
- Nhân vật chính:
  + Hoàng đế: Người ham chuộng chưng diện váy áo, kiêu ngạo, dễ bị nịnh hót.
  + Hai kẻ lừa đảo: Tự xưng là thợ dệt giỏi nhất, dệt ra loại vải vô hình đối với kẻ ngu ngốc hoặc không làm tròn bổn phận.
  + Đứa trẻ: Người duy nhất dũng cảm nói lên sự thật hiển nhiên.
- Cốt truyện truyền thống:
  1. Hoàng đế chỉ thích mặc đồ đẹp. Hai kẻ lừa đảo đến hoàng cung dụ dỗ làm bộ đồ từ một loại vải kỳ lạ: kẻ ngu đần hoặc làm việc kém cỏi sẽ không thể nhìn thấy vải.
  2. Nhà vua cử các quan đại thần đi kiểm tra tiến độ dệt vải. Dù không ai thấy sợi chỉ nào trên khung dệt trống rỗng, họ đều dối lòng ca ngợi vải đẹp vì sợ bị đánh giá là bất tài.
  3. Cuối cùng bộ quần áo "hoàn thành". Hai kẻ lừa đảo giả vờ mặc đồ cho vua. Vua đứng trước gương tự ngắm nghĩa và tấm tắc khen ngợi bộ đồ tàng hình.
  4. Vua cởi trần đi diễu hành ngoài phố dưới sự tung hô của dân chúng sợ hãi. Cho đến khi một đứa trẻ ngây thơ hét lên: "Kìa, Hoàng đế không mặc quần áo gì cả!". Cả đám đông bừng tỉnh hùa theo, khiến nhà vua vô cùng xấu hổ nhưng vẫn phải tiếp tục đi hết buổi lễ.
- Lời thoại và tạo ảnh:
  + Sự mỉa mai châm biếm sâu cay thói giả dối, nịnh hót của triều đình.
  + Cảnh tượng khôi hài: Hoàng đế mặc đồ tàng hình (thực chất chỉ mặc đồ lót) kiêu hãnh đi trước đám đông cờ hoa rực rỡ.
"""
    },
    "nang_tien_ca": {
        "canonical_title": "Nàng tiên cá",
        "keywords": ["nang tien ca", "ariel", "bot bien", "giong hat", "phu thuy bien", "hoang tu", "doi chan"],
        "context": """
- Bối cảnh: Cung điện nguy nga dưới đáy đại dương và vương quốc đất liền của hoàng tử.
- Nhân vật chính:
  + Nàng tiên cá út (Ariel): Có giọng hát trong trẻo ngọt ngào nhất đại dương, khao khát có được linh hồn con người và tình yêu đích thực.
  + Hoàng tử: Chàng trai quý tộc được nàng tiên cá giải cứu sau tai nạn đắm tàu.
  + Phù thủy đại dương: Gian ác, độc địa, lấy giọng hát của nàng đổi lấy đôi chân con người.
- Cốt truyện truyền thống:
  1. Nàng tiên cá cứu hoàng tử khỏi vụ đắm tàu, mang chàng lên bãi cát rồi ẩn mình. Hoàng tử tỉnh dậy tưởng người cứu mình là một cô gái khác.
  2. Yêu hoàng tử sâu sắc, nàng tiên cá tìm đến phù thủy xin làm người. Phù thủy lấy đi giọng hát tuyệt trần của nàng để đổi lấy đôi chân. Bà ta cảnh báo: Mỗi bước đi trên đất liền sẽ đau như bước trên dao nhọn, và nếu hoàng tử cưới người khác, nàng sẽ hóa thành bọt biển vào bình minh hôm sau.
  3. Nàng câm lặng bên cạnh hoàng tử nhưng không thể thổ lộ sự thật. Hoàng tử tuyên bố đính hôn với công chúa nước láng giềng vì nghĩ đó là người cứu mình.
  4. Đêm trước ngày cưới, các chị gái nàng mang đến một con dao đổi bằng mái tóc dài của họ, bảo nàng đâm vào tim hoàng tử để dòng máu chảy xuống chân sẽ giúp nàng hóa lại thành tiên cá về với biển sâu.
  5. Nhìn hoàng tử ngủ say bên vợ mới cưới, nàng tiên cá không nỡ ra tay, vứt con dao xuống sóng nước rồi gieo mình xuống biển biến thành bọt biển lấp lánh dưới ánh bình minh (sau đó được các con gái không trung đón lấy).
- Lời thoại và tạo ảnh:
  + Sự u buồn, hy sinh thầm lặng của tình yêu vô điều kiện.
  + Hình ảnh nàng tiên cá đứng trên mỏm đá sóng vỗ ngắm nhìn hoàng cung rực sáng ánh đèn khiêu vũ, và cảnh nàng hóa thành bọt biển lấp lánh dưới nắng sớm.
"""
    },
    "aladin_va_cay_den_than": {
        "canonical_title": "Aladin và cây đèn thần",
        "keywords": ["aladin", "cay den than", "than den", "tham bay", "phu thuy", "jasmine"],
        "context": """
- Bối cảnh: Thành phố cổ xứ Ba Tư xa xôi đầy cát vàng sa mạc.
- Nhân vật chính:
  + Aladin: Chàng trai nghèo khổ, lanh lợi, dũng cảm và giàu lòng nhân ái.
  + Thần Đèn: Vị thần quyền năng khổng lồ màu xanh lam, cư ngụ trong cây đèn dầu đồng cổ, thực hiện mọi điều ước của người sở hữu đèn.
  + Phù thủy độc ác: Lão phù thủy xứ Maghreb xảo quyệt muốn chiếm đoạt cây đèn thần.
  + Công chúa Jasmine: Con gái quốc vương xinh đẹp, cá tính.
- Cốt truyện truyền thống:
  1. Lão phù thủy lừa Aladin vào hang báu vật bí mật để lấy cây đèn dầu cũ. Aladin phát hiện âm mưu của lão nên giữ lại đèn, bị lão khóa kín trong hang tối.
  2. Nhờ chiếc nhẫn thần phù thủy đưa trước đó, Aladin thoát ra ngoài. Về nhà, chàng lau chùi đèn thần, vị thần đèn khổng lồ xuất hiện ban cho chàng của cải, lâu đài tráng lệ để hỏi cưới công chúa Jasmine.
  3. Lão phù thủy quay lại dùng kế đổi "đèn cũ lấy đèn mới" lừa công chúa lấy mất cây đèn thần, biến mất cùng lâu đài và công chúa sang xứ khác.
  4. Aladin dùng nhẫn thần tìm đường đến lâu đài, mưu trí phối hợp cùng Jasmine đầu độc phù thủy lấy lại đèn thần, đưa lâu đài trở về sống hạnh phúc.
- Lời thoại và tạo ảnh:
  + Lời thoại oai vệ của Thần Đèn khi hiện ra: "Tôi là thần đèn, chủ nhân muốn ước điều gì?".
  + Cảnh Aladin bay trên tấm thảm thần kỳ giữa trời đêm đầy sao lấp lánh, ngắm nhìn kinh thành cổ kính bên dưới.
"""
    },
    "ali_baba_va_bon_muoi_ten_cuop": {
        "canonical_title": "Ali Baba và bốn mươi tên cướp",
        "keywords": ["ali baba", "bon muoi ten cuop", "vung oi mo ra", "chum dau", "morgiana"],
        "context": """
- Bối cảnh: Đất nước Ba Tư cổ đại đầy bí ẩn.
- Nhân vật chính:
  + Ali Baba: Tiều phu nghèo khổ, thật thà, tốt bụng.
  + Cassim: Người anh trai giàu có nhưng tham lam vô độ của Ali Baba.
  + Morgiana: Cô hầu gái trung thành, cực kỳ thông minh, dũng cảm và nhanh trí.
  + Bọn cướp: Băng cướp 40 người tàn ác, sở hữu hang báu bí mật trong lòng núi đá.
- Cốt truyện truyền thống:
  1. Ali Baba đốn củi trong rừng vô tình chứng kiến băng cướp mở cửa hang đá bằng câu thần chú: "Vừng ơi, mở ra!" (Open Sesame). Chờ bọn cướp đi, anh đọc thần chú vào hang lấy một ít vàng về nuôi gia đình.
  2. Người anh Cassim phát hiện, bắt Ali Baba chỉ đường. Cassim vào hang lấy đầy bao vàng nhưng do quá tham lam phấn khích nên quên mất câu thần chú mở cửa hang để ra ngoài ("Lúa mạch ơi mở ra!", "Yến mạch ơi mở ra!"). Bọn cướp trở về phát hiện và giết chết Cassim.
  3. Bọn cướp lần theo dấu vết tìm đến nhà Ali Baba đòi trả thù. Tên trùm cướp giả dạng thương nhân buôn dầu đem theo 40 chiếc chum lớn chứa cướp trốn bên trong để mai phục hành thích.
  4. Morgiana thông minh phát hiện tiếng thì thầm trong chum dầu, nấu dầu sôi dội vào từng chum tiêu diệt bọn cướp. Sau đó, cô biểu diễn điệu múa kiếm đâm chết tên trùm cướp giải nguy cho Ali Baba. Ali Baba gả con trai cho Morgiana và chia sẻ kho báu hang đá.
- Lời thoại và tạo ảnh:
  + Câu thần chú vang dội: "Vừng ơi, mở ra!" và "Vừng ơi, đóng lại!".
  + Hình ảnh vách đá dựng đứng nứt đôi lộ ra hang vàng bạc rực rỡ lấp lánh ánh kim.
"""
    },
    "sinbad_nguoi_di_bien": {
        "canonical_title": "Sinbad người đi biển",
        "keywords": ["sinbad", "chim roc", "nguoi khong lo", "di bien", "phieu luu", "bao tap"],
        "context": """
- Bối cảnh: Đại dương bao la với những hòn đảo kỳ bí và quái thú huyền thoại vùng Trung Đông cổ đại.
- Nhân vật chính:
  + Sinbad: Chàng thủy thủ dũng cảm, kiên cường, khao khát thám hiểm đại dương, luôn mưu trí vượt qua cái chết.
  + Chim Roc: Con chim khổng lồ huyền thoại chuyên cắp voi ăn thịt.
  + Người khổng lồ một mắt: Ác thú chuyên bắt ăn thịt các thủy thủ lạc vào đảo.
- Cốt truyện truyền thống:
  - Sinbad trải qua 7 chuyến phiêu lưu mạo hiểm trên biển:
    1. Đỗ thuyền lên một hòn đảo nhỏ hóa ra là lưng một con cá voi khổng lồ đang ngủ sâu. Cá voi thức giấc lặn xuống biển sâu khiến thuyền đắm.
    2. Bị bỏ lại trên đảo hoang, Sinbad dùng khăn buộc mình vào chân chim khổng lồ Roc để bay thoát khỏi đảo đến thung lũng kim cương đầy rắn khổng lồ.
    3. Đối đầu người khổng lồ một mắt độc ác bằng cách dùng sắt nung đỏ đâm mù mắt hắn rồi chạy trốn bằng bè gỗ tự chế.
    4. Trải qua các vùng đất kỳ lạ, học hỏi các kỹ nghệ thủ công, tích lũy vô số ngọc ngà châu báu mang về quê hương Bagdad giàu có.
- Lời thoại và tạo ảnh:
  + Sự oai hùng, khí chất của Sinbad trước sóng gió biển khơi và quái thú khổng lồ.
  + Cảnh tượng chim Roc khổng lồ che rợp cả bầu trời, móng vuốt sắc nhọn cắp chặt con mồi bay vút qua núi đá.
"""
    },
    "con_cao_va_chum_nho": {
        "canonical_title": "Con cáo và chùm nho",
        "keywords": ["con cao va chum nho", "nho con xanh", "ngu ngon", "aesop", "kieu ngao"],
        "context": """
- Bối cảnh: Khu vườn đầy hoa trái mùa thu mát mẻ.
- Nhân vật chính:
  + Con Cáo: Đang đói bụng, tự cao, tinh ranh nhưng dễ nản lòng và hay tự dối mình.
- Cốt truyện truyền thống:
  1. Con cáo đi dạo trong vườn nho, phát hiện những chùm nho chín mọng, căng tròn mọng nước treo lủng lẳng trên cành cao.
  2. Thèm thuồng hương vị ngọt ngào, Cáo lùi lại lấy đà rồi nhảy lên định hái nho nhưng không tới được.
  3. Cáo cố gắng nhảy lại nhiều lần, đổi nhiều tư thế nhưng chùm nho vẫn quá cao so với tầm với của chú.
  4. Mệt lả người, kiệt sức và thất vọng, Cáo bỏ đi với vẻ mặt khinh khỉnh, lẩm bẩm tự nhủ: "Nho còn xanh lắm, chắc chắn là chua lắm, chả báu gì!".
- Lời thoại và tạo ảnh:
  + Lời thoại mang tính châm biếm sâu sắc thói tự biện hộ của con người khi thất bại. Câu nói kinh điển: "Nho còn xanh lắm!".
  + Hình ảnh con cáo đỏ kiễng chân, vươn mõm nhảy cao hướng về phía chùm nho tím mọng lấp lánh nắng thu phía trên giàn lá xanh.
"""
    },
    "cho_soi_va_cuu_non": {
        "canonical_title": "Chó sói và cừu non",
        "keywords": ["cho soi va cuu non", "nguy bien", "dong suoi", "doc ac", "an thit", "ngu ngon"],
        "context": """
- Bối cảnh: Dòng suối trong lành mát rượi ven bìa rừng.
- Nhân vật chính:
  + Chó Sói: Hung dữ, độc ác, luôn tìm cách ngụy biện vô lý để hợp thức hóa hành vi tàn ác của mình.
  + Cừu non: Ngây thơ, nhút nhát, hiền lành, cố gắng dùng lý lẽ lẽ phải để tự bảo vệ mình.
- Cốt truyện truyền thống:
  1. Cừu non đang uống nước ở hạ nguồn suối. Sói ở thượng nguồn thấy vậy chạy đến quát mắng cừu làm đục nước suối của nó uống.
  2. Cừu non giải thích lễ phép nước chảy từ trên xuống dưới sao con làm đục nước phía trên của ông được.
  3. Sói thẹn quá hóa giận buộc tội cừu nói xấu sói năm ngoái, cừu bảo năm ngoái mình chưa ra đời.
  4. Sói nói tiếp: "Không phải mày thì là bố mày hoặc dòng họ nhà mày", rồi vồ lấy cừu ăn thịt không cần nghe giải thích thêm.
- Lời thoại và tạo ảnh:
  + Lời thoại thể hiện sự ngang ngược vô lý của Sói và sự bất lực, sợ hãi của Cừu non yếu ớt.
  + Hình ảnh chú cừu nhỏ trắng muốt co rúm bên bờ nước, đối diện với con sói xám to lớn nhe nanh vuốt hung hãn.
"""
    },
    "cau_be_chan_cuu": {
        "canonical_title": "Cậu bé chăn cừu",
        "keywords": ["cau be chan cuu", "noi doi", "soi xuat hien", "gạt dan lang", "hau qua", "dan cuu"],
        "context": """
- Bối cảnh: Cánh đồng cỏ xanh mướt trải dài gần bìa rừng.
- Nhân vật chính:
  + Cậu bé chăn cừu: Thích nghịch ngợm, đùa cợt vô ý thức bằng những lời nói dối để giải sầu.
  + Người dân làng: Chăm chỉ, thật thà, tốt bụng, luôn sẵn lòng giúp đỡ người khác.
  + Con sói: Kẻ săn mồi hoang dã rình rập đàn cừu.
- Cốt truyện truyền thống:
  1. Cậu bé chăn cừu thấy buồn chán liền nghĩ ra trò đùa tinh nghịch. Cậu chạy lên đồi hét lớn: "Sói! Có sói cứu tôi với!".
  2. Người dân làng đang làm việc nghe tiếng kêu cứu liền bỏ hết cuốc xẻng chạy ra giúp đỡ, nhưng ra đến nơi chỉ thấy cậu bé cười ngặt nghẽo chế giễu họ vì đã tin lời nói dối của cậu.
  3. Mấy ngày sau, cậu bé lặp lại trò đùa tai hại này một lần nữa và người dân vẫn chạy ra cứu, rồi lại bị cậu lừa cười cợt.
  4. Một ngày nọ, con sói thật sự xuất hiện từ bìa rừng nhảy vào tấn công đàn cừu. Cậu bé hoảng sợ tột độ gào thét cầu cứu thảm thiết: "Sói! Sói thật đấy! Cứu cháu với!".
  5. Người dân làng nghe tiếng hét nhưng nghĩ cậu bé lại bày trò nói dối như những lần trước nên không ai chạy ra nữa. Kết cục sói ăn thịt mất sạch đàn cừu của cậu bé.
- Lời thoại và tạo ảnh:
  + Bài học đạo đức sâu sắc: Kẻ nói dối sẽ không được tin tưởng ngay cả khi họ nói thật.
  + Cảnh cậu bé đứng khóc lóc bất lực nhìn đàn cừu bị sói đuổi bắt tán loạn trên đồi cỏ vắng bóng người giúp đỡ.
"""
    },
    "pinocchio": {
        "canonical_title": "Pinocchio (Chú bé người gỗ)",
        "keywords": ["pinocchio", "nguoi go", "mui dai ra", "noi doi", "geppetto", "co tien xanh", "ca voi"],
        "context": """
- Bối cảnh: Ngôi nhà mộc cũ kỹ ấm áp và những vùng đất phiêu lưu giả tưởng đầy cám dỗ.
- Nhân vật chính:
  + Pinocchio: Chú bé người gỗ bướng bỉnh, ham chơi, dễ bị dụ dỗ nhưng mang trái tim nhân hậu, muốn trở thành con người thật sự. Mỗi lần nói dối, mũi của chú sẽ tự dài ra.
  + Geppetto: Bác thợ mộc già nghèo khổ, coi Pinocchio như con đẻ của mình, hết lòng yêu thương chú.
  + Cô Tiên Xanh: Bà tiên nhân từ ban sự sống cho Pinocchio và uốn nắn chú sống trung thực, dũng cảm.
  + Dế Jiminy: Người bạn nhỏ trung thành, đóng vai trò là "lương tâm" nhắc nhở Pinocchio làm việc đúng đắn.
- Cốt truyện truyền thống:
  1. Geppetto đẽo một khúc gỗ thành con rối Pinocchio. Cô tiên xanh hóa phép cho chú cử động và nói chuyện được, hứa nếu chú chứng minh được sự ngoan ngoãn, trung thực thì sẽ biến chú thành người thật.
  2. Pinocchio đi học nhưng liên tục bị dụ dỗ bỏ học đi xem xiếc rối, bị cáo và mèo lừa tiền, bị biến thành lừa ở đảo Đồ chơi do thói ham chơi lười biếng. Cứ mỗi lần nói dối cô tiên, chiếc mũi gỗ của chú lại dài ngoằng ra đầy xấu hổ.
  3. Bác Geppetto đi tìm Pinocchio trên biển rộng, bị một con cá voi khổng lồ nuốt chửng vào bụng.
  4. Pinocchio hối cải, dũng cảm lao ra biển khơi tìm cha, lọt vào bụng cá voi gặp lại Geppetto. Hai cha con nhóm lửa tạo khói khiến cá voi hắt hơi đẩy họ ra ngoài thoát nạn.
  5. Cảm động trước sự hiếu thảo, dũng cảm cứu cha của Pinocchio, cô tiên xanh hóa phép biến chú bé người gỗ thành một cậu bé bằng xương bằng thịt khỏe mạnh thực sự.
- Lời thoại và tạo ảnh:
  + Lời thoại ngây ngô của Pinocchio và chiếc mũi gỗ tự động dài ra cản trở chú mỗi lần nói dối.
  + Hình ảnh ấm áp hai cha con ôm lấy nhau trong khoang bụng tối tăm của con cá voi khổng lồ bên ánh lửa bập bùng.
"""
    },
    "peter_pan": {
        "canonical_title": "Peter Pan",
        "keywords": ["peter pan", "neverland", "tinker bell", "moc sat", "thuyen truong hook", "wendy", "bay bay"],
        "context": """
- Bối cảnh: Đảo Neverland (Xứ sở Không bao giờ) thần thoại đầy phép màu kì ảo.
- Nhân vật chính:
  + Peter Pan: Cậu bé không bao giờ lớn, mặc áo lá xanh, biết bay, sống ở đảo Neverland cùng các cậu bé đi lạc.
  + Wendy Darling: Cô bé Luân Đôn hiền dịu, đóng vai trò người mẹ chăm sóc các cậu bé ở Neverland.
  + Tiên Tinker Bell: Cô tiên nhỏ bé lấp lánh, hay ghen tị nhưng trung thành, giúp Peter Pan bay bằng bụi tiên.
  + Thuyền trưởng Hook (Móc Sắt): Kẻ thù truyền kiếp của Peter Pan, chỉ huy băng cướp biển độc ác, cánh tay bị cá sấu cắn mất thế bằng chiếc móc sắt.
- Cốt truyện truyền thống:
  1. Peter Pan bay đến cửa sổ phòng ngủ nhà Wendy ở Luân Đôn, tìm lại chiếc bóng bị mất của mình. Cậu rắc bụi tiên giúp Wendy và các em bay đến đảo Neverland.
  2. Tại Neverland, Wendy kể chuyện cho các cậu bé đi lạc nghe. Họ cùng Peter Pan trải qua những trận chiến vui nhộn chống lại băng cướp biển của Thuyền trưởng Hook.
  3. Hook bắt cóc Wendy và bọn trẻ lên tàu cướp biển đòi xử tử. Peter Pan dũng cảm đột nhập tàu chiến đấu kịch liệt với Hook, đẩy lão rơi xuống biển làm mồi cho con cá sấu tích tắc đeo bám lão bấy lâu.
  4. Wendy và các em nhớ nhà, quyết định bay trở về Luân Đôn để lớn lên bên cha mẹ. Peter Pan từ chối đi cùng vì muốn mãi mãi giữ tâm hồn của một đứa trẻ bay nhảy tự do tại Neverland.
- Lời thoại và tạo ảnh:
  + Cảnh Wendy và các em bay qua bầu trời đêm Luân Đôn dưới ánh trăng tròn hướng về phía ngôi sao sáng thứ hai bên phải.
  + Lời thoại vui tươi, thách thức tinh nghịch của Peter Pan đối đầu với Hook giận dữ cầm kiếm.
"""
    },
    "phu_thuy_xu_oz": {
        "canonical_title": "Phù thủy xứ Oz",
        "keywords": ["phu thuy xu oz", "dorothy", "nguoi thiec", "bu nhin rom", "su tu", "thanh pho ngoc luc bao", "lốc xoáy"],
        "context": """
- Bối cảnh: Xứ Oz kỳ diệu rực rỡ sắc màu được nối liền bằng con đường gạch vàng lấp lánh.
- Nhân vật chính:
  + Dorothy: Cô bé nhỏ nhắn người Kansas bị cơn lốc xoáy cuốn bay đến xứ Oz cùng chú chó nhỏ Toto.
  + Bù nhìn rơm: Mong muốn xin phù thủy xứ Oz một bộ não để suy nghĩ thông minh.
  + Người thiếc: Mong muốn xin một trái tim để biết yêu thương và cảm thông.
  + Sư tử nhút nhát: Mong muốn xin lòng dũng cảm để xứng đáng làm chúa tể muông thú.
  + Phù thủy xứ Oz: Người đàn ông bình thường dùng máy móc ảo thuật giả dạng vị thần quyền lực ở thành phố Ngọc Lục Bảo.
- Cốt truyện truyền thống:
  1. Dorothy bị lốc xoáy cuốn bay đến xứ Oz. Để tìm đường về nhà ở Kansas, cô được hướng dẫn đi men theo con đường gạch vàng tìm đến Phù thủy xứ Oz ở thành phố Ngọc Lục Bảo cầu xin giúp đỡ.
  2. Dọc đường, cô kết bạn và đồng hành cùng Bù nhìn rơm, Người thiếc và Sư tử nhút nhát đang có những ước mong của riêng mình.
  3. Nhóm bạn trải qua nhiều nguy hiểm, tiêu diệt được Phù thủy phương Tây độc ác để chứng minh thực lực.
  4. Khi gặp Phù thủy xứ Oz, họ phát hiện vị phù thủy thực chất chỉ là một người bình thường bị lạc khinh khí cầu đến đây. Nhưng ông đã giúp họ nhận ra: Bù nhìn vốn đã thông minh qua các kế hoạch cứu nguy, Người thiếc vốn đã nhân hậu, Sư tử vốn đã rất dũng cảm trên hành trình hiểm nguy.
  5. Dorothy gõ gót đôi giày bạc thần kỳ ba lần, nói lời tạm biệt bạn bè và trở về nhà an toàn bên người dì Em ở quê nhà Kansas.
- Lời thoại và tạo ảnh:
  + Con đường gạch vàng uốn lượn rực rỡ dẫn đến thành phố Ngọc Lục Bảo nguy nga tráng lệ màu xanh ngọc.
  + Tình bạn gắn kết ấm áp của nhóm bạn kì lạ nâng đỡ nhau vượt qua hoạn nạn.
"""
    },
    "ba_chu_heo_con": {
        "canonical_title": "Ba chú heo con",
        "keywords": ["ba chu heo con", "xay nha gach", "nha go", "nha rom", "cho soi thoi bay"],
        "context": """
- Bối cảnh: Khu rừng xanh bình yên và những ngôi nhà nhỏ tự xây của ba chú heo.
- Nhân vật chính:
  + Ba chú heo con: Heo cả (lười biếng, ham chơi), Heo thứ (chăm chỉ vừa phải) và Heo út (chăm chỉ, khôn ngoan, biết nhìn xa trông rộng).
  + Con sói hung ác: Luôn rình rập rắp tâm thổi bay nhà để ăn thịt các chú heo.
- Cốt truyện truyền thống:
  1. Ba chú heo con ra ở riêng tự xây nhà. Heo cả làm nhà bằng rơm sơ sài cho nhanh để có thời gian đi chơi. Heo thứ làm nhà bằng củi gỗ lỏng lẻo. Heo út miệt mài gánh gạch xếp vôi xây ngôi nhà gạch vững chắc kiên cố bất chấp hai anh trêu cười.
  2. Con sói đói mò đến nhà heo cả bằng rơm, hít một hơi thật sâu rồi thổi bay ngôi nhà rơm. Heo cả hốt hoảng chạy sang nhà heo thứ.
  3. Sói tìm đến nhà gỗ của heo thứ, lại lấy hơi thổi bay sập cả nhà gỗ. Hai chú heo hoảng sợ chạy thục mạng sang nhà gạch của heo út.
  4. Sói đến nhà heo út dùng hết sức thổi cật lực nhưng ngôi nhà gạch vững chãi không hề lung lay.
  5. Tức giận, sói tìm cách leo qua ống khói để vào nhà. Heo út đoán trước mưu đồ liền đốt lửa đặt sẵn một nồi nước sôi khổng lồ dưới bếp lò. Sói trượt xuống rơi thẳng vào nồi nước sôi chết nóng. Ba chú heo con sống hạnh phúc, an toàn bên nhau.
- Lời thoại và tạo ảnh:
  + Bài học giáo dục sâu sắc về lòng kiên trì, chăm chỉ chịu khó và chuẩn bị kỹ lưỡng trước hiểm nguy.
  + Cảnh sói lấy hơi phồng má thổi bay nhà rơm, nhà gỗ và cảnh căn nhà gạch màu đỏ vững chãi sưởi ấm trong đêm rừng.
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
