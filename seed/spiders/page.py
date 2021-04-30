import scrapy


class PageSpider(scrapy.Spider):
    name = 'page'
    allowed_domains = ['bbs.wenxuecity.com']
    start_urls = ['https://bbs.wenxuecity.com/memory/']

    def parse(self, response):
        divs = response.xpath("//div[@class='odd' or @class='even']")

        page = {}
        threads = []
        nicks = []

        # process category only once per page
        page['cat_slug'] = response.url.split('/')[-2]

        # i['cat_name'] = response.xpath("normalize-space(//h1/text())").get()
        page['cat_name'] = response.xpath(
            "string(//h1)").get().replace(" ", "")

        page['page_url'] = response.url
        page['crawler'] = 'sql'

        for div in divs:
            parent = list()
            p = div.xpath('.//p')  # here we have all posts in a thread
            for k in range(0, len(p)):
                i = {}

                # I have i['hits'] and i['votes'] not implemented. May bring them back if process time allow.
                i['hits'] = 0
                i['votes'] = 0

                strtmp = p[k].xpath("normalize-space(.//small)")
                i['post_date'] = " ".join(
                    strtmp.re(r'(\d+:\d+:\d+)|(\d+/\d+/\d+)')).strip()
                i['nick'] = p[k].xpath('.//a[@class="b"]/text()').get()

                gender = p[k].xpath('text()').re_first(r'.*(♂|♀).*')
                i['gender'] = 0 if gender == '♂' else 1 if gender == '♀' else None

                if {'nick':i['nick'], 'gender':i['gender']} not in nicks:
                    nicks.append({'nick':i['nick'], 'gender':i['gender']})

                try:
                    i['bytes'] = int(strtmp.re_first(r'\d+'))
                except TypeError:
                    i['bytes'] = 0

                # i['num_replies'] = (len(p) - 1) if k == 0 else 0
                # i['is_op'] = 1 if k == 0 else 0

                # this will get full url
                # i['url'] = response.urljoin(p[k].xpath('./a/@href').get())
                # this will get the integer part of url only
                i['url'] = p[k].xpath('./a/@href').re_first(r'\d+')

                i['title'] = p[k].xpath('normalize-space(./a/text())').get()

                i['reply_to'] = parent.pop() if len(parent) else None
                if p[k].xpath('./@style').re_first(r'.* (\d+)px;.*'):
                    margin = int(p[k].xpath(
                        './@style').re_first(r'.* (\d+)px;.*'))
                else:
                    margin = 20
                try:
                    next_p = p[k + 1]

                    if next_p.xpath('./@style').re_first(r'.* (\d+)px;.*'):
                        next_margin = int(next_p.xpath(
                            './@style').re_first(r'.* (\d+)px;.*'))
                    else:
                        next_margin = 20
                    if next_margin > margin:
                        if i['reply_to']:
                            parent.append(i['reply_to'])
                        parent.append(i['url'])

                    elif next_margin == margin:
                        parent.append(i['reply_to'])
                    else:
                        for _ in range(int((margin - next_margin) / 20 - 1)):
                            parent.pop()
                except IndexError:
                    pass
                threads.append(i)
        page['nicks'] = nicks
        page['threads'] = threads
        yield page

        try:
            next_page = response.xpath('//a[contains(text(), "下一页")]')[0]
        except IndexError:
            next_page = None

        if next_page is not None:
            yield response.follow(next_page, self.parse)
