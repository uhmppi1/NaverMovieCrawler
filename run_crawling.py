import os
import json
import shutil
from NaverMovieCrawler import NaverMovieCrawler


data_dir = './movielist'
data_finished_dir = './movielist_finished'
data_to_save_dir = './data'


def crawl_one_list(crawler, movielist_file):
  all_data = {}

  file_path_to_read = os.path.join(data_dir, movielist_file)
  file_path_finished = os.path.join(data_finished_dir, movielist_file)

  movieList = crawler.load_movieList(file_path_to_read)

  for movieData in movieList:
    result = crawler.get_movie(movieData)
    if result != None:
      code, data = result
      crawler.movieCommentData[code] = data

  file_path_to_save = os.path.join(data_to_save_dir, 'data_' + movielist_file)
  crawler.save_data(file_path_to_save)


  shutil.move(file_path_to_read, file_path_finished)


#
#
wd = "./chromedriver"
crawler = NaverMovieCrawler()

# crawler.log_in('kpdpkp@naver.com', 'meanimo123')  # 댓글 더보기를 하려면 로그인 해야 함.

#
#
#
file_list = os.listdir(data_dir)
file_list.sort()

for file in file_list:
  crawl_one_list(crawler, file)

# with open('./movielist/curPage=1&itemPerPage=100&prdtStartYear=2016&prdtEndYear=2016.json', 'r', encoding='utf-8') as f:
#   list_before = json.load(f) #json.loads(f.read())
#   # sss = f.read(100)
#   # sss = sss.encode('utf-8').decode('unicode_escape')
#   # # sss = sss.decode('unicode_escape')
#   # print(sss)
#   print(list_before)