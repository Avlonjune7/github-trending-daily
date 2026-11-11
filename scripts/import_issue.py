#!/usr/bin/env python3
"""Validate public issue JSON and create Hugo content. No network or credentials."""
import json,sys,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=Path(sys.argv[1]); d=json.loads(p.read_text())
assert d['period'] in ('daily','weekly','monthly')
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',d['date'])
assert d['id']==d['period']+'-'+d['date']
assert d['sourceUrl']=='https://github.com/trending?since='+d['period']
assert isinstance(d['projects'],list) and d['projects']
seen=set()
for x in d['projects']:
 assert re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',x['repo'])
 assert x['repo'] not in seen; seen.add(x['repo'])
 assert x['url']=='https://github.com/'+x['repo']
 assert isinstance(x['stars'],int) and x['stars']>=0
 for k in ('title','category','language','features','deployment','reason','caution'): assert isinstance(x[k],str) and x[k].strip()
d['periodLabel']={'daily':'日榜','weekly':'周榜','monthly':'月榜'}[d['period']]
content=json.dumps(d,ensure_ascii=False,indent=2)+'\n\n'
content+='## 数据说明\n\n本期是采集时间对应的快照，增星数不是最终结算；项目功能来自官方说明，未逐个安装实测。\n'
out=root/'content'/d['period']/(d['date']+'.md');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(content)
print(out.relative_to(root))
