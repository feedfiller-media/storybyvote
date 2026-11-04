# ---- render ----
def frame(t):
    if t < 1.0/FPS: return COVER.copy()
    li = cur_line(t); name = SCENE_OF_LINE[li]
    fr = render_scene(name, t)
    if name in TRANS:
        typ, TD = TRANS[name]; st = scene_start(name)
        p = (t - st)/TD
        if 0 <= p < 1:
            prev = ORDER[ORDER.index(name)-1]
            if typ == "slide":
                e = 1 - (1-p)**3; old = render_scene(prev, t)
                comp = Image.new("RGBA", (W, H)); comp.paste(old, (int(-W*e), 0)); comp.paste(fr, (int(W*(1-e)), 0)); fr = comp
            elif typ == "fade":
                fr = Image.blend(render_scene(prev, t), fr, ease(p))
            elif typ == "black":
                if p < 0.5: fr = Image.blend(render_scene(prev, t), Image.new("RGBA", (W, H), (0, 0, 0, 255)), ease(p*2))
                else: fr = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), fr, ease((p-0.5)*2))
            elif typ == "flash":
                fr = Image.blend(fr, Image.new("RGBA", (W, H), (255, 255, 255, 255)), 0.8*(1-p))
    hud(fr, t)
    captions(fr, t, CAP_Y[name])
    return fr

if os.environ.get("TEST"):
    ts = [float(x) for x in os.environ["TEST"].split(",")]
    for i, tt in enumerate(ts): frame(tt).convert("RGB").resize((360, 640)).save(f"t2_{i:02d}.png")
    raise SystemExit
N = int(TOTAL*FPS)
ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-i", "mix.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                       "-c:a", "aac", "-b:a", "192k", "-shortest", os.environ.get("OUT", "episode.mp4")], stdin=subprocess.PIPE)
for f in range(N):
    ff.stdin.write(frame(f/FPS).convert("RGB").tobytes())
    if f % 300 == 0: print(f, N, flush=True)
ff.stdin.close(); ff.wait(); print("done")
