# PR #19 (WhatsApp Ref v2.1): gói chuẩn bị Phase 10 (06/11/2026)

**Trạng thái gói này:** chỉ chuẩn bị. Chưa mở web server, chưa thao tác WhatsApp, chưa đổi code hay chính sách, chưa push, merge hay deploy.

**Baseline đọc lại lúc 17:10, 06/11:**
- PR #19 (Draft) ở `6212acd`, `main` ở `81c32fe`, đúng 3 file.
- `assets/oai-conversions.js` có hash `153e428a…`.
- Trang thử dùng chính file JS này (hash `153e428a`, đã đối chiếu).

---

## A. Thử trên điện thoại (16 trường hợp): CHỜ ANH DUYỆT
Server chạy trên máy Mac, **anh tự chạy**. Em không mở cổng và không sửa firewall.

```
mkdir -p ~/mlo-ref-test
cp ~/Downloads/whatsapp-ref-device-test.html ~/mlo-ref-test/index.html
cd ~/mlo-ref-test
ipconfig getifaddr en0        # IP của Mac trong Wi-Fi, ví dụ 192.168.1.100
python3 -m http.server 8000 --bind "$(ipconfig getifaddr en0)"
```

- **Phạm vi mạng:** chỉ thiết bị trong cùng Wi-Fi của cửa hàng. Server chỉ phục vụ thư mục `~/mlo-ref-test` (một file), không có Pixel, không có dữ liệu khách.
  - Nếu macOS hỏi "cho phép Python nhận kết nối đến", anh tự quyết. Chọn Từ chối thì điện thoại không vào được và các ô này giữ NOT VERIFIED.
- **Tắt server:** bấm `Ctrl+C` trong cửa sổ Terminal đó. Muốn dọn sạch thì xoá thư mục `~/mlo-ref-test`.
- **Trên điện thoại:**
  - Trường hợp C: mở `http://<IP>:8000/index.html?oppref=FAKE-TEST`, bấm "Giả lập click quảng cáo".
  - Trường hợp R: mở tab mới tới `http://<IP>:8000/index.html` (không có `?oppref`).

Cookie dùng trong thử nghiệm là cookie giả, do trang thử đặt trên địa chỉ IP này. Nó không phải cookie của OpenAI.

| Ca | Thao tác | Mong đợi | iPhone Safari | Android Chrome |
|---|---|---|---|---|
| T1 | Xoá hết → link thường | Không có Ref | | |
| T2 | Xoá hết → link kính râm | Không có Ref, câu gốc còn dấu cách cuối | | |
| T3 | Có `?oppref` + "Giả lập click" → link thường | Đúng `Ref: C-XXXXXX` | | |
| T4 | Như T3 → link kính râm | Dòng Ref ở đầu, một dòng trống, rồi câu gốc | | |
| T5 | Tab mới, không có `?oppref` → link thường | `Ref: R-` với cùng 6 ký tự | | |
| T6 | "Cho mã hết hạn" rồi bấm; sau đó "Xoá cookie" rồi bấm | Hết hạn: mã mới. Xoá cookie: không có Ref, ô "Mã đã lưu" trống | | |
| T7 | Bấm một link 3 lần | Cùng mã, chỉ một dòng Ref | | |
| T8 | Link tiếng Việt và link emoji | Hiển thị đúng | | |

Sau mỗi thiết bị, anh bấm "Chép kết quả" và gửi em. Ô nào không làm được thì giữ NOT VERIFIED.

## B. WhatsApp app và WhatsApp Web (9 trường hợp): ANH TỰ LÀM
- Link trong trang thử **không có số người nhận**. WhatsApp sẽ hỏi gửi cho ai: **chọn chat "Bạn" / "Message yourself"** (chat với chính số của anh), hoặc dùng một tài khoản WhatsApp thử riêng.
- **Không mở hay đọc hội thoại của khách. Không bấm gửi.** Xem xong khung soạn tin thì xoá nội dung và thoát.
- WhatsApp Web: nếu tài khoản của shop đang đăng nhập, danh sách chat của khách sẽ hiện ra. Nên dùng tài khoản thử. Nếu không có tài khoản thử, ghi NOT VERIFIED.

| Ca | iPhone app | Android app | WhatsApp Web |
|---|---|---|---|
| W1: không có Ref, link kính râm → câu gốc giữ nguyên | | | |
| W2: Ref C, link kính râm → dòng Ref ở đầu, dòng trống, câu gốc; con trỏ ở cuối tin | | | |
| W3: Ref C, link thường → khung soạn tin chỉ có `Ref: C-XXXXXX` | | | |

