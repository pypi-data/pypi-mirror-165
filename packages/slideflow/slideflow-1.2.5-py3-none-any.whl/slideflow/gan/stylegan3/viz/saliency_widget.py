# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import imgui
from gui_utils import imgui_utils

#----------------------------------------------------------------------------

class SaliencyWidget:

    def __init__(self, viz):
        self.viz        = viz
        self.enabled    = False
        self.overlay    = False
        self.method_idx = 0
        self._saliency_methods_all = {
            'Vanilla': 0,
            'Vanilla (Smoothed)': 1,
            'Integrated Gradients': 2,
            'Integrated Gradients (Smooth)': 3,
            'Guided Integrated Gradients': 4,
            'Guided Integrated Gradients (Smooth)': 5,
            'Blur Integrated Gradients': 6,
            'Blur Integrated Gradients (Smooth)': 7,
        }
        self._saliency_methods_names = list(self._saliency_methods_all.keys())

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz

        if show:
            imgui.text('Saliency')
            imgui.same_line(viz.label_w)
            _clicked, self.enabled = imgui.checkbox('Enable', self.enabled)

            imgui.same_line(viz.label_w + viz.font_size * 5)
            with imgui_utils.grayed_out(not self.enabled):
                _clicked, self.overlay = imgui.checkbox('Overlay', self.overlay)

            imgui.same_line(viz.label_w + viz.font_size * 10)
            with imgui_utils.item_width(viz.font_size * 12), imgui_utils.grayed_out(not self.enabled):
                _clicked, self.method_idx = imgui.listbox("Method", self.method_idx, self._saliency_methods_names)

        viz.args.show_saliency = self.enabled
        viz.args.saliency_overlay = self.overlay

#----------------------------------------------------------------------------
