from pocketsphinx import Decoder
import json, re, numpy as np
tim = json.load(open("timing.json"))  # rough per token [word,start,end]
raw = np.frombuffer(open("v16.wav", "rb").read()[44:], np.int16)
SR = 16000; dur = len(raw)/SR
def norm(w):
    w = w.replace("…", "").replace("7", "seven").replace("a.m.", "a m")
    return re.sub(r"[^A-Za-z' ]", " ", w).lower().split()
# group tokens to lines by sentence end
groups = []; cur = []
for i, (w, s, e) in enumerate(tim):
    cur.append(i)
    if (re.search(r"[.?!…]$", w) and w != "a.m.") or i == len(tim)-1: groups.append(cur); cur = []
res = [None]*len(tim); fails = 0; prev_end = 0.0
d = Decoder(samprate=SR, bestpath=False, loglevel="FATAL")
for gi, g in enumerate(groups):
    a = max(0, prev_end - 0.05); b = min(dur, max(tim[g[-1]][2], a + 1.0) + 1.6)
    seq = []; owner = []
    for i in g:
        for p in norm(tim[i][0]): seq.append(p); owner.append(i)
    try:
        d.set_align_text(" ".join(seq)); d.start_utt()
        d.process_raw(raw[int(a*SR):int(b*SR)].tobytes(), full_utt=True); d.end_utt()
        al = [w for w in d.seg() if w.word not in ("<sil>", "<s>", "</s>", "(NULL)", "[NOISE]")]
        al = [(w.word, a + w.start_frame/100, a + (w.end_frame+1)/100) for w in al]
        assert len(al) == len(seq)
        prev_end = al[-1][2]
        for (nm, s, e), i in zip(al, owner):
            if res[i] is None: res[i] = [tim[i][0], s, e]
            else: res[i][2] = e
    except Exception as ex:
        fails += 1; print("fail", gi, ex)
        for i in g: res[i] = tim[i]
        prev_end = tim[g[-1]][2]
json.dump(res, open("timing_aligned.json", "w"))
print("fails", fails)
for r0, r1 in list(zip(tim, res))[:12]: print(r0, [round(x, 2) if isinstance(x, float) else x for x in r1])
