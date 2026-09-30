#!/usr/bin/env python3
"""
name: build-reading-copy
type: script
description: Render architecture.md + decisions.md into one self-contained HTML page (no external scripts) with a table of contents and two tabs.
why: Gordon reads the design outside Claude, sometimes offline; Markdown is hard to read raw and the artifact needs a network.
reads: _design/architecture.md, _design/decisions.md
writes: _design/sancho-architecture.html (also used as the Artifact source)
test: run it; open the HTML in a browser with wifi off; both tabs render, TOC links work.
"""
import re, datetime, markdown, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
arch = (HERE / 'architecture.md').read_text(encoding='utf-8')
dec  = (HERE / 'decisions.md').read_text(encoding='utf-8')
today = datetime.date.today().isoformat()

def render(md_text):
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'toc_depth': '2-3'}})
    body = md.convert(md_text)
    # wrap tables for horizontal scroll
    body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')
    return body, md.toc

a_body, a_toc = render(arch)
d_body, d_toc = render(dec)

css = """
:root{--bg:#F7F6F2;--ink:#1E2A24;--muted:#66716B;--line:#D8DBD4;--accent:#5B7A3A;--card:#FFFFFF;--code:#EEEDE7;--th:#E7EEDB;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--disp:"Bricolage Grotesque","IBM Plex Sans",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#161A18;--ink:#E6E9E3;--muted:#97A19A;--line:#2C332F;--accent:#93B56E;--card:#1C201E;--code:#222724;--th:#233120}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#161A18;--ink:#E6E9E3;--muted:#97A19A;--line:#2C332F;--accent:#93B56E;--card:#1C201E;--code:#222724;--th:#233120}
body{background:var(--bg);color:var(--ink);font:15.5px/1.6 var(--sans);margin:0}
.wrap{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:24px 80px}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:12px 24px;border-bottom:1px solid var(--line);padding-bottom:14px}
h1.site{font:700 30px/1.05 var(--disp);margin:0}
.meta{color:var(--muted);font-size:13px}
.tabs{display:flex;gap:6px;margin:16px 0 0}
.tabs button{font:600 14px var(--sans);padding:8px 14px;border:1px solid var(--line);border-bottom:none;border-radius:8px 8px 0 0;background:var(--code);color:var(--muted);cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--card);color:var(--ink)}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.panel{display:grid;grid-template-columns:260px minmax(0,1fr);gap:28px;border:1px solid var(--line);border-radius:0 10px 10px 10px;background:var(--card);padding:22px}
@media (max-width:860px){.panel{grid-template-columns:1fr}}
nav.toc{position:sticky;top:env(safe-area-inset-top,0px);align-self:start;max-height:calc(100vh - 24px);overflow:auto;font-size:13px;padding-right:6px}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc ul ul{padding-left:12px}
nav.toc a{display:block;color:var(--muted);text-decoration:none;padding:3px 0 3px 8px;border-left:2px solid transparent;line-height:1.35}
nav.toc ul ul a{font-size:12.5px}
nav.toc a:hover,nav.toc a.active{color:var(--ink);border-left-color:var(--accent)}
@media (max-width:860px){nav.toc{position:static;max-height:none;border-bottom:1px solid var(--line);padding-bottom:10px}}
article{min-width:0;max-width:78ch}
article h1{font:700 28px/1.15 var(--disp);margin:0 0 8px;text-wrap:balance}
article h2{font:700 22px/1.2 var(--disp);margin:40px 0 10px;padding-top:14px;border-top:1px solid var(--line);text-wrap:balance}
article h3{font:600 16.5px/1.3 var(--sans);margin:24px 0 6px}
article p{margin:0 0 12px}
article ul,article ol{padding-left:22px;margin:0 0 12px}
article li{margin:3px 0}
article code{font:500 .88em var(--mono);background:var(--code);padding:1px 5px;border-radius:4px}
article pre{background:var(--code);padding:12px 14px;border-radius:8px;overflow-x:auto;font:12.5px/1.5 var(--mono);margin:0 0 14px}
article pre code{background:none;padding:0;font-size:inherit}
.tw{overflow-x:auto;margin:0 0 16px}
article table{border-collapse:collapse;font-size:13.5px;min-width:100%}
article th,article td{border:1px solid var(--line);padding:6px 9px;vertical-align:top;text-align:left}
article th{background:var(--th);font-weight:600;white-space:nowrap}
article td:first-child{white-space:nowrap}
article blockquote{border-left:3px solid var(--accent);margin:0 0 12px;padding:2px 12px;color:var(--muted)}
article hr{border:0;border-top:1px solid var(--line);margin:28px 0}
article a{color:var(--accent)}
.hidden{display:none}
"""

js = """
(function(){
  var tabs={'t-arch':'p-arch','t-dec':'p-dec'};
  Object.keys(tabs).forEach(function(tid){
    document.getElementById(tid).addEventListener('click',function(){
      Object.keys(tabs).forEach(function(k){document.getElementById(k).setAttribute('aria-selected',k===tid?'true':'false');document.getElementById(tabs[k]).classList.toggle('hidden',k!==tid);});
      try{localStorage.setItem('sancho-arch-tab',tid);}catch(e){}
      window.scrollTo(0,0);
    });
  });
  try{var t=localStorage.getItem('sancho-arch-tab'); if(t&&tabs[t]) document.getElementById(t).click();}catch(e){}
  if(location.hash==='#decisions'){document.getElementById('t-dec').click();}
  var links=[].slice.call(document.querySelectorAll('nav.toc a'));
  function mark(){var y=window.scrollY+120;var cur=null;links.forEach(function(a){var id=decodeURIComponent(a.getAttribute('href').slice(1));var el=document.getElementById(id);if(el&&el.offsetTop<=y&&!el.closest('.hidden'))cur=a;});links.forEach(function(a){a.classList.toggle('active',a===cur);});}
  window.addEventListener('scroll',mark,{passive:true}); mark();
})();
"""

page = f"""<title>Sancho Architecture</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<div class="wrap">
  <div class="top">
    <div><h1 class="site">Sancho Architecture</h1><div class="meta">Rendered from <code>_design/architecture.md</code> and <code>_design/decisions.md</code> · snapshot {today} · the files on disk are the truth; this page is a reading copy. Works offline (fonts fall back).</div></div>
    <div class="meta">Approved 2026-09-30 · Phase 3 under way</div>
  </div>
  <div class="tabs" role="tablist">
    <button role="tab" id="t-arch" aria-selected="true" aria-controls="p-arch">Architecture</button>
    <button role="tab" id="t-dec" aria-selected="false" aria-controls="p-dec">Decisions log</button>
  </div>
  <div class="panel" id="p-arch" role="tabpanel"><nav class="toc">{a_toc}</nav><article>{a_body}</article></div>
  <div class="panel hidden" id="p-dec" role="tabpanel"><nav class="toc">{d_toc}</nav><article>{d_body}</article></div>
</div>
<script>{js}</script>
"""
(HERE / 'sancho-architecture.html').write_text(page, encoding='utf-8')
# a standalone copy that opens directly in a browser (adds the html skeleton the Artifact tool would otherwise add)
standalone = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + page.replace('<title>', '<title>', 1) + '</head><body></body></html>'
# move body content properly: simplest is to put everything after </style> into body
head_end = page.index('</style>') + len('</style>')
standalone = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
              + page[:head_end] + '</head><body style="margin:0">' + page[head_end:] + '</body></html>')
(HERE / 'Sancho-Architecture-standalone.html').write_text(standalone, encoding='utf-8')
print('wrote', len(page), 'and', len(standalone), 'bytes')