---

## C. Bản tóm tắt cho chuyên gia pháp lý (LEGAL REVIEW REQUIRED, em không kết luận việc tuân thủ)
| # | Nội dung | Thực tế (đã kiểm bằng code và test) |
|---|---|---|
| 1 | `__oppref` | Cookie first-party do OpenAI Pixel đặt từ tham số URL khi khách bấm quảng cáo trên ChatGPT. Mục đích: đo hiệu quả quảng cáo. Lưu 30 ngày, tính lại mỗi lần có mã mới. Pixel tự coi là đã có đồng ý nếu site không gọi `oaiq("consent", false)` |
| 2 | `mlo_wa_ref` (localStorage) | `{c: mã 6 ký tự ngẫu nhiên, e: hạn dùng}`. Chỉ tạo khi có `__oppref` và khách bấm WhatsApp. Mục đích: cửa hàng tự thống kê lượt hỏi và đơn hàng đến từ quảng cáo ChatGPT. Lưu 30 ngày kể từ khi tạo, tính lại mỗi lần vào từ quảng cáo. Mã hết hạn bị xoá hoặc thay ở lần bấm WhatsApp kế tiếp |
| 3 | `mlo_ad_visit` (sessionStorage) | Giá trị `"1"`. Ghi khi URL có `oppref`, kể cả khi không có cookie. Mất khi đóng tab |
| 4 | Thời điểm tạo | `__oppref`: sau khi Pixel tải xong (sau sự kiện load). `mlo_ad_visit`: khi trang tải. `mlo_wa_ref`: lần đầu bấm WhatsApp lúc đang có cookie |
| 5 | Điều kiện C/R | Có `__oppref` và tab có `mlo_ad_visit` thì là C, chỉ có cookie thì là R. Không có cookie thì không gắn Ref |
| 6 | Dữ liệu gửi tới WhatsApp (Meta) | Mã Ref nằm trong đường dẫn wa.me, nên Meta nhận được ngay khi mở link, kể cả khi khách không gửi tin. Nếu khách gửi, mã đến tài khoản WhatsApp của shop kèm số điện thoại và hồ sơ WhatsApp của khách. Không gửi giá trị `oppref` |
| 7 | Liên kết với đơn hàng | Nhân viên ghi mã cạnh đơn hàng. Từ đó mã liên kết được với một khách cụ thể (qua cuộc chat và đơn hàng) |
| 8 | Cơ chế đồng ý | **Không có** banner hay cơ chế đồng ý/từ chối. Chính sách bảo mật mô tả các mục trên nhưng không xin đồng ý |
| 9 | Quyền của khách | Khách có thể xoá dòng Ref trước khi gửi tin, và xoá cookie/storage trong trình duyệt. Chưa có quy trình cửa hàng tiếp nhận yêu cầu xoá hoặc truy cập dữ liệu Ref trong sổ bán hàng |

**Câu hỏi cho chuyên gia** (các ý trích nguồn chỉ để tham khảo, cần chuyên gia xác nhận):
1. Mã Ref sau khi ghép với đơn hàng và số WhatsApp có là dữ liệu cá nhân theo Luật 91/2025/QH15 không? Cơ sở pháp lý nào phù hợp cho từng hoạt động (lưu trên thiết bị, ghi vào sổ bán hàng)?
2. Theo tóm tắt của EY về Nghị định 356/2025/NĐ-CP:
   - **Dữ liệu theo dõi hành vi** và dữ liệu sử dụng dịch vụ trực tuyến được xếp vào **dữ liệu cá nhân nhạy cảm**. Việc đo "khách đến từ quảng cáo" có thuộc nhóm này không?
   - Đồng ý phải rõ ràng, kiểm chứng được và được lưu lại; cấm đặt sẵn lựa chọn đồng ý. Website hiện chưa có cơ chế nào như vậy.
   - Hộ kinh doanh và doanh nghiệp siêu nhỏ được miễn một số nghĩa vụ; doanh nghiệp nhỏ được ân hạn 5 năm. Mạnh Long thuộc loại nào? Phần miễn trừ có áp dụng khi xử lý dữ liệu nhạy cảm không?
