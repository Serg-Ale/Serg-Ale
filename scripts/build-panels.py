#!/usr/bin/env python3
"""Regenerates the text panels of the profile README from the data below.

Run from the repo root:  python3 scripts/build-panels.py

It rewrites assets/h-*.svg, proof.svg, how.svg, trajectory.svg and stack.svg. The hero,
the case cards and the project cards are hand-made and stay as they are. Icons come from
scripts/icons.json (Simple Icons and Lucide paths, the same set the portfolio site uses).
Facts follow the CVs and the portfolio at https://saerix.vercel.app/en/dev; update the data
here when they change, then rebuild.
"""
import html
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json"), encoding="utf-8"))

SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"
BG, LINE, DARK = "#141417", "#26262B", "#0D0D0F"
ORANGE, TEAL, TEXT, MUTED = "#FF6B35", "#2EC4B6", "#EDEDED", "#8A8A8A"

BRAND = {
    "ts": "#3178C6", "js": "#F7DF1E", "py": "#FFD43B", "react": "#61DAFB", "next": "#E6E6E6",
    "nest": "#E0234E", "fastapi": "#09B39F", "node": "#5FA04E", "pg": "#6F93E6", "prisma": "#8C9BFF",
    "trpc": "#398CCB", "docker": "#2496ED", "n8n": "#EA4B71", "whatsapp": "#25D366", "junit": "#25A162",
    "agents": "#FF5B1F", "cicd": "#2DD4BF", "chatbot": "#FF5B1F", "jest": "#C21325", "tailwind": "#38BDF8",
    "gsap": "#88CE02", "reactquery": "#FF4154", "supabase": "#3ECF8E", "typeorm": "#E83524",
    "vitest": "#8FC13A", "playwright": "#2EAD33", "git": "#F05032", "neovim": "#57A143",
    "linux": "#FCC624", "claude": "#D97757", "pnpm": "#F69220",
}
NAMES = {
    "ts": "TypeScript", "js": "JavaScript", "py": "Python", "react": "React", "next": "Next.js",
    "tailwind": "Tailwind", "reactquery": "React Query", "gsap": "GSAP", "node": "Node.js", "nest": "NestJS",
    "fastapi": "FastAPI", "pg": "PostgreSQL", "prisma": "Prisma", "typeorm": "TypeORM", "trpc": "tRPC",
    "supabase": "Supabase", "agents": "AI agents", "n8n": "n8n", "whatsapp": "WhatsApp API",
    "chatbot": "Chatbots", "jest": "Jest", "vitest": "Vitest", "playwright": "Playwright", "junit": "JUnit",
    "cicd": "CI/CD", "docker": "Docker", "linux": "Linux", "neovim": "Neovim", "git": "Git", "pnpm": "pnpm",
    "claude": "Claude Code",
}

# ---------------------------------------------------------------- data
HEADINGS = [
    ("h-cases", "01", "Case studies"),
    ("h-own", "02", "Built on my own"),
    ("h-stack", "03", "Stack"),
    ("h-how", "04", "How I work"),
    ("h-path", "05", "Path"),
    ("h-contact", "06", "Let's talk"),
]

PROOF = [
    ("4+ years", "shipping web products, from intern to mid-level", ORANGE),
    (">80%", "test coverage on Aeon Tech's product", TEAL),
    ("Mid-level", "since March 2026, at Aeon Tech", ORANGE),
    ("72/100", "on the EF SET English test", TEAL),
]

HOW_TITLE = ("Speak", "-driven development.")
HOW_TAGLINE = "I talk, Claude asks, and the spec comes out of the conversation. It is not prompt engineering."
PIPELINE = [
    ("q", "/grill-me", "Grill the plan"),
    ("spec", "/to-spec", "Write the spec"),
    ("tickets", "/to-tickets", "Cut the tickets"),
    ("tdd", "/tdd", "Test first"),
    ("review", "/code-review", "Review in a clean context"),
]
PRINCIPLES = [
    ("Align on the whole", "I ask before I code. The team and the PO share one vision before the first ticket.", ORANGE),
    ("AI executes, I direct", "It researches and executes faster than I do, and flags risks early. It has bias, so the mental model and the questions stay mine.", ORANGE),
    ("Prove it in the open", "Spec, tickets, TDD and review in a public repository, so anyone can check.", TEAL),
    ("Speak up when something is off", "In payments and I see an auth problem elsewhere? I say so, and since code is cheap now, I fix it or write it up right then.", TEAL),
]

