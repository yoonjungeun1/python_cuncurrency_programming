import threading
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from collections import defaultdict
import threading

base_url = "https://news.ycombinator.com/news?p="
output_dir = "hackernews3/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 크롤링 함수
def newsCrawler(page):
    url = base_url + str(page)
    data_by_author = defaultdict(list)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find_all('tr', class_='athing')

            for article in articles:
                # 제목과 링크 추출
                title_tag = article.find('span', class_='titleline').find('a')
                if title_tag:
                    title = title_tag.text
                    link = title_tag['href']
                else:
                    title = 'No title'
                    link = 'No link'

                # 점수, 작성자, 댓글 수 등의 정보가 포함된 'subtext' 영역 추출
                subtext = article.find_next_sibling('tr').find('td', class_='subtext')
                score_tag = subtext.find('span', class_='score')
                score = score_tag.text if score_tag else 'No score'

                author_tag = subtext.find('a', class_='hnuser')
                author = author_tag.text if author_tag else 'Unknown author'

                comments_tag = subtext.find_all('a')[-1]
                comments = comments_tag.text if comments_tag else 'No comments'

                # 작성자별로 데이터를 저장
                data_by_author[author].append({
                    "제목": title,
                    "링크": link,
                    "점수": score,
                    "댓글 수": comments
                })

            # 각 작성자별로 엑셀 파일 생성
            for author, data in data_by_author.items():
                df = pd.DataFrame(data)
                filename = f"{author}_hackernews_data_page_{page}.xlsx"
                filepath = os.path.join(output_dir, filename)
                df.to_excel(filepath, index=False)
                print(f"엑셀 파일 저장 완료: {filepath}")
        else:
            print(f"페이지 {page}에 접근 실패: 상태 코드 {response.status_code}")
    except Exception as e:
        print(f"페이지 {page} 크롤링 중 오류 발생: {e}")

# 메인 함수
def main():
    start_time = time.time()
    print(f"{time.strftime('%X')} : 스레딩 크롤링 작업 시작")

    # 크롤링할 페이지 수 (예: 5페이지)
    total_pages = 5

    # 각 페이지를 병렬로 크롤링하는 스레드 리스트
    threads = []
    for page in range(1, total_pages + 1):
        thread = threading.Thread(target=newsCrawler, args=(page,))
        threads.append(thread)
        thread.start()

    # 모든 스레드가 끝날 때까지 대기
    for thread in threads:
        thread.join()

    print(f"{time.strftime('%X')} : 모든 크롤링 작업 완료")
    print(f"스레딩 방식 전체 수행 시간: {time.time() - start_time:.2f} 초")


if __name__ == "__main__":
    main()
