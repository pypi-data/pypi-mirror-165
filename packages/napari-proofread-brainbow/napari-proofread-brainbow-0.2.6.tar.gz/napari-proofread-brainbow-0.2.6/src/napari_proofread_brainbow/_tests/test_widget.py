from napari_proofread_brainbow import MainWidget
from napari_proofread_brainbow._widget import widget_cvtRGB
import numpy as np

# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
def test_main_widget(make_napari_viewer):
    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create main widget, passing in the viewer
    main_widget = MainWidget()

    # Check sub-widgets
    assert main_widget[0].label == 'Description'  # widget_desc
    assert main_widget[1].label == 'Convert to RGB'  # widget_cvtRGB
    assert main_widget[2].label == 'Normalize'  # widget_norm
    assert main_widget[3].label == 'Contrast max'  # widget_contrast_limits_all
    assert main_widget[4].label == 'ZYX scale'  # widget_scale
    assert main_widget[5].label == 'Points size'  # widget_points

    # read captured output and check that it's as we expected
    # captured = capsys.readouterr()
    # assert captured.out == "napari has 1 layers\n"


# def test_example_magic_widget(make_napari_viewer, capsys):
#     viewer = make_napari_viewer()
#     layer = viewer.add_image(np.random.random((100, 100)))

#     # this time, our widget will be a MagicFactory or FunctionGui instance
#     my_widget = example_magic_widget()

#     # if we "call" this object, it'll execute our function
#     my_widget(viewer.layers[0])

#     # read captured output and check that it's as we expected
#     captured = capsys.readouterr()
#     assert captured.out == f"you have selected {layer}\n"
