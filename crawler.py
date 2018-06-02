import requests
import json
import base64
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from algoliasearch import algoliasearch
import re

client = algoliasearch.Client("OCSEOFWPG9", api-admin-key)
index = client.init_index('py-search-awesome')

master = 0


class UlExtractor(Treeprocessor):
    def run(self, doc):
        "Find all images and append to markdown.images. "
        self.markdown.ul = []
        for ul in doc.findall('.//ul'):
            ul = ul.get()
            print(ul)
            #index.add_objects(ul)


class UlExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        ul_ext = UlExtractor(md)
        md.treeprocessors.add('ulext', ul_ext, '>inline')


class LinkExtractor(Treeprocessor):
    def run(self, doc):
        global master
        if master == 0:
            "Find all images and append to markdown.images. "
            master = 1
            self.markdown.links = []
            for link in doc.findall('.//a'):
                l = link.get('href')
                if l.startswith('https://github.com/'):
                    if not l.startswith('https://github.com/shlomi-noach/awesome-mysql/blob/gh-pages/'):
                        l = l.replace(
                            'https://github.com', 'https://api.github.com/repos')
                        l += '/readme'
                    else:
                        l = 'https://raw.githubusercontent.com/shlomi-noach/awesome-mysql/gh-pages/index.md'
                    print(l)
                    getReadme(l)


class LinkExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        link_ext = LinkExtractor(md)
        md.treeprocessors.add('linkext', link_ext, '>inline')


md = markdown.Markdown(extensions=[LinkExtExtension()])


def getReadme(url):
  r = requests.get(url, auth=(github-username, github-token))
  if not url.startswith('https://raw.githubusercontent.com'):
    basecont = json.loads(r.content)['content']
    con = base64.b64decode(basecont)
  else:
    con = r.content
  if not url.startswith('https://raw.githubusercontent.com/shlomi-noach/awesome-mysql/gh-pages/'):
    url = url.replace(
      'https://api.github.com/repos','https://github.com').replace('/readme','')
  else:
    url = 'https://github.com/shlomi-noach/awesome-mysql/blob/gh-pages/index.md'
  secs = re.split('\#\#\#\# |\#\#\# |\#\# |\# ' , con.decode("utf-8"))
  for sec in secs:
    header = sec.split('\n')[0]
    print([{'link': url,'header': header,'content': sec}])
    try:
      index.add_objects([{'link': url,'header': header, 'content': sec}])
    except:
      pass
  return con 

masterlist = 'https://api.github.com/repos/sindresorhus/awesome/readme'
con = getReadme(masterlist)
html = md.convert(con)
