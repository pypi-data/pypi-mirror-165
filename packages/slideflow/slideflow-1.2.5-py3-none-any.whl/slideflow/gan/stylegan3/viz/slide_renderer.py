# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import sys
import copy
import traceback
import numpy as np
import torch
import torch.fft
import torch.nn
import matplotlib.cm
import dnnlib
from torch_utils.ops import upfirdn2d
import legacy # pylint: disable=import-error

from rich import print
import slideflow as sf

#----------------------------------------------------------------------------

class CapturedException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            _type, value, _traceback = sys.exc_info()
            assert value is not None
            if isinstance(value, CapturedException):
                msg = str(value)
            else:
                msg = traceback.format_exc()
        assert isinstance(msg, str)
        super().__init__(msg)

#----------------------------------------------------------------------------

class CaptureSuccess(Exception):
    def __init__(self, out):
        super().__init__()
        self.out = out

#----------------------------------------------------------------------------

def _sinc(x):
    y = (x * np.pi).abs()
    z = torch.sin(y) / y.clamp(1e-30, float('inf'))
    return torch.where(y < 1e-30, torch.ones_like(x), z)

def _lanczos_window(x, a):
    x = x.abs() / a
    return torch.where(x < 1, _sinc(x), torch.zeros_like(x))

def _reduce_dropout_preds(yp_drop, num_outcomes, stack=True):
    if sf.backend() == 'tensorflow':
        import tensorflow as tf
        if num_outcomes > 1:
            if stack:
                yp_drop = [tf.stack(yp_drop[n], axis=0) for n in range(num_outcomes)]
            else:
                yp_drop = [yp_drop[0] for n in range(num_outcomes)]
            yp_mean = [tf.math.reduce_mean(yp_drop[n], axis=0).numpy() for n in range(num_outcomes)]
            yp_std = [tf.math.reduce_std(yp_drop[n], axis=0).numpy() for n in range(num_outcomes)]
        else:
            if stack:
                yp_drop = tf.stack(yp_drop[0], axis=0)
            else:
                yp_drop = yp_drop[0]
            yp_mean = tf.math.reduce_mean(yp_drop, axis=0).numpy()
            yp_std = tf.math.reduce_std(yp_drop, axis=0).numpy()
    else:
        if num_outcomes > 1:
            if stack:
                yp_drop = [torch.stack(yp_drop[n], dim=0) for n in range(num_outcomes)]
            else:
                yp_drop = [yp_drop[0] for n in range(num_outcomes)]
            yp_mean = [torch.mean(yp_drop[n], dim=0) for n in range(num_outcomes)]
            yp_std = [torch.std(yp_drop[n], dim=0) for n in range(num_outcomes)]
        else:
            if stack:
                yp_drop = torch.stack(yp_drop[0], dim=0)  # type: ignore
            else:
                yp_drop = yp_drop[0]
            yp_mean = torch.mean(yp_drop, dim=0)  # type: ignore
            yp_std = torch.std(yp_drop, dim=0)  # type: ignore
    return yp_mean, yp_std

#----------------------------------------------------------------------------

def _construct_affine_bandlimit_filter(mat, a=3, amax=16, aflt=64, up=4, cutoff_in=1, cutoff_out=1):
    assert a <= amax < aflt
    mat = torch.as_tensor(mat).to(torch.float32)

    # Construct 2D filter taps in input & output coordinate spaces.
    taps = ((torch.arange(aflt * up * 2 - 1, device=mat.device) + 1) / up - aflt).roll(1 - aflt * up)
    yi, xi = torch.meshgrid(taps, taps)
    xo, yo = (torch.stack([xi, yi], dim=2) @ mat[:2, :2].t()).unbind(2)

    # Convolution of two oriented 2D sinc filters.
    fi = _sinc(xi * cutoff_in) * _sinc(yi * cutoff_in)
    fo = _sinc(xo * cutoff_out) * _sinc(yo * cutoff_out)
    f = torch.fft.ifftn(torch.fft.fftn(fi) * torch.fft.fftn(fo)).real

    # Convolution of two oriented 2D Lanczos windows.
    wi = _lanczos_window(xi, a) * _lanczos_window(yi, a)
    wo = _lanczos_window(xo, a) * _lanczos_window(yo, a)
    w = torch.fft.ifftn(torch.fft.fftn(wi) * torch.fft.fftn(wo)).real

    # Construct windowed FIR filter.
    f = f * w

    # Finalize.
    c = (aflt - amax) * up
    f = f.roll([aflt * up - 1] * 2, dims=[0,1])[c:-c, c:-c]
    f = torch.nn.functional.pad(f, [0, 1, 0, 1]).reshape(amax * 2, up, amax * 2, up)
    f = f / f.sum([0,2], keepdim=True) / (up ** 2)
    f = f.reshape(amax * 2 * up, amax * 2 * up)[:-1, :-1]
    return f

