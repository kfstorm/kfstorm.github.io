import html
import json
import regex as re
import shutil
import os
import tomd
from urllib.parse import unquote

def normalize_file_name(file_name):
  return re.sub(r'\p{P}+', "-", unquote(file_name))

def get_file_name(post):
  return normalize_file_name(post["post_name"])

def get_article_link(post):
  return "[{}](/article/{})".format(post["post_title"], get_file_name(post))

def replace_urls(content):
  content = re.sub(r'https?://[^"<>\s]+/wp-content/uploads/', r'/attachment/uploads/', content)
  content = content.replace("http://up.kfstorm.com/BingWallpaper", "/attachment/up/bingwallpaper/BingWallpaper")
  content = content.replace("http://up.kfstorm.com/", "/attachment/up/")
  content = content.replace("/_thumb", "/thumb")
  content = content.replace("http://doubanfmcloud-client.stor.sinaapp.com/", "/attachment/up/doubanfm/")
  content = re.sub(r'https?://(www\.)?kfstorm.com/blog/doubanfm/?', r'/article/doubanfm', content)
  content = re.sub(r'https?://(?:www\.)?kfstorm.com/blog/\d+/\d+/\d+/([^/"<>]+)/?', lambda m: "/article/{}".format(normalize_file_name(m.group(1))), content)
  content = re.sub(r'>/.*?</a>', r'>链接</a>', content)
  return content

with open("_posts.json", "r") as posts_file:
  posts_file_content = posts_file.read().replace("\\r\\n", "\\n")
  posts = json.loads(posts_file_content)
  posts.sort(key=lambda p: p["post_date"], reverse=True)

for post in posts:
  # replace URLs
  content = post["post_content"]
  content = replace_urls(content)
  # replace video tag
  content = re.sub(r'<(?:embed|object).*\"http://player.youku.com/player.php/sid/(\w+)/v.swf.*</(?:embed|object)>', r'<iframe height=498 width=510 src="http://player.youku.com/embed/\g<1>" frameborder=0 "allowfullscreen"></iframe>', content)
  post["post_content"] = content

with open("_comments.json", "r") as comments_file:
  comments_file_content = comments_file.read().replace("\\r\\n", "\\n")
  comments = json.loads(comments_file_content)
  comments.sort(key=lambda p: p["comment_date"], reverse=True)
  # remove spams
  comments = [_ for _ in comments if _["comment_author"] != "DanielShok"]

for comment in comments:
  comment["comment_content"] = replace_urls(comment["comment_content"])

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

    # replace code tags with placeholders
    code_pattern = r'<pre class="brush:(\w+)">(.*?)</pre>'
    code_blocks = re.findall(code_pattern, post_content, flags=re.DOTALL)
    post_content = re.sub(code_pattern, r'\n<pre><code>CODE_LANGUAGE;CODE_CONTENT</code></pre>\n', post_content, flags=re.DOTALL)

    post_content = post_content.replace("&#160;", "")
    post_content = post_content.replace("&nbsp;", "")
    post_content = post_content.replace("<!--more-->", "")
    post_content = re.sub("<br\s*/?>", "\n", post_content)
    post_content = post_content.replace("<p>", "\n<p>")
    post_content = post_content.replace("</p>", "</p>\n")
    post_content = re.sub("<h\d>", "\n\g<0>", post_content)
    post_content = re.sub("</h\d>", "\g<0>\n", post_content)
    post_content = re.sub("<p>\s*</p>", "", post_content)
    post_content = re.sub("<h\d+>\s*</h\d+>", "", post_content)

    post_content = re.sub(r'<blockquote>(.*?)</blockquote>', lambda m: "<blockquote>{}</blockquote>".format(m.group(1).replace("\n", "").replace("<p>", "").replace("</p>", "").strip()), post_content, flags=re.DOTALL)

    lines = [_.strip() for _ in post_content.split("\n")]
    lines = [_ for _ in lines if len(_) > 0]
    lines = [_ if not _.startswith("<p>") or _.endswith("</p>") else "{}</p>".format(_) for _ in lines]
    lines = [_ if _.startswith("<h") or _.startswith("<p>") or _.startswith("<pre>") or _.startswith("<blockquote>") else "<p>{}</p>".format(_) for _ in lines]

    # replace placeholders with code
    j = 0
    for i in range(0, len(lines)):
      if 'CODE_CONTENT' in lines[i]:
        lines[i] = lines[i].replace('CODE_LANGUAGE;', 'CODE_LANGUAGE;' + code_blocks[j][0] + "\n")
        lines[i] = lines[i].replace('CODE_CONTENT', html.unescape(code_blocks[j][1]))
        j += 1

    post_content = "\n".join(lines)
    post_content = tomd.convert(post_content)
    post_content = post_content.replace("```\nCODE_LANGUAGE;", "```")
    post_content = "# {}\n{}".format(post["post_title"], post_content)
    post_file.write(post_content)

    post_comments = [_ for _ in comments if _["comment_post_ID"] == post["ID"]]
    comments_content = "\n# 评论\n\n"
    if len(post_comments) > 0:
      comments_content += "发布者 | 时间 | 内容\n--- | --- | ---\n"
      for comment in post_comments:
        comments_content += "{} | {} | {}\n".format(comment["comment_author"], comment["comment_date"], comment["comment_content"].replace("\n", "<br/>").replace("|", "\|"))
    else:
      comments_content += "（无）\n"
    post_file.write(comments_content)

with open("_index.md.template", "r") as index_template_file:
  index_template = index_template_file.read()

article_list = "文章 | 发布时间\n-- | --\n"
for post in posts:
  article = "{} | {}\n".format(get_article_link(post), post["post_date"])
  article_list += article

index_template = re.sub(r'ARTICLE_LINK_(\d+)', lambda m: get_article_link([_ for _ in posts if _["ID"] == int(m.group(1))][0]), index_template)
index_content = index_template.replace(r'ARTICLE_LIST', article_list)
with open("index.md", "w") as index_file:
  index_file.write(index_content)
