import click

import multiprocessing
import numpy as np
import imgui
import OpenGL.GL as gl
from gui_utils import imgui_window
from gui_utils import imgui_utils
from gui_utils import gl_utils
from gui_utils import text_utils
from viz import slide_renderer as renderer
from viz import slide_widget
from viz import saliency_widget
from viz import performance_widget
from viz import capture_widget
from viz import layer_widget
from viz import thumb_widget
from viz import prediction_widget

import pyvips

try:
    from . import dnnlib
except ImportError:
    # Error occurs when running script in StyleGAN3 directory
    import dnnlib

import slideflow as sf
import slideflow.grad

if sf.backend() == 'tensorflow':
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices('GPU')
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)

#----------------------------------------------------------------------------

class Visualizer(imgui_window.ImguiWindow):
    def __init__(self, classifier, classifier_args=None, capture_dir=None, ):
        super().__init__(title='Slide Visualizer', window_width=3840, window_height=2160)

        # Internals.
        self._last_error_print  = None
        self._async_renderer    = AsyncRenderer(self)
        self._defer_rendering   = 0
        self._tex_img           = None
        self._tex_obj           = None
        self._thumb_tex_img     = None
        self._thumb_tex_obj     = None
        self._predictions       = None
        self._classifier        = classifier
        self._classifier_args   = classifier_args
        self._use_classifier    = classifier is not None
        self._use_uncertainty   = classifier_args is not None and classifier_args.config['hp']['uq']
        self._gan_config        = None
        self._uncertainty       = None
        self._content_width     = None

        # Widget interface.
        self.wsi                = None
        self.thumb              = None
        self.thumb_zoom         = None
        self.thumb_origin       = None
        self.thumb_offset       = None
        self.thumb_focus_x      = None
        self.thumb_focus_y      = None
        self.box_x              = 0
        self.box_y              = 0
        self.tile_px            = classifier_args.config['tile_px']
        self.tile_um            = classifier_args.config['tile_um']
        self.args               = dnnlib.EasyDict()
        self.result             = dnnlib.EasyDict()
        self.pane_w             = 0
        self.label_w            = 0
        self.button_w           = 0
        self.x                  = 0
        self.y                  = 0

        # Widgets.
        self.slide_widget       = slide_widget.SlideWidget(self)
        self.prediction_widget  = prediction_widget.PredictionWidget(self)
        self.saliency_widget    = saliency_widget.SaliencyWidget(self)
        self.perf_widget        = performance_widget.PerformanceWidget(self)
        self.capture_widget     = capture_widget.CaptureWidget(self)
        self.layer_widget       = layer_widget.LayerWidget(self)
        self.thumb_widget       = thumb_widget.ThumbWidget(self)

        # Prepare saliency.
        self.smap = sf.grad.SaliencyMap(classifier, class_idx=1)

        if capture_dir is not None:
            self.capture_widget.path = capture_dir

        # Initialize window.
        self.set_position(0, 0)
        self._adjust_font_size()
        self.skip_frame() # Layout may change after first frame.

    def close(self):
        super().close()
        if self._async_renderer is not None:
            self._async_renderer.close()
            self._async_renderer = None

    def add_recent_slide(self, slide, ignore_errors=False):
        self.slide_widget.add_recent(slide, ignore_errors=ignore_errors)

    def load_slide(self, slide, ignore_errors=False):
        self.slide_widget.load(slide, ignore_errors=ignore_errors)

    def print_error(self, error):
        error = str(error)
        if error != self._last_error_print:
            print('\n' + error + '\n')
            self._last_error_print = error

    def defer_rendering(self, num_frames=1):
        self._defer_rendering = max(self._defer_rendering, num_frames)

    def clear_result(self):
        self._async_renderer.clear_result()

    def set_async(self, is_async):
        if is_async != self._async_renderer.is_async:
            self._async_renderer.set_async(is_async)
            self.clear_result()
            if 'image' in self.result:
                self.result.message = 'Switching rendering process...'
                self.defer_rendering()

    def _adjust_font_size(self):
        old = self.font_size
        self.set_font_size(min(self.content_width / 120, self.content_height / 60))
        if self.font_size != old:
            self.skip_frame() # Layout changed.

    def reset_thumb(self, width):
        max_w = (self.content_width - self.pane_w)
        max_h = self.content_height
        slide_hw_ratio = (self.wsi.dimensions[1] / self.wsi.dimensions[0])

        if (max_h / max_w) < slide_hw_ratio:
            _width = max_h // slide_hw_ratio
        else:
            _width = width

        self.thumb = np.asarray(self.wsi.thumb(width=_width))
        self.thumb_zoom = self.wsi.dimensions[0] / self.thumb.shape[1]
        self.thumb_origin = (0, 0)
        self.thumb_offset = (
            (max_w - self.thumb.shape[1]) / 2,
            (max_h - self.thumb.shape[0]) / 2
        )
        self.thumb_focus_x = self.wsi.dimensions[0] // 2
        self.thumb_focus_y = self.wsi.dimensions[1] // 2

    def wsi_coords_to_display_coords(self, x, y):
        return (
            int(((x - self.thumb_origin[0]) / self.thumb_zoom) + self.thumb_offset[0]),
            int(((y - self.thumb_origin[1]) / self.thumb_zoom) + self.thumb_offset[1])
        )

    def display_coords_to_wsi_coords(self, x, y):
        return (
            int((x - self.thumb_offset[0]) * self.thumb_zoom + self.thumb_origin[0]),
            int((y - self.thumb_offset[1]) * self.thumb_zoom + self.thumb_origin[1])
        )

    def draw_frame(self):
        self.begin_frame()
        self.args = dnnlib.EasyDict()
        self.pane_w = self.font_size * 45
        self.button_w = self.font_size * 5
        self.label_w = round(self.font_size * 4.5)

        # Begin control pane.
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.pane_w, self.content_height)
        imgui.begin('##control_pane', closable=False, flags=(imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE))

        # Widgets.
        expanded, _visible = imgui_utils.collapsing_header('Whole-slide image', default=True)
        self.slide_widget(expanded)
        expanded, _visible = imgui_utils.collapsing_header('Prediction & saliency', default=True)
        self.prediction_widget(expanded)
        self.saliency_widget(expanded)
        expanded, _visible = imgui_utils.collapsing_header('Performance & capture', default=True)
        self.perf_widget(expanded)
        self.capture_widget(expanded)
        expanded, _visible = imgui_utils.collapsing_header('Layers & channels', default=True)
        self.layer_widget(expanded)
        expanded, _visible = imgui_utils.collapsing_header('Example', default=True)
        self.thumb_widget(expanded)

        # Display.
        max_w = self.content_width - self.pane_w
        max_h = self.content_height

        # Detect mouse dragging in the thumbnail display.
        clicking, cx, cy, wheel = imgui_utils.click_hidden_window('##result_area', x=self.pane_w, y=0, width=self.content_width-self.pane_w, height=self.content_height)
        dragging, dx, dy = imgui_utils.shift_drag_hidden_window('##result_area', x=self.pane_w, y=0, width=self.content_width-self.pane_w, height=self.content_height)

        if self.thumb is not None:
            wsi_x, wsi_y = self.display_coords_to_wsi_coords(cx, cy)

            if dragging:
                self.thumb_focus_x -= (dx * self.thumb_zoom)
                self.thumb_focus_y -= (dy * self.thumb_zoom)
            if wheel > 0:
                self.thumb_zoom /= 1.5
            if wheel < 0:
                self.thumb_zoom *= 1.5
            if wheel:
                self.thumb_focus_x = wsi_x
                self.thumb_focus_y = wsi_y
            if wheel or dragging:
                try:
                    window_size = (int(max_w * self.thumb_zoom),
                                   int(max_h * self.thumb_zoom))

                    top_left = (
                        self.thumb_focus_x - (cx * window_size[0] / max_w),
                        self.thumb_focus_y - (cy * window_size[1] / max_h)
                    )

                    # Enforce boundary limits.
                    top_left = (max(top_left[0], 0), max(top_left[1], 0))
                    top_left = (min(top_left[0], self.wsi.dimensions[0]-window_size[0]), min(top_left[1], self.wsi.dimensions[1]-window_size[1]))

                    self.thumb_origin = top_left
                    target_size = (max_w, max_h)
                    region = self.wsi.slide.read_from_pyramid(
                        top_left=top_left,
                        window_size=window_size,
                        target_size=target_size)
                    if region.bands == 4:
                        region = region.flatten()  # removes alpha
                    self.thumb = sf.slide.vips2numpy(region)
                except pyvips.error.Error as e:
                    self.reset_thumb(max_w)

        # Re-generate thumbnail if the window size changed.
        if self._content_width != self.content_width:
            self.reset_thumb(max_w)
            self._content_width = self.content_width

        # Display thumbnail.
        if self.thumb is not None:

            # Render thumbnail.
            t_pos = np.array([self.pane_w + max_w / 2, max_h / 2])
            if self._thumb_tex_img is not self.thumb:
                self._thumb_tex_img = self.thumb
                if self._thumb_tex_obj is None or not self._thumb_tex_obj.is_compatible(image=self._thumb_tex_img):
                    self._thumb_tex_obj = gl_utils.Texture(image=self._thumb_tex_img, bilinear=False, mipmap=False)
                else:
                    self._thumb_tex_obj.update(self._thumb_tex_img)
            t_zoom = min(max_w / self._thumb_tex_obj.width, max_h / self._thumb_tex_obj.height)
            t_zoom = np.floor(t_zoom) if t_zoom >= 1 else t_zoom
            self._thumb_tex_obj.draw(pos=t_pos, zoom=t_zoom, align=0.5, rint=True)

            # Calculate thumbnail zoom and offset.
            self.thumb_offset = ((max_w - self.thumb.shape[1]) / 2, (max_h - self.thumb.shape[0]) / 2)
            thumb_max_x = self.thumb_offset[0] + self.thumb.shape[1]
            thumb_max_y = self.thumb_offset[1] + self.thumb.shape[0]

            # Calculate location for classifier display.
            if clicking and (self.thumb_offset[0] <= cx <= thumb_max_x) and (self.thumb_offset[1] <= cy <= thumb_max_y):
                self.x = wsi_x - (self.wsi.full_extract_px/2)
                self.y = wsi_y - (self.wsi.full_extract_px/2)
            if clicking or wheel:
                self.box_x, self.box_y = self.wsi_coords_to_display_coords(self.x, self.y)
                self.box_x += self.pane_w
            tw = self.wsi.full_extract_px // self.thumb_zoom

            # Draw box with OpenGL.
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
            gl.glLineWidth(3)
            #thumb_orig = np.array([self.pane_w + self.thumb_offset[0], self.thumb_offset[1]])
            box_pos = np.array([self.box_x, self.box_y])
            #gl_utils.draw_rect(pos=thumb_orig, size=np.array([tw, tw]), color=[0, 0, 1], mode=gl.GL_LINE_LOOP)
            gl_utils.draw_rect(pos=box_pos, size=np.array([tw, tw]), color=[1, 0, 0], mode=gl.GL_LINE_LOOP)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            gl.glLineWidth(3)

        # Render.
        self.args.x = self.x
        self.args.y = self.y
        if self.is_skipping_frames():
            pass
        elif self._defer_rendering > 0:
            self._defer_rendering -= 1
        #elif self.args.pkl is not None:
        else:
            self._async_renderer.set_args(**self.args)
            result = self._async_renderer.get_result()
            if result is not None:
                self.result = result

        # Display input image.
        pos = np.array([self.pane_w + max_w - (self.tile_px/2 + 20), max_h / 2])
        if 'image' in self.result:
            if self._tex_img is not self.result.image:
                self._tex_img = self.result.image
                if self._tex_obj is None or not self._tex_obj.is_compatible(image=self._tex_img):
                    self._tex_obj = gl_utils.Texture(image=self._tex_img, bilinear=False, mipmap=False)
                else:
                    self._tex_obj.update(self._tex_img)
            self._tex_obj.draw(pos=pos, zoom=1, align=0.5, rint=True)
        if 'error' in self.result:
            self.print_error(self.result.error)
            if 'message' not in self.result:
                self.result.message = str(self.result.error)
        if 'message' in self.result:
            tex = text_utils.get_texture(self.result.message, size=self.font_size, max_width=max_w, max_height=max_h, outline=2)
            tex.draw(pos=pos, align=0.5, rint=True, color=1)

        # End frame.
        self._adjust_font_size()
        imgui.end()
        self.end_frame()

