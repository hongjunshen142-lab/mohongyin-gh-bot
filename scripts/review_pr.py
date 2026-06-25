import os,json,requests
GITHUB_TOKEN=os.environ["GITHUB_TOKEN"]
OPENROUTER_KEY=os.environ["OPENROUTER_KEY"]
LANG=os.environ.get("LANGUAGE","zh")
with open(os.environ["GITHUB_EVENT_PATH"]) as f:event=json.load(f)
pr=event.get("pull_request",{})
repo=os.environ["GITHUB_REPOSITORY"]
if not pr:print("skip");exit(0)
h={"Authorization":f"Bearer {GITHUB_TOKEN}","Accept":"application/vnd.github.v3.diff"}
diff=requests.get(pr.get("diff_url",""),headers=h).text[:8000]
prompt=f"Code review:\nTitle: {pr.get('title','')}\nBody: {(pr.get('body','') or '')[:2000]}\nDIFF:\n{diff}\n\nOutput format (in {'Chinese' if LANG=='zh' else 'English'}): ✅Strengths | ⚠️Issues | 💡Suggestions | 📊Score(1-10)"
r=requests.post("https://openrouter.ai/api/v1/chat/completions",headers={"Authorization":f"Bearer {OPENROUTER_KEY}","Content-Type":"application/json"},json={"model":"google/gemini-2.0-flash-001","messages":[{"role":"user","content":prompt}],"max_tokens":1500},timeout=60)
review=r.json()["choices"][0]["message"]["content"]
url=f"https://api.github.com/repos/{repo}/issues/{pr['number']}/comments"
requests.post(url,headers={"Authorization":f"Bearer {GITHUB_TOKEN}","Accept":"application/vnd.github.v3+json"},json={"body":review+"\n\n---\n🤖 墨鸿隐 AI | [Install](https://github.com/hongjunshen142-lab/mohongyin-gh-bot)"})
print("done")
