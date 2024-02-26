import os
import glob
import json
import markdown
import pathlib
import datetime



# <div class="smw en">
#         <h2 style="text-align: center; color: #f3ff07;"> ﷼﷼﷼ دونیتر های عزیز ﷼﷼﷼</h2>
#         <p style="font-family: 'Courier New', Courier, monospace;">usdt: TL8DgNqKXTBh3QfSmmNAwTBJF4gaGW3pYw <br>ton:
#             UQDGtMOv9-Q-1aN0stCUuAUUvmTJoTdRI3WZxkS11Hm8bCYK</p>

#         <ul>
#             <li><a href="https://t.me/SteelFalcon">steel falcon</a> - 18.6 usdt</li>
#             <li>maziar - 13 usdt</li>
#         </ul>
#     </div>




# base_index_html = """
# <!DOCTYPE html>
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <link rel="stylesheet" href="/static/style.css">
#     <title>/mmd/</title>
# </head>

# <body>
#     <header>
#         <a href="emailto: {%email%}">email</a>
#         <span> -- </span>
#         <a href="{%tg%}">tg</a>
#     </header>
#     <div class="fa">
#         <img src="/static/velvet.png" alt="">
#         <h3>{%bio%}</h3>
#     </div>
    
# </body>

# </html>
# """
base_index_html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/style.css">
    <title>/mmd/</title>
</head>

<body>

    <div class="c">
        <header class="en">
            <a href="emailto: {%email%}">gmail</a>
            <span> - </span>
            <a href="{%tg%}">tg</a>
            <span> - </span>
            <a href="#">/mle/</a>
            <span> - </span>
            <a href="http://git.ar3642.top">git</a>

            <h3 class="fa">
                {%bio%}
            </h3>

        </header>
         <ul class="fa">
            {%body%}
        </ul>

    </div>

</body>

</html>
"""


lofmds = list(filter(os.path.isfile, glob.glob(r"../mds" + "/*")))
lofmds.sort(key=os.path.getctime)

for md in lofmds:
    n = f"pandoc -f markdown -t html5 --template base.html -o ../public_html/{md.split('/')[-1].split('.')[0]}.html {md}"
    cmd = f"pandoc -s --template base.html {md} -o ../public_html/{md.split('/')[-1].split('.')[0]}.html"
    os.system(n)


with open("base.json", "rb") as f:
    dta = json.load(f)
    base_index_html = base_index_html.replace("{%email%}", dta['email'])
    base_index_html = base_index_html.replace("{%tg%}", dta['tg'])
    # base_index_html = base_index_html.replace("{%xmpp%}", dta['xmpp'])
    base_index_html = base_index_html.replace("{%bio%}", dta['bio'])


posts = ''
lofmds.reverse()
for s in lofmds:

    date = str(datetime.datetime.today())[:-10]

    data = pathlib.Path(s).read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=['meta'])
    md.convert(data)
    if md.Meta['date'] == [""]:
        with open(s, 'r') as file:
            data = file.readlines()
        data[2] = f'date: {date}\n'

        with open(s, 'w') as file:
            file.writelines(data)
    else:
        date = md.Meta['date'][0]

    if md.Meta['draft'][0] == 'false':
        # <span>::</span> <small>{date}</small>
        # posts += f"<div class='box'><a href='{s.split('/')[-1].split('.')[0]}.html'><h3>{md.Meta['title'][0]}</h3></a>  <small>{md.Meta['tldr'][0]}</small></div>"
        posts += f"<li><span>{md.Meta['date'][0].split(" ")[0]}</span> <a href='{s.split('/')[-1].split('.')[0]}.html'>{md.Meta['title'][0]}</a></li>"
base_index_html = base_index_html.replace("{%body%}", posts)

with open('../public_html/index.html', 'w') as file:
    file.writelines(base_index_html)
