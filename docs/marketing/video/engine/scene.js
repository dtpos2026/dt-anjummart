/* Anjum Mart reel engine: builds one scene from a plan and draws any moment with window.__seek(t).
   Everything is a pure function of the time t, so the frames are identical on every run (see render.mjs). */
(function () {
  'use strict';
  var W = 1080, H = 1920;
  var clamp = function (x, a, b) { a = a === undefined ? 0 : a; b = b === undefined ? 1 : b; return Math.min(b, Math.max(a, x)); };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var tw = function (t, a, b) { return clamp((t - a) / (b - a)); };
  var E = {
    lin: function (x) { return x; },
    outCubic: function (x) { return 1 - Math.pow(1 - x, 3); },
    inCubic: function (x) { return x * x * x; },
    inOut: function (x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; },
    outBack: function (x) { var c1 = 1.2, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    outQuint: function (x) { return 1 - Math.pow(1 - x, 5); }
  };
  function rnd(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function mk(parent, cls, css, tag) {
    var e = document.createElement(tag || 'div');
    if (cls) e.className = cls;
    if (css) e.style.cssText = css;
    parent.appendChild(e);
    return e;
  }
  function loadImg(src) {
    return new Promise(function (res, rej) {
      var i = new Image();
      i.onload = function () { res(i); };
      i.onerror = function () { rej(new Error('image failed: ' + src)); };
      i.src = src;
    });
  }
  function fitText(span, max, minPx) {
    var fs = parseFloat(getComputedStyle(span).fontSize);
    while (span.offsetWidth > max && fs > (minPx || 40)) { fs -= 2; span.style.fontSize = fs + 'px'; }
  }
  function line(parent, cls, text, top, width) {
    var box = mk(parent, 'abs center line ' + cls, 'top:' + top + 'px;left:' + ((W - width) / 2) + 'px;width:' + width + 'px;text-align:center');
    var s = mk(box, '', '', 'span');
    s.textContent = text;
    return { box: box, span: s };
  }
  function reveal(l, p, dy) {
    // line mask reveal: the text rises out of its own box
    l.span.style.transform = 'translateY(' + ((1 - p) * (dy || 110)) + '%)';
    l.box.style.opacity = p > 0 ? 1 : 0;
  }

  var P = null, S = {};
  var WA = '<svg viewBox="0 0 32 32" fill="#111"><path d="M16.04 3C9.4 3 4 8.38 4 15.02c0 2.12.55 4.2 1.6 6.03L4 29l8.14-1.56a12.02 12.02 0 0 0 3.9.65C22.68 28.09 28 22.7 28 16.07 28 9.4 22.7 3 16.04 3zm0 22.1c-1.2 0-2.38-.3-3.42-.87l-.5-.27-4.83.93.96-4.7-.3-.52a9.1 9.1 0 0 1-1.4-4.84c0-5.03 4.1-9.1 9.15-9.1 5.02 0 9.1 4.07 9.1 9.1 0 5.04-4.08 9.27-8.76 9.27zm5.1-6.9c-.28-.14-1.65-.82-1.9-.9-.26-.1-.44-.14-.63.14-.19.28-.72.9-.88 1.1-.16.18-.32.2-.6.07-.28-.14-1.18-.44-2.25-1.4-.83-.74-1.4-1.66-1.56-1.94-.16-.28-.02-.43.12-.57.13-.12.28-.32.42-.48.14-.16.19-.28.28-.47.1-.19.05-.35-.02-.5-.07-.14-.63-1.5-.86-2.06-.23-.54-.46-.47-.63-.48h-.54c-.19 0-.5.07-.76.35-.26.28-1 .97-1 2.38s1.03 2.76 1.17 2.95c.14.19 2.02 3.08 4.9 4.32.68.3 1.22.47 1.63.6.69.22 1.31.19 1.8.11.55-.08 1.65-.67 1.88-1.32.23-.65.23-1.2.16-1.32-.07-.12-.26-.19-.54-.33z"/></svg>';

  /* ---------- shared pieces ------------------------------------------------------------------------------------- */
  function buildBackdrop() {
    var bk = document.getElementById('bokehs');
    var r = rnd(7);
    S.bokeh = [];
    for (var i = 0; i < 18; i++) {
      var size = 50 + r() * 150;
      var e = mk(bk, 'abs bk', 'width:' + size + 'px;height:' + size + 'px;opacity:0');
      S.bokeh.push({ e: e, x: r() * W, y: r() * H, v: 14 + r() * 34, a: 0.1 + r() * 0.22, ph: r() * 6.28, sz: size });
    }
    var g = document.getElementById('grain').getContext('2d');
    var id = g.createImageData(600, 1020);
    var rr = rnd(99);
    for (var k = 0; k < id.data.length; k += 4) { var v = rr() * 255; id.data[k] = id.data[k + 1] = id.data[k + 2] = v; id.data[k + 3] = 255; }
    g.putImageData(id, 0, 0);
    S.grain = document.getElementById('grain');
    S.bg = document.getElementById('bg');
    S.rays = document.getElementById('rays');
    S.glow2 = document.getElementById('glow2');
    S.flash = document.getElementById('flash');
    document.getElementById('grain').style.transform = 'scale(2)';
    document.getElementById('grain').style.transformOrigin = '0 0';
  }
  function drawBackdrop(t) {
    S.bg.style.transform = 'scale(' + (1 + 0.05 * (t / P.duration)) + ')';
    S.rays.style.transform = 'rotate(' + (t * 2.2) + 'deg)';
    S.rays.style.opacity = P.rays === undefined ? 0.55 : P.rays;
    S.glow2.style.opacity = 0.6 + 0.4 * Math.sin(t * 0.8);
    S.bokeh.forEach(function (b) {
      var y = ((b.y - t * b.v) % (H + 300) + (H + 300)) % (H + 300) - 150;
      var x = b.x + Math.sin(t * 0.4 + b.ph) * 30;
      b.e.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      b.e.style.opacity = (b.a * (0.6 + 0.4 * Math.sin(t * 0.9 + b.ph))).toFixed(3);
    });
    var f = Math.floor(t * 30);
    var gx = (f * 53) % 60, gy = (f * 97) % 60;
    S.grain.style.left = (-gx) + 'px';
    S.grain.style.top = (-gy) + 'px';
  }
  function buildEnd(startT) {
    var c = document.getElementById('endcard');
    c.style.background = 'radial-gradient(ellipse 80% 55% at 50% 48%,rgba(77,57,16,.0),rgba(0,0,0,.0))';
    var o = {};
    o.start = startT;
    o.logo = mk(c, 'abs prod', 'left:' + ((W - 470) / 2) + 'px;top:520px;width:470px', 'img');
    o.logo.src = P.assets.logo;
    o.tag = line(c, 'title', 'Timeless Style. Everyday Luxury.', 1010, 960);
    o.tag.box.style.font = '600 58px/1.2 Cormorant,serif';
    o.tag.span.style.font = '600 58px/1.2 Cormorant,serif';
    o.rule = mk(c, 'abs rule', 'left:' + ((W - 360) / 2) + 'px;top:1100px;width:360px;opacity:0');
    o.url = line(c, 'sub', 'anjummart.com', 1140, 800);
    o.url.span.style.font = '500 46px/1.2 Jost,sans-serif';
    o.url.span.style.letterSpacing = '6px';
    o.url.span.style.color = '#f1d98a';
    o.cta = mk(c, 'abs cta', 'left:50%;top:1290px;opacity:0');
    o.cta.innerHTML = WA + 'ORDER ON WHATSAPP';
    o.chips = mk(c, 'abs center chips', 'top:1440px;opacity:0;text-align:center');
    o.chips.textContent = 'Free Delivery All Pakistan  ·  Cash on Delivery';
    S.end = o;
    S.endEl = c;
  }
  function drawEnd(t) {
    var o = S.end, c = S.endEl, s = o.start;
    var a = tw(t, s, s + 0.5);
    c.style.opacity = a;
    if (a <= 0) return;
    var p1 = E.outCubic(tw(t, s + 0.05, s + 0.8));
    o.logo.style.opacity = p1;
    o.logo.style.transform = 'translateY(' + ((1 - p1) * 50) + 'px) scale(' + lerp(0.92, 1, p1) + ')';
    reveal(o.tag, E.outCubic(tw(t, s + 0.45, s + 1.05)));
    o.rule.style.opacity = tw(t, s + 0.7, s + 1.1);
    o.rule.style.transform = 'scaleX(' + E.outCubic(tw(t, s + 0.7, s + 1.3)) + ')';
    reveal(o.url, E.outCubic(tw(t, s + 0.85, s + 1.35)));
    var pc = E.outBack(tw(t, s + 1.1, s + 1.65));
    var pulse = 1 + 0.03 * Math.sin((t - s) * 5);
    o.cta.style.opacity = tw(t, s + 1.1, s + 1.4);
    o.cta.style.transform = 'translateX(-50%) translateY(' + ((1 - pc) * 40) + 'px) scale(' + (pc * pulse) + ')';
    o.chips.style.opacity = tw(t, s + 1.5, s + 1.9) * 0.95;
  }
  function flashAt(t, t0, peak) {
    var d = t - t0;
    if (d < 0 || d > 0.45) return 0;
    return peak * (d < 0.06 ? d / 0.06 : Math.pow(1 - (d - 0.06) / 0.39, 2));
  }

  /* ---------- product reel ---------------------------------------------------------------------------------------- */
  function sizeFor(kind, nw, nh) {
    if (kind === 'photo') return { w: 600, h: 800 };
    if (kind === 'jewellery') { var w = 900, h = w * nh / nw; if (h > 740) { h = 740; w = h * nw / nh; } return { w: w, h: h }; }
    var hh = 820; return { w: hh * nw / nh, h: hh };
  }
  function makeProduct(parent, item, kind) {
    // returns {wrap, img, shine, reflect, w, h}
    var o = { kind: kind };
    o.wrap = mk(parent, 'abs prod', 'left:0;top:0;width:0;height:0');
    if (kind === 'photo') {
      o.w = 600; o.h = 800;
      o.glow = mk(o.wrap, 'abs', 'left:-560px;top:-560px;width:1120px;height:1120px;background:radial-gradient(circle,rgba(212,175,55,.28),rgba(212,175,55,0) 62%)');
      o.card = mk(o.wrap, 'abs card', 'left:' + (-o.w / 2) + 'px;top:' + (-o.h / 2) + 'px;width:' + o.w + 'px;height:' + o.h + 'px;overflow:hidden');
      o.inner = mk(o.card, 'abs', 'inset:0;background-size:cover;background-position:center;background-image:url(' + item.src + ')');
      o.shine = mk(o.card, 'abs', 'inset:0;background:linear-gradient(100deg,rgba(255,255,255,0) 38%,rgba(255,255,255,.55) 50%,rgba(255,255,255,0) 62%);background-size:300% 100%;background-position:150% 0;mix-blend-mode:soft-light');
      return o;
    }
    var d = sizeFor(kind, item.nw, item.nh);
    o.w = d.w; o.h = d.h;
    o.glow = mk(o.wrap, 'abs', 'left:-620px;top:-620px;width:1240px;height:1240px;background:radial-gradient(circle,rgba(212,175,55,.30),rgba(212,175,55,0) 60%)');
    o.floor = mk(o.wrap, 'abs', 'left:' + (-d.w * 0.55) + 'px;top:' + (d.h / 2 + 34) + 'px;width:' + (d.w * 1.1) + 'px;height:70px;background:radial-gradient(ellipse,rgba(0,0,0,.8),rgba(0,0,0,0) 70%)');
    o.reflect = mk(o.wrap, 'abs', 'left:' + (-d.w / 2) + 'px;top:' + (d.h / 2 + 18) + 'px;width:' + d.w + 'px;height:' + (d.h * 0.2) + 'px;opacity:.16;overflow:hidden;-webkit-mask-image:linear-gradient(to bottom,#000,transparent);mask-image:linear-gradient(to bottom,#000,transparent)');
    var ri = mk(o.reflect, 'abs', 'left:0;top:' + (-d.h * 0.55) + 'px;width:' + d.w + 'px;height:' + d.h + 'px;transform:scaleY(-1)', 'img');
    ri.src = item.src;
    o.img = mk(o.wrap, 'abs', 'left:' + (-d.w / 2) + 'px;top:' + (-d.h / 2) + 'px;width:' + d.w + 'px;height:' + d.h + 'px;filter:drop-shadow(0 34px 44px rgba(0,0,0,.65))', 'img');
    o.img.src = item.src;
    o.shine = mk(o.wrap, 'abs', 'left:' + (-d.w / 2) + 'px;top:' + (-d.h / 2) + 'px;width:' + d.w + 'px;height:' + d.h + 'px;-webkit-mask-image:url(' + item.src + ');mask-image:url(' + item.src + ');-webkit-mask-size:100% 100%;mask-size:100% 100%;background:linear-gradient(100deg,rgba(255,255,255,0) 36%,rgba(255,255,255,.95) 50%,rgba(255,255,255,0) 64%);background-size:320% 100%;background-position:160% 0;opacity:.0');
    return o;
  }
  function placeProduct(o, x, y, sc, rot, op, blur) {
    o.wrap.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) rotate(' + rot.toFixed(2) + 'deg) scale(' + sc.toFixed(4) + ')';
    o.wrap.style.opacity = op.toFixed(3);
    var f = blur > 0.3 ? 'blur(' + blur.toFixed(1) + 'px)' : 'none';
    o.wrap.style.filter = f;
  }
  function sweep(o, p, strength) {
    // p 0..1: light slides across the product only
    if (!o.shine) return;
    if (p <= 0 || p >= 1) { o.shine.style.opacity = 0; return; }
    o.shine.style.opacity = strength * Math.sin(p * Math.PI);
    o.shine.style.backgroundPosition = lerp(160, -60, p) + '% 0';
  }

  function initProduct() {
    var pr = P.product;
    var kind = pr.kind;
    var content = document.getElementById('content');
    S.sting = mk(content, 'abs prod', 'left:' + ((W - 300) / 2) + 'px;top:' + (H / 2 - 190) + 'px;width:300px;opacity:0', 'img');
    S.sting.src = P.assets.mark;
    S.hair = mk(content, 'abs rule', 'left:' + (W / 2 - 220) + 'px;top:' + (H / 2 + 150) + 'px;width:440px;opacity:0');
    S.prod = makeProduct(content, pr, kind);
    S.eb = line(content, 'eyebrow', pr.eyebrow, 296, 960);
    S.ti = line(content, 'title', pr.title, 346, 960);
    S.su = line(content, 'sub', pr.sub, 468, 960);
    S.ru = mk(content, 'abs rule', 'left:' + ((W - 520) / 2) + 'px;top:546px;width:520px;opacity:0');
    S.price = mk(content, 'abs center price', 'top:1392px;opacity:0;text-align:center');
    S.price.textContent = pr.price;
    S.chips = mk(content, 'abs center chips', 'top:1536px;opacity:0;text-align:center');
    S.chips.textContent = 'Free Delivery All Pakistan  ·  Cash on Delivery';
    S.pline = mk(content, 'abs rule', 'left:' + ((W - 300) / 2) + 'px;top:1518px;width:300px;opacity:0');
    fitText(S.ti.span, 940);
    fitText(S.su.span, 940, 24);
    buildEnd(P.endStart);
  }
  function drawProduct(t) {
    var T = P.t;
    var reveal0 = T.reveal;
    // brand sting
    var sp = E.outCubic(tw(t, 0.1, 0.75));
    S.sting.style.opacity = sp * (1 - tw(t, reveal0 - 0.25, reveal0));
    S.sting.style.transform = 'scale(' + (lerp(0.86, 1.02, sp) + 0.04 * Math.sin(t * 3)) + ')';
    S.hair.style.opacity = tw(t, 0.25, 0.6) * (1 - tw(t, reveal0 - 0.25, reveal0));
    S.hair.style.transform = 'scaleX(' + E.outCubic(tw(t, 0.25, 1.0)) + ')';
    // product
    var pp = tw(t, reveal0, reveal0 + 1.25);
    var e = E.outBack(pp);
    var out = E.inCubic(tw(t, T.out, T.out + 0.55));
    var sc = lerp(1.32, 1.0, e) * (1 + (S.prod.kind === 'photo' ? 0.025 : 0.065) * tw(t, reveal0 + 1.25, T.out)) * lerp(1, 0.94, out);
    var fy = t > reveal0 + 1.2 ? Math.sin((t - reveal0 - 1.2) * 1.5) * 10 : 0;
    var y = P.cy + lerp(90, 0, e) + fy - out * 40;
    var rot = Math.sin((t - reveal0) * 0.9) * 1.4;
    var op = tw(t, reveal0, reveal0 + 0.5) * (1 - out);
    var blur = lerp(16, 0, tw(t, reveal0, reveal0 + 0.9));
    placeProduct(S.prod, W / 2, y, sc, S.prod.kind === 'photo' ? rot * 0.5 : rot, op, blur);
    if (S.prod.inner) S.prod.inner.style.transform = 'scale(' + (1.06 + 0.1 * tw(t, reveal0, T.out)) + ')';
    if (S.prod.reflect) S.prod.reflect.style.opacity = 0.16 * (1 - 0.8 * tw(t, T.price, T.price + 0.5));
    sweep(S.prod, tw(t, reveal0 + 0.7, reveal0 + 1.7), 0.7);
    if (t > reveal0 + 3.2) sweep(S.prod, tw(t, T.shine2, T.shine2 + 1.0), 0.7);
    // text
    var tx = T.text;
    reveal(S.eb, E.outCubic(tw(t, tx, tx + 0.7)), 140);
    reveal(S.ti, E.outCubic(tw(t, tx + 0.1, tx + 0.9)), 120);
    reveal(S.su, E.outCubic(tw(t, tx + 0.3, tx + 1.0)), 140);
    S.ru.style.opacity = tw(t, tx + 0.45, tx + 0.8);
    S.ru.style.transform = 'scaleX(' + E.outCubic(tw(t, tx + 0.45, tx + 1.2)) + ')';
    var fade = 1 - out;
    [S.eb, S.ti, S.su].forEach(function (l) { l.box.style.opacity = (parseFloat(l.box.style.opacity) || 0) * fade; });
    S.ru.style.opacity = parseFloat(S.ru.style.opacity) * fade;
    // price
    var pr = T.price;
    var pe = E.outBack(tw(t, pr, pr + 0.7));
    S.price.style.opacity = tw(t, pr, pr + 0.35) * fade;
    S.price.style.transform = 'translateY(' + ((1 - pe) * 60) + 'px) scale(' + lerp(0.9, 1, pe) + ')';
    S.pline.style.opacity = tw(t, pr + 0.3, pr + 0.6) * fade;
    S.pline.style.transform = 'scaleX(' + E.outCubic(tw(t, pr + 0.3, pr + 1.0)) + ')';
    S.chips.style.opacity = tw(t, pr + 0.55, pr + 0.95) * fade * 0.95;
    S.flash.style.opacity = flashAt(t, reveal0, 0.32) + flashAt(t, P.endStart, 0.14);
    drawEnd(t);
  }

  /* ---------- collection reel -------------------------------------------------------------------------------------- */
  function initCollection() {
    var content = document.getElementById('content');
    var c = P.coll;
    S.intro = {};
    S.intro.mark = mk(content, 'abs prod', 'left:' + ((W - 260) / 2) + 'px;top:560px;width:260px;opacity:0', 'img');
    S.intro.mark.src = P.assets.mark;
    S.intro.eb = line(content, 'eyebrow', c.eyebrow, 900, 960);
    S.intro.ti = line(content, 'title', c.title, 960, 980);
    S.intro.su = line(content, 'sub', c.sub, 1100, 960);
    S.intro.ru = mk(content, 'abs rule', 'left:' + ((W - 520) / 2) + 'px;top:1188px;width:520px;opacity:0');
    fitText(S.intro.ti.span, 960);
    S.items = P.items.map(function (it, i) {
      var o = {};
      o.p = makeProduct(content, it, it.kind);
      o.eb = line(content, 'eyebrow', it.eyebrow, 296, 960);
      o.ti = line(content, 'title', it.title, 346, 960);
      o.su = line(content, 'sub', it.sub, 468, 960);
      fitText(o.ti.span, 940);
      fitText(o.su.span, 940, 24);
      o.price = mk(content, 'abs center price', 'top:1392px;opacity:0;text-align:center');
      o.price.textContent = it.price;
      o.count = mk(content, 'abs count', 'left:70px;top:236px;opacity:0');
      o.count.textContent = ('0' + (i + 1)).slice(-2) + ' / ' + ('0' + P.items.length).slice(-2);
      return o;
    });
    S.cchips = mk(content, 'abs center chips', 'top:1536px;opacity:0;text-align:center');
    S.cchips.textContent = 'Free Delivery All Pakistan  ·  Cash on Delivery';
    buildEnd(P.endStart);
  }
  function drawCollection(t) {
    var T = P.t;
    // intro
    var ip = E.outCubic(tw(t, 0.15, 0.8));
    var iOut = E.inCubic(tw(t, T.introOut, T.introOut + 0.4));
    S.intro.mark.style.opacity = ip * (1 - iOut);
    S.intro.mark.style.transform = 'scale(' + lerp(0.86, 1.04, ip) + ')';
    reveal(S.intro.eb, E.outCubic(tw(t, 0.35, 1.0)), 140);
    reveal(S.intro.ti, E.outCubic(tw(t, 0.5, 1.3)), 120);
    reveal(S.intro.su, E.outCubic(tw(t, 0.8, 1.5)), 140);
    S.intro.ru.style.opacity = tw(t, 0.9, 1.2);
    S.intro.ru.style.transform = 'scaleX(' + E.outCubic(tw(t, 0.9, 1.6)) + ')';
    [S.intro.eb, S.intro.ti, S.intro.su].forEach(function (l) { l.box.style.opacity = (parseFloat(l.box.style.opacity) || 0) * (1 - iOut); });
    S.intro.ru.style.opacity = parseFloat(S.intro.ru.style.opacity) * (1 - iOut);
    // slots
    var anyShown = false;
    S.items.forEach(function (o, i) {
      var s = P.slots[i];
      var inP = E.outQuint(tw(t, s.start, s.start + 0.6));
      var outP = E.inCubic(tw(t, s.end - 0.4, s.end));
      var vis = t >= s.start - 0.01 && t <= s.end + 0.01;
      var on = vis ? 1 : 0;
      o.p.wrap.style.visibility = vis ? 'visible' : 'hidden';
      ['eb', 'ti', 'su'].forEach(function (k) { o[k].box.style.visibility = vis ? 'visible' : 'hidden'; });
      o.price.style.visibility = vis ? 'visible' : 'hidden';
      o.count.style.visibility = vis ? 'visible' : 'hidden';
      if (!vis) return;
      anyShown = true;
      var x = W / 2 + lerp(720, 0, inP) - outP * 720;
      var fy = Math.sin((t - s.start) * 1.5 + i) * 9;
      var sc = (1 + (o.p.kind === 'photo' ? 0.025 : 0.06) * tw(t, s.start, s.end)) * lerp(0.9, 1, inP);
      if (o.p.reflect) o.p.reflect.style.opacity = 0.16 * (1 - 0.8 * tw(t, s.start + 0.7, s.start + 1.1));
      var blur = lerp(26, 0, inP) + outP * 18;
      placeProduct(o.p, x, P.cy + fy, sc, Math.sin((t - s.start) * 0.9) * 1.3 * (o.p.kind === 'photo' ? 0.4 : 1), (1 - outP) * tw(t, s.start, s.start + 0.2), blur);
      if (o.p.inner) o.p.inner.style.transform = 'scale(' + (1.06 + 0.12 * tw(t, s.start, s.end)) + ')';
      sweep(o.p, tw(t, s.start + 0.5, s.start + 1.4), 0.65);
      var tx = s.start + 0.25;
      reveal(o.eb, E.outCubic(tw(t, tx, tx + 0.55)), 140);
      reveal(o.ti, E.outCubic(tw(t, tx + 0.08, tx + 0.7)), 120);
      reveal(o.su, E.outCubic(tw(t, tx + 0.2, tx + 0.8)), 140);
      var fo = 1 - outP;
      ['eb', 'ti', 'su'].forEach(function (k) { o[k].box.style.opacity = parseFloat(o[k].box.style.opacity) * fo; });
      var pe = E.outBack(tw(t, s.start + 0.7, s.start + 1.3));
      o.price.style.opacity = tw(t, s.start + 0.7, s.start + 1.0) * fo;
      o.price.style.transform = 'translateY(' + ((1 - pe) * 50) + 'px) scale(' + lerp(0.92, 1, pe) + ')';
      o.count.style.opacity = tw(t, s.start + 0.1, s.start + 0.4) * fo * 0.9;
    });
    var cc = tw(t, P.slots[0].start + 0.9, P.slots[0].start + 1.3) * (1 - tw(t, T.chipsOut, T.chipsOut + 0.4));
    S.cchips.style.opacity = cc * 0.95;
    var fl = 0;
    P.slots.forEach(function (s) { fl += flashAt(t, s.start + 0.1, 0.16); });
    S.flash.style.opacity = fl + flashAt(t, P.endStart, 0.14);
    drawEnd(t);
  }

  /* ---------- brand reel ------------------------------------------------------------------------------------------- */
  function initBrand() {
    var content = document.getElementById('content');
    var b = P.brand;
    S.bmark = mk(content, 'abs prod', 'left:' + ((W - 360) / 2) + 'px;top:' + (H / 2 - 260) + 'px;width:360px;opacity:0', 'img');
    S.bmark.src = P.assets.mark;
    S.bhair = mk(content, 'abs rule', 'left:' + (W / 2 - 260) + 'px;top:' + (H / 2 + 170) + 'px;width:520px;opacity:0');
    S.bword = P.words.map(function (w, i) {
      var o = {};
      o.p = makeProduct(content, w, w.kind);
      o.l = line(content, 'title', w.word, 1420, 1000);
      o.l.span.style.fontSize = '120px';
      o.l.span.style.letterSpacing = '12px';
      o.n = line(content, 'eyebrow', ('0' + (i + 1)).slice(-2) + ' / 0' + P.words.length, 300, 900);
      return o;
    });
    S.t1 = line(content, 'title', b.line1, 800, 980);
    S.t2 = line(content, 'title', b.line2, 940, 980);
    S.t2.span.style.color = '#f1d98a';
    S.t2.span.style.fontStyle = 'italic';
    S.tr = mk(content, 'abs rule', 'left:' + ((W - 520) / 2) + 'px;top:1090px;width:520px;opacity:0');
    S.ts = line(content, 'sub', b.sub, 1130, 960);
    buildEnd(P.endStart);
  }
  function drawBrand(t) {
    var T = P.t;
    var sp = E.outCubic(tw(t, 0.15, 0.9));
    var so = tw(t, T.words, T.words + 0.3);
    S.bmark.style.opacity = sp * (1 - so);
    S.bmark.style.transform = 'scale(' + (lerp(0.8, 1.04, sp)) + ')';
    S.bhair.style.opacity = tw(t, 0.4, 0.8) * (1 - so);
    S.bhair.style.transform = 'scaleX(' + E.outCubic(tw(t, 0.4, 1.3)) + ')';
    P.slots.forEach(function (s, i) {
      var o = S.bword[i];
      var vis = t >= s.start - 0.01 && t <= s.end + 0.01;
      o.p.wrap.style.visibility = vis ? 'visible' : 'hidden';
      o.l.box.style.visibility = vis ? 'visible' : 'hidden';
      o.n.box.style.visibility = vis ? 'visible' : 'hidden';
      if (!vis) return;
      var inP = E.outQuint(tw(t, s.start, s.start + 0.45));
      var outP = E.inCubic(tw(t, s.end - 0.3, s.end));
      var sc = lerp(1.25, 1.0, inP) * (1 + 0.05 * tw(t, s.start, s.end));
      placeProduct(o.p, W / 2, P.cy - 60 + Math.sin(t * 1.5 + i) * 8, sc, Math.sin((t - s.start) * 1.0) * 1.2, (1 - outP) * tw(t, s.start, s.start + 0.15), lerp(16, 0, inP) + outP * 14);
      sweep(o.p, tw(t, s.start + 0.2, s.start + 0.9), 0.6);
      reveal(o.l, E.outCubic(tw(t, s.start + 0.1, s.start + 0.55)), 130);
      reveal(o.n, E.outCubic(tw(t, s.start + 0.05, s.start + 0.4)), 140);
      o.l.box.style.opacity = parseFloat(o.l.box.style.opacity) * (1 - outP);
      o.n.box.style.opacity = parseFloat(o.n.box.style.opacity) * (1 - outP);
    });
    var tg = T.tag;
    var gOut = E.inCubic(tw(t, P.endStart - 0.4, P.endStart));
    reveal(S.t1, E.outCubic(tw(t, tg, tg + 0.8)), 130);
    reveal(S.t2, E.outCubic(tw(t, tg + 0.35, tg + 1.15)), 130);
    S.tr.style.opacity = tw(t, tg + 0.8, tg + 1.1) * (1 - gOut);
    S.tr.style.transform = 'scaleX(' + E.outCubic(tw(t, tg + 0.8, tg + 1.5)) + ')';
    reveal(S.ts, E.outCubic(tw(t, tg + 1.0, tg + 1.7)), 140);
    [S.t1, S.t2, S.ts].forEach(function (l) { l.box.style.opacity = parseFloat(l.box.style.opacity) * (1 - gOut); });
    var fl = flashAt(t, 0.12, 0.12) + flashAt(t, T.words, 0.2) + flashAt(t, tg, 0.14) + flashAt(t, P.endStart, 0.14);
    P.slots.forEach(function (s) { fl += flashAt(t, s.start, 0.1); });
    S.flash.style.opacity = fl;
    drawEnd(t);
  }

  /* ---------- montage reel: fast colour-story cut of many products, one colour world per product ---------------- */
  function gradCss(bg, dark) {
    return 'linear-gradient(180deg,' + bg[0] + ' 0%,' + bg[1] + ' 100%)';
  }
  function layerBox(content, bg) {
    // the layer is 120 px wider on each side so the blurred edge of a whip never shows a dark strip
    var el = mk(content, 'abs', 'left:-120px;top:-120px;width:' + (W + 240) + 'px;height:' + (H + 240) + 'px;overflow:hidden;background:' + bg);
    var box = mk(el, 'abs', 'left:120px;top:120px;width:' + W + 'px;height:' + H + 'px');
    return { el: el, box: box };
  }
  function initMontage() {
    var content = document.getElementById('content');
    document.getElementById('vig').style.opacity = '.4';
    document.getElementById('grain').style.display = 'none';
    var M = P.montage;
    S.layers = [];
    // layer 0: cream intro, layers 1..n: product slides, last layer: cream tagline
    var introL = layerBox(content, gradCss(['#f7f0df', '#e6d6b0']));
    var intro = introL.box;
    mk(intro, 'abs', 'left:-200px;top:300px;width:1480px;height:1480px;background:radial-gradient(circle,rgba(212,175,55,.22),rgba(212,175,55,0) 62%)');
    var iw = mk(intro, 'abs', 'left:0;top:0;width:' + W + 'px;text-align:center;font:600 330px/1 Cormorant,serif;letter-spacing:6px;color:rgba(122,84,20,.10);white-space:nowrap;top:560px');
    iw.textContent = 'ANJUM';
    var im = mk(intro, 'abs prod', 'left:' + ((W - 250) / 2) + 'px;top:620px;width:250px', 'img');
    im.src = P.assets.mark;
    var il1 = line(intro, 'title', M.intro.line1, 930, 960);
    var il2 = line(intro, 'title', M.intro.line2, 1050, 960);
    il1.span.style.color = '#241706'; il2.span.style.color = '#7a5414'; il2.span.style.fontStyle = 'italic';
    var ir = mk(intro, 'abs rule', 'left:' + ((W - 420) / 2) + 'px;top:1190px;width:420px');
    var is = line(intro, 'sub', M.intro.sub, 1230, 960);
    is.span.style.color = '#4a3c1c'; is.span.style.letterSpacing = '6px'; is.span.style.textTransform = 'uppercase'; is.span.style.fontSize = '30px';
    S.layers.push({ el: introL.el, kind: 'intro', mark: im, word: iw, l1: il1, l2: il2, rule: ir, sub: is });

    P.slides.forEach(function (sl, i) {
      var th = sl.theme;
      var fg = th.dark ? '#1b1307' : '#ffffff';
      var lay = layerBox(content, gradCss(th.bg, th.dark));
      var el = lay.box;
      mk(el, 'abs', 'left:-200px;top:260px;width:1480px;height:1480px;background:radial-gradient(circle,rgba(255,255,255,' + (th.dark ? '.45' : '.20') + '),rgba(255,255,255,0) 60%)');
      var wm = mk(el, 'abs', 'left:-60px;top:' + (P.cy - 330) + 'px;width:' + (W + 120) + 'px;text-align:center;font:600 380px/1 Cormorant,serif;letter-spacing:4px;white-space:nowrap;color:' + (th.dark ? 'rgba(27,19,7,.12)' : 'rgba(255,255,255,.2)'));
      wm.textContent = th.word;
      // shrink long words so they stay inside the picture
      var fs = 380;
      var probe = mk(el, 'abs', 'visibility:hidden;white-space:nowrap;font:600 380px/1 Cormorant,serif;letter-spacing:4px', 'span');
      probe.textContent = th.word;
      while (probe.offsetWidth > 1000 && fs > 200) { fs -= 12; probe.style.fontSize = fs + 'px'; }
      wm.style.fontSize = fs + 'px';
      wm.style.top = (P.cy - 330 + (380 - fs) / 2) + 'px';
      el.removeChild(probe);
      var mk2 = mk(el, 'abs prod', 'left:' + ((W - 96) / 2) + 'px;top:96px;width:96px;opacity:.92', 'img');
      mk2.src = P.assets.mark;
      var cnt = mk(el, 'abs count', 'left:70px;top:132px;color:' + th.acc + ';opacity:.95');
      cnt.textContent = ('0' + (i + 1)).slice(-2) + ' / ' + ('0' + P.slides.length).slice(-2);
      var prod = makeProduct(el, sl, sl.kind);
      var hk = line(el, 'title', th.hook, 1290, 980);
      hk.span.style.font = 'italic 600 74px/1.1 Cormorant,serif';
      hk.span.style.color = fg;
      fitText(hk.span, 960, 40);
      var nm = line(el, 'eyebrow', sl.title, 1410, 980);
      nm.span.style.color = th.acc;
      nm.span.style.fontSize = '30px';
      fitText(nm.span, 960, 22);
      var pill = mk(el, 'abs', 'left:50%;top:1500px;height:96px;padding:0 54px;border-radius:48px;display:flex;align-items:center;gap:22px;font:600 38px/1 Jost,sans-serif;letter-spacing:2px;white-space:nowrap;background:' + (th.dark ? '#1b1307' : '#f7f0df') + ';color:' + (th.dark ? '#f1d98a' : '#1b1307') + ';box-shadow:0 16px 40px rgba(0,0,0,.35)');
      pill.textContent = sl.price + '  ·  anjummart.com';
      S.layers.push({ el: lay.el, kind: 'slide', prod: prod, wm: wm, hook: hk, name: nm, pill: pill, cnt: cnt, item: sl });
    });

    var tgL = layerBox(content, gradCss(['#f7f0df', '#e6d6b0']));
    var tg = tgL.box;
    mk(tg, 'abs', 'left:-200px;top:300px;width:1480px;height:1480px;background:radial-gradient(circle,rgba(212,175,55,.22),rgba(212,175,55,0) 62%)');
    var tm = mk(tg, 'abs prod', 'left:' + ((W - 200) / 2) + 'px;top:560px;width:200px', 'img');
    tm.src = P.assets.mark;
    var t1 = line(tg, 'title', M.tag.line1, 820, 980);
    t1.span.style.color = '#241706'; t1.span.style.fontSize = '104px';
    fitText(t1.span, 960, 50);
    var tr = mk(tg, 'abs rule', 'left:' + ((W - 420) / 2) + 'px;top:990px;width:420px');
    var t2 = line(tg, 'sub', M.tag.line2, 1040, 960);
    t2.span.style.color = '#4a3c1c'; t2.span.style.letterSpacing = '8px'; t2.span.style.textTransform = 'uppercase'; t2.span.style.fontSize = '34px';
    var t3 = line(tg, 'title', M.tag.line3, 1150, 980);
    t3.span.style.color = '#7a5414'; t3.span.style.fontStyle = 'italic'; t3.span.style.fontSize = '62px';
    S.layers.push({ el: tgL.el, kind: 'tag', mark: tm, l1: t1, rule: tr, l2: t2, l3: t3 });
    buildEnd(P.endStart);
    if (P.endPhone) {
      S.end.phone = mk(document.getElementById('endcard'), 'abs center', 'top:1420px;opacity:0;text-align:center;font:500 36px/1 Jost,sans-serif;letter-spacing:4px;color:#f1d98a');
      S.end.phone.textContent = P.endPhone;
      S.end.chips.style.top = '1500px';
    }
  }
  function drawMontage(t) {
    var n = S.layers.length; // intro, slides, tag
    // times: layer k becomes the front at P.slots[k].start (slot 0 = intro, last = tag). The whip lasts 0.3 s and begins 0.2 s early.
    var HEAD = 0.2, TAIL = 0.1;
    S.layers.forEach(function (L, k) {
      var s = P.slots[k];
      var uIn = k === 0 ? 1 : E.inOut(tw(t, s.start - HEAD, s.start + TAIL));
      var nxt = P.slots[k + 1];
      var uOut = nxt ? E.inOut(tw(t, nxt.start - HEAD, nxt.start + TAIL)) : E.inOut(tw(t, P.endStart - 0.35, P.endStart + 0.15));
      var vis = uIn > 0 && uOut < 1;
      L.el.style.visibility = vis ? 'visible' : 'hidden';
      if (!vis) return;
      var x = (1 - uIn) * W - uOut * W;
      var blur = 26 * Math.sin(Math.PI * uIn) + 26 * Math.sin(Math.PI * uOut);
      L.el.style.transform = 'translateX(' + x.toFixed(1) + 'px)';
      L.el.style.filter = blur > 0.6 ? 'blur(' + blur.toFixed(1) + 'px)' : 'none';
      var lt = t - s.start;       // time since the layer arrived
      if (L.kind === 'slide') {
        var e = E.outBack(tw(lt, 0.0, 0.5));
        var par = (1 - uIn) * 160 - uOut * 160;
        L.wm.style.transform = 'translateX(' + (-par * 0.7 + Math.sin(lt * 0.9) * 14).toFixed(1) + 'px) scale(' + (1 + 0.04 * tw(lt, 0, 1.0)).toFixed(4) + ')';
        var sc = 0.86 * lerp(1.14, 1.0, e) * (1 + (L.prod.kind === 'photo' ? 0.02 : 0.05) * tw(lt, 0, s.end - s.start));
        var rot = Math.sin(lt * 4.5) * lerp(2.0, 0.0, tw(lt, 0, 0.9)) + Math.sin(lt * 0.9) * 0.9;
        placeProduct(L.prod, W / 2 + par * 0.25, P.cy - 50 + Math.sin(lt * 1.5) * 8 + lerp(40, 0, e), sc, L.prod.kind === 'photo' ? rot * 0.5 : rot, 1, 0);
        if (L.prod.inner) L.prod.inner.style.transform = 'scale(' + (1.06 + 0.1 * tw(lt, 0, s.end - s.start)) + ')';
        if (L.prod.reflect) L.prod.reflect.style.opacity = 0.14;
        sweep(L.prod, tw(lt, 0.15, 0.8), 0.7);
        reveal(L.hook, E.outCubic(tw(lt, 0.1, 0.5)), 130);
        reveal(L.name, E.outCubic(tw(lt, 0.2, 0.6)), 150);
        var pe = E.outBack(tw(lt, 0.25, 0.65));
        L.pill.style.opacity = tw(lt, 0.25, 0.45);
        L.pill.style.transform = 'translateX(-50%) translateY(' + ((1 - pe) * 46) + 'px) scale(' + lerp(0.9, 1, pe) + ')';
        L.cnt.style.opacity = 0.95 * tw(lt, 0.0, 0.3);
      } else if (L.kind === 'intro') {
        var ip = E.outCubic(tw(t, 0.1, 0.8));
        L.mark.style.opacity = ip; L.mark.style.transform = 'scale(' + lerp(0.86, 1.02, ip) + ')';
        L.word.style.transform = 'translateX(' + (Math.sin(t * 0.8) * 20 - (1 - ip) * 80).toFixed(1) + 'px)';
        reveal(L.l1, E.outCubic(tw(t, 0.45, 1.1)), 130);
        reveal(L.l2, E.outCubic(tw(t, 0.7, 1.35)), 130);
        L.rule.style.opacity = tw(t, 1.0, 1.3);
        L.rule.style.transform = 'scaleX(' + E.outCubic(tw(t, 1.0, 1.6)) + ')';
        reveal(L.sub, E.outCubic(tw(t, 1.2, 1.8)), 140);
      } else {
        var tp = E.outCubic(tw(lt, 0.05, 0.6));
        L.mark.style.opacity = tp; L.mark.style.transform = 'scale(' + lerp(0.86, 1.02, tp) + ')';
        reveal(L.l1, E.outCubic(tw(lt, 0.15, 0.75)), 130);
        L.rule.style.opacity = tw(lt, 0.5, 0.8);
        L.rule.style.transform = 'scaleX(' + E.outCubic(tw(lt, 0.5, 1.1)) + ')';
        reveal(L.l2, E.outCubic(tw(lt, 0.6, 1.2)), 140);
        reveal(L.l3, E.outCubic(tw(lt, 0.9, 1.5)), 140);
      }
    });
    var fl = flashAt(t, P.endStart, 0.14);
    P.slots.forEach(function (s, k) { if (k > 0) fl += flashAt(t, s.start - 0.05, 0.08); });
    S.flash.style.opacity = Math.min(fl, 0.4);
    drawEnd(t);
    if (S.end.phone) S.end.phone.style.opacity = tw(t, P.endStart + 1.4, P.endStart + 1.8) * 0.95;
  }

  /* ---------- entry points ----------------------------------------------------------------------------------------- */
  window.__init = function (plan) {
    P = plan;
    buildBackdrop();
    var jobs = [];
    var imgs = [];
    function need(it) {
      if (!it || !it.src || it.kind === 'photo') return;
      jobs.push(loadImg(it.src).then(function (i) { it.nw = i.naturalWidth; it.nh = i.naturalHeight; }));
    }
    if (P.type === 'product') need(P.product);
    if (P.items) P.items.forEach(need);
    if (P.words) P.words.forEach(need);
    if (P.slides) P.slides.forEach(need);
    jobs.push(loadImg(P.assets.logo));
    jobs.push(loadImg(P.assets.mark));
    jobs.push(document.fonts.ready);
    ['Cormorant', 'Jost'].forEach(function (f) { jobs.push(document.fonts.load('600 40px ' + f)); jobs.push(document.fonts.load('400 40px ' + f)); jobs.push(document.fonts.load('500 40px ' + f)); });
    return Promise.all(jobs).then(function () {
      if (P.type === 'product') initProduct();
      else if (P.type === 'collection') initCollection();
      else if (P.type === 'montage') initMontage();
      else initBrand();
      if (P.preview) {
        var rb = mk(document.getElementById('stage'), 'abs', 'left:0;right:0;top:1780px;height:92px;background:rgba(165,28,48,.92);color:#fff;font:600 34px/92px Jost,sans-serif;letter-spacing:6px;text-align:center;z-index:50');
        rb.textContent = 'PREVIEW \u00b7 NOT FOR POSTING';
      }
      window.__seek(0);
      return true;
    });
  };
  window.__seek = function (t) {
    drawBackdrop(t);
    if (P.type === 'product') drawProduct(t);
    else if (P.type === 'collection') drawCollection(t);
    else if (P.type === 'montage') drawMontage(t);
    else drawBrand(t);
  };
})();