#----------------------------------------------------------------------------

def _apply_affine_transformation(x, mat, up=4, **filter_kwargs):
    _N, _C, H, W = x.shape
    mat = torch.as_tensor(mat).to(dtype=torch.float32, device=x.device)

    # Construct filter.
    f = _construct_affine_bandlimit_filter(mat, up=up, **filter_kwargs)
    assert f.ndim == 2 and f.shape[0] == f.shape[1] and f.shape[0] % 2 == 1
    p = f.shape[0] // 2

    # Construct sampling grid.
    theta = mat.inverse()
    theta[:2, 2] *= 2
    theta[0, 2] += 1 / up / W
    theta[1, 2] += 1 / up / H
    theta[0, :] *= W / (W + p / up * 2)
    theta[1, :] *= H / (H + p / up * 2)
    theta = theta[:2, :3].unsqueeze(0).repeat([x.shape[0], 1, 1])
    g = torch.nn.functional.affine_grid(theta, x.shape, align_corners=False)

    # Resample image.
    y = upfirdn2d.upsample2d(x=x, f=f, up=up, padding=p)
    z = torch.nn.functional.grid_sample(y, g, mode='bilinear', padding_mode='zeros', align_corners=False)

    # Form mask.
    m = torch.zeros_like(y)
    c = p * 2 + 1
    m[:, :, c:-c, c:-c] = 1
    m = torch.nn.functional.grid_sample(m, g, mode='nearest', padding_mode='zeros', align_corners=False)
    return z, m

#----------------------------------------------------------------------------

