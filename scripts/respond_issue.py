import os,json,requests
GITHUB_TOKEN=os.environ["GITHUB_TOKEN"]
OPENROUTER_KEY=os.environ["OPENROUTER_KEY"]
LANG=os.environ.get("LANGUAGE","zh")
with open(os.environ["GITHUB_EVENT_PATH"]) as f:event=json.load(f)
if event.get("action")!="opened":print("skip");exit(0)
issue=event.get("issue",{})
repo=os.environ["GITHUB_REPOSITORY"]
prompt=f"Issue response:\nTitle: {issue.get('title','')}\nBody: {(issue.get('body','') or '')[:3000]}\nLabels: {[l['name']for l in issue.get('labels',[])]}\n\nReply in {'Chinese' if LANG=='zh' else 'English'}: 📋Analysis | 🏷️Suggested Labels | 💡Tips | ⚡Troubleshooting. Be friendly"
r=requests.post("https://openrouter.ai/api/v1/chat/completions",headers={"Authorization":f"Bearer {OPENROUTER_KEY}","Content-Type":"application/json"},json={"model":"google/gemini-2.0-flash-001","messages":[{"role":"user","content":prompt}],"max_tokens":1200},timeout=60)
reply=r.json()["choices"][0]["message"]["content"]
labels=[lb for lb in ["bug","enhancement","documentation","question","help wanted"] if lb in reply.lower()]
if labels:
    requests.post(f"https://api.github.com/repos/{repo}/issues/{issue['number']}/labels",headers={"Authorization":f"Bearer {GITHUB_TOKEN}"},json=labels[:3])
url=f"https://api.github.com/repos/{repo}/issues/{issue['number']}/comments"
requests.post(url,headers={"Authorization":f"Bearer {GITHUB_TOKEN}","Accept":"application/vnd.github.v3+json"},json={"body":reply+"\n\n---\n🤖 墨鸿隐 AI | [Install](https://github.com/hongjunshen142-lab/mohongyin-gh-bot)"})
print("done")
