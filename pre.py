# coding=utf-8
import os
import codecs


class Processor():

    def is_zh(self, c):
        x = ord (c)
        # Punct & Radicals
        if x >= 0x2e80 and x <= 0x33ff:
            return False
        # '：'
        if x == 0xff1a:
            return False

        if x == 0xff08 or x == 0xff09:
            return False

        # Fullwidth Latin Characters
        elif x >= 0xff00 and x <= 0xffef:
            return True

        # CJK Unified Ideographs &
        # CJK Unified Ideographs Extension A
        elif x >= 0x4e00 and x <= 0x9fbb:
            return True
        # CJK Compatibility Ideographs
        elif x >= 0xf900 and x <= 0xfad9:
            return True

        # CJK Unified Ideographs Extension B
        elif x >= 0x20000 and x <= 0x2a6d6:
            return True

        # CJK Compatibility Supplement
        elif x >= 0x2f800 and x <= 0x2fa1d:
            return True

        else:
            return False

    def split_zh_en(self, zh_en_str):
        zh_group = []
        zh_gather = ""
        zh_status = False

        for c in zh_en_str:
            if not zh_status and self.is_zh(c):
                zh_status = True
            elif not self.is_zh(c) and zh_status:
                zh_status = False
                if zh_gather != "":
                    zh_group.append(zh_gather)
            if zh_status:
                zh_gather += c
            else:
                zh_gather = ""

        if zh_gather != "":
                zh_group.append(zh_gather)
        return zh_group

    def writefile(self, fn, v_ls):
        f = codecs.open(fn, 'wb', 'utf-8')
        for i in v_ls:
            f.write(i + os.linesep)
        f.close()

    def readfile(self, fn):
        rf = codecs.open(fn, 'r', 'utf-8')
        wf = codecs.open('post.txt', 'w', 'utf-8')
        for line in rf:
            group = self.split_zh_en(line.strip())
            if len(group) > 0:
                ch = group[0]
            wf.write(ch + os.linesep)
        rf.close()
        wf.close()

if __name__ == '__main__':
    processor = Processor()
    processor.readfile(u'pre.txt')
