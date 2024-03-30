from collections import deque

import requests
from bs4 import BeautifulSoup

from configurations.orient_db_config import OrientDBConfig

# Khai báo danh sách tập seeds chứa các URLs ban đầu
seeds = [
    "https://vnexpress.net",
    "https://dantri.com.vn",
    "https://vietnamnet.vn"
]

# Danh sách các URL đã truy cập
visited = []

# Chiều sâu duyệt tối đa của mỗi URL
MAX_DEPTH = 3


def fetch_by_bfs():
    for url in seeds:
        db_client = OrientDBConfig()
        visited.append(url)
        queue = deque([[url, "", 0]])

        while queue:
            # Lấy thông tin về: URL gốc (base), URL đang duyệt và chiều sâu (depth) ra khỏi queue
            base, path, depth = queue.popleft()

            # Kiểm tra xem chiều sâu hiện tại đã vượt quá [MAX_DEPTH] hay chưa
            if depth < MAX_DEPTH:
                try:
                    # Tải nội dung ở định dạng  của webpage hiện tại đang đứng
                    # Ở bước này chúng ta có thể lưu nội dung của website vào CSDL để phục vụ cho việc chỉ mục sau này
                    html_content = BeautifulSoup(requests.get(base + path).text, "html.parser")

                    website_properties = f"url = '{base}'"
                    db_client.create_node('Website', website_properties)

                    # Lấy toàn bộ các thẻ  là các thẻ chứa hyper-links (href) của webpage đang đứng
                    a_tags = html_content.find_all("a")

                    # Duyệt qua từng hyper-links của webpage đang có
                    for link in a_tags:

                        # Lấy ra đường dẫn liên kết trong attribute [href]
                        href = link.get("href")

                        # Kiểm tra xem đường dẫn này chúng ta đã duyệt qua hay chưa? thông qua đối chiếu trong danh sách [visited]
                        if href not in visited:

                            # Nếu chưa duyệt qua tiến hành bỏ hyper-link này vào [visited]
                            visited.append(href)

                            # print('Chiều sâu (depth) hiện tại: [{}/{}] - duyệt URL: [{}], '.format(depth, MAX_DEPTH,
                            #                                                                 href))

                            # Kiểm tra xem đường dẫn này có phải là một đường dẫn hợp lệ - bắt đầu bằng http, ví dụ: https://vnexpress.net
                            if href.startswith("http"):
                                # Nếu hợp lệ - tiến hành bỏ hyper-link đang xét (href) vào [queue], và href sẽ là [base] mới, tăng chiều sâu [depth] lên 1
                                queue.append([href, "", depth + 1])

                                linked_website_properties = f"url = '{href}'"
                                db_client.create_node('Website', linked_website_properties)

                                create_url_neighbor_query = (f"create edge References from "
                                                             f"(select from Website where url = '{base}') "
                                                             f"to(select from Website where url = '{href}')")

                                db_client.command(create_url_neighbor_query)

                            else:
                                # Nếu không hợp lệ - bỏ lại hyper-link cha [base] và (href) đang duyệt lại vào [queue] như cũ, tăng chiều sâu [depth] lên 1
                                queue.append([base, href, depth + 1])

                except:
                    pass
