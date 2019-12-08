import json
import shutil
import os
from urllib.parse import unquote


with open("posts.json", "r") as json_file:
  posts = json.load(json_file)

shutil.rmtree("article", ignore_errors=True)
os.mkdir("article")
for post in posts:
  post_file_name = "article/{}.html".format(unquote(post["post_name"]))
  with open(post_file_name, "w") as post_file:
    post_file.write(post["post_content"])

with open("index.md.template", "r") as index_template_file:
  index_template = index_template_file.read()

article_list = ""
for post in posts:
  article = """
[{} {}](/article/{}.html)

""".format(post["post_title"], post["post_date"], post["post_name"])
  article_list += article

index_content = index_template.replace("ARTICLE_LIST", article_list)
with open("index.md", "w") as index_file:
  index_file.write(index_content)
