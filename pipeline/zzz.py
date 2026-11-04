def zzz(fr, x, y, t, sz=40, col=(255, 255, 255), speed=0.45):
    d = ImageDraw.Draw(fr)
    for i in range(3):
        p = ((t*speed) + i/3) % 1
        a = int(255*math.sin(p*math.pi))
        d.text((x + math.sin(p*6)*14 + p*30, y - p*120), "z", font=font(sz*(0.6+0.7*p)), fill=col + (a,),
               anchor="mm", stroke_width=3, stroke_fill=(40, 40, 70, a))

