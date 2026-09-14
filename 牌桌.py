# -*- coding: utf-8 -*-
"""《月幕万象》可视化牌桌 · 五页版

    主界面.html  —— 这一局走到哪、构筑、称号、难度
    牌桌.html    —— 打牌的那一刻：饰物、手牌、分数、播报
    商店.html    —— 货架、月币、卡包
    收藏.html    —— 464 条题记、成就墙

零依赖，只用标准库。四个 html 互相链接，双击任意一个都能开，不需要服务器。

用法（在游戏进程里）：
    import 牌桌四页 as ui
    ui.dump_all(state, 输出目录, jokers=..., hands=..., bosses=..., achievements=..., log=...)
"""
from pathlib import Path

SUIT_SYM = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}
SUIT_RED = {"H", "D"}
RANK_TXT = {11: "J", 12: "Q", 13: "K", 14: "A"}
ENH_TXT = {"bonus": "加值", "mult": "倍率", "wild": "百搭", "glass": "琉璃",
           "steel": "钢铸", "stone": "石像", "gold": "鎏金", "lucky": "幸运"}
SEAL_COLOR = {"gold": "#f0c04a", "red": "#e2334a", "blue": "#009dff", "purple": "#a45ede"}
EDITION_GLOW = {
    "foil": "0 0 14px #7fd4ff, inset 0 0 20px rgba(127,212,255,.45)",
    "holo": "0 0 14px #ff8fd0, inset 0 0 20px rgba(255,143,208,.45)",
    "poly": "0 0 18px #b07cff, inset 0 0 24px rgba(176,124,255,.5)",
    "negative": "0 0 16px #444, inset 0 0 26px rgba(0,0,0,.6)",
}
EDITION_TXT = {"foil": "银箔", "holo": "幻彩", "poly": "棱光", "negative": "负片"}
PAGES = [("主界面", "主界面.html"), ("牌桌", "牌桌.html"),
         ("商店", "商店.html"), ("收藏", "收藏.html"), ("往事", "往事.html")]


