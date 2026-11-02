"""Build the installable app (index.html + sw.js) from src/app.html, the page published as the claude.ai Artifact.

Run from the repository root: python3 tools/build_pwa.py
"""
import hashlib, re

src = open("src/app.html", encoding="utf-8").read()
head = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#120c13">
<meta name="description" content="Gestion de cave à vin : bouteilles, emplacements, carte des vins, dégustations.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Ma Cave">
<style>html,body{margin:0}*,*::before,*::after{box-sizing:border-box}</style>
"""
# the artifact page starts with <title>, <meta>, <link> and <style>: keep them in <head>, the rest goes in <body>
cut = src.index("</style>") + len("</style>")
html = head + src[:cut] + "\n</head>\n<body>\n" + src[cut:] + "\n</body>\n</html>\n"
open("index.html", "w", encoding="utf-8").write(html)

version = hashlib.sha1((html + open("communes.js", encoding="utf-8").read()[:2000]).encode()).hexdigest()[:10]
sw = open("tools/sw.template.js", encoding="utf-8").read().replace("__VERSION__", version)
open("sw.js", "w", encoding="utf-8").write(sw)
print("index.html", len(html), "bytes; sw version", version)
