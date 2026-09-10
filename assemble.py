#!/usr/bin/env python3
import base64, pathlib

BASE = pathlib.Path(__file__).resolve().parent
OPT = BASE / "assets"

MIME = {".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",
        ".svg":"image/svg+xml",".webp":"image/webp"}

def datauri(name):
    p = OPT / name
    data = p.read_bytes()
    mime = MIME[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(data).decode()

tpl = (BASE / "deck_template.html").read_text(encoding="utf-8")
mapping = {
    "__HERO__": datauri("hero.jpg"),
    "__CHART__": datauri("chart.jpg"),
    "__PROFILE__": datauri("profile.jpg"),
    "__C1__": datauri("c1.jpg"),
    "__C2__": datauri("c2.jpg"),
    "__C3__": datauri("c3.jpg"),
    "__POSTER__": datauri("poster.jpg"),
    "__JUP_ICON__": datauri("jup-icon.svg"),
    "__JUPCUT_LOGO__": datauri("jupcut-logo-sm.png"),
    "__JUP_SCRIPT__": datauri("jup-script.jpg"),
    "__JUP_TELE__": datauri("jup-teleprompter.jpg"),
    "__JUP_CUT__": datauri("jup-cut.jpg"),
    "__F_TOFU__": datauri("f-tofu.jpg"),
    "__F_MOFU__": datauri("f-mofu.jpg"),
    "__F_BOFU__": datauri("f-bofu.jpg"),
    "__F_CONV__": datauri("f-conv.jpg"),
    "__P1__": datauri("p1.jpg"),
    "__P2__": datauri("p2.jpg"),
    "__P3__": datauri("p3.jpg"),
    "__ALI_1__": datauri("ali-1.jpg"),
    "__ALI_2__": datauri("ali-2.jpg"),
    "__ALI_3__": datauri("ali-3.jpg"),
    "__DISC_HERO__": datauri("disc-hero.webp"),
    "__DISC_SEARCH__": datauri("disc-search.webp"),
    "__DISC_FILTERS__": datauri("disc-filters.webp"),
    "__DISC_SCRIPT__": datauri("disc-script.webp"),
    "__JUP_CAPTIONS__": datauri("jup-captions.webp"),
    "__JUP_SCENES__": datauri("jup-scenes.png"),
    "__JUP_FX__": datauri("jup-fx.jpg"),
    "__POS_DEMO__": datauri("pos-demo.png"),
    "__QR_IOS__": datauri("qr-ios.svg"),
    "__QR_ANDROID__": datauri("qr-android.svg"),
    "__JUPAI_EDIT__": datauri("jupai-edit.webp"),
    "__JUPAI_BA__": datauri("jupai-ba.jpg"),
    "__JUPAI_CAPS__": datauri("jupai-caps.jpg"),
    "__JUPAI_BROLL__": datauri("jupai-broll.jpg"),
    "__G_WHYIP__": datauri("g-why-ip.jpg"),
    "__G_COACH__": datauri("g-coach.jpg"),
    "__G_CAL__": datauri("g-blank-calendar.jpg"),
    "__G_READ__": datauri("g-read-aloud.jpg"),
    "__G_PICK__": datauri("g-pick-card.jpg"),
}
for k, v in mapping.items():
    tpl = tpl.replace(k, v)

out = BASE / "deck.html"
out.write_text(tpl, encoding="utf-8")
(BASE / "index.html").write_text(tpl, encoding="utf-8")  # GitHub Pages entry point
print("wrote", out, f"{len(tpl)/1024:.0f} KB")