def esc(t):
    return (str(t).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def rank_txt(r):
    return RANK_TXT.get(r, str(r))


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#2b3538;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
  color:#fff;padding:0 0 24px;min-height:100vh}
.nav{background:#1a2225;border-bottom:3px solid #121a1c;padding:10px 20px;display:flex;
  align-items:center;gap:8px;position:sticky;top:0;z-index:50}
.nav .logo{font-size:15px;font-weight:900;color:#ffd166;letter-spacing:2px;margin-right:14px}
.nav a{color:#8fa3a8;text-decoration:none;font-size:13px;font-weight:700;padding:6px 14px;
  border-radius:8px;background:#232d31;border:2px solid #121a1c}
.nav a.on{color:#1a2225;background:#ffd166;border-color:#121a1c}
.nav a:hover{color:#fff;background:#2f3d42}
.nav .right{margin-left:auto;font-size:12px;color:#6b7d82;display:flex;gap:10px}
.nav .right b{color:#cfe3e8}
.wrap{max-width:1240px;margin:16px auto;padding:0 16px}
.panel{background:#1f282b;border:3px solid #121a1c;border-radius:14px;padding:14px;margin-bottom:14px}
.ptitle{font-size:11px;color:#8fa3a8;letter-spacing:2px;margin-bottom:10px}
.card{width:78px;height:110px;background:#fdf6e6;border:3px solid #121a1c;border-radius:10px;
  position:relative;color:#22303a;flex-shrink:0}
.card.red{color:#e2334a}
.card.debuff{filter:grayscale(1) brightness(.62)}
.card .corner{position:absolute;display:flex;flex-direction:column;align-items:center;line-height:1}
.card .tl{top:5px;left:6px} .card .br{bottom:5px;right:6px;transform:rotate(180deg)}
.card .r{font-size:17px;font-weight:900} .card .s{font-size:13px}
.card .pip{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:34px}
.card .enh{position:absolute;top:-9px;left:50%;transform:translateX(-50%);background:#ff9e2c;
  color:#1b1b1b;font-size:10px;font-weight:800;padding:1px 6px;border-radius:7px;border:2px solid #121a1c}
.card .ed{position:absolute;bottom:-9px;left:50%;transform:translateX(-50%);background:#a45ede;
  color:#fff;font-size:10px;font-weight:800;padding:1px 6px;border-radius:7px;border:2px solid #121a1c}
.card .seal{position:absolute;top:6px;right:6px;width:11px;height:11px;border-radius:50%;border:2px solid #121a1c}
.card.stone{background:#7d8a8f}
.stone-face{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:26px;font-weight:900;color:#2b3538}
.cards{display:flex;gap:10px;flex-wrap:wrap}
.joker{width:96px;height:130px;background:#fdf6e6;border:3px solid #121a1c;border-radius:11px;
  color:#1b1b1b;padding:7px;position:relative;display:flex;flex-direction:column}
.joker.empty{background:#2b3538;border-style:dashed;border-color:#3f4e52}
.jname{font-size:13px;font-weight:900;line-height:1.15;margin-bottom:4px}
.jdesc{font-size:10px;line-height:1.3;color:#4a4a4a;flex:1;overflow:hidden}
.jed{position:absolute;top:-8px;right:-6px;background:#a45ede;color:#fff;font-size:10px;
  padding:2px 6px;border-radius:8px;border:2px solid #121a1c;font-weight:800}
.jflag{font-size:9px;background:#121a1c;color:#ffd166;border-radius:5px;padding:1px 4px;margin-top:2px;align-self:flex-start}
[data-lore]{cursor:help}
[data-lore]::after{content:"";position:absolute;bottom:4px;right:5px;width:6px;height:6px;
  border-radius:50%;background:#a45ede;box-shadow:0 0 6px #a45ede}
#loremask{position:fixed;inset:0;background:rgba(0,0,0,.72);display:none;align-items:center;
  justify-content:center;z-index:99;padding:24px}
#loremask.on{display:flex}
#lorecard{max-width:470px;background:#fdf6e6;color:#22303a;border:4px solid #121a1c;
  border-radius:16px;padding:22px 24px;box-shadow:0 0 40px rgba(164,94,222,.5)}
#lorename{font-size:19px;font-weight:900;color:#7a3fb8;margin-bottom:12px;letter-spacing:1px}
#loretext{font-size:15px;line-height:1.85;color:#2f3d46}
#lorehint{font-size:11px;color:#8a9aa2;margin-top:16px;text-align:right}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.stat{background:#121a1c;border-radius:10px;padding:12px;text-align:center}
.stat .lbl{font-size:10px;color:#8fa3a8;letter-spacing:1px}
.stat .val{font-size:26px;font-weight:900;margin-top:3px}

@media (max-width:820px){
  html,body{overflow-x:hidden}
  .wrap,.panel,.shopwrap,.shopside,.shopmain,.tablegrid,.felt,.shelfbox,.jokerbar,
  .signbox,.sbtn,.sgrid,.sbox,.grid2,.grid3{max-width:100%;min-width:0}
  .nav{padding:8px 10px;gap:5px;flex-wrap:wrap}
  .nav .logo{font-size:13px;margin-right:6px;width:100%;margin-bottom:4px}
  .nav a{font-size:12px;padding:5px 10px;flex:1;text-align:center}
  .nav .right{width:100%;margin:5px 0 0;font-size:11px;justify-content:center}
  .wrap{padding:0 10px;margin:10px auto}
  .panel{padding:10px;margin-bottom:10px;border-width:2px}
  .grid2,.grid3{grid-template-columns:1fr 1fr;gap:8px}
  .stat{padding:8px}
  .stat .val{font-size:19px}
  /* 牌桌：两列变一列 */
  .tablegrid{grid-template-columns:1fr!important;gap:10px}
  .statusbar{padding:8px 10px;gap:7px}
  .stext{font-size:12px} .stime{font-size:10px}
  .felt{padding:12px 8px}
  .cards{gap:5px}
  .card{width:52px;height:74px;border-width:2px}
  .played-row .card{width:54px;height:77px}
  .played-row .card .pip{font-size:22px} .played-row .card .r{font-size:12px}
  .handzone .card{width:44px;height:63px}
  .handzone .card .pip{font-size:18px} .handzone .card .r{font-size:11px}
  .stage{padding:12px 8px;min-height:104px}
  .card .r{font-size:12px} .card .s{font-size:9px} .card .pip{font-size:22px}
  .card .tl{top:3px;left:3px} .card .br{bottom:3px;right:3px}
  .card .enh,.card .ed{font-size:8px;padding:0 4px}
  .joker{width:74px;height:104px;padding:5px;border-width:2px}
  .jname{font-size:11px} .jdesc{font-size:9px}
  .scoreline{gap:7px;margin-bottom:10px}
  .chip{font-size:20px;padding:4px 12px;min-width:72px}
  .mult{font-size:18px;padding:4px 10px}
  .handname{font-size:14px}
  .logbox{max-height:300px}
  .cmdbox{max-height:190px}
  .cmdrow{font-size:11px} .ct{font-size:9px}
  .lg{font-size:11px;padding:4px 7px}
  /* 商店：侧栏塌到上面 */
  .shopwrap{grid-template-columns:1fr!important;gap:10px}
  .shopside{flex-direction:row;flex-wrap:wrap;gap:7px}
  .signbox{flex:1 1 100%;padding:9px}
  .sign{font-size:25px}
  .signsub{font-size:11px;margin-top:4px}
  .sbtn{flex:1;padding:9px;font-size:13px}
  .sgrid{flex:1 1 100%;gap:6px}
  .jokerbar{padding:7px;gap:5px;overflow-x:auto}
  .shelfbox{padding:10px 8px}
  .shelf{gap:12px;justify-content:center}
  .sc{width:118px;min-height:156px;padding:10px 8px}
  .scname{font-size:12px} .scdesc{font-size:9px}
  /* 成就墙、题记 */
  .achwall,.stkwrap,.chlwrap{grid-template-columns:1fr 1fr;gap:6px}
  .stkn{font-size:12px} .stkd,.chd{font-size:8px} .chn{font-size:11px}
  .an{font-size:10px} .ad{font-size:8px}
  .lit{font-size:11px;padding:4px 9px}
  .litwrap{gap:5px}
  #lorecard{padding:18px;max-width:none}
  #lorename{font-size:16px} #loretext{font-size:14px;line-height:1.75}
  .kv{font-size:12px}
  .lvrow{font-size:11px}
  .hrow{font-size:11px;gap:8px}
}
@media (max-width:420px){
  .card{width:44px;height:63px}
  .card .pip{font-size:18px} .card .r{font-size:11px}
  .joker{width:66px;height:94px}
  .sc{width:calc(50% - 6px);min-height:142px}
  .shelf{gap:12px 8px}
}
"""

SCRIPT = """
<div id="loremask"><div id="lorecard">
  <div id="lorename"></div><div id="loretext"></div>
  <div id="lorehint">点任意处关闭</div></div></div>
<script>
(function(){
  var mask=document.getElementById('loremask'),
      nm=document.getElementById('lorename'),
      tx=document.getElementById('loretext'),timer=null;
  function show(el){ if(!el.dataset.lore)return;
    nm.textContent=el.dataset.name||''; tx.textContent=el.dataset.lore; mask.classList.add('on'); }
  mask.addEventListener('click',function(){mask.classList.remove('on')});
  document.querySelectorAll('[data-lore]').forEach(function(el){
    el.addEventListener('mouseenter',function(){timer=setTimeout(function(){show(el)},600)});
    el.addEventListener('mouseleave',function(){clearTimeout(timer)});
    el.addEventListener('touchstart',function(){timer=setTimeout(function(){show(el)},500)},{passive:true});
    el.addEventListener('touchend',function(){clearTimeout(timer)});
    el.addEventListener('touchmove',function(){clearTimeout(timer)});
    el.addEventListener('click',function(){clearTimeout(timer);show(el)});
  });
})();
</script>
"""


def shell(title, active, body, state=None, live=False):
    st = state or {}
    nav = "".join(
        f'<a href="{href}"{" class=on" if name == active else ""}>{name}</a>'
        for name, href in PAGES)
    right = (f'第 <b>{st.get("ante", 1)}</b> 幕 · 月币 <b>${st.get("money", 0)}</b>'
             f' · 总分 <b>{st.get("run_score", 0):,}</b>' if state else "")
    refresh = '<meta http-equiv="refresh" content="5">' if live else ""
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">{refresh}
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 月幕万象</title><style>{CSS}</style></head><body>
<div class="nav"><div class="logo">🌙 月幕万象</div>{nav}<div class="right">{right}</div></div>
<div class="wrap">{body}</div>
{SCRIPT}
</body></html>"""


def card_html(c, lore="", debuffed=False, fly=None, sel=False, fresh=None):
    suit = c.get("suit", "S")
    cls = "card" + (" red" if suit in SUIT_RED else "") + (" debuff" if debuffed else "")
    if sel:
        cls += " sel"
    if fly is not None:
        cls += " fly"
        style_fly = f' style="--i:{fly}"'
    elif fresh is not None:
        cls += " fresh"
        style_fly = f' style="--i:{fresh}"'
    else:
        style_fly = ""
    label = f'{rank_txt(c.get("rank"))}{SUIT_SYM.get(suit, "")}'
    attr = f' data-lore="{esc(lore)}" data-name="{esc(label)}"' if lore else ""
    style = f' style="box-shadow:{EDITION_GLOW[c.get("edition")]}"' if c.get("edition") in EDITION_GLOW else ""
    if c.get("enhancement") == "stone":
        return f'<div class="{cls} stone"{attr}{style}{style_fly}><div class="stone-face">石</div></div>'
    tags = ""
    if c.get("enhancement"):
        tags += f'<div class="enh">{ENH_TXT.get(c["enhancement"], c["enhancement"])}</div>'
    if c.get("edition"):
        tags += f'<div class="ed">{EDITION_TXT.get(c["edition"], c["edition"])}</div>'
    if c.get("seal"):
        tags += f'<div class="seal" style="background:{SEAL_COLOR.get(c["seal"], "#888")}"></div>'
    return (f'<div class="{cls}"{attr}{style}{style_fly}>'
            f'<div class="corner tl"><span class="r">{rank_txt(c.get("rank"))}</span>'
            f'<span class="s">{SUIT_SYM.get(suit, suit)}</span></div>'
            f'<div class="pip">{SUIT_SYM.get(suit, suit)}</div>'
            f'<div class="corner br"><span class="r">{rank_txt(c.get("rank"))}</span>'
            f'<span class="s">{SUIT_SYM.get(suit, suit)}</span></div>{tags}</div>')


def joker_html(meta, inst):
    flags = "".join(f'<div class="jflag">{t}</div>' for t, k in
                    (("永恒", "eternal"), ("易逝", "perishable"), ("租赁", "rental")) if inst.get(k))
    ed = inst.get("edition", "")
    style = f' style="box-shadow:{EDITION_GLOW[ed]}"' if ed in EDITION_GLOW else ""
    badge = f'<div class="jed">{EDITION_TXT.get(ed, ed)}</div>' if ed else ""
    lore = meta.get("lore", "")
    attr = f' data-lore="{esc(lore)}" data-name="{esc(meta.get("name", ""))}"' if lore else ""
    return (f'<div class="joker"{attr}{style}><div class="jname">{esc(meta.get("name", "?"))}</div>'
            f'<div class="jdesc">{esc(meta.get("desc", ""))}</div>{badge}{flags}</div>')


# ─────────────────────────── 四个页面 ───────────────────────────

def _lore_read(p):
    v = p.get("lore_read")
    if isinstance(v, int):
        return v
    if isinstance(v, (list, set, tuple)):
        return len(v)
    if isinstance(v, dict):
        return sum(len(x) for x in v.values() if hasattr(x, "__len__"))
    return 0


def page_home(state, ctx):
    """主界面：这一局走到哪"""
    hands, bosses = ctx.get("hands", {}), ctx.get("bosses", {})
    stakes, decks = ctx.get("stakes", {}), ctx.get("decks", {})
    titles = ctx.get("titles", {})
    p = state.get("profile") or {}

    levels = state.get("hand_levels") or {}
    usage = state.get("hand_usage") or {}
    lv_rows = ""
    for key, row in hands.items():
        nm = row[0] if isinstance(row, (list, tuple)) else row
        lore = (ctx.get("lore_hands") or {}).get(key, "")
        attr = f' data-lore="{esc(lore)}" data-name="{esc(nm)}"' if lore else ""
        lv_rows += (f'<div class="lvrow" style="position:relative"{attr}><span>{esc(nm)}</span>'
                    f'<span class="lvn">Lv.{levels.get(key, 1)}</span>'
                    f'<span class="lvu">{usage.get(key, 0)}次</span></div>')

    stake_row = stakes.get(state.get("stake", 1))
    stake_nm = stake_row[0] if isinstance(stake_row, (list, tuple)) else f'难度{state.get("stake",1)}'
    deck_row = decks.get(state.get("deck_id", "moon"))
    deck_nm = deck_row[0] if isinstance(deck_row, (list, tuple)) else state.get("deck_id", "")
    title_row = titles.get(p.get("equipped_title", "beloved")) or {}

    cur_stake = state.get("stake", 1)
    stake_cells = ""
    for k in sorted(stakes):
        row = stakes[k]
        nm = row[0] if isinstance(row, (list, tuple)) else str(k)
        dsc = row[1] if isinstance(row, (list, tuple)) and len(row) > 1 else ""
        lore = (ctx.get("lore_stakes") or {}).get(k, "")
        attr = f' data-lore="{esc(lore)}" data-name="{esc(nm)}"' if lore else ""
        cls = "stk on" if k == cur_stake else ("stk done" if k < cur_stake else "stk")
        stake_cells += (f'<div class="{cls}"{attr}><div class="stkn">{esc(nm)}</div>'
                        f'<div class="stkd">{esc(dsc)}</div></div>')

    chs = ctx.get("challenges") or {}
    cur_ch = state.get("challenge", "none")
    ch_cells = ""
    for k, row in chs.items():
        nm = row[0] if isinstance(row, (list, tuple)) else str(k)
        dsc = row[1] if isinstance(row, (list, tuple)) and len(row) > 1 else ""
        lore = (ctx.get("lore_challenges") or {}).get(k, "")
        attr = f' data-lore="{esc(lore)}" data-name="{esc(nm)}"' if lore else ""
        ch_cells += (f'<div class="chl{" on" if k == cur_ch else ""}"{attr}>'
                     f'<div class="chn">{esc(nm)}</div><div class="chd">{esc(dsc)}</div></div>')

    vouchers_meta = ctx.get("vouchers") or {}
    v_cells = ""
    for vid in (state.get("vouchers") or []):
        vm = vouchers_meta.get(vid) or {}
        lore = vm.get("lore", "") if isinstance(vm, dict) else ""
        attr = f' data-lore="{esc(lore)}" data-name="{esc(vm.get("name", vid))}"' if lore else ""
        v_cells += (f'<div class="vch"{attr}><div class="vn">{esc(vm.get("name", vid))}</div>'
                    f'<div class="vd">{esc(vm.get("desc", ""))}</div></div>')

    usage = state.get("hand_usage") or {}
    top_used = sorted(usage.items(), key=lambda kv: -kv[1])[:6]
    use_cells = "".join(
        f'<div class="ucell"><div class="un">{esc((hands.get(k) or [k])[0])}</div>'
        f'<div class="uv">{v}</div></div>' for k, v in top_used if v)

    hist = state.get("hand_history") or []
    hist_rows = "".join(
        f'<div class="hrow"><span>第{h.get("ante")}幕</span>'
        f'<span>{esc((hands.get(h.get("hand")) or [h.get("hand")])[0])}</span>'
        f'<span class="hs">{h.get("score", 0):,}</span>'
        f'<span class="ht">/{h.get("target", 0):,}</span></div>'
        for h in hist[-12:])

    return f"""
<div class="grid3">
  <div class="stat"><div class="lbl">当前幕</div><div class="val" style="color:#ffd166">{state.get('ante',1)}</div></div>
  <div class="stat"><div class="lbl">本局总分</div><div class="val" style="color:#fff">{state.get('run_score',0):,}</div></div>
  <div class="stat"><div class="lbl">月币</div><div class="val" style="color:#f0c04a">${state.get('money',0)}</div></div>
</div>
<div class="grid2">
  <div class="panel"><div class="ptitle">这一局</div>
    <div class="kv"><span>难度</span><b style="color:#fe5f55">{esc(stake_nm)}</b></div>
    <div class="kv"><span>牌组</span><b>{esc(deck_nm)}</b></div>
    <div class="kv"><span>称号</span><b style="color:#ffd166">👑 {esc(title_row.get('name','—'))}</b></div>
    <div class="kv"><span>构筑名</span><b>{esc(state.get('build_name') or '未命名')}</b></div>
    <div class="kv"><span>seed</span><b>{state.get('seed','—')}</b></div>
    <div class="kv"><span>连胜</span><b>{state.get('win_streak',0)}</b></div>
    <div class="kv"><span>已读题记</span><b style="color:#a45ede">{_lore_read(p)} 条</b></div>
  </div>
  <div class="panel"><div class="ptitle">牌型等级（点开看题记）</div>{lv_rows}</div>
</div>
<div class="grid2">
  <div class="panel"><div class="ptitle">设施 · 这一局买下的（{len(state.get('vouchers') or [])} 件）</div>
    <div class="vchwrap">{v_cells or '<div style="color:#6b7d82;font-size:12px">还没买过设施</div>'}</div></div>
  <div class="panel"><div class="ptitle">本局战绩</div>
    <div class="grid2" style="gap:8px">
      <div class="stat"><div class="lbl">单手最高</div>
        <div class="val" style="color:#ff8fd0;font-size:20px">{state.get('run_best_hand',0):,}</div></div>
      <div class="stat"><div class="lbl">连胜</div>
        <div class="val" style="color:#3fd18a;font-size:20px">{state.get('rounds_won',0)}</div></div>
    </div>
    <div class="ptitle" style="margin:12px 0 6px">打过哪些牌型</div>
    <div class="usewrap">{use_cells or '<div style="color:#6b7d82;font-size:12px">还没出过牌</div>'}</div>
  </div>
</div>
<div class="panel"><div class="ptitle">难度 · 八档（金色=当前，灰勾=已走过）</div>
  <div class="stkwrap">{stake_cells}</div></div>
<div class="panel"><div class="ptitle">挑战模式 · {len(chs)} 种（点开看题记）</div>
  <div class="chlwrap">{ch_cells}</div></div>
<div class="panel"><div class="ptitle">这一局打过的每一手</div>
  {hist_rows or '<div style="color:#6b7d82;font-size:12px">还没出牌</div>'}</div>
<style>
.kv{{display:flex;justify-content:space-between;font-size:13px;padding:6px 2px;
  border-bottom:1px solid #253034;color:#8fa3a8}}
.kv b{{color:#cfe3e8}}
.lvrow{{display:flex;justify-content:space-between;font-size:12px;padding:5px 6px;color:#cfe3e8;
  border-radius:6px}}
.lvrow:hover{{background:#182023}}
.lvn{{color:#009dff;font-weight:800}} .lvu{{color:#6b7d82;width:34px;text-align:right}}
.vchwrap{{display:flex;flex-direction:column;gap:7px}}
.vch{{background:#182a22;border:2px solid #2a4a3a;border-left:3px solid #3fd18a;
  border-radius:8px;padding:8px 10px;position:relative}}
.vn{{font-size:12px;font-weight:800;color:#9fe8c4}}
.vd{{font-size:10px;color:#7fa896;margin-top:2px;line-height:1.4}}
.usewrap{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}}
.ucell{{background:#121a1c;border-radius:7px;padding:6px;text-align:center}}
.un{{font-size:10px;color:#8fa3a8}}
.uv{{font-size:17px;font-weight:900;color:#009dff}}
.stkwrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.stk{{background:#182023;border:2px solid #253034;border-radius:9px;padding:9px;opacity:.55;position:relative}}
.stk.on{{opacity:1;border-color:#f0c04a;background:#2a2418;box-shadow:0 0 14px rgba(240,192,74,.25)}}
.stk.done{{opacity:.8;border-color:#3fd18a}}
.stk.done::before{{content:"✓";position:absolute;top:5px;right:7px;color:#3fd18a;font-weight:900;font-size:12px}}
.stkn{{font-size:13px;font-weight:900;color:#ffe08a}}
.stk:not(.on) .stkn{{color:#8fa3a8}}
.stkd{{font-size:9px;color:#8fa3a8;line-height:1.4;margin-top:4px}}
.chlwrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}}
.chl{{background:#182023;border:2px solid #253034;border-radius:8px;padding:8px;position:relative}}
.chl.on{{border-color:#a45ede;background:#241f2e}}
.chn{{font-size:12px;font-weight:800;color:#cfe3e8}}
.chd{{font-size:9px;color:#8fa3a8;line-height:1.35;margin-top:3px}}
.hrow{{display:flex;gap:14px;font-size:12px;padding:6px 4px;border-bottom:1px solid #253034;color:#8fa3a8}}
.hrow .hs{{margin-left:auto;color:#fff;font-weight:800}} .hrow .ht{{color:#6b7d82}}
</style>"""


def page_table(state, ctx):
    """牌桌：打牌的那一刻"""
    hands, bosses = ctx.get("hands", {}), ctx.get("bosses", {})
    jokers_meta, log = ctx.get("jokers", {}), ctx.get("log", "")
    cards = {c["uid"]: c for c in state.get("cards", [])}
    hand = [cards[u] for u in (state.get("hand") or []) if u in cards]
    this_hand = ctx.get("this_hand") or []
    played = [cards[u] for u in this_hand if u in cards]

    sel_uids = set(ctx.get("selected") or [])
    fresh_uids = set(ctx.get("fresh_uids") or [])
    score, target = state.get("score", 0), state.get("target", 0)
    pct = min(100, int(score * 100 / target)) if target else 0
    blind = {0: "小盲注", 1: "大盲注", 2: "幕主"}.get(state.get("blind", 0), "—")
    bkey = state.get("boss") or ""
    brow = bosses.get(bkey)
    bname = brow[0] if brow else bkey
    brule = brow[1] if brow and len(brow) > 1 else ""
    blore = (ctx.get("lore_bosses") or {}).get(bkey, "")
    battr = f' data-lore="{esc(blore)}" data-name="{esc(bname)}"' if blore else ""

    jk = "".join(joker_html(jokers_meta.get(i.get("id"), {}), i) for i in state.get("jokers", []))
    jk += '<div class="joker empty"></div>' * max(0, 5 - len(state.get("jokers", [])))

    hist = state.get("hand_history") or []
    last = (hist[-1] if hist else {}) if this_hand else {}   # 台上空着时分数也归零
    lkey = state.get("last_hand") or last.get("hand", "")
    lrow = hands.get(lkey)
    lname = lrow[0] if lrow else lkey
    llore = (ctx.get("lore_hands") or {}).get(lkey, "")
    lattr = f' data-lore="{esc(llore)}" data-name="{esc(lname)}"' if llore else ""

    log_html = ""
    for line in (log or "").split("\n"):
        t = line.strip()
        if not t or t.startswith("[STATE]"):
            continue
        cls = ("lg star" if t.startswith("★") else
               "lg lore" if t[:1] in "💌💕" else
               "lg ach" if t[:1] in "💍🏆" else
               "lg call" if t[:1] in "💬💞" else
               "lg good" if t[:1] in "✨🎁💡" else
               "lg play" if t.startswith(("打出：", "结算")) else "lg")
        log_html += f'<div class="{cls}">{esc(t)}</div>'

    return f"""
<div class="statusbar">
  <span class="sdot"></span>
  <span class="stext"><code>{esc((ctx.get("cmd_log") or [{{}}])[-1].get("c", "还没动手"))}</code>{
    (' <span class="sarrow">→</span> <b>' + esc((ctx.get("cmd_log") or [{{}}])[-1]["cards"]) + '</b>')
    if (ctx.get("cmd_log") or [{{}}])[-1].get("cards") else ''}</span>
  <span class="stime">{esc((ctx.get("cmd_log") or [{{}}])[-1].get("t", ""))}</span>
</div>
<div class="tablegrid">
  <div>
    <div class="panel"><div class="ptitle">饰物 {len(state.get('jokers',[]))}/5</div>
      <div style="display:flex;gap:9px">{jk}</div></div>
    <div class="felt">
      <div class="handname"{lattr} style="position:relative">{esc(lname)}</div>
      <div class="scoreline">
        <div class="chip" data-count="{last.get('score',0)}">{last.get('score',0):,}</div><div class="x">分</div>
        <div class="mult">Lv.{(state.get('hand_levels') or {}).get(lkey,1)}</div></div>
      <div class="stage">
        <div class="cards played-row" style="justify-content:center">
          {"".join(card_html(c, fly=i) for i, c in enumerate(played)) or '<div class="stageempty">等着上牌</div>'}</div>
      </div>
    </div>
    <div class="handzone">
      <div class="hlabel">手　牌 {len(hand)} 张</div>
      <div class="cards" style="justify-content:center">
        {"".join(card_html(c, sel=(c["uid"] in sel_uids), fresh=(i if c["uid"] in fresh_uids else None)) for i, c in enumerate(hand))}</div>
    </div>
  </div>
  <div>
    <div class="panel">
      <div class="blindbox"{battr} style="position:relative">
        <div class="bname">{blind}</div>
        {f'<div class="bossname">👑 {esc(bname)}</div><div class="brule">{esc(brule)}</div>' if bkey else ''}
      </div>
      <div class="stat" style="margin-top:10px"><div class="lbl">目标</div>
        <div class="val" style="color:#fe5f55;font-size:22px">{target:,}</div></div>
      <div class="stat" style="margin-top:8px"><div class="lbl">本轮得分</div>
        <div class="val" style="font-size:24px">{score:,}</div>
        <div class="bar"><i style="width:{pct}%"></i></div></div>
      <div class="grid2" style="margin-top:8px">
        <div class="stat"><div class="lbl">出手</div>
          <div class="val" style="color:#009dff;font-size:20px">{state.get('hands_left',0)}</div></div>
        <div class="stat"><div class="lbl">弃牌</div>
          <div class="val" style="color:#fe5f55;font-size:20px">{state.get('discards_left',0)}</div></div>
      </div>
    </div>
    <div class="panel cmdbox"><div class="ptitle">我敲的命令（最近 {len(ctx.get("cmd_log") or [])} 条）</div>
      {"".join('<div class="cmdrow"><span class="ct">' + esc(r.get("t","")) + '</span><code>' + esc(r.get("c","")) + '</code>' + ('<span class="cc">→ ' + esc(r["cards"]) + '</span>' if r.get("cards") else '') + '</div>' for r in reversed((ctx.get("cmd_log") or [])[-14:])) or '<div class="cmdrow" style="color:#6b7d82">还没敲过命令</div>'}
    </div>
    <div class="panel logbox"><div class="ptitle">这一手发生了什么</div>
      {log_html or '<div class="lg">还没出牌</div>'}</div>
  </div>
</div>
<style>
.statusbar{{background:#182023;border:2px solid #2a3a2e;border-left:4px solid #3fd18a;
  border-radius:11px;padding:10px 14px;margin-bottom:12px;display:flex;align-items:center;gap:10px}}
.sdot{{width:9px;height:9px;border-radius:50%;background:#3fd18a;flex-shrink:0;
  box-shadow:0 0 10px #3fd18a;animation:blip 1.8s infinite}}
@keyframes blip{{50%{{opacity:.3;transform:scale(.8)}}}}
.stext{{font-size:13px;color:#cfe3e8;flex:1;line-height:1.45}}
.stext code{{font-family:ui-monospace,Menlo,Consolas,monospace;color:#9fe8c4;
  background:#0f1719;padding:2px 7px;border-radius:5px}}
.stext b{{color:#ffd166;font-size:14px;letter-spacing:1px}}
.sarrow{{color:#5d6f74;margin:0 4px}}
.cc{{color:#ffd166;font-size:11px;margin-left:6px;letter-spacing:1px}}
.stime{{font-size:11px;color:#6b7d82;flex-shrink:0}}
.tablegrid{{display:grid;grid-template-columns:1fr 320px;gap:14px;align-items:start}}
.felt{{background:#1d5b40;border:3px solid #121a1c;border-radius:14px;padding:18px;
  background-image:radial-gradient(circle at 50% 0%,rgba(255,255,255,.06),transparent 60%)}}
.handname{{text-align:center;font-size:16px;font-weight:800;color:#ffd166;letter-spacing:3px;
  margin-bottom:8px;min-height:22px;display:inline-block;width:100%}}
.scoreline{{display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:14px}}
.chip{{background:#009dff;border:3px solid #121a1c;border-radius:10px;padding:6px 18px;
  font-size:26px;font-weight:900;min-width:100px;text-align:center}}
.mult{{background:#fe5f55;border:3px solid #121a1c;border-radius:10px;padding:6px 16px;
  font-size:24px;font-weight:900}}
.x{{font-size:22px;font-weight:900}}
.card.sel{{transform:translateY(-18px);box-shadow:0 0 0 3px #ffd166, 0 10px 18px rgba(0,0,0,.45);
  animation:lift .25s ease backwards}}
@keyframes lift{{from{{transform:translateY(0)}}to{{transform:translateY(-18px)}}}}
.card.fly{{animation:flyin .42s cubic-bezier(.2,.9,.3,1.3) backwards;
  animation-delay:calc(var(--i) * .09s)}}
@keyframes flyin{{
  0%{{transform:translateY(120px) scale(.72) rotate(-8deg);opacity:0}}
  70%{{transform:translateY(-8px) scale(1.06) rotate(2deg);opacity:1}}
  100%{{transform:none;opacity:1}}
}}
.card.fresh{{animation:dealin .38s cubic-bezier(.25,.9,.3,1.2) backwards;
  animation-delay:calc(var(--i) * .07s)}}
@keyframes dealin{{
  0%{{transform:translateY(-70px) rotate(6deg);opacity:0}}
  100%{{transform:none;opacity:1}}
}}
.chip.pop{{animation:pop .3s ease}}
@keyframes pop{{50%{{transform:scale(1.16)}}}}
.stage{{background:rgba(0,0,0,.22);border:2px dashed rgba(255,255,255,.16);border-radius:12px;
  padding:16px 12px;min-height:126px;display:flex;align-items:center;justify-content:center}}
.stageempty{{color:#7fae95;font-size:12px;letter-spacing:3px}}
.played-row .card{{width:70px;height:99px;box-shadow:0 6px 13px rgba(0,0,0,.45)}}
.played-row .card .r{{font-size:16px}} .played-row .card .pip{{font-size:30px}}
.handzone{{background:#1a2225;border:3px solid #121a1c;border-radius:14px;padding:12px;margin-top:12px}}
.handzone .card{{width:62px;height:88px;opacity:.9}}
.handzone .card .r{{font-size:14px}} .handzone .card .s{{font-size:10px}}
.handzone .card .pip{{font-size:26px}}
.handzone .card.sel{{opacity:1}}
.hlabel{{text-align:center;font-size:11px;color:#6b7d82;letter-spacing:4px;margin-bottom:10px}}

.blindbox{{background:#3a4a4e;border:3px solid #121a1c;border-radius:12px;padding:12px;text-align:center}}
.bname{{font-size:19px;font-weight:800;letter-spacing:2px;color:#ffd166}}
.bossname{{font-size:13px;font-weight:800;color:#ff9e2c;margin-top:5px}}
.brule{{font-size:11px;color:#ff8f8f;margin-top:3px;line-height:1.4}}
.bar{{height:8px;background:#0d1214;border-radius:5px;overflow:hidden;margin-top:8px}}
.bar>i{{display:block;height:100%;background:linear-gradient(90deg,#fe5f55,#ffd166)}}
.cmdbox{{max-height:250px;overflow-y:auto}}
.cmdrow{{display:flex;gap:9px;align-items:baseline;font-size:12px;padding:4px 7px;
  border-radius:6px;margin-bottom:3px;background:#141c1f}}
.cmdrow:first-child{{background:#1d2e26;border-left:3px solid #3fd18a}}
.ct{{color:#5d6f74;font-size:10px;flex-shrink:0;font-variant-numeric:tabular-nums}}
.cmdrow code{{color:#9fe8c4;font-family:ui-monospace,Menlo,Consolas,monospace;word-break:break-all}}
.cmdrow:first-child code{{color:#d6ffe9;font-weight:700}}
.logbox{{max-height:520px;overflow-y:auto;display:flex;flex-direction:column;gap:6px}}
.lg{{font-size:12px;line-height:1.55;color:#b9cdd2;padding:5px 8px;border-radius:7px;background:#182023}}
.lg.play{{color:#fff;font-weight:800;background:#243033}}
.lg.star{{color:#ffd4ea;background:#2e1f2a;border-left:3px solid #ff8fd0}}
.lg.ach{{color:#ffe08a;background:#2e2a18;border-left:3px solid #f0c04a;font-weight:700}}
.lg.lore{{color:#d9c4ff;background:#241f2e;border-left:3px solid #a45ede;line-height:1.75}}
.lg.call{{color:#9fe8c4;background:#182a22;border-left:3px solid #3fd18a}}
.lg.good{{color:#8fd9ff;background:#17252e;border-left:3px solid #009dff}}
</style>"""


def page_shop(state, ctx):
    """商店：货架、月币、卡包"""
    shop = state.get("shop") or {}
    items = (shop.get("offers") or []) + (shop.get("packs") or [])
    if shop.get("voucher"):
        items = items + [shop["voucher"]]
    rows = ""
    for it in items:
        kind = it.get("kind")
        lore = ""
        if kind == "joker":
            meta = (ctx.get("jokers") or {}).get(it.get("id"), {})
            name, desc = meta.get("name", it.get("id")), meta.get("desc", "")
            lore = meta.get("lore", "")
            tag, color = "饰物", "#ffd166"
        elif kind == "pack":
            prow = (ctx.get("packs") or {}).get(it.get("id"))
            name = prow[0] if prow else it.get("id")
            size = {"normal": "标准", "jumbo": "加量", "mega": "巨型"}.get(it.get("size", "normal"), "")
            name, desc = f"{size}{name}", ""
            lore = (ctx.get("lore_packs") or {}).get(it.get("id"), "")
            tag, color = "卡包", "#a45ede"
        elif kind == "voucher":
            vrow = (ctx.get("vouchers") or {}).get(it.get("id")) or {}
            name, desc = vrow.get("name", it.get("id")), vrow.get("desc", "")
            lore = (ctx.get("lore_vouchers") or {}).get(it.get("id"), "")
            tag, color = "设施", "#3fd18a"
        else:
            src = {"arcana": ctx.get("arcana"), "planet": ctx.get("planets"),
                   "spectral": ctx.get("spectrals")}.get(kind) or {}
            row = src.get(it.get("id"))
            name = row[0] if row else it.get("id")
            desc = row[1] if row and len(row) > 1 else ""
            tag = {"arcana": "秘仪", "planet": "星图", "spectral": "幻灵"}.get(kind, kind)
            color = "#009dff"
        attr = f' data-lore="{esc(lore)}" data-name="{esc(name)}"' if lore else ""
        attr = f' data-lore="{esc(lore)}" data-name="{esc(name)}"' if lore else ""
        rows += (f'<div class="sc"{attr}><div class="scno">{it.get("shop_id","?")}</div>'
                 f'<div class="sctag" style="background:{color}">{tag}</div>'
                 f'<div class="scname">{esc(name)}</div>'
                 f'<div class="scdesc">{esc(desc)}</div>'
                 f'<div class="sccost">${it.get("cost",0)}</div></div>')

    pack = state.get("pack_state")
    pack_html = ""
    if pack:
        opts = ""
        for i, o in enumerate(pack.get("options", []), 1):
            nm = (o.get("card") and f'{rank_txt(o["card"]["rank"])}{SUIT_SYM.get(o["card"]["suit"],"")}') or o.get("id", "")
            opts += f'<div class="popt">{i}. {esc(nm)}</div>'
        pack_html = (f'<div class="panel"><div class="ptitle">正在拆包 · 还可选 {pack.get("picks",0)} 项</div>'
                     f'{opts}</div>')

    reroll = 0 if state.get("free_rerolls") else state.get("reroll_cost", 0)
    jokers_row = ""
    for inst in state.get("jokers", []):
        jokers_row += joker_html((ctx.get("jokers") or {}).get(inst.get("id"), {}), inst)
    jokers_row += '<div class="joker empty"></div>' * max(0, 5 - len(state.get("jokers", [])))

    return f"""
<div class="shopwrap">
  <div class="shopside">
    <div class="signbox"><div class="sign">SHOP</div><div class="signsub">来变强吧！</div></div>
    <div class="sbtn red">下一个回合</div>
    <div class="sbtn green">重掷 ${reroll}</div>
    <div class="sgrid">
      <div class="sbox"><div class="sl">月币</div><div class="sv gold">${state.get('money',0)}</div></div>
      <div class="sbox"><div class="sl">饰物位</div><div class="sv">{len(state.get('jokers',[]))}/5</div></div>
    </div>
    <div class="sgrid">
      <div class="sbox"><div class="sl">幕</div><div class="sv yel">{state.get('ante',1)}</div></div>
      <div class="sbox"><div class="sl">总分</div><div class="sv small">{state.get('run_score',0):,}</div></div>
    </div>
  </div>
  <div class="shopmain">
    <div class="jokerbar">{jokers_row}<div class="deckcnt">牌库<br><b>{len(state.get('draw',[]) or [])}/{len(state.get('cards',[]))}</b></div></div>
    <div class="shelfbox">
      <div class="shelftitle">有紫点的能点开看题记</div>
      <div class="shelf">{rows or '<div style="color:#9fc4b0;font-size:12px">当前不在商店</div>'}</div>
    </div>
    {pack_html}
  </div>
</div>
<style>
.shopwrap{{display:grid;grid-template-columns:230px 1fr;gap:14px;align-items:start}}
.shopside{{display:flex;flex-direction:column;gap:10px}}
.signbox{{background:#1a2225;border:4px solid #e2334a;border-radius:14px;padding:14px 10px;
  text-align:center;box-shadow:0 0 0 3px #121a1c, 0 0 22px rgba(226,51,74,.35)}}
.sign{{font-size:34px;font-weight:900;color:#ffd166;letter-spacing:3px;
  text-shadow:0 0 8px #ff9e2c,0 0 18px rgba(255,158,44,.7);
  border:3px dotted #ffd166;border-radius:9px;padding:4px 6px}}
.signsub{{font-size:13px;color:#ff8f8f;margin-top:7px;font-weight:800}}
.sbtn{{border:3px solid #121a1c;border-radius:11px;padding:12px;text-align:center;
  font-size:15px;font-weight:900;color:#fff;box-shadow:0 4px 0 rgba(0,0,0,.4)}}
.sbtn.red{{background:#e2334a}} .sbtn.green{{background:#2ea86a}}
.sgrid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.sbox{{background:#121a1c;border:3px solid #0b1113;border-radius:10px;padding:8px;text-align:center}}
.sl{{font-size:10px;color:#8fa3a8}}
.sv{{font-size:21px;font-weight:900;color:#fff}}
.sv.gold{{color:#f0c04a}} .sv.yel{{color:#ffd166}} .sv.small{{font-size:14px;color:#cfe3e8}}
.shopmain{{display:flex;flex-direction:column;gap:12px}}
.jokerbar{{background:#2a6b4c;border:3px solid #121a1c;border-radius:12px;padding:11px;
  display:flex;gap:9px;align-items:center}}
.deckcnt{{margin-left:auto;font-size:10px;color:#bfe0cd;text-align:center;line-height:1.5}}
.deckcnt b{{font-size:14px;color:#fff}}
.shelfbox{{background:#1d5b40;border:3px solid #e2334a;border-radius:14px;padding:16px;
  box-shadow:inset 0 0 0 3px #121a1c;
  background-image:radial-gradient(circle at 50% 0%,rgba(255,255,255,.07),transparent 62%)}}
.shelftitle{{font-size:10px;color:#9fc4b0;letter-spacing:2px;margin-bottom:26px}}
.shelf{{display:flex;gap:18px;flex-wrap:wrap}}
.sc{{width:132px;min-height:178px;background:#fdf6e6;border:3px solid #121a1c;border-radius:11px;
  padding:13px 10px 12px;position:relative;color:#22303a;display:flex;flex-direction:column;
  box-shadow:0 6px 0 rgba(0,0,0,.3);margin-top:12px}}
.sc:hover{{transform:translateY(-5px);transition:.12s}}
.scno{{position:absolute;top:-11px;left:-9px;width:25px;height:25px;border-radius:50%;
  background:#ffd166;border:3px solid #121a1c;display:flex;align-items:center;
  justify-content:center;font-size:11px;font-weight:900;color:#121a1c}}
.sccost{{position:absolute;top:-27px;left:50%;transform:translateX(-50%);background:#f0c04a;
  border:3px solid #121a1c;border-radius:8px;padding:1px 10px;font-size:14px;font-weight:900;
  color:#121a1c;white-space:nowrap}}
.sctag{{align-self:flex-start;font-size:9px;color:#121a1c;padding:2px 7px;border-radius:5px;
  font-weight:900;border:2px solid #121a1c;margin-bottom:7px}}
.scname{{font-size:13px;font-weight:900;line-height:1.2;margin-bottom:6px}}
.scdesc{{font-size:10px;line-height:1.4;color:#4a4a4a;flex:1}}
.sc[data-lore]::after{{bottom:8px;right:8px}}
.popt{{font-size:13px;color:#cfe3e8;padding:7px 10px;background:#182023;border-radius:8px;margin-bottom:6px}}
</style>"""


def page_lore(state, ctx):
    """收藏：464 条题记 + 成就墙"""
    p = state.get("profile") or {}
    got = set(p.get("achievements") or [])
    ach = ctx.get("achievements") or {}
    seen = p.get("seen") or {}

    ach_on, ach_off = "", ""
    for key, a in sorted(ach.items(), key=lambda kv: (kv[0] not in got, kv[0])):
        on = key in got
        if on:
            attr = (f' data-lore="{esc(a.get("lore",""))}" data-name="{esc(a.get("name",key))}"'
                    if a.get("lore") else "")
            ach_on += (f'<div class="ac on"{attr}><div class="an">{esc(a.get("name", key))}</div>'
                       f'<div class="ad">{esc(a.get("desc",""))}</div></div>')
        else:
            ach_off += (f'<div class="ac"><div class="an">？？？</div>'
                        f'<div class="ad">{esc(a.get("hint","") or a.get("desc",""))}</div></div>')
    ach_pct = int(len(got) * 100 / len(ach)) if ach else 0

    # 信物碎片：一句话拆成四片，各自挂在不同成就上
    got_pieces = set(p.get("keepsakes") or [])
    ks_html = ""
    for sid, st_ in (ctx.get("keepsake_sets") or {}).items():
        pieces = st_.get("pieces") if isinstance(st_, dict) else ()
        rows = ""
        have = 0
        for pid, text, need in pieces:
            on = pid in got_pieces
            if on:
                have += 1
            rows += (f'<div class="kp{" on" if on else ""}">'
                     f'{esc(text) if on else "▫▫▫▫▫▫"}</div>')
        ks_html += (f'<div class="kset"><div class="kname">{esc(st_.get("name", sid))}'
                    f'<span class="kcnt">{have}/{len(pieces)}</span></div>{rows}</div>')

    # 构筑共鸣：触发过的才亮出长文（seen_combos 里混存了构筑命名，得分开数）
    seen_all = set(p.get("seen_combos") or [])
    combo_table = ctx.get("combo_lore") or {}
    seen_combos = seen_all & set(combo_table)
    build_names = sorted(seen_all - set(combo_table))
    cb_html = ""
    for name, texts in combo_table.items():
        on = name in seen_combos
        txt = (texts[0] if isinstance(texts, (list, tuple)) else str(texts)) if on else ""
        attr = f' data-lore="{esc(txt)}" data-name="{esc(name)}"' if on else ""
        cb_html += (f'<div class="cb{" on" if on else ""}"{attr}>'
                    f'{esc(name) if on else "？？？"}</div>')
    bn_html = "".join(f'<div class="bn">{esc(x)}</div>' for x in build_names)

    # 宿敌录：跟哪个幕主结过账
    riv = p.get("rivalry") or {}
    bosses_meta = ctx.get("bosses") or {}
    riv_html = ""
    for bid, r in sorted(riv.items(), key=lambda kv: -kv[1].get("encounters", 0)):
        row = bosses_meta.get(bid)
        nm = row[0] if row else bid
        riv_html += (f'<div class="riv"><span class="rn">{esc(nm)}</span>'
                     f'<span class="rw">{r.get("wins",0)}胜</span>'
                     f'<span class="rl">{r.get("losses",0)}负</span>'
                     f'<span class="re">遭遇{r.get("encounters",0)}次</span></div>')

    # 只有这四类真的有题记（挂在各自表的 lore 字段上）
    LORE_TABLES = [("jokers", "饰物"), ("vouchers", "设施"),
                   ("titles", "称号"), ("achievements", "成就")]
    sections = ""
    total = 0
    for cat, label in LORE_TABLES:
        table = ctx.get(cat) or {}
        items = ""
        n = 0
        for key, row in table.items():
            lore = row.get("lore", "") if isinstance(row, dict) else ""
            if not lore:
                continue
            n += 1
            total += 1
            nm = row.get("name", key) if isinstance(row, dict) else key
            items += (f'<div class="lit" data-lore="{esc(lore)}" data-name="{esc(nm)}">'
                      f'{esc(nm)}</div>')
        if items:
            sections += (f'<div class="panel"><div class="ptitle">{label}（{n} 条）</div>'
                         f'<div class="litwrap">{items}</div></div>')

    return f"""
<div class="grid3">
  <div class="stat"><div class="lbl">成就</div>
    <div class="val" style="color:#f0c04a">{len(got)}<span style="font-size:14px;color:#6b7d82">/{len(ach)}</span></div></div>
  <div class="stat"><div class="lbl">题记总数</div>
    <div class="val" style="color:#a45ede">{total}</div></div>
  <div class="stat"><div class="lbl">信物碎片</div>
    <div class="val" style="color:#3fd18a;font-size:22px">{len(p.get('keepsakes') or [])}</div></div>
</div>
<div class="panel">
  <div class="ptitle">成就 · 已解锁 {len(got)} / {len(ach)}</div>
  <div class="pbar"><i style="width:{ach_pct}%"></i><span>{ach_pct}%</span></div>
  <div class="achwall" style="margin-top:12px">{ach_on or '<div style="color:#6b7d82;font-size:12px">一个都还没解锁</div>'}</div>
  <details class="drawer"><summary>还没解锁的 {len(ach)-len(got)} 个（点开看条件）</summary>
    <div class="achwall" style="margin-top:10px">{ach_off}</div></details>
</div>
<div class="panel"><div class="ptitle">信物碎片 · 拼成一句话（{len(got_pieces)} 片已得）</div>
  {ks_html}</div>
{f'<div class="panel"><div class="ptitle">构筑命名 · 游戏给我的牌组起过的名字（{len(build_names)} 个）</div><div class="cbwrap">{bn_html}</div></div>' if bn_html else ''}
<div class="panel"><div class="ptitle">构筑共鸣 · 触发过 {len(seen_combos)}/{len(combo_table)}（要关键组件真实联动+高分才显形，未触发不剧透名字）</div>
  <div class="cbwrap">{cb_html}</div></div>
{f'<div class="panel"><div class="ptitle">宿敌录 · 跟幕主的旧账</div>{riv_html}</div>' if riv_html else ''}
{sections}
<style>
.pbar{{height:22px;background:#121a1c;border-radius:11px;overflow:hidden;position:relative}}
.pbar>i{{display:block;height:100%;background:linear-gradient(90deg,#f0c04a,#ffe08a)}}
.pbar>span{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:900;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.8)}}
.drawer{{margin-top:14px;border-top:1px solid #253034;padding-top:10px}}
.drawer summary{{cursor:pointer;font-size:12px;color:#8fa3a8;padding:6px 10px;
  background:#182023;border-radius:8px;list-style:none;user-select:none}}
.drawer summary:hover{{color:#fff;background:#222d31}}
.drawer summary::-webkit-details-marker{{display:none}}
.drawer summary::before{{content:"▸ ";color:#f0c04a}}
.drawer[open] summary::before{{content:"▾ "}}
.kset{{background:#182023;border-radius:10px;padding:11px 13px;margin-bottom:9px}}
.kname{{font-size:12px;font-weight:800;color:#ffd166;margin-bottom:7px;display:flex;gap:8px;align-items:center}}
.kcnt{{font-size:10px;color:#6b7d82;font-weight:400}}
.kp{{font-size:13px;line-height:1.9;color:#3a4a4e;letter-spacing:2px}}
.kp.on{{color:#d9c4ff}}
.cbwrap{{display:flex;flex-wrap:wrap;gap:7px}}
.cb{{font-size:12px;padding:6px 12px;border-radius:8px;background:#141c1f;color:#3f4e52;
  border:1px solid #253034;position:relative}}
.bn{{font-size:13px;padding:7px 14px;border-radius:8px;background:#2a2418;color:#ffe08a;
  border:2px solid #f0c04a;font-weight:800;letter-spacing:1px}}
.cb.on{{background:#241f2e;color:#d9c4ff;border-color:#a45ede;cursor:help;font-weight:700}}
.riv{{display:flex;gap:12px;align-items:baseline;font-size:12px;padding:6px 8px;
  border-bottom:1px solid #253034;color:#8fa3a8}}
.rn{{color:#ff9e2c;font-weight:800;min-width:70px}}
.rw{{color:#3fd18a}} .rl{{color:#fe5f55}}
.re{{margin-left:auto;color:#6b7d82;font-size:11px}}
.achwall{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}}
.ac{{background:#182023;border:2px solid #253034;border-radius:9px;padding:8px;opacity:.42}}
.ac.on{{opacity:1;border-color:#f0c04a;background:#2a2418;cursor:help;position:relative}}
.an{{font-size:11px;font-weight:800;color:#ffe08a;line-height:1.2}}
.ac:not(.on) .an{{color:#5d6b70}}
.ad{{font-size:9px;color:#8fa3a8;line-height:1.35;margin-top:3px}}
.litwrap{{display:flex;flex-wrap:wrap;gap:6px}}
.lit{{font-size:12px;padding:5px 11px;border-radius:8px;background:#182023;color:#cfe3e8;
  cursor:help;position:relative;border:1px solid #253034}}
.lit:hover{{background:#2a2136;border-color:#a45ede;color:#fff}}
.lit.dim{{opacity:.45}}
.lit::after{{display:none}}
</style>"""


def dump_all(state, outdir, **ctx):
    """一次生成四页。ctx 里塞游戏的各种表（jokers/hands/bosses/achievements/log/...）"""
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    live = ctx.pop("live", False)
    pages = [("主界面", page_home), ("牌桌", page_table),
             ("商店", page_shop), ("收藏", page_lore), ("往事", page_hall)]
    for name, fn in pages:
        html = shell(name, name, fn(state, ctx), state=state, live=live)
        (out / f"{name}.html").write_text(html, encoding="utf-8")
    return [str(out / f"{n}.html") for n, _ in pages]


def page_hall(state, ctx):
    """往事：名人堂——每一局的构筑名、结局、战绩、留信"""
    p = state.get("profile") or {}
    rows = p.get("hall_of_fame") or p.get("history") or []
    jk = ctx.get("jokers") or {}
    hands = ctx.get("hands") or {}
    decks = ctx.get("decks") or {}
    stakes = ctx.get("stakes") or {}

    wins = sum(1 for r in rows if r.get("outcome") == "通关")
    best = max((int(r.get("best_hand") or 0) for r in rows), default=0)
    top = max((int(r.get("score") or 0) for r in rows), default=0)

    cards = ""
    for r in reversed(rows[-60:]):
        oc = r.get("outcome", "")
        cls = ("hw" if oc == "通关" else "hl" if oc == "落败" else "hr")
        jnames = "、".join(jk.get(x, {}).get("name", x) for x in (r.get("jokers") or [])[:5])
        fav = hands.get(r.get("favorite_hand"))
        fav = fav[0] if fav else (r.get("favorite_hand") or "—")
        dk = decks.get(r.get("deck"))
        dk = dk[0] if dk else r.get("deck", "")
        stk = stakes.get(r.get("stake"))
        stk = stk[0] if stk else ""
        letter = r.get("letter") or ""
        cards += (
            f'<div class="hcard {cls}">'
            f'<div class="hhead"><span class="hno">#{r.get("attempt","?")}</span>'
            f'<span class="hbuild">{esc(r.get("build_name") or "未命名构筑")}</span>'
            f'<span class="houtcome">{esc(oc)}</span></div>'
            f'<div class="hmeta">第{r.get("ante","?")}幕 · {esc(dk)} · {esc(stk)}'
            f' · 主牌型 {esc(fav)} · seed {r.get("seed","?")}</div>'
            f'<div class="hnums"><span>总分 <b>{int(r.get("score") or 0):,}</b></span>'
            f'<span>最高单手 <b>{int(r.get("best_hand") or 0):,}</b></span></div>'
            + (f'<div class="hjk">{esc(jnames)}</div>' if jnames else "")
            + (f'<div class="hletter">💌 “{esc(letter)}”</div>' if letter else "")
            + "</div>")

    return f"""
<div class="grid3">
  <div class="stat"><div class="lbl">打过多少局</div>
    <div class="val" style="color:#cfe3e8">{len(rows)}</div></div>
  <div class="stat"><div class="lbl">通关</div>
    <div class="val" style="color:#f0c04a">{wins}</div></div>
  <div class="stat"><div class="lbl">历史最高单手</div>
    <div class="val" style="color:#ff8fd0;font-size:21px">{best:,}</div></div>
</div>
<div class="panel"><div class="ptitle">月下名人堂 · 每一局都记着（最近 {min(60, len(rows))} 条，新的在上）</div>
  <div class="hwrap">{cards or '<div style="color:#6b7d82;font-size:12px">还没有任何一局被记下来</div>'}</div>
</div>
<style>
.hwrap{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.hcard{{background:#182023;border:2px solid #253034;border-left:4px solid #3f4e52;
  border-radius:10px;padding:11px 13px}}
.hcard.hw{{border-left-color:#f0c04a;background:#241f14}}
.hcard.hl{{border-left-color:#fe5f55}}
.hcard.hr{{border-left-color:#6b7d82;opacity:.75}}
.hhead{{display:flex;gap:8px;align-items:baseline;margin-bottom:5px}}
.hno{{font-size:10px;color:#5d6f74;font-variant-numeric:tabular-nums}}
.hbuild{{font-size:14px;font-weight:900;color:#ffd166;flex:1}}
.houtcome{{font-size:11px;color:#8fa3a8;background:#0f1719;padding:1px 8px;border-radius:5px}}
.hcard.hw .houtcome{{color:#121a1c;background:#f0c04a;font-weight:800}}
.hmeta{{font-size:10px;color:#6b7d82;line-height:1.5}}
.hnums{{display:flex;gap:14px;font-size:11px;color:#8fa3a8;margin-top:5px}}
.hnums b{{color:#fff;font-size:13px}}
.hjk{{font-size:10px;color:#7fa896;margin-top:5px;line-height:1.4}}
.hletter{{font-size:12px;color:#d9c4ff;margin-top:7px;line-height:1.6;
  border-top:1px solid #253034;padding-top:6px}}
@media (max-width:820px){{
  .hwrap{{grid-template-columns:1fr}}
  .hbuild{{font-size:13px}}
}}
</style>"""


def dump_one(state, outpath, **ctx):
    """四页合成一个 html：页内 tab 切换，一个文件就是全部。"""
    live = ctx.pop("live", False)
    pages = [("主界面", page_home), ("牌桌", page_table),
             ("商店", page_shop), ("收藏", page_lore), ("往事", page_hall)]
    tabs = "".join(
        f'<a href="#" class="tab{" on" if i == 1 else ""}" data-tab="{n}">{n}</a>'
        for i, (n, _) in enumerate(pages))
    bodies = "".join(
        f'<div class="tabpage" data-page="{n}"'
        f'{"" if n == "牌桌" else " style=display:none"}>{fn(state, ctx)}</div>'
        for n, fn in pages)
    st = state
    right = (f'第 <b>{st.get("ante",1)}</b> 幕 · 月币 <b>${st.get("money",0)}</b>'
             f' · 总分 <b>{st.get("run_score",0):,}</b>')
    refresh = '<meta http-equiv="refresh" content="5">' if live else ""
    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">{refresh}
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>月幕万象</title><style>{CSS}
.tab{{cursor:pointer}}
</style></head><body>
<div class="nav"><div class="logo">🌙 月幕万象</div>{tabs}<div class="right">{right}</div></div>
<div class="wrap">{bodies}</div>
{SCRIPT}
<script>
(function(){{
  var KEY='moonlit_tab', SCR='moonlit_scroll', PK='moonlit_play';
  function go(name, keep){{
    document.querySelectorAll('.tab').forEach(function(x){{
      x.classList.toggle('on', x.dataset.tab===name);
    }});
    document.querySelectorAll('.tabpage').forEach(function(p){{
      p.style.display = (p.dataset.page===name)?'':'none';
    }});
    if(!keep) window.scrollTo(0,0);
  }}
  // 自动刷新后回到刚才那一页、刚才那个位置
  try{{
    var saved=localStorage.getItem(KEY);
    if(saved && document.querySelector('[data-page="'+saved+'"]')) go(saved, true);
    var y=parseInt(localStorage.getItem(SCR)||'0',10);
    if(y>0) window.scrollTo(0,y);
  }}catch(e){{}}
  document.querySelectorAll('.tab').forEach(function(t){{
    t.addEventListener('click',function(e){{
      e.preventDefault();
      try{{ localStorage.setItem(KEY,t.dataset.tab); localStorage.setItem(SCR,'0'); }}catch(err){{}}
      go(t.dataset.tab,false);
    }});
  }});
  var tick=null;
  window.addEventListener('scroll',function(){{
    clearTimeout(tick);
    tick=setTimeout(function(){{
      try{{ localStorage.setItem(SCR,String(window.scrollY||0)); }}catch(e){{}}
    }},120);
  }},{{passive:true}});
  // 内容没变就不重播动画（治整页刷新的抖动）
  var chip=document.querySelector('.chip[data-count]');
  var sig=(document.querySelector('.handname')||{{}}).textContent||'';
  sig += '|' + (chip?chip.dataset.count:'');
  document.querySelectorAll('.played-row .card, .handzone .card').forEach(function(c){{
    sig += '|' + (c.textContent||'').trim();
  }});
  var isNew=false;
  try{{ isNew=(localStorage.getItem(PK)!==sig); localStorage.setItem(PK,sig); }}catch(e){{ isNew=true; }}
  if(!isNew){{
    document.querySelectorAll('.card.fly, .card.fresh').forEach(function(c){{c.style.animation='none'}});
  }} else if(chip){{
    var end=parseInt(chip.dataset.count||'0',10), t0=null, dur=620;
    if(end>0){{
      chip.classList.add('pop');
      var step=function(ts){{
        if(!t0) t0=ts;
        var k=Math.min(1,(ts-t0)/dur), e=1-Math.pow(1-k,3);
        chip.textContent=Math.round(end*e).toLocaleString();
        if(k<1) requestAnimationFrame(step);
      }};
      requestAnimationFrame(step);
    }}
  }}
}})();
</script>
</body></html>"""
    Path(outpath).write_text(html, encoding="utf-8")
    return str(outpath)
