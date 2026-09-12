#!/usr/bin/env python3
import base64, pathlib

BASE = pathlib.Path(__file__).resolve().parent
OPT = BASE / "assets"

MIME = {".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",
        ".svg":"image/svg+xml",".webp":"image/webp",".mp4":"video/mp4"}

def datauri(name):
    p = OPT / name
    data = p.read_bytes()
    mime = MIME[p.suffix.lower()]
    return f"data:{mime};base64," + base64.b64encode(data).decode()

def relpath(name):
    assert (OPT / name).exists(), name
    return f"assets/{name}"

INLINE = datauri

tpl = (BASE / "deck_template.html").read_text(encoding="utf-8")
names = {
    "__HERO__": "hero.jpg",
    "__CHART__": "chart.jpg",
    "__PROFILE__": "profile.jpg",
    "__FACEBOOK__": "facebook.jpg",
    "__C1__": "c1.jpg",
    "__C2__": "c2.jpg",
    "__C3__": "c3.jpg",
    "__POSTER__": "poster.jpg",
    "__JUP_ICON__": "jup-icon.svg",
    "__JUPCUT_LOGO__": "jupcut-logo-sm.png",
    "__JUP_SCRIPT__": "jup-script.jpg",
    "__JUP_TELE__": "jup-teleprompter.jpg",
    "__JUP_CUT__": "jup-cut.jpg",
    "__F_TOFU__": "f-tofu.jpg",
    "__F_MOFU__": "f-mofu.jpg",
    "__F_BOFU__": "f-bofu.jpg",
    "__F_CONV__": "f-conv.jpg",
    "__P1__": "p1.jpg",
    "__P2__": "p2.jpg",
    "__P3__": "p3.jpg",
    "__ALI_1__": "ali-1.jpg",
    "__ALI_2__": "ali-2.jpg",
    "__ALI_YT__": "ali-yt.jpg",
    "__VIDEOOS_YT__": "videoos-yt.jpg",
    "__DISC_SEARCH__": "disc-search.webp",
    "__DISC_FILTERS__": "disc-filters.webp",
    "__DISC_SCRIPT__": "disc-script.webp",
    "__JUP_CAPTIONS__": "jup-captions.webp",
    "__JUP_SCENES__": "jup-scenes.png",
    "__JUP_FX__": "jup-fx.jpg",
    "__POS_DEMO__": "pos-demo.png",
    "__STITCH_MP4__": "stitch-loop.mp4",
    "__QR_IOS__": "qr-ios.svg",
    "__QR_WA__": "qr-whatsapp.png",
    "__ICON_GEMINI__": "icon-gemini.svg",
    "__ICON_CHATGPT__": "icon-chatgpt.svg",
    "__KALLAWAY_IG__": "kallaway-ig.jpg",
    "__KALLAWAY_MP4__": "kallaway-ig.mp4",
    "__JUPCUT_ICON__": "jupcut-icon.png",
    "__QR_ANDROID__": "qr-android.svg",
    "__JUPAI_EDIT__": "jupai-edit.webp",
    "__JUPAI_BA__": "jupai-ba.jpg",
    "__JUPAI_CAPS__": "jupai-caps.jpg",
    "__JUPAI_BROLL__": "jupai-broll.jpg",
    "__G_WHYIP__": "g-why-ip.jpg",
    "__G_COACH__": "g-coach.jpg",
    "__G_CAL__": "g-blank-calendar.jpg",
    "__G_READ__": "g-read-aloud.jpg",
    "__G_PICK__": "g-pick-card.jpg",
}
mapping = {k: INLINE(v) for k, v in names.items()}
# deck.html: single-file build with everything inlined (offline / share as one file)
inline = tpl
for k, v in mapping.items():
    inline = inline.replace(k, v)
(BASE / "deck.html").write_text(inline, encoding="utf-8")
print("wrote deck.html", f"{len(inline)/1024:.0f} KB (inline)")

# index.html: GitHub Pages entry point, references assets/ by relative path
hosted = tpl
for k, v in mapping.items():
    hosted = hosted.replace(k, relpath(names[k]))
(BASE / "index.html").write_text(hosted, encoding="utf-8")
print("wrote index.html", f"{len(hosted)/1024:.0f} KB (relative assets/)")