3. Có phải xin đồng ý **trước** khi lưu `mlo_wa_ref`, `mlo_ad_visit` và cookie của Pixel không?
4. GDPR / ePrivacy / UK PECR có áp dụng không, khi cửa hàng ở Hà Nội nhưng có trang tiếng Anh hướng tới khách du lịch và người nước ngoài?
5. Thông báo hiện tại về việc Meta nhận mã qua link WhatsApp đã đủ minh bạch chưa?
6. Việc mã Ref đi tới Meta (máy chủ ở nước ngoài) có phải là chuyển dữ liệu ra nước ngoài, cần đánh giá tác động (CTIA) không? Thời hạn lưu và xoá dữ liệu bắt buộc là bao lâu?

---

## D. Lưu mã Ref trong sổ bán hàng: phương án tối thiểu (ANH QUYẾT)
**Hai thời hạn khác nhau, không được nhầm:**
- Cookie `__oppref` và mã `mlo_wa_ref` nằm **trên trình duyệt của khách**, khoảng 30 ngày.
- Mã Ref trong **sổ bán hàng của shop**: do anh quyết, không phụ thuộc 30 ngày trên.

**Nguyên tắc:**
- Chỉ ghi mã Ref cạnh mã đơn. Không chép số WhatsApp hay tên khách vào bảng đo lường.
- Để bảng đo lường riêng với sổ kế toán: kế toán giữ đơn hàng, bảng đo lường chỉ có mã đơn, mã Ref, số tiền và trạng thái.
- Chỉ chủ shop và một người được giao được sửa; những người khác chỉ xem, hoặc không được xem.
- Hết hạn: xoá giá trị ô Ref, giữ dòng đơn hàng. Báo cáo tháng hoặc quý đã chốt chỉ giữ số tổng, không giữ mã.

**Các mốc để anh chọn:**
| Lựa chọn | Thời hạn giữ mã Ref | Phù hợp khi |
|---|---|---|
| 1 | Tới khi chốt báo cáo tháng, cộng 1 tháng | Chỉ cần số liệu theo tháng |
| 2 | Tới khi chốt báo cáo quý | Đánh giá quảng cáo theo quý |
| 3 | 12 tháng | Cần so sánh cùng kỳ năm trước |

Thời hạn anh chọn cần được ghi vào chính sách bảo mật, và chuyên gia pháp lý cần xác nhận.

---

## E. Các mục lưu sẵn trên site (ngoài PR #19; em chỉ đọc, không sửa)
| Mục | Lưu gì | Khi nào | Thời hạn | Gửi đi đâu | Nguồn |
|---|---|---|---|---|---|
| `mlong_views_v1` (localStorage) | Số lượt xem theo bài và theo ngày, thời điểm xem gần nhất | Khi một bài mở được 5 giây; tối đa 1 lần/bài/24 giờ | Không hết hạn | Không gửi đi | `cua-hang.html:3597` |
| `ml_ff_seen` (localStorage) | Thời điểm đóng bảng chọn gọng | Khi đóng bảng | Không hết hạn | Không gửi đi | `chon-gong.js:150` |
| `ml_ff_log` (localStorage) | 50 lần dùng công cụ chọn gọng gần nhất: thời gian, ngôn ngữ, mục đích dùng, **dáng mặt**, chất liệu, 5 gọng gợi ý | Khi hoàn tất 3 bước | Không hết hạn | Bản log không gửi đi, nhưng **các câu trả lời được gửi lên GA4** qua `ff_step` và `ff_complete` | `chon-gong.js:145, 151, 112` |

**Đề xuất (PR riêng, chờ duyệt):**
- Thêm 3 mục này vào phần "Bộ nhớ trình duyệt" của chính sách bảo mật.
- Ghi rõ câu trả lời của công cụ chọn gọng được gửi tới GA4.
- Cân nhắc đặt thời hạn hoặc giới hạn kích thước cho `mlong_views_v1`.
- Hỏi chuyên gia pháp lý xem dữ liệu dáng mặt cộng client ID của GA4 có cần đồng ý không.

Nguồn:
- [EY Vietnam: Nghị định 356/2025/NĐ-CP](https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-so-356-2025-nd-cp-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-bao-ve-du-lieu-ca-nhan)
- [PwC Vietnam: Quy định mới về bảo vệ dữ liệu cá nhân](https://www.pwc.com/vn/vn/publications/legal-news-brief/20260128-new-rules-personal-data-protection.html)
- [Thư viện pháp luật: Nghị định 356/2025/NĐ-CP](https://thuvienphapluat.vn/van-ban/Quyen-dan-su/Nghi-dinh-356-2025-ND-CP-huong-dan-Luat-Bao-ve-du-lieu-ca-nhan-687428.aspx)
