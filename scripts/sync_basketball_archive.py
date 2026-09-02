from pathlib import Path
import json, re

data = json.loads(Path("basketball-sync-data.json").read_text())
games = data["games"]

def link(href, label="View evidence."):
    return f' <a href="{href}">{label}</a>' if href else ""

def season_games(season):
    return [g for g in games if g["season"] == season]

def point_bounds(gs):
    low = high = 0
    for g in gs:
        p = g["points"].replace("–", "-")
        if "-" in p:
            a,b = map(int,p.split("-",1))
        else:
            a=b=int(p)
        low += a; high += b
    return low, high

jr = season_games("2003–04")
sr = season_games("2004–05")
assert len(jr) == 19 and point_bounds(jr) == (200,200)
assert len(sr) == 16 and point_bounds(sr) == (234,235)

def main_rows():
    out=[]
    for g in games:
        out.append(
            f'      <tr><td>{g["season"]}</td><td>{g["display_date"]}</td><td>{g["opponent"]}</td>'
            f'<td>{g["result"]}</td><td><strong>{g["points"]} points</strong></td>'
            f'<td>{g["note"]}{link(g["evidence"])}</td></tr>'
        )
    return "\n".join(out)

def bball_rows(gs):
    out=[]
    for g in gs:
        src=f'{g["source"]}, {g["display_date"]}'
        if g["page"] != "—":
            if g["page"].startswith("D") or g["page"].startswith("Section") or " / " in g["page"]:
                src += f', {g["page"]}'
            else:
                src += f', p. {g["page"]}'
        out.append(
            f'<tr><td>{g["opponent"]}</td><td><strong>{g["points"]}</strong></td><td>{g["result"]}</td>'
            f'<td>{src}. {g["note"]}{link(g["evidence"])}</td></tr>'
        )
    return "\n".join(out)

junior_honors_main = [
'      <tr><td>2004-03-11</td><td>The Daily Review</td><td>9</td><td>Local players notch postseason awards</td><td>Murphy Skinner was named Second-Team All-District 7-3A in basketball.</td></tr>',
'      <tr><td>2004-03-12</td><td>The Daily Review</td><td>8</td><td>All-Parish boys prep b-ball team</td><td>Murphy Skinner received All-Parish honorable mention.</td></tr>',
'      <tr><td>2004-05-11</td><td>The Daily Review</td><td>8</td><td>Jacks, Jills athletes honored in ceremony</td><td>Second source confirming Murphy Skinner&#39;s All-Parish honorable mention in basketball.</td></tr>',
]
senior_honor_main = '      <tr><td>2005 postseason</td><td>Archived newspaper article</td><td>—</td><td>Jacks load players</td><td>Confirms Murphy Skinner as First-Team All-District 7-3A; Patterson won the district championship and advanced to the Class 3A quarterfinals. Publication date and page number are still being documented. <a href="basketball-2004-05-all-district.html">View honor record.</a></td></tr>'

junior_honors_bball = [
'<tr><td>2004-03-11</td><td>The Daily Review</td><td>9</td><td>Murphy Skinner was named Second-Team All-District 7-3A in basketball.</td></tr>',
'<tr><td>2004-03-12</td><td>The Daily Review</td><td>8</td><td>Murphy Skinner received All-Parish honorable mention.</td></tr>',
'<tr><td>2004-05-11</td><td>The Daily Review</td><td>8</td><td>Second source confirming Murphy Skinner&#39;s All-Parish honorable mention in basketball.</td></tr>',
]
senior_honor_bball = '<tr><td>2005 postseason</td><td>Archived newspaper article</td><td>—</td><td><em>Jacks load players</em> confirms Murphy Skinner as First-Team All-District 7-3A; Patterson won the district championship and advanced to the Class 3A quarterfinals. Publication date and page number are still being documented. <a href="basketball-2004-05-all-district.html">View honor record.</a></td></tr>'

def source_main():
    def row(g):
        return (
            f'      <tr><td>{g["source_date"]}</td><td>{g["source"]}</td><td>{g["page"]}</td>'
            f'<td>{g["coverage"]}</td><td>{g["fact"]}{link(g["evidence"])}</td></tr>'
        )
    return "\n".join([*(row(g) for g in jr), *junior_honors_main, *(row(g) for g in sr), senior_honor_main])

def source_bball():
    def row(g):
        return (
            f'<tr><td>{g["source_date"]}</td><td>{g["source"]}</td><td>{g["page"]}</td>'
            f'<td>{g["fact"]}{link(g["evidence"])}</td></tr>'
        )
    return "\n".join([*(row(g) for g in jr), *junior_honors_bball, *(row(g) for g in sr), senior_honor_bball])

jr_section = f'''<section id="junior"><div class="wrap"><div class="eyebrow">2003–04 · Junior season · No. 23 · reconstruction in progress</div><h2>Junior honors & recovered scoring record</h2>
<div class="card"><h3>Verified junior honors</h3><ul><li><strong>Second-Team All-District 7-3A</strong></li><li><strong>All-Parish Honorable Mention</strong></li></ul><p>Patterson reached the Louisiana Class 3A playoffs.</p></div>
<div class="grid">
  <div class="card"><div class="stat">200</div><strong>Points documented</strong><p class="small">Across 19 currently located junior-season game reports.</p></div>
  <div class="card"><div class="stat">10.5</div><strong>Points per recovered game</strong><p class="small">This is not a full-season scoring average.</p></div>
  <div class="card"><div class="stat">25</div><strong>Recovered single-game high</strong><p class="small">Led all scorers against Assumption.</p></div>
</div>
<div class="card"><h3>Recovered 2003–04 game scoring</h3><table><thead><tr><th>Opponent</th><th>Points</th><th>Team result</th><th>Source / note</th></tr></thead><tbody>
{bball_rows(jr)}
</tbody></table></div>
<p class="notice"><strong>Status:</strong> The 2003–04 season is still being reconstructed. The 200 points shown here cover 19 located game reports and are not a claimed full-season point total. The 10.5 figure is only the average across those recovered games.</p>
</div></section>'''

