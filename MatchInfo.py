# 图片匹配信息对象
class MatchInfo:
    def __init__(self, filepath, pic_urls):
        # md文件路径
        self.filepath = filepath
        # 文件中所有匹配到的图片url
        self.pic_urls = pic_urls

    def toString(self):
        s = "======================\n"
        s += self.filepath + ":\n"
        s += "\n".join(map(str, self.pic_urls))
        return s

    def to_dict(self):
        return {"filepath": self.filepath, "pic_urls": self.pic_urls}

    @classmethod
    def from_dict(cls, data):
        return cls(data["filepath"], data["pic_urls"])
