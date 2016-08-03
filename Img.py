import os


class Image:
    def __init__(self, search_tag, img_id, tags, sample_url, sample_width, sample_height, jpeg_url, jpeg_width, jpeg_height):
        self.search_tag = search_tag
        self.img_id = img_id
        self.tags = tags
        self.sample_url = sample_url
        self.sample_width = int(sample_width)
        self.sample_height = int(sample_height)
        self.jpeg_url = jpeg_url
        self.jpeg_width = int(jpeg_width)
        self.jpeg_height = int(jpeg_height)

    def is_hd(self):
        if self.sample_width == self.jpeg_height:
            return False
        else:
            return True

    def get_local_path(self):
        if self.search_tag == '':
            self.search_tag = 'All'
        if os.path.exists('/home/pi/spider/%s/' % self.search_tag) is False:
            os.makedirs('/home/pi/spider/%s/' % self.search_tag)
        return '/home/pi/spider/%s/%s.%s' % (self.search_tag, self.img_id, 'jpg' if self.is_hd() else 'png')

    def get_img_url(self):
        return self.jpeg_url if self.is_hd() else self.sample_url
