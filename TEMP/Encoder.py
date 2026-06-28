import re, base64, json, sys, os

XOR_KEY = 0xA3

def extract_parts(html):
    m_style = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    if not m_style: raise ValueError('No <style> found')
    css = m_style.group(1)

    m_body = re.search(r'<body>(.*)</body>', html, re.DOTALL)
    if not m_body: raise ValueError('No <body> found')
    body_c = m_body.group(1)

    scripts = re.findall(r'<script>(.*?)</script>', body_c, re.DOTALL)
    body_html = re.sub(r'<script>.*?</script>', '', body_c, flags=re.DOTALL)
    body_html = '\n'.join(line for line in body_html.split('\n') if line.strip())
    all_js = '\n'.join(s.strip() for s in scripts)

    return css.strip(), body_html.strip(), all_js

def minify_js(js):
    js = re.sub(r'(?m)^\s*//.*$', '', js)
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'\s+', ' ', js)
    js = re.sub(r'\s*([{}()=;,:+\-*/!<>])\s*', r'\1', js)
    return js.strip()

def encode_data(css, html, js):
    package = json.dumps({'c': css, 'h': html, 'j': js}, ensure_ascii=False)
    raw = package.encode('utf-8')
    xored = bytes(b ^ XOR_KEY for b in raw)
    return base64.b64encode(xored).decode('ascii')

def build_bootstrap(payload_b64):
    head = '<!DOCTYPE html>\n<html lang="ko">\n<head>\n'
    head += '<meta charset="UTF-8">\n'
    head += '<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">\n'
    head += '<meta name="robots" content="noindex, nofollow">\n'
    head += '<meta name="theme-color" content="#28a745">\n'
    head += '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data:; connect-src \'self\' https://www.yeogicyber.co.kr https://api.yeogicyber.co.kr https://*.yeogicyber.co.kr; font-src \'self\'; manifest-src \'self\';">\n'
    head += '<link rel="manifest" href=\'data:application/json,{"display":"standalone","theme_color":"#28a745"}\'>\n'
    head += '<link rel="icon" id="dynamic-favicon" type="image/png">\n'
    head += '<title>\uc2a4\ub9c8\ud2b8 AI \ud559\uc2b5\uc9c0\uc6d0 \ub3c4\uc6b0\ubbf8 V5.9</title>\n'
    head += '<style>\n'
    head += '#_z{position:fixed;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#fdfdfd;z-index:999999;font-family:sans-serif;color:#28a745;font-size:18px;font-weight:700}\n'
    head += "#_z::after{content:'\\ubcf5\\ud638\\ud654 \\uc911...';animation:_p 1.5s ease-in-out infinite}\n"
    head += '@keyframes _p{0%,100%{opacity:1}50%{opacity:.3}}\n'
    head += '</style>\n</head>\n<body>\n<div id="_z"></div>\n<script>\n'
    head += "var P='" + payload_b64 + "',K=" + str(XOR_KEY) + '|0;\n'
    head += '(function(){var R=atob(P),B=new Uint8Array(R.length),i=0;for(;i<R.length;i++)B[i]=R.charCodeAt(i)^K;\n'
    head += 'var D=JSON.parse(new TextDecoder().decode(B));\n'
    head += "document.getElementById('_z').remove();\n"
    head += "var s=document.createElement('style');s.textContent=D.c;document.head.appendChild(s);\n"
    head += 'document.body.innerHTML=D.h;\n'
    head += "var j=document.createElement('script');j.textContent=D.j;document.body.appendChild(j);})();\n"
    head += '</script>\n</body>\n</html>'
    return head

def main():
    if len(sys.argv) < 2:
        print('Usage: python encode.py <input.html> [output.html]')
        sys.exit(1)
    inpath = sys.argv[1]
    if len(sys.argv) > 2:
        outpath = sys.argv[2]
    else:
        d = os.path.dirname(inpath)
        outpath = os.path.join(d, 'SMART_AI_Helper.html')

    with open(inpath, 'r', encoding='utf-8') as f:
        html = f.read()

    css, body_html, js = extract_parts(html)
    js_min = minify_js(js)
    payload = encode_data(css, body_html, js_min)
    output = build_bootstrap(payload)

    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(output)

    in_size = len(html)
    out_size = len(output)
    pct = 100 - (out_size * 100 // in_size)
    print(f'[encode.py] OK')
    print(f'  Input : {inpath} ({in_size:,} bytes)')
    print(f'  Output: {outpath} ({out_size:,} bytes, -{pct}%)')

if __name__ == '__main__':
    main()
