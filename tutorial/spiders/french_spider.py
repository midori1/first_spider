# coding=utf-8
import codecs
import os
import scrapy
from scrapy.http import Request, FormRequest


class FrenchSpider(scrapy.Spider):
    name = "french"
    allowed_domains = ["frenchfriend.net"]
    start_urls = [
        "http://frenchfriend.net/cidian/mpdic.aspx"
    ]

    url = "http://frenchfriend.net/cidian/mpdic.aspx"

    headers = {
        'Host': 'frenchfriend.net',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'

    }
    cookies = {
        'User': 'UserName=lushi01&Token=705548533424'
    }

    form_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUKMTI1ODUxMzM2MQ9kFgICAw9kFgYCAw8PFgIeBFRleHQFB2x1c2hpMDFkZAIJDxYCHwAFGOWFseafpeivouWIsCAyIOadoeS+i+WPpWQCCw8WAh4LXyFJdGVtQ291bnQCAhYEZg9kFgYCAQ8PFgIfAAUsPHNwYW4gc3R5bGU9ImNvbG9yOiNmZjAwMDAiPuWVg+iAgeaXjzwvc3Bhbj5kZAIDDw8WAh8ABXljZXV4IHF1aSB2aXZlbnQgdG91am91cnMgYXV4IGNyb2NoZXRzLyBkw6lwZW5zIGRlIGxldXJzIHBhcmVudHM7IMKrdW4gdGFuZ3V5wrsgKGFkdWx0ZSB2aXZhbnQgYXV4IGTDqXBlbnMgZGUgc2VzIHBhcmVudHMpZGQCBQ8PFgIeB1Zpc2libGVoZBYEAgEPDxYCHwJoZGQCAw8PFgIfAmhkZAIBD2QWBgIBDw8WAh8ABQnmnIjogIHml49kZAIDDw8WAh8ABa4BamV1bmVzIHBlcnNvbm5lcyBxdWkgZMOpcGVuc2VudCB0b3V0IGxldXIgc2FsYWlyZSBtZW5zdWVsIHBvdXIgZXV4LW3Dqm1lcyBldCB2aXZlbnQgYXV4IGTDqXBlbnMgZGUgbGV1cnMgcGFyZW50c+OAlOaciOWFieaXjyArIDxzcGFuIHN0eWxlPSJjb2xvcjojZmYwMDAwIj7llYPogIHml488L3NwYW4+44CVZGQCBQ8PFgIfAmhkFgQCAQ8PFgIfAmhkZAIDDw8WAh8CaGRkZDMqAcEpimm3FNmzyoWBFjU0KMXSEmvIk0E6DU4KLLqj',
        '__EVENTVALIDATION': '/wEdAAdL8DAMKp/RQgR3klfReoN23Zv7MWyIYa1ewtyvzeUqVBEghZBVv0boc2NaC2/zVFTN+DvxnwFeFeJ9MIBWR693H2gCHI1iwyD0QjZ+dKtTm/yCNLbZogGKbc6O5rlRxUWWECZPQRLurjTFVUPTWENW+sYDIrYWfoOzGv9P/1fd7ENtzsestvqc/lD04qjGpeo=',
        'TextBox1': u'命运共同体',
        'Button1': u'查询 Rechercher',
        'RadioButtonList1': u'模糊查询'
    }

    data = [
        u'惠农政策'
    ]

    # def init_data(self):
    #     rf = codecs.open('post.txt', 'r', 'utf-8')
    #     self.data =[line.strip() for line in rf]
    #     rf.close()

    def start_requests(self):
        # self.init_data()
        for item in self.data:
            self.form_data['TextBox1'] = item
            yield self.make_requests_from_url(self.url)

    def make_requests_from_url(self, url):
        return FormRequest(url, headers=self.headers, cookies=self.cookies, formdata=self.form_data)

    def parse(self, response):
        # filename = response.url.split("/")[-1] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        filename = 'output'
        with codecs.open(filename, 'a', 'utf-8') as f:
            chinese_spans = response.xpath('//*[starts-with(@id, "RepeaterRst_LabelSCh_")]')
            french_spans = response.xpath('//*[starts-with(@id, "RepeaterRst_LabelSfr_")]')
            word = response.xpath('//*[@id="TextBox1"]//@value').extract()[0]
            f.write(u'**' + word + u'**' + os.linesep)
            # print word
            limit = 0
            for chinese, french in zip(chinese_spans, french_spans):
                if limit < 5:
                    f.write(u'&emsp;&emsp;' + chinese.xpath('string(.)').extract()[0] + os.linesep)
                    f.write(u'&emsp;&emsp;&emsp;&emsp;' + french.xpath('string(.)').extract()[0] + os.linesep)
                    limit += 1
                else:
                    break
