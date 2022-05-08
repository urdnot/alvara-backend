from PIL import Image


def _sort_layers(layers):
    def layers_sort_func(o):
        return int(o['z'])
    layers.sort(key=layers_sort_func)


def mix(layers, destination):
    _sort_layers(layers)
    result = Image.open(layers[0]['path'])
    for i in range(1, len(layers)):
        new_img = Image.open(layers[i]['path'])
        result.paste(new_img, (0, 0), new_img)
        new_img.close()
    result.save(destination, 'PNG')
    result.close()
    return destination