sr_section = f'''<section id="senior"><div class="wrap"><div class="eyebrow">2004–05 · Senior season · No. 23 · reconstruction in progress</div><h2>Senior honors & recovered scoring record</h2>
<div class="card"><h3>Verified senior honors & team finish</h3><ul><li><strong><a href="basketball-2004-05-all-district.html">First-Team All-District 7-3A</a></strong> — selected by the district coaches.</li><li><strong>District 7-3A champion</strong></li><li><strong>Louisiana Class 3A state quarterfinalist</strong></li></ul></div>
<div class="grid">
  <div class="card"><div class="stat">234–235</div><strong>Points documented</strong><p class="small">Across 16 currently located senior-season game reports; the range reflects one unresolved source conflict.</p></div>
  <div class="card"><div class="stat">27</div><strong>Recovered single-game high</strong><p class="small">Scored against Franklin in an 84–60 Patterson victory.</p></div>
  <div class="card"><div class="stat">1st Team</div><strong>All-District 7-3A</strong><p class="small">Verified senior postseason honor.</p></div>
</div>
<div class="card"><h3>Recovered 2004–05 game scoring</h3><table><thead><tr><th>Opponent</th><th>Points</th><th>Team result</th><th>Source / note</th></tr></thead><tbody>
{bball_rows(sr)}
</tbody></table></div>
<p class="notice"><strong>Status:</strong> The 2004–05 senior season is under reconstruction. The 234–235 points shown here cover 16 located game reports and are not a final season total. The one-point range preserves the unresolved Terrebonne source conflict: one newspaper reports 15 points and another reports 16.</p>
</div></section>'''

jr_card = '      <article class="card"><div class="eyebrow">2003–04 · Junior · No. 23</div><h3>200 points across 19 currently located game reports</h3><p class="small">This is a recovered-game subtotal only, not a claimed full-season total. The recovered-game average is 10.5 points.</p><h4>Verified honors</h4><ul><li><strong>Second-Team All-District 7-3A</strong></li><li><strong>All-Parish Honorable Mention</strong></li></ul><p>Patterson reached the Louisiana Class 3A playoffs. The All-Parish honor is confirmed by two separate Daily Review articles.</p></article>'
sr_card = '      <article class="card"><div class="eyebrow">2004–05 · Senior · No. 23</div><h3>234–235 points across 16 currently located game reports</h3><p class="small">This is a recovered-game subtotal only. The one-point range reflects conflicting 15- and 16-point newspaper reports for the Terrebonne game.</p><h4>Verified honors</h4><ul><li><strong><a href="basketball-2004-05-all-district.html">First-Team All-District 7-3A</a></strong></li><li><strong>District 7-3A champion</strong></li></ul><p>Patterson advanced to the Louisiana Class 3A state quarterfinals.</p><h4>Verified postseason run</h4><ul><li>Patterson defeated Catholic–New Iberia 83–60; Skinner scored 14 points.</li><li>Patterson defeated Northwest 63–62; Skinner scored 10 points.</li><li>Patterson&#39;s season ended in a 73–63 quarterfinal loss to Marksville; Skinner scored 11 points.</li></ul></article>'

def sub1(pattern, replacement, text, label):
    out,n = re.subn(pattern,replacement,text,count=1,flags=re.S)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 replacement, got {n}")
    return out

p=Path("index.html"); s=p.read_text()
s=sub1(r'      <article class="card"><div class="eyebrow">2003–04 · Junior · No. 23</div>.*?</article>',jr_card,s,"index junior card")
s=sub1(r'      <article class="card"><div class="eyebrow">2004–05 · Senior · No. 23</div>.*?</article>',sr_card,s,"index senior card")
s=sub1(r'(<h3>Verified basketball scoring games</h3>\s*<table><thead><tr><th>Season</th><th>Source / report date</th><th>Opponent</th><th>Result</th><th>Murphy Skinner</th><th>Notes</th></tr></thead><tbody>\n).*?(\n    </tbody></table>\n    <p class="notice"><strong>Basketball archive status:)',lambda m:m.group(1)+main_rows()+m.group(2),s,"index scoring table")
s=sub1(r'(<tr><td>2005-11-13</td><td>Mission Football Conference</td>.*?</tr>\n).*?(\n    </tbody></table></div></section>\n\n    <section id="updates">)',lambda m:m.group(1)+source_main()+m.group(2),s,"index source register")
s=s.replace("Version 5.4 · September 2, 2026","Version 5.5 · September 2, 2026",1)
p.write_text(s)

p=Path("basketball.html"); s=p.read_text()
s=sub1(r'<section id="junior">.*?</div></section>\s*(?=<section id="senior">)',jr_section+"\n\n",s,"basketball junior")
s=sub1(r'<section id="senior">.*?</div></section>\s*(?=<section id="sources">)',sr_section+"\n\n",s,"basketball senior")
s=sub1(r'(<section id="sources">.*?<tbody>\n).*?(\n</tbody></table></div>)',lambda m:m.group(1)+source_bball()+m.group(2),s,"basketball sources")
s=re.sub(r'Version 2\.\d+','Version 3.0',s,count=1)
p.write_text(s)

print("Synced basketball archive: junior 19 games/200 points; senior 16 games/234–235 points.")