#----------------------------------------------------------------------------

class AsyncRenderer:
    def __init__(self, visualizer):
        self._visualizer    = visualizer
        self._closed        = False
        self._is_async      = False
        self._cur_args      = None
        self._cur_result    = None
        self._cur_stamp     = 0
        self._renderer_obj  = None
        self._args_queue    = None
        self._result_queue  = None
        self._process       = None

    def close(self):
        self._closed = True
        self._renderer_obj = None
        if self._process is not None:
            self._process.terminate()
        self._process = None
        self._args_queue = None
        self._result_queue = None

    @property
    def is_async(self):
        return self._is_async

    def set_async(self, is_async):
        self._is_async = is_async

    def set_args(self, **args):
        assert not self._closed
        if args != self._cur_args:
            if self._is_async:
                self._set_args_async(**args)
            else:
                self._set_args_sync(**args)
            self._cur_args = args

    def _set_args_async(self, **args):
        if self._process is None:
            self._args_queue = multiprocessing.Queue()
            self._result_queue = multiprocessing.Queue()
            try:
                multiprocessing.set_start_method('spawn')
            except RuntimeError:
                pass
            self._process = multiprocessing.Process(target=self._process_fn, args=(self._args_queue, self._result_queue), daemon=True)
            self._process.start()
        self._args_queue.put([args, self._cur_stamp])

    def _set_args_sync(self, **args):
        if self._renderer_obj is None:
            self._renderer_obj = renderer.Renderer(self._visualizer)
        self._cur_result = self._renderer_obj.render(**args)

    def get_result(self):
        assert not self._closed
        if self._result_queue is not None:
            while self._result_queue.qsize() > 0:
                result, stamp = self._result_queue.get()
                if stamp == self._cur_stamp:
                    self._cur_result = result
        return self._cur_result

    def clear_result(self):
        assert not self._closed
        self._cur_args = None
        self._cur_result = None
        self._cur_stamp += 1

    @staticmethod
    def _process_fn(args_queue, result_queue):
        renderer_obj = renderer.Renderer()
        cur_args = None
        cur_stamp = None
        while True:
            args, stamp = args_queue.get()
            while args_queue.qsize() > 0:
                args, stamp = args_queue.get()
            if args != cur_args or stamp != cur_stamp:
                result = renderer_obj.render(**args)
                if 'error' in result:
                    result.error = renderer.CapturedException(result.error)
                result_queue.put([result, stamp])
                cur_args = args
                cur_stamp = stamp

