import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!

def index(image, x, y):
    # x is the width index, y is the height index(in the given test case)
    i = image['width'] * y + x
    return i

def get_pixel(image, x, y):
    return image['pixels'][index(image, x, y)]


def set_pixel(image, x, y, c):
    image['pixels'][index(image, x, y)] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0 for _ in range(image['height'] * image['width'])],
    }

    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS




def range_list(n):
    """
    output: [(x,y), ...]
    """
    r = []
    limit = n//2
    for y in range(-limit, limit + 1):
        for x in range(-limit, limit + 1):
            r.append((x, y))
    return r


def kernel_repr(n, value):
    """
    value is a list.
    output: {(-1,1): v, (..):...}
    """
    k = {}
    l = range_list(n)
    i = 0
    for v in value:
        k[l[i]] = v
        i += 1
    return k

# def get_edge_pixel(i, j, image):
#     """
#     Deal with the edge effects.
#     If either one is negative, replace with the corresponding value.
#     input: out of bound range
#     output: index (x', y') of the image
#     l = (i, j)
#     """
#     if i < 0 and j < 0:





def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    kernel:assume that kernels will always be square and that every kernel will
    have an odd number of rows and columns.
    I want to support {(0,0),(0,1),(0.-1),...} search.
    kernel is a list.
    """
    # naive approach: assume that the image pixels are in suitable range and
    # kernel size is three.
    n = int(len(kernel) ** (1/2))
    k = kernel_repr(n, kernel)
    range_l = range_list(n)
    h = image['height']
    w = image['width']

    result = {
        'height': h,
        'width': w,
        'pixels': [0 for _ in range(h * w)]
    }

    for y in range(h):
        for x in range(w):
            cumulate = 0
            for l in range_l:
                xi = x + l[0]
                yi = y + l[1]
                # edge case
                # row case
                if xi < 0:
                    xi = 0
                elif xi >= w:
                    xi = w - 1
                # column case
                if yi < 0:
                    yi = 0
                elif yi >= h:
                    yi = h - 1
                color = get_pixel(image, xi, yi)
                cumulate += color * k[l]
            set_pixel(result, x, y, cumulate)

    return result

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0 for _ in range(image['height'] * image['width'])],
    }

    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            if type(color) is not int:
                color = round(color)  # notice the if statement
            if color < 0:
                set_pixel(result, x, y, 0)
            elif color > 255:
                set_pixel(result, x, y, 255)
            else:
                set_pixel(result, x, y, color)
    return result

# FILTERS


def box_k(n):
    """
    Kernel is a list. The kernel is an n\times nn×n square of identical values that sum to 1.
    Output: [1/n**2, ...,]
    """
    i = 1/n**2
    return [i for _ in range(n**2)]


def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    k = box_k(n)

    # then compute the correlation of the input image with that kernel
    corred = correlate(image, k)

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    result = round_and_clip_image(corred)
    return result

def sharpened(image, n):
    """
    Return a new image representing the result of applying an unsharp mask
    from a scaled version of the original image.

    input: n denotes the size of the blur kernel
    """
    kernel = box_k(n)
    corred = correlate(image, kernel)
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0 for _ in range(image['height'] * image['width'])],
    }

    for x in range(image['width']):
        for y in range(image['height']):
            pix = 2*get_pixel(image, x, y) - get_pixel(corred, x, y)
            set_pixel(result, x, y, pix);
    result = round_and_clip_image(result)
    return result

def edges(image):
    """
    Return a new image representing the result of applying edge detector.
    """
    K_x = [-1, 0, 1,
           -2, 0, 2,
           -1, 0, 1]
    K_y = [-1, -2, -1,
           0, 0, 0,
           1, 2, 1]
    O_x = correlate(image, K_x)
    O_y = correlate(image, K_y)
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0 for _ in range(image['height'] * image['width'])],
    }
    for x in range(image['width']):
        for y in range(image['height']):
            pix = (get_pixel(O_x, x, y)**2 + get_pixel(O_y, x, y)**2)**(1/2)
            set_pixel(result, x, y, pix)
    result = round_and_clip_image(result)
    return result

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    # test_cor = load_image("test_images/centered_pixel.png")
    kernel = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    k_nine = [0 for i in range(81)]
    k_nine[18] = 1
    # test_r_cor = correlate(test_cor, kernel)
    # save_image(test_r_cor, "test_results/test_cor.png")
    test_cor_hard = load_image("test_images/pigbird.png")
    cored = correlate(test_cor_hard, k_nine)
    save_image(cored, "test_results/cor_hard.png")