class Renderer:
    def __init__(self, visualizer):
        self._visualizer        = visualizer
        self._device            = torch.device('cuda')
        self._pkl_data          = dict()    # {pkl: dict | CapturedException, ...}
        self._networks          = dict()    # {cache_key: torch.nn.Module, ...}
        self._pinned_bufs       = dict()    # {(shape, dtype): torch.Tensor, ...}
        self._cmaps             = dict()    # {name: torch.Tensor, ...}
        self._is_timing         = False
        self._start_event       = torch.cuda.Event(enable_timing=True)
        self._end_event         = torch.cuda.Event(enable_timing=True)
        self._net_layers        = dict()    # {cache_key: [dnnlib.EasyDict, ...], ...}
        self._uq_thread         = None
        self._stop_uq_thread    = False
        self._stop_pred_thread  = False

    def render(self, **args):
        self._is_timing = True
        self._start_event.record(torch.cuda.current_stream(self._device))
        res = dnnlib.EasyDict()
        try:
            self._render_impl(res, **args)
        except:
            res.error = CapturedException()
        self._end_event.record(torch.cuda.current_stream(self._device))
        if 'error' in res:
            res.error = str(res.error)
        if self._is_timing:
            self._end_event.synchronize()
            res.render_time = self._start_event.elapsed_time(self._end_event) * 1e-3
            self._is_timing = False
        return res

    def get_network(self, pkl, key, **tweak_kwargs):
        data = self._pkl_data.get(pkl, None)
        if data is None:
            print(f'Loading "{pkl}"... ', end='', flush=True)
            try:
                with dnnlib.util.open_url(pkl, verbose=False) as f:
                    data = legacy.load_network_pkl(f)
                print('Done.')
            except:
                data = CapturedException()
                print('Failed!')
            self._pkl_data[pkl] = data
            self._ignore_timing()
        if isinstance(data, CapturedException):
            raise data

        orig_net = data[key]
        cache_key = (orig_net, self._device, tuple(sorted(tweak_kwargs.items())))
        net = self._networks.get(cache_key, None)
        if net is None:
            try:
                net = copy.deepcopy(orig_net)
                net = self._tweak_network(net, **tweak_kwargs)
                net.to(self._device)
            except:
                net = CapturedException()
            self._networks[cache_key] = net
            self._ignore_timing()
        if isinstance(net, CapturedException):
            raise net
        return net

    def _tweak_network(self, net):
        # Print diagnostics.
        #for name, value in misc.named_params_and_buffers(net):
        #    if name.endswith('.magnitude_ema'):
        #        value = value.rsqrt().numpy()
        #        print(f'{name:<50s}{np.min(value):<16g}{np.max(value):g}')
        #    if name.endswith('.weight') and value.ndim == 4:
        #        value = value.square().mean([1,2,3]).sqrt().numpy()
        #        print(f'{name:<50s}{np.min(value):<16g}{np.max(value):g}')
        return net

    def _get_pinned_buf(self, ref):
        key = (tuple(ref.shape), ref.dtype)
        buf = self._pinned_bufs.get(key, None)
        if buf is None:
            buf = torch.empty(ref.shape, dtype=ref.dtype).pin_memory()
            self._pinned_bufs[key] = buf
        return buf

    def to_device(self, buf):
        return self._get_pinned_buf(buf).copy_(buf).to(self._device)

    def to_cpu(self, buf):
        return self._get_pinned_buf(buf).copy_(buf).clone()

    def _ignore_timing(self):
        self._is_timing = False

    def _apply_cmap(self, x, name='viridis'):
        cmap = self._cmaps.get(name, None)
        if cmap is None:
            cmap = matplotlib.cm.get_cmap(name)
            cmap = cmap(np.linspace(0, 1, num=1024), bytes=True)[:, :3]
            cmap = self.to_device(torch.from_numpy(cmap))
            self._cmaps[name] = cmap
        hi = cmap.shape[0] - 1
        x = (x * hi + 0.5).clamp(0, hi).to(torch.int64)
        x = torch.nn.functional.embedding(x, cmap)
        return x

    def _calc_preds_and_uncertainty(self, img, uq_n=30):
        self._visualizer._uncertainty = None

        import tensorflow as tf
        yp = self._visualizer._classifier(tf.repeat(img, repeats=uq_n, axis=0), training=False)
        num_outcomes = 1 if not isinstance(yp, list) else len(yp)
        yp_drop = {n: [] for n in range(num_outcomes)}
        if num_outcomes > 1:
            for o in range(num_outcomes):
                yp_drop[o] = yp[o]
        else:
            yp_drop[0] = yp
        yp_mean, yp_std = _reduce_dropout_preds(yp_drop, num_outcomes, stack=False)
        if num_outcomes > 1:
            self._visualizer._uncertainty = [np.mean(s) for s in yp_std]
        else:
            self._visualizer._uncertainty = np.mean(yp_std)
        self._visualizer._predictions = yp_mean

    def _classify_img(self, img):
        c = self._visualizer._classifier_args

        def run_classification():
            nonlocal img
            if sf.backend() == 'tensorflow':
                import tensorflow as tf
                img = tf.expand_dims(img, axis=0)
                to_numpy = lambda x: x.numpy()
            elif sf.backend() == 'torch':
                img = torch.unsqueeze(img, dim=0)
                to_numpy = lambda x: x.cpu().detach().numpy()

            if c.config is not None and c.config['hp']['uq'] and self._visualizer._use_uncertainty:
                self._calc_preds_and_uncertainty(img)
            else:
                preds = self._visualizer._classifier(img)
                if isinstance(preds, list):
                    preds = [to_numpy(p[0]) for p in preds]
                else:
                    preds = to_numpy(preds[0])
                self._visualizer._predictions = preds

        run_classification()

    def _render_impl(self, res,
        x               = 0,
        y               = 0,
        show_saliency   = False,
        saliency_overlay= False,
        saliency_method = 0,
        pkl             = None,
        w0_seeds        = [[0, 1]],
        stylemix_idx    = [],
        stylemix_seed   = 0,
        class_idx       = None,
        mix_class       = None,
        trunc_psi       = 1,
        trunc_cutoff    = 0,
        random_seed     = 0,
        noise_mode      = 'const',
        force_fp32      = False,
        layer_name      = None,
        sel_channels    = 3,
        base_channel    = 0,
        img_scale_db    = 0,
        img_normalize   = False,
        fft_show        = False,
        fft_all         = True,
        fft_range_db    = 50,
        fft_beta        = 8,
        input_transform = None,
        untransform     = False,
    ):
        import pyvips
        # Stop UQ thread if running.
        self._stop_uq_thread = True
        viz = self._visualizer
        wsi = viz.wsi

        try:
            region = wsi.slide.read_region(
                (x, y),
                wsi.downsample_level,
                (wsi.extract_px, wsi.extract_px) #args.extract_px
            )
            if region.bands == 4:
                region = region.flatten()  # removes alpha
            if int(wsi.tile_px) != int(wsi.extract_px):
                region = region.resize(wsi.tile_px/wsi.extract_px)

            img = sf.slide.vips2numpy(region)
        except pyvips.error.Error as e:
            print(f"Tile coordinates {x}, {y} are out of bounds, skipping")
        else:
            # Select channels and compute statistics.
            #out = out.to(torch.float32)
            #if sel_channels > out.shape[0]:
            #    sel_channels = 1
            #base_channel = max(min(base_channel, out.shape[0] - sel_channels), 0)
            #sel = out[base_channel : base_channel + sel_channels]
            #res.stats = torch.stack([
            #    out.mean(), sel.mean(),
            #    out.std(), sel.std(),
            #    out.norm(float('inf')), sel.norm(float('inf')),
            #])

            res.image = img

            # Pre-process image.
            normalizer = viz._classifier_args.normalizer
            if sf.backend() == 'tensorflow':
                import tensorflow as tf
                dtype = tf.uint8
            elif sf.backend() == 'torch':
                dtype = torch.uint8
            proc_img = sf.io.convert_dtype(img, dtype)
            if sf.backend() == 'tensorflow':
                proc_img = sf.io.tensorflow.preprocess_uint8(
                    proc_img,
                    normalizer=normalizer,
                    standardize=True)['tile_image']
            elif sf.backend() == 'torch':
                proc_img = sf.io.torch.preprocess_uint8(
                    proc_img,
                    normalizer=normalizer,
                    standardize=True)

            # Saliency.
            if show_saliency:
                mask = viz.smap.get(proc_img, grad=saliency_method)
                if saliency_overlay:
                    res.image = sf.grad.plot_utils.overlay(img, mask)
                else:
                    res.image = sf.grad.plot_utils.inferno(mask)

            # FFT.
            if fft_show:
                out = torch.from_numpy(out)
                #sig = out if fft_all else sel
                sig = sig.to(torch.float32)
                sig = sig - sig.mean(dim=[1,2], keepdim=True)
                sig = sig * torch.kaiser_window(sig.shape[1], periodic=False, beta=fft_beta, device=self._device)[None, :, None]
                sig = sig * torch.kaiser_window(sig.shape[2], periodic=False, beta=fft_beta, device=self._device)[None, None, :]
                fft = torch.fft.fftn(sig, dim=[1,2]).abs().square().sum(dim=0)
                fft = fft.roll(shifts=[fft.shape[0] // 2, fft.shape[1] // 2], dims=[0,1])
                fft = (fft / fft.mean()).log10() * 10 # dB
                fft = self._apply_cmap((fft / fft_range_db + 1) / 2)
                res.image = torch.cat([img.expand_as(fft), fft], dim=1)

            # Show predictions.
            if viz._use_classifier:
                self._classify_img(proc_img)

    @staticmethod
    def run_synthesis_net(net, *args, capture_layer=None, **kwargs): # => out, layers
        submodule_names = {mod: name for name, mod in net.named_modules()}
        unique_names = set()
        layers = []

        def module_hook(module, _inputs, outputs):
            outputs = list(outputs) if isinstance(outputs, (tuple, list)) else [outputs]
            outputs = [out for out in outputs if isinstance(out, torch.Tensor) and out.ndim in [4, 5]]
            for idx, out in enumerate(outputs):
                if out.ndim == 5: # G-CNN => remove group dimension.
                    out = out.mean(2)
                name = submodule_names[module]
                if name == '':
                    name = 'output'
                if len(outputs) > 1:
                    name += f':{idx}'
                if name in unique_names:
                    suffix = 2
                    while f'{name}_{suffix}' in unique_names:
                        suffix += 1
                    name += f'_{suffix}'
                unique_names.add(name)
                shape = [int(x) for x in out.shape]
                dtype = str(out.dtype).split('.')[-1]
                layers.append(dnnlib.EasyDict(name=name, shape=shape, dtype=dtype))
                if name == capture_layer:
                    raise CaptureSuccess(out)

        hooks = [module.register_forward_hook(module_hook) for module in net.modules()]
        try:
            out = net(*args, **kwargs)
        except CaptureSuccess as e:
            out = e.out
        for hook in hooks:
            hook.remove()
        return out, layers

#----------------------------------------------------------------------------
