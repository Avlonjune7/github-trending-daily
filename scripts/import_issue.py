#!/usr/bin/env python3
"""Validate public issue JSON and create Hugo content. No network or credentials."""
import json,sys,re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=Path(sys.argv[1]); d=json.loads(p.read_text())
assert d['period'] in ('daily','weekly','monthly')
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',d['date'])
assert d['id']==d['period']+'-'+d['date']
assert d['sourceUrl']=='https://github.com/trending?since='+d['period']
assert isinstance(d['projects'],list) and d['projects']
# Keep pre-existing historical snapshots intact; new dailies must be the official top ten.
if d['period']=='daily' and d['date']>='2026-11-12':
 assert len(d['projects'])==10, 'Daily issues from 2026-11-12 must contain exactly 10 projects'
assert [x['rank'] for x in d['projects']]==list(range(1,len(d['projects'])+1)), 'Keep official rank order'
seen=set()
for x in d['projects']:
 assert re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',x['repo'])
 assert x['repo'] not in seen; seen.add(x['repo'])
 assert x['url']=='https://github.com/'+x['repo']
 assert isinstance(x['stars'],int) and x['stars']>=0
 if 'metrics' in x:
  m=x['metrics']
  assert isinstance(m['totalStars'],int) and m['totalStars']>=x['stars']
  assert isinstance(m['forks'],int) and m['forks']>=0
  assert m['gained']==x['stars'], 'Snapshot gain must match issue gain'
  assert m['collectedAt'][:10]==d['date'], 'Snapshot must belong to the same daily issue'
  assert m['sourceUrl']=='https://githubtrending.today/archive/'+d['date']+'/'
 for k in ('title','category','language','features','overview','deployment','reason','caution'): assert isinstance(x[k],str) and x[k].strip()
 assert x['overview'].strip()!=x['features'].strip(), 'Overview must be distinct from list summary'
 assert isinstance(x.get('contentSources'),list) and x['contentSources'], 'Official content sources required'
 for source in x['contentSources']:
  assert source['url'].startswith('https://github.com/'+x['repo']+'/blob/'), 'Use the official repository documentation'
  assert re.fullmatch(r'[0-9a-f]{40}',source['sha']), 'Preserve the verified source blob SHA'
 assert datetime.fromisoformat(x['contentCheckedAt'].replace('Z','+00:00')).tzinfo is not None
assert datetime.fromisoformat(d['collectedAt'].replace('Z','+00:00')).tzinfo is not None
d['periodLabel']={'daily':'日榜','weekly':'周榜','monthly':'月榜'}[d['period']]
content=json.dumps(d,ensure_ascii=False,indent=2)+'\n\n'
content+='## 数据说明\n\n本期是采集时间对应的快照，增星数不是最终结算；项目功能来自官方说明，未逐个安装实测。\n'
if d.get('contentUpdatedAt'):
 checked=datetime.fromisoformat(d['contentUpdatedAt'].replace('Z','+00:00')).astimezone(ZoneInfo('Asia/Shanghai'))
 content+='\n项目介绍于 '+checked.strftime('%Y-%m-%d %H:%M')+'（北京时间）按官方资料重新核验；这是介绍补充时间，不是榜单采集时间。来源与版本记录保存在本期原始数据中。\n'
out=root/'content' /d['period']/(d['date']+'.md');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(content)
print(out.relative_to(root))
