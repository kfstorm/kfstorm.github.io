import html
import json
import regex as re
import shutil
import os
import tomd
from urllib.parse import unquote


def get_file_name(post):
  return re.sub(r'\p{P}+', "-", unquote(post["post_name"]))


with open("_posts.json", "r") as posts_file:
  posts_file_content = posts_file.read().replace("\\r\\n", "\\n")
  posts = json.loads(posts_file_content)
  posts.sort(key=lambda p: p["post_date"], reverse=True)

for post in posts:
  # replace URLs
  content = post["post_content"]
  content = re.sub(r'https?://[^"<>\s]+/wp-content/uploads/', r'/attachment/uploads/', content)
  content = content.replace("http://up.kfstorm.com/BingWallpaper", "/attachment/up/bingwallpaper/BingWallpaper")
  content = content.replace("http://up.kfstorm.com/", "/attachment/up/")
  content = content.replace("/_thumb", "/thumb")
  content = content.replace("http://doubanfmcloud-client.stor.sinaapp.com/", "/attachment/up/doubanfm/")
  content = re.sub(r'https?://(www\.)?kfstorm.com/blog/doubanfm/?', r'/article/doubanfm', content)
  content = re.sub(r'https?://(?:www\.)?kfstorm.com/blog/\d+/\d+/\d+/([^/"<>]+)/?', r'/article/\g<1>', content)
  content = re.sub(r'>/.*?</a>', r'>链接</a>', content)
  # replace video tag
  content = re.sub(r'<(?:embed|object).*\"http://player.youku.com/player.php/sid/(\w+)/v.swf.*</(?:embed|object)>', r'<iframe height=498 width=510 src="http://player.youku.com/embed/\g<1>" frameborder=0 "allowfullscreen"></iframe>', content)
  post["post_content"] = content

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
    lines = [_.strip() for _ in post_content.split("\n")]
    lines = [_ for _ in lines if len(_) > 0]
    lines = [_ if not _.startswith("<p>") or _.endswith("</p>") else "{}</p>".format(_) for _ in lines]
    lines = [_ if _.startswith("<h") or _.startswith("<p") else "<p>{}</p>".format(_) for _ in lines]

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

with open("_index.md.template", "r") as index_template_file:
  index_template = index_template_file.read()

article_list = ""
for post in posts:
  article = "[{}](/article/{}) {}\n\n" \
    .format(post["post_title"], get_file_name(post), post["post_date"], get_file_name(post))
  article_list += article

index_content = index_template.replace("ARTICLE_LIST", article_list)
with open("index.md", "w") as index_file:
  index_file.write(index_content)