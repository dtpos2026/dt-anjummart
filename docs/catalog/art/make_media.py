import json
ART="/tmp/claude-0/-home-user-dt-anjummart/c864131b-01ff-5ff1-af34-95ffa4805d08/scratchpad/art2"
S=json.load(open(f'{ART}/scenes.json'))
exec(open(f'{ART}/media_meta.py').read())  # defines P
def esc(s): return s.replace("&","&amp;")
def details(n,brand,kind,title,lines,tint):
    jew = n>=10
    head=f'''
      <div style="position:absolute;inset:34px;border:2px solid #D4AF37"></div>
      <div style="position:absolute;inset:50px;border:1px solid rgba(212,175,55,.55)"></div>
      <div style="position:absolute;left:0;right:0;top:96px;text-align:center;font:500 28px Jost;letter-spacing:.5em;color:#7A5C14;text-indent:.5em">{brand}</div>
      <div style="position:absolute;left:100px;right:100px;top:146px;text-align:center;font:600 78px/1.05 Cormorant;color:#111">{esc(title)}</div>
      <div style="position:absolute;left:0;right:0;top:300px;text-align:center;color:#D4AF37;font-size:22px;letter-spacing:.3em">&#9472;&#9472;&#9472; &#9670; &#9472;&#9472;&#9472;</div>'''
    foot='''<div style="position:absolute;left:50px;right:50px;bottom:50px;height:84px;background:#111;display:flex;align-items:center;justify-content:center;gap:28px;font:500 22px Jost;letter-spacing:.3em;color:#EAD48A;white-space:nowrap"><span>FREE DELIVERY ALL OVER PAKISTAN</span><span style="color:#D4AF37">&#9670;</span><span>CASH ON DELIVERY</span></div>'''
    if not jew:
        rows=''.join(f'<div style="display:flex;align-items:flex-start;gap:22px;padding:26px 0;border-top:1px solid #E3DAC6"><span style="color:#D4AF37;font-size:22px;line-height:44px">&#9670;</span><span>{esc(l)}</span></div>' for l in lines)
        body=f'''
      <div style="position:absolute;left:110px;top:380px;width:470px;height:1000px;background:#fff;border:1px solid #E7E0D0;border-radius:235px 235px 0 0"></div>
      <img src="file://{ART}/cut-{n:02d}.png" style="position:absolute;left:345px;top:890px;height:800px;transform:translate(-50%,-50%);filter:drop-shadow(0 24px 24px rgba(17,17,17,.28))">
      <div style="position:absolute;left:640px;right:110px;top:470px;font:500 22px Jost;letter-spacing:.4em;color:#7A5C14">KEY DETAILS</div>
      <div style="position:absolute;left:640px;right:110px;top:530px;font:400 36px/1.3 Jost;color:#111;border-bottom:1px solid #E3DAC6">{rows}</div>'''
    else:
        cells=''.join(f'<div style="display:flex;align-items:flex-start;gap:18px;padding:22px 0;border-top:1px solid #E3DAC6"><span style="color:#D4AF37;font-size:20px;line-height:40px">&#9670;</span><span>{esc(l)}</span></div>' for l in lines)
        body=f'''
      <div style="position:absolute;left:110px;top:372px;width:980px;height:700px;background:#fff;border:1px solid #E7E0D0;border-radius:490px 490px 0 0"></div>
      <img src="file://{ART}/cut-{n:02d}.png" style="position:absolute;left:600px;top:735px;height:640px;transform:translate(-50%,-50%);filter:drop-shadow(0 22px 22px rgba(17,17,17,.28))">
      <div style="position:absolute;left:110px;right:110px;top:1118px;text-align:center;font:500 22px Jost;letter-spacing:.4em;color:#7A5C14;text-indent:.4em">KEY DETAILS</div>
      <div style="position:absolute;left:110px;right:110px;top:1170px;display:grid;grid-template-columns:1fr 1fr;column-gap:60px;font:400 32px/1.25 Jost;color:#111">{cells}</div>'''
    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>__FONTS__
    html,body{{margin:0;background:#000}} #c{{position:relative;width:1200px;height:1600px;overflow:hidden;background:#F8F7F4;font-family:Jost}}
    </style></head><body>__NOISE__<div id="c">{head}{body}{foot}</div></body></html>'''
    return {"dir":"media","w":1200,"h":1600,"html":html,"q":86}
for (n,brand,kind,title,lines,tint) in P:
    S[f"p{n:02d}-c"]=details(n,brand,kind,title,lines,tint)
json.dump(S,open(f'{ART}/scenes.json','w'))
