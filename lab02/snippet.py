def make_box(color):
    def create_image(h, w):
        return {'height': h, 'width': w, 'pixels': [color for _ in range(h*w)]}
    return create_image

maker = make_box(40)
im = maker(20, 30)
print(maker)
# print(im)