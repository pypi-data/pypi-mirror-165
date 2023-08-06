"""Plugin main widgets

widgets
-------
widget_cvtRGB()
    Put channel dims to the last dims so that napari can understand it as RGB
widget_norm
    Normalize the selected image with 99 percentile
widget_contrast_limits_all
    Change contrast limit max of all images at once
widget_scale
    Change scales of z, y, x
widget_points
    Change size of points at once
"""
import numpy as np

from magicgui import magic_factory, magicgui
from magicgui.widgets import Container, Label
from napari import layers as L
from napari import types


@magic_factory(
    img_layer=dict(tooltip="Select raw Brainbow image"),
    call_button='convertRGB',
)
def widget_cvtRGB(
    viewer: 'napari.Viewer',
    img_layer: L.Image,
) -> types.LayerDataTuple:
    # print(len(viewer.layers))
    # print(f"you have selected {img_layer}")
    data = img_layer.data
    # print(data.shape, data.ndim, data.dtype)
    if data.ndim == 4:
        # assume (z, c=3, y, x) or (c=3, z, y, x)
        if data.shape[-1] != 3:
            # (z, c=3, y, x)
            # data = img_layer.data.transpose(1, 0, 2, 3)
            viewer.layers.pop(viewer.layers.index(img_layer))
            kwargs = dict(
                name=img_layer.name + '_rgb'
            )
            return (data.transpose(0, 2, 3, 1), kwargs, 'image')
        else:
            return None
    else:
        return None


@magicgui(
    img_layer=dict(tooltip="Set maximum contrast limit to 99 percentile of the "
                   "given image"),
    call_button='normalize(img layer)(perc=99)',
)
def widget_norm(
    viewer: 'napari.Viewer',
    img_layer: L.Image,
):
    data = img_layer.data
    # print(data.shape)
    if data.shape[-1] == 3:
        # per channel
        _vmax = np.percentile(data, 99, axis=tuple(range(data.ndim - 1)))
        # print(f'_vmax: {_vmax}')
        vmax = max(_vmax)
        # print(f'vmax: {vmax}')
    else:
        vmax = np.percentile(data, 99)
        # print(f'vmax: {vmax}')
    contrast_limits = [img_layer.contrast_limits[0], vmax]
    # print(f'contrast_limits: {contrast_limits}')
    img_layer.contrast_limits = contrast_limits


@magicgui(
    contrast_limits_vmax=dict(
        label='vmax',
        widget_type='Slider',
        value=255,
        step=1,
        min=1,
        max=255,
        tooltip="Adjust all images' contrast_limits at once"
    ),
    auto_call=True,
)
def widget_contrast_limits_all(
    viewer: 'napari.Viewer',
    contrast_limits_vmax,
):
    for l in viewer.layers:
        if isinstance(l, L.Image):
            l.contrast_limits = [l.contrast_limits[0], contrast_limits_vmax]


@magicgui(
    scale_z=dict(
        widget_type='FloatSlider',
        value=1.0,
        step=0.1,
        min=0.5,
        max=5.0,
    ),
    scale_y=dict(
        widget_type='FloatSlider',
        value=1.0,
        step=0.1,
        min=0.5,
        max=5.0,
    ),
    scale_x=dict(
        widget_type='FloatSlider',
        value=1.0,
        step=0.1,
        min=0.5,
        max=5.0,
    ),
    scale_z_default=dict(
        widget_type='PushButton',
        value=True,
        text='default_z'
    ),
    scale_y_default=dict(
        widget_type='PushButton',
        value=True,
        text='default_y'
    ),
    scale_x_default=dict(
        widget_type='PushButton',
        value=True,
        text='default_x'
    ),
    auto_call=True,
    call_button=False,
)
def widget_scale(
    viewer: 'napari.Viewer',
    scale_z,
    scale_y,
    scale_x,
    scale_z_default,
    scale_y_default,
    scale_x_default,
):
    scale_z = round(scale_z, 1)
    scale_y = round(scale_y, 1)
    scale_x = round(scale_x, 1)
    # print(scale_z, scale_y, scale_x)
    scale = scale_z, scale_y, scale_x
    for l in viewer.layers:
        if hasattr(l, 'scale'):
            # print(f"set scale of {l.name} to {scale}")
            l.scale = scale


