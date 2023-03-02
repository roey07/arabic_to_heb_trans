import sys
import os.path

trans_d = { u'\u0627': u'\u05d0',
         u'\u0623': u'\u05d0',
         u'\u0625': u'\u05d0\u05b4',
         u'\u0628': u'\u05d1',
         u'\u062a': u'\u05ea',
         u'\u062b': u"\u05ea'",
         u'\u062c': u"\u05d2'",
         u'\u062d': u'\u05d7',
         u'\u062e': u"\u05d7'",
         u'\u062f': u'\u05d3',
         u'\u0630': u"\u05d3'",
         u'\u0631': u'\u05e8',
         u'\u0632': u'\u05d6',
         u'\u0633': u'\u05e1',
         u'\u0634': u'\u05e9',
         u'\u0635': u'\u05e6',
         u'\u0636': u"\u05e6'",
         u'\u0637': u'\u05d8',
         u'\u0638': u"\u05d8'",
         u'\u0639': u'\u05e2',
         u'\u063a': u"\u05e2'",
         u'\u0641': u'\u05e4',
         u'\u0642': u'\u05e7',
         u'\u0643': u'\u05db',
         u'\u0644': u'\u05dc',
         u'\u0645': u'\u05de',
         u'\u0646': u'\u05e0',
         u'\u0647': u'\u05d4',
         u'\u0648': u'\u05d5',
         u'\u064a': u'\u05d9',
         u'\u0621': u'\u05d0',
         u'\u0629': u'\u05d4',
         u'\u0649': u'\u05d0',
         u'\u0652': u'\u05b0',
         u'\u064e': u'\u05b8',
         u'\u0651': u'\ufb1e',
         u'\u0650': u'\u05b4',
         u'\u0624': u'\u05d0',
         u'\u0626': u'\u05d0',
         u'\u0671': u'\u05d0',
         u'\u0622': u'\u05d0\u05b8\u05d0'}


trans_d_signs = {u'\u061f': u"?",
                 u'\u060c': u","}

heb_finals = { u'\u05de': u'\u05dd', 
               u'\u05e0': u'\u05df', 
               u'\u05e6': u'\u05e5', 
               u'\u05db': u'\u05da', 
               u'\u05e4': u'\u05e3' }

ignore = [u'\u0640']

nikud = [u'\u05b0', u'\u05b8', u'\ufb1e', u'\u05b4']
tashkeel = [u'\u0652', u'\u064e', u'\u0651', u'\u0650']

def last_letter(heb):
    t = 1
    while t <= len(heb):
        if heb[-t] not in nikud:
            break
        t += 1
    return heb[-t:] 


def transliterate(arabic):
    arabic += u" "
    heb = u""
    add_nun = False
    add_u = False
    for i, k in enumerate(arabic):
        if k in trans_d:
            if k in tashkeel and heb[-1] == u"'":
                heb = heb[:-1] + trans_d[k] + heb[-1]
            else:
                heb += trans_d[k]
        elif k == u'\u064b':
            add_nun = True
        elif k == u'\u064f':
            if i + 1 < len(arabic) and arabic[i+1] == u'\u0648':
                add_u = True
                continue
            elif heb[-1] == u"'":
                heb = heb[:-1] + u'\u05bb' + heb[-1]
            else:
                heb += u'\u05bb'
        else:
            if add_nun:
                heb += u'\u05df'
            if len(heb) != 0 and last_letter(heb)[0] in heb_finals:
                heb = heb[:-len(last_letter(heb))] + heb_finals[last_letter(heb)[0]] + last_letter(heb)[1:]
            if k in trans_d_signs:
                heb += trans_d_signs[k]
            elif k not in ignore:
                heb += k
            add_nun = False

        if add_u:
            heb += u'\u05BC'
            add_u = False

    return heb[:-1]


def main():
    if len(sys.argv) != 2:
        print("USAGE: transliterate.py <TEXT_FILE>")
        exit(1)
    f = open(sys.argv[1], "r", encoding="utf8")
    heb = transliterate(f.read())
    f.close()
    f = open(os.path.splitext(sys.argv[1])[0] + "_t" + os.path.splitext(sys.argv[1])[1], "w", encoding="utf8")
    f.write(heb)
    f.close()
    print("SUCCESS")
    return

if __name__ == "__main__":
    main()
