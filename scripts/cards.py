import json,subprocess,collections,html
def gh(*a): return json.loads(subprocess.check_output(["gh","api",*a]))
u=gh("users/HenioSampaio")
repos=gh("users/HenioSampaio/repos?per_page=100")
langs=collections.Counter()
for r in repos:
    if r.get("language"): langs[r["language"]]+=1
G="#00ff66";B="#0a0e0a";D="#00aa44"
def card(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" rx="6" fill="{B}" stroke="#003d1a"/><g font-family="Consolas,Menlo,monospace">{body}</g></svg>'
stats=[("repos públicos",u["public_repos"]),("seguidores",u["followers"]),("seguindo",u["following"]),("no GitHub desde",u["created_at"][:4])]
b=f'<text x="20" y="32" fill="{G}" font-size="16">$ stats --user hbs</text>'
for i,(k,v) in enumerate(stats): b+=f'<text x="20" y="{64+i*24}" fill="{D}" font-size="14">{k:<18}</text><text x="230" y="{64+i*24}" fill="{G}" font-size="14">{v}</text>'
open("assets/stats.svg","w").write(card(340,165,b))
tot=sum(langs.values()) or 1
b=f'<text x="20" y="32" fill="{G}" font-size="16">$ langs --top</text>'
for i,(l,n) in enumerate(langs.most_common(5)):
    p=n/tot; b+=f'<text x="20" y="{62+i*22}" fill="{D}" font-size="13">{html.escape(l)}</text><rect x="130" y="{52+i*22}" width="{int(150*p)}" height="10" fill="{G}"/><text x="290" y="{62+i*22}" fill="{G}" font-size="13">{p:.0%}</text>'
open("assets/langs.svg","w").write(card(340,165,b))
for name in ["trama-versoes","memecoin-lab-versoes"]:
    r=next((x for x in repos if x["name"]==name),None)
    if not r: continue
    d=html.escape((r.get("description") or "")[:55])
    b=f'<text x="20" y="34" fill="{G}" font-size="16">📦 {name}</text><text x="20" y="62" fill="{D}" font-size="12">{d}</text><text x="20" y="92" fill="{G}" font-size="12">★ {r["stargazers_count"]}   ⑂ {r["forks_count"]}   {html.escape(r.get("language") or "")}</text>'
    open(f"assets/pin-{name}.svg","w").write(card(400,110,b))
