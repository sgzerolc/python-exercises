## correlation

Correlation is a 3 by 3 convolution. It takes nine pixels multiplied by its factor in kernel as input and return a sum as output.

I found two problems in design:

1. Corner cases: how to represent the corner case?
2. Kernel representations: using a list involves five cases at least in correlation process

Implementations:

In order to represent the nine locations in a cleaner way, we can think of how to use relative locations:(0,0),(1,0)... A dictionary to store the location and corresponding factor in kernel should suffice.

- Kernel: {location: kernel_element, ...}

Therefore, correlation can loop over the dictionary to compute new pixel of every location.











