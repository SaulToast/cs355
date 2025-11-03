### Unsharp Masking

newImage = Image + alpha(Image - blurImage)

### edge detection

convolve with x kernel, convolve with y kernel, take the magntude of the gradient

*always divide by 8 when doing the sobel kernel convolutions*