PATH_INTRO = ("I like understanding how technology works underneath. It is the closest thing to magic we have: "
              "with a computer and an idea, I can change what is around me.")
PATH = [
    ("School", "Alura", None, "The state of Paraná gave students access to Alura. I started with Java, mostly because of Minecraft."),
    ("2022", "UTFPR + TCS", "INTERN", "First job in June, degree in July. Front end to back end, Java, Spring Boot and Node.js, and Scrum Master on the capstone."),
    ("2023", "TCS", "ANALYST", "Production support for a large retail chain's overnight systems, and the technical link in incident war rooms."),
    ("2024", "Aeon Tech", "JR", "Rebuilt the product with a team of four to five. Front end, auth and the landing page, plus a self-hosted WhatsApp automation base."),
    ("2026", "Aeon Tech + Kaizen", "MID-LEVEL", "Mid-level since March, on Corta-ai across web, API, billing and analytics. Partner-dev at Kaizen, on Atrium."),
]

STACK = [
    ("LANGUAGES", ["ts", "js", "py"]),
    ("FRONT END", ["react", "next", "tailwind", "reactquery", "gsap"]),
    ("BACK END AND DATA", ["node", "nest", "fastapi", "pg", "prisma", "typeorm", "trpc", "supabase"]),
    ("AUTOMATION AND AI", ["agents", "n8n", "whatsapp", "chatbot"]),
    ("QUALITY AND DELIVERY", ["jest", "vitest", "playwright", "junit", "cicd", "docker"]),
    ("DAILY TOOLS", ["linux", "neovim", "git", "pnpm", "claude"]),
]


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=False)


def wrap(s, size, width, factor=0.54):
    limit = max(1, int(width / (size * factor)))
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if len(trial) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def t(x, y, s, size, fill, font=SANS, weight=None, spacing=None, anchor=None):
    attrs = f'x="{x}" y="{y}" font-family="{font}" font-size="{size}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if spacing:
        attrs += f' letter-spacing="{spacing}"'
    return f'<text {attrs} fill="{fill}">{s}</text>'


def paragraph(x, y, s, size, fill, width, line_h):
    out = []
    for i, line in enumerate(wrap(s, size, width)):
        out.append(t(x, y + i * line_h, esc(line), size, fill))
    return "".join(out), y + len(wrap(s, size, width)) * line_h


def icon(key, x, y, size, color):
    ic = ICONS[key]
    scale = size / 24
    if ic["kind"] == "fill":
        paths = "".join(f'<path d="{d}"/>' for d in ic["paths"])
        return f'<g transform="translate({x},{y}) scale({scale:.4f})" fill="{color}">{paths}</g>'
    return (f'<g transform="translate({x},{y}) scale({scale:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ic["inner"]}</g>')


def write(name, w, h, body, label, rx=20):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
           f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{BG}" stroke="{LINE}"/>'
           f'{body}</svg>\n')
    with open(os.path.join(ASSETS, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------------- panels
def build_headings():
    for name, num, title in HEADINGS:
        line_x = int(68 + len(title) * 15.6 + 24)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 64" role="img" aria-label="{esc(title)}">'
               f'<rect x="0.5" y="0.5" width="1199" height="63" rx="14" fill="{BG}" stroke="{LINE}"/>'
               f'{t(28, 39, num, 14, ORANGE, MONO)}'
               f'{t(68, 42, esc(title), 26, TEXT, MONO, 700)}'
               f'<line x1="{line_x}" y1="32" x2="1172" y2="32" stroke="{LINE}" stroke-width="1"/></svg>\n')
        with open(os.path.join(ASSETS, name + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)


def build_proof():
    gap, w, h = 18, 1200, 150
    tile_w = (w - gap * (len(PROOF) - 1)) / len(PROOF)
    body = []
    for i, (value, label, color) in enumerate(PROOF):
        x = i * (tile_w + gap)
        body.append(f'<rect x="{x + 0.5:.1f}" y="0.5" width="{tile_w - 1:.1f}" height="{h - 1}" rx="16" fill="{BG}" stroke="{LINE}"/>')
        body.append(f'<rect x="{x + 16:.1f}" y="0.5" width="{tile_w - 32:.1f}" height="3" rx="1.5" fill="{color}"/>')
        body.append(t(f"{x + 26:.1f}", 70, esc(value), 36, color, MONO, 700))
        for j, line in enumerate(wrap(label, 16, tile_w - 52)):
            body.append(t(f"{x + 26:.1f}", 104 + j * 22, esc(line), 16, MUTED))
    label = "Proof: " + "; ".join(f"{v} {l}" for v, l, _ in PROOF)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">{"".join(body)}</svg>\n'
    with open(os.path.join(ASSETS, "proof.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def waveform(x0, cy, count=26, bar=6, gap=4):
    out = []
    for i in range(count):
        base = 14 + (math.sin(i * 1.7) + math.sin(i * 0.63 + 1) + 2) * 13
        lo = max(4, base * 0.3)
        color = TEAL if i % 7 == 0 else ORANGE
        x = x0 + i * (bar + gap)
        delay = -((i * 137) % 1150) / 1000
        out.append(
            f'<rect x="{x}" y="{cy - base / 2:.1f}" width="{bar}" height="{base:.1f}" rx="3" fill="{color}" fill-opacity="{0.5 + base / 100:.2f}">'
            f'<animate attributeName="height" values="{lo:.1f};{base:.1f};{lo:.1f}" dur="1.15s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{cy - lo / 2:.1f};{cy - base / 2:.1f};{cy - lo / 2:.1f}" dur="1.15s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "".join(out)


def build_how():
    w, m = 1200, 44
    body = []
    # title and tagline on the left, mic and waveform on the right
    body.append(t(m, 70, f'<tspan fill="{ORANGE}">{HOW_TITLE[0]}</tspan>{esc(HOW_TITLE[1])}', 36, TEXT, SANS, 800))
    tag, _ = paragraph(m, 108, HOW_TAGLINE, 18, MUTED, 620, 26)
    body.append(tag)
    mic_x, mic_y = 790, 70
    body.append(f'<circle cx="{mic_x}" cy="{mic_y}" r="30" fill="{ORANGE}"/>')
    body.append(f'<circle cx="{mic_x}" cy="{mic_y}" r="30" fill="none" stroke="{ORANGE}" stroke-opacity="0.5">'
                f'<animate attributeName="r" values="30;46;30" dur="2.4s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values="0.5;0;0.5" dur="2.4s" repeatCount="indefinite"/></circle>')
    body.append(icon("mic", mic_x - 14, mic_y - 14, 28, "#0D0D0F"))
    body.append(waveform(mic_x + 62, mic_y))
    body.append(t(mic_x + 62, mic_y + 52, "I TALK", 12, ORANGE, MONO, None, 2))

    # pipeline
    py = 205
    body.append(t(m, py - 30, "THEN THE SAME FIVE STEPS, EVERY TIME", 12, MUTED, MONO, None, 2))
    span = w - 2 * m
    centers = [m + span * (i + 0.5) / len(PIPELINE) for i in range(len(PIPELINE))]
    body.append(f'<line x1="{centers[0]:.1f}" y1="{py + 22}" x2="{centers[-1]:.1f}" y2="{py + 22}" stroke="{LINE}" stroke-width="2"/>')
    for i, (key, skill, title) in enumerate(PIPELINE):
        cx = centers[i]
        a, b = i / len(PIPELINE), (i + 1) / len(PIPELINE)
        times = f"0;{a:.3f};{min(a + 0.03, b):.3f};{max(b - 0.03, a):.3f};{b:.3f};1"
        body.append(f'<circle cx="{cx:.1f}" cy="{py + 22}" r="34" fill="{ORANGE}" opacity="0">'
                    f'<animate attributeName="opacity" values="0;0;0.16;0.16;0;0" keyTimes="{times}" dur="10s" repeatCount="indefinite"/></circle>')
        body.append(f'<circle cx="{cx:.1f}" cy="{py + 22}" r="22" fill="{DARK}" stroke="{ORANGE}" stroke-width="2"/>')
        body.append(icon(key, f"{cx - 10:.1f}", py + 12, 20, ORANGE))
        body.append(t(f"{cx:.1f}", py + 72, esc(skill), 14, TEXT, MONO, 700, None, "middle"))
        for j, line in enumerate(wrap(title, 15, 190)):
            body.append(t(f"{cx:.1f}", py + 94 + j * 19, esc(line), 15, MUTED, SANS, None, None, "middle"))

    # principles
    top = py + 160
    body.append(f'<line x1="{m}" y1="{top}" x2="{w - m}" y2="{top}" stroke="{LINE}" stroke-width="1"/>')
    col_w = span / len(PRINCIPLES)
    end = top
    for i, (title, text_, color) in enumerate(PRINCIPLES):
        x = m + i * col_w
        body.append(t(f"{x:.1f}", top + 38, f"0{i + 1}", 13, color, MONO, None, 2))
        ty = top + 66
        for line in wrap(title, 20, col_w - 24, 0.52):
            body.append(t(f"{x:.1f}", ty, esc(line), 20, TEXT, SANS, 700))
            ty += 26
        para, ty = paragraph(f"{x:.1f}", ty + 6, text_, 16, MUTED, col_w - 28, 23)
        body.append(para)
        end = max(end, ty)
    write("how", w, end + 30, "".join(body),
          "How I work, speak-driven development: I talk, Claude asks, and the spec comes out of the conversation. "
          "Grill the plan, write the spec, cut the tickets, test first, review in a clean context.")


def build_path():
    w, pitch, text_w = 1272, 240, 212
    body = ['<g transform="translate(36,36)">']
    intro, y = paragraph(0, 30, PATH_INTRO, 20, TEXT, 1180, 30)
    body.append(intro)
    line_y = y + 24
    body.append(f'<line x1="0" y1="{line_y}" x2="1200" y2="{line_y}" stroke="{LINE}" stroke-width="2"/>')
    end = line_y
    for i, (year, org, level, text_) in enumerate(PATH):
        x = i * pitch
        now = i == len(PATH) - 1
        color = TEAL if now else ORANGE
        body.append(f'<circle cx="{x + 8}" cy="{line_y}" r="8" fill="{DARK}" stroke="{color}" stroke-width="3"/>')
        if now:
            body.append(f'<circle cx="{x + 8}" cy="{line_y}" r="8" fill="none" stroke="{TEAL}">'
                        f'<animate attributeName="r" values="8;18;8" dur="2.4s" repeatCount="indefinite"/>'
                        f'<animate attributeName="stroke-opacity" values="0.6;0;0.6" dur="2.4s" repeatCount="indefinite"/></circle>')
        ty = line_y + 42
        body.append(t(x, ty, year, 14, color, MONO, None, 2))
        ty += 32
        for line in wrap(org, 21, text_w, 0.5):
            body.append(t(x, ty, esc(line), 21, TEXT, SANS, 700))
            ty += 26
        if level:
            body.append(t(x, ty + 2, level, 12, color, MONO, None, 2))
            ty += 24
        else:
            ty += 4
        para, ty = paragraph(x, ty + 2, text_, 16, MUTED, text_w, 22)
        body.append(para)
        end = max(end, ty)
    body.append("</g>")
    write("trajectory", w, end + 36 + 28, "".join(body),
          "Path: school with Alura and Java, 2022 intern at TCS, 2023 analyst at TCS, 2024 junior at Aeon Tech, "
          "2026 mid-level at Aeon Tech and partner developer at Kaizen.")


def build_stack():
    w, tile, pitch, label_w = 1272, 52, 86, 250
    body = ['<g transform="translate(36,32)">']
    y = 0
    for row_label, keys in STACK:
        body.append(t(0, y + 33, esc(row_label), 13, MUTED, MONO, None, 1.5))
        for i, key in enumerate(keys):
            x = label_w + i * pitch
            color = BRAND[key]
            body.append(f'<rect x="{x}" y="{y + 4}" width="{tile}" height="{tile}" rx="12" fill="{color}" fill-opacity="0.09" '
                        f'stroke="{color}" stroke-opacity="0.35"/>')
            body.append(icon(key, x + 13, y + 17, 26, color))
            body.append(t(x + tile / 2, y + tile + 22, esc(NAMES[key]), 12, MUTED, SANS, None, None, "middle"))
        y += 92
        body.append(f'<line x1="0" y1="{y - 12}" x2="1200" y2="{y - 12}" stroke="{LINE}" stroke-width="1"/>')
    body.append("</g>")
    write("stack", w, y + 32 + 20, "".join(body), "Tech stack: " + "; ".join(f"{r.lower()}: " + ", ".join(NAMES[k] for k in ks) for r, ks in STACK))


if __name__ == "__main__":
    build_headings()
    build_proof()
    build_how()
    build_path()
    build_stack()
    print("built:", ", ".join(n for n, *_ in HEADINGS), "proof, how, trajectory, stack")