#----------------------------------------------------------------------------

@click.command()
@click.argument('slides', metavar='PATH', nargs=-1)
@click.option('--capture-dir', help='Where to save screenshot captures', metavar='PATH', default=None)
@click.option('--browse-dir', help='Specify model path for the \'Browse...\' button', metavar='PATH')
@click.option('--classifier', help='Classifier network for categorical predictions.', metavar='PATH')
def main(
    slides,
    capture_dir,
    browse_dir,
    classifier,
):
    """Interactive model visualizer.

    Optional PATH argument can be used specify which .pkl file to load.
    """

    if classifier is not None:
        print("Loading classifier at {}...".format(classifier))
        config = sf.util.get_model_config(classifier)
        classifier_args = dnnlib.EasyDict(
            config=config,
            normalizer=sf.util.get_model_normalizer(classifier))

        print("Classifier args:")
        print("Tile px:   ", config['tile_px'])
        print("Tile um:   ", config['tile_um'])
        print("Normalizer:", classifier_args.normalizer)

        if sf.backend() == 'tensorflow':
            import tensorflow as tf
            model = tf.keras.models.load_model(classifier)
        elif sf.backend() == 'torch':
            model = sf.model.torch.load(classifier)
            model = model.eval()
    else:
        model = None
        classifier_args = None

    viz = Visualizer(capture_dir=capture_dir, classifier=model, classifier_args=classifier_args)

    if browse_dir is not None:
        viz.slide_widget.search_dirs = [browse_dir]

    # List pickles.
    if len(slides) > 0:
        for slide in slides:
            viz.add_recent_slide(slide)
        viz.load_slide(slides[0])
    else:
        pretrained = [
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-afhqv2-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-ffhq-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-ffhqu-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-ffhqu-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-metfaces-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-metfacesu-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-afhqv2-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-ffhq-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-ffhqu-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-ffhqu-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-metfaces-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-t-metfacesu-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-afhqcat-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-afhqdog-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-afhqv2-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-afhqwild-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-brecahad-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-celebahq-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-cifar10-32x32.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-ffhq-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-ffhq-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-ffhq-512x512.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-ffhqu-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-ffhqu-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-lsundog-256x256.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-metfaces-1024x1024.pkl',
            'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan2/versions/1/files/stylegan2-metfacesu-1024x1024.pkl'
        ]

        # Populate recent pickles list with pretrained model URLs.
        for url in pretrained:
            viz.add_recent_slide(url)

    # Run.
    while not viz.should_close():
        viz.draw_frame()
    viz.close()

#----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------
