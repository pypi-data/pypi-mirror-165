# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import imgui
import numpy as np
from array import array
from gui_utils import imgui_utils

#----------------------------------------------------------------------------

class PredictionWidget:
    def __init__(self, viz):
        self.viz = viz

    @imgui_utils.scoped_by_object_id
    def __call__(self, show=True):
        viz = self.viz
        if viz._classifier_args:
            config = viz._classifier_args.config
        else:
            config = None
        if viz._use_classifier and viz._predictions is not None and isinstance(viz._predictions, list):
            for p, _pred_array in enumerate(viz._predictions):
                imgui.text(f'Pred {p}')
                imgui.same_line(viz.label_w)
                imgui.core.plot_histogram('##pred', array('f', _pred_array), scale_min=0, scale_max=1)
                imgui.same_line(viz.label_w + viz.font_size * 30)
                ol = config['outcome_labels'][config['outcomes'][p]]
                pred_str = ol[str(np.argmax(_pred_array))]
                if viz._use_uncertainty and viz._uncertainty is not None:
                    pred_str += " (UQ: {:.4f})".format(viz._uncertainty[p])
                imgui.text(pred_str)
        elif viz._use_classifier and viz._predictions is not None:
            imgui.text('Prediction')
            imgui.same_line(viz.label_w)
            imgui.core.plot_histogram('##pred', array('f', viz._predictions), scale_min=0, scale_max=1)
            imgui.same_line(viz.label_w + viz.font_size * 30)
            ol = config['outcome_labels']
            pred_str = ol[str(np.argmax(viz._predictions))]
            if viz._use_uncertainty and viz._uncertainty is not None:
                pred_str += " (UQ: {:.4f})".format(viz._uncertainty)
            imgui.text(pred_str)
        if viz._gan_config is not None and 'slideflow_kwargs' in viz._gan_config:
            sf_kw = viz._gan_config['slideflow_kwargs']
            if 'outcome_labels' in sf_kw:
                latent_idx = viz.latent_widget.class_idx
                if latent_idx >= 0 and str(latent_idx) in sf_kw['outcome_labels']:
                    imgui.text("Latent class: {} ({})".format(
                        sf_kw['outcome_labels'][str(latent_idx)],
                        latent_idx
                    ))
                else:
                    imgui.text("Latent class: -")