@widget_scale.scale_z_default.changed.connect
def _scale_z_default(value):
    viewer = widget_scale.viewer.value
    # print(viewer, type(viewer))
    scale_z = 1.0
    scale_y = widget_scale.scale_y.value
    scale_x = widget_scale.scale_x.value
    scale = scale_z, scale_y, scale_x
    # update widget_scale_z
    widget_scale.scale_z.value = scale_z
    for l in viewer.layers:
        if hasattr(l, 'scale'):
            # print(f"set scale of {l.name} to {scale}")
            l.scale = scale


@widget_scale.scale_y_default.changed.connect
def _scale_y_default(value):
    viewer = widget_scale.viewer.value
    scale_z = widget_scale.scale_z.value
    scale_y = 1.0
    scale_x = widget_scale.scale_x.value
    scale = scale_z, scale_y, scale_x
    # update widget_scale_z
    widget_scale.scale_y.value = scale_y
    for l in viewer.layers:
        if hasattr(l, 'scale'):
            # print(f"set scale of {l.name} to {scale}")
            l.scale = scale


@widget_scale.scale_x_default.changed.connect
def _scale_x_default(value):
    viewer = widget_scale.viewer.value
    scale_z = widget_scale.scale_z.value
    scale_y = widget_scale.scale_y.value
    scale_x = 1.0
    scale = scale_z, scale_y, scale_x
    # update widget_scale_z
    widget_scale.scale_x.value = scale_x
    for l in viewer.layers:
        if hasattr(l, 'scale'):
            # print(f"set scale of {l.name} to {scale}")
            l.scale = scale


@magicgui(
    point_size=dict(
        tooltip="Change size of all points at once",
        widget_type="Slider",
        value=10,
        max=15
    ),
    auto_call=True,
    call_button=False,
)
def widget_points(
    point_layer: L.Points,
    point_size,
):
    # print(f"you have selected {point_layer}")
    # Seems to interact with scales and distance from camera
    point_layer.size = point_size


class MainWidget(Container):
    def __init__(
        self,
        layout='vertical',
        widgets=[
            widget_cvtRGB(),  # 0
            widget_norm,      # 1
            widget_contrast_limits_all,  # 2
            widget_scale,     # 3
            widget_points,    # 4
        ]
    ):
        widgets[0].label = 'Convert to RGB'
        widgets[1].label = 'Normalize'
        widgets[2].label = 'Contrast max'
        widgets[3].label = 'ZYX scale'
        widgets[4].label = 'Points size'

        widget_desc = Label(
            name='Description',
            label="Description",
            value=(
                "1. Open an image (or drag-and-drop)\n"
                "2. Convert it to RGB\n"
                "3. In 'layer list' on the left, right-click \n"
                "  the image layer and 'Split Stack'. This \n"
                "  will split channels into layers. This is \n"
                "  useful when you go 3D (Ctrl+Y).\n"
                "4. You can adjust 'contrast limits' either \n"
                "  using 'Normalize' module or 'Contrast max'\n"
                "5. When you are on 3D view mode (Ctrl+Y), \n"
                "  z-scale is too short. Increasing it may \n"
                "  help by 'ZYX scale' slider.\n"
                "6. When you load a .csv file, it becomes a \n"
                "  Points layer in napari. You can resize \n"
                "  points using 'Points size' module.\n"
            ),
        )
        widgets.insert(0, widget_desc)
        super().__init__(layout=layout, widgets=widgets)


@magic_factory(
    img_layer=dict(tooltip="Select raw probability image"),
    threshold=dict(widget_type='FloatSlider',
                   min=0, max=1.0, step=0.01, value=0.5),
    auto_call=True
)
def threshold_prob(
    img_layer: L.Image,
    threshold
) -> types.LabelsData:
    return img_layer.data.copy() > threshold
