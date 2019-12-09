import json
import re
import shutil
import os
import tomd
from urllib.parse import unquote


def get_file_name(post):
  return unquote(post["post_name"]).replace("！", "")


with open("posts.json", "r") as posts_file:
  posts_file_content = posts_file.read().replace("\\r\\n", "\\n")
  # replace URLs
  posts_file_content = re.sub(r'https?://[^"<>\s]+/wp-content/uploads/', r'/attachment/uploads/', posts_file_content)
  posts_file_content = posts_file_content.replace("http://up.kfstorm.com/", "/attachment/up/")
  posts = json.loads(posts_file_content)
  posts.sort(key=lambda p: p["post_date"], reverse=True)

shutil.rmtree("article", ignore_errors=True)
os.mkdir("article")
for post in posts:
  post_file_name = "article/{}-html.html".format(get_file_name(post))
  with open(post_file_name, "w") as post_file:
    post_file.write(post["post_content"])
  post_file_name = "article/{}.md".format(get_file_name(post))
  with open(post_file_name, "w") as post_file:
    # TODO: replace h1 with h2, h2 with h3, ...
    # TODO: images with anchor
    # TODO: replace "1、" with "1. "
    post_content = post["post_content"]
    post_content = post_content.replace("</p>", "</p>\n")
    post_content = post_content.replace("<p>&nbsp;</p>", "")
    lines = [_.strip() for _ in post_content.split("\n")]
    lines = [_ for _ in lines if len(_) > 0 and _ != "&nbsp;"]
    lines = [_ if _.startswith("<h") or _.startswith("<p") else "<p>{}</p>".format(_) for _ in lines]
    post_content = "\n".join(lines)
    post_file.write("# {}\n{}".format(post["post_title"], tomd.convert(post_content)))

with open("index.md.template", "r") as index_template_file:
  index_template = index_template_file.read()

article_list = ""
for post in posts:
  article = "[{}](/article/{}.md) {} [HTML版本](/article/{}-html.html)\n\n" \
    .format(post["post_title"], get_file_name(post), post["post_date"], get_file_name(post))
  article_list += article

index_content = index_template.replace("ARTICLE_LIST", article_list)
with open("index.md", "w") as index_file:
  index_file.write(index_content)
