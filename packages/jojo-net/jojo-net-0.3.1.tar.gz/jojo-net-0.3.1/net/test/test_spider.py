from net import *


w = Spider()
print(w.search("嘌呤").find("是"))
print(Spider().search("嘌呤").find("是"))
print("")

b = ZhiDao("李白 出生地")
print(b.count(), "条答案")
print(b.answer())
# print(ZhiDao("李白 出生地").answer())
print("")

b = BaiKe("爱在深秋", "谭咏麟")
print(b.catalog)
if '歌词' in b:
    print(b['歌词'])
# print(BaiKe("爱在深秋", "谭咏麟")['歌词'])
print("")

b = BaiKe("静夜思")
print(b['全文', '原文'])
# print(BaiKe("静夜思")['全文', '原文'])
print("")

b = WebImage('黑洞', 'png', count=5)
print(b.download_all())
# for index, img in enumerate(b.images):
#     print(img.filename, img.file_ext, img.url)
#     if not img.download(index):
#         print("error downloading image of %s" % index)


# username = ''
# password = ''
# mail = Mail(username, password)
