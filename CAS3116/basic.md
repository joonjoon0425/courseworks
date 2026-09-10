# Basics
- Sampling: pick bins
- Quantize: round each sample to a nearest integer (int8)

For color images, we can use Bayer filter.
We represent the color images with R G B color channels.

# Images in MATLAB
C * N * M
- C: channel in order of RGB
- the number of rows
- the number of columns

im(y, x, k): row y, column x, channel k
(i guess MATLAB uses column major format)

# Vectors in MATLAB
transpose: `v'`

Just practice MATLAB on your own.