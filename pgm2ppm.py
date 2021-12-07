import numpy as np
import skimage

def single_yuv2rgb(im, progressive=False, top_field=False):
    final_img_shape = int(im.shape[0] * 2 / 3), im.shape[1]
    y_shape = final_img_shape
    u_shape = int(im.shape[0] * 1 / 3), im.shape[1] // 2
    v_shape = int(im.shape[0] * 1 / 3), im.shape[1] // 2

    assert y_shape[0] + u_shape[0] == im.shape[0]
    # 4:2:0 sample mode
    # Get array of each channel
    y_img = im[:y_shape[0], :y_shape[1]]
    u_img = im[y_shape[0]:, :u_shape[1]]
    v_img = im[y_shape[0]:, u_shape[1]:]

    # if not progressive and not top_field:
    #     y_img = y_img[:-1]
    #     y_img = np.vstack((y_img[0], y_img))

    #     u_img = u_img[:-1]
    #     u_img = np.vstack((u_img[0], u_img))

    #     v_img = v_img[:-1]
    #     v_img = np.vstack((v_img[0], v_img))

    # Alignment `U` channel
    u_img = np.repeat(np.repeat(u_img, 2, axis=1), 2, axis=0)

    # Alignement `V` channel
    v_img = np.repeat(np.repeat(v_img, 2, axis=1), 2, axis=0)

    # Upscale if top field first
    if not progressive:
        # Upscale `Y` channel
        y_img = np.repeat(y_img, 2, axis=0)

        # Upscale `U` channel
        u_img = np.repeat(u_img, 2, axis=0)

        # Upscale `U` channel
        v_img = np.repeat(v_img, 2, axis=0)

    # Rescale values `Y` channel between [0, 1]
    y_img = y_img / 255.

    # Rescale values `U` channel between [-u_max, +u_max]
    u_max = 0.436
    u_img = u_img / 255. * 2 * u_max - u_max
    # Rescale values `V` channel between [-v_max, +v_max]
    v_max = 0.615
    v_img = v_img / 255. * 2 * v_max - v_max

    # Concatenate the 3 channels
    yuv_img = np.concatenate((np.expand_dims(y_img, axis=-1),
                              np.expand_dims(u_img, axis=-1),
                              np.expand_dims(v_img, axis=-1)), axis=-1)

    # YUV conversion matrix
    yuv2rgb = np.array([[1, 0, 1.13983],
                        [1., -0.39465, -0.58060],
                        [1.0, 2.03211, 0.]])
    # Convert with matrice multiplication
    rgb_img = yuv2rgb @ yuv_img.reshape((-1, 3)).T
    rgb_img = rgb_img.T.reshape(yuv_img.shape)

    # Max value is not 1.0! Clip values between [0, 1]
    rgb_img = np.clip(rgb_img, 0, 1)
    # Convert to uint8 (values between [0, 255])
    rgb_img = (rgb_img * 255).astype(np.uint8)
    return rgb_img

def yuv2rgb(im_path, out_path=None, progressive=False):
    im = skimage.io.imread(im_path)


    if progressive:
        rgb_img = single_yuv2rgb(im, progressive=True)
        if out_path:
            skimage.io.imsave(out_path + ".ppm", rgb_img)
        return rgb_img
    else:
        # top field first
        # Convert
        rgb_img_1 = single_yuv2rgb(im[::2], progressive=False, top_field=True)
        # Copy lines
        if out_path:
            skimage.io.imsave(out_path + "1.ppm", rgb_img_1)

        # bottom field
        rgb_img_2 = single_yuv2rgb(im[1::2], progressive=False, top_field=False)
        if out_path:
            skimage.io.imsave(out_path + "2.ppm", rgb_img_2)
        return rgb_img_1, rgb_img_2