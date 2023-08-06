"""
Implements support for matplotlib extensions such as pyplot.plot.
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import numba
import numpy as np
from numba.core import ir_utils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_global, signature
from numba.extending import infer_getattr, overload, overload_method
import bodo
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, gen_objmode_func_overload, gen_objmode_method_overload, get_overload_const_int, is_overload_constant_bool, is_overload_constant_int, is_overload_true, raise_bodo_error
from bodo.utils.utils import unliteral_all
this_module = sys.modules[__name__]
mpl_plt_kwargs_funcs = ['gca', 'plot', 'scatter', 'bar', 'contour',
    'contourf', 'quiver', 'pie', 'fill', 'fill_between', 'step', 'text',
    'errorbar', 'barbs', 'eventplot', 'hexbin', 'xcorr', 'imshow',
    'subplots', 'suptitle', 'tight_layout']
mpl_axes_kwargs_funcs = ['annotate', 'plot', 'scatter', 'bar', 'contour',
    'contourf', 'quiver', 'pie', 'fill', 'fill_between', 'step', 'text',
    'errorbar', 'barbs', 'eventplot', 'hexbin', 'xcorr', 'imshow',
    'set_xlabel', 'set_ylabel', 'set_xscale', 'set_yscale',
    'set_xticklabels', 'set_yticklabels', 'set_title', 'legend', 'grid',
    'tick_params', 'get_figure', 'set_xticks', 'set_yticks']
mpl_figure_kwargs_funcs = ['suptitle', 'tight_layout', 'set_figheight',
    'set_figwidth']
mpl_gather_plots = ['plot', 'scatter', 'bar', 'contour', 'contourf',
    'quiver', 'pie', 'fill', 'fill_between', 'step', 'errorbar', 'barbs',
    'eventplot', 'hexbin', 'xcorr', 'imshow']


def _install_mpl_types():
    jzxa__paxhn = [('mpl_figure_type', matplotlib.figure.Figure), (
        'mpl_axes_type', matplotlib.axes.Axes), ('mpl_text_type',
        matplotlib.text.Text), ('mpl_annotation_type', matplotlib.text.
        Annotation), ('mpl_line_2d_type', matplotlib.lines.Line2D), (
        'mpl_path_collection_type', matplotlib.collections.PathCollection),
        ('mpl_bar_container_type', matplotlib.container.BarContainer), (
        'mpl_quad_contour_set_type', matplotlib.contour.QuadContourSet), (
        'mpl_quiver_type', matplotlib.quiver.Quiver), ('mpl_wedge_type',
        matplotlib.patches.Wedge), ('mpl_polygon_type', matplotlib.patches.
        Polygon), ('mpl_poly_collection_type', matplotlib.collections.
        PolyCollection), ('mpl_axes_image_type', matplotlib.image.AxesImage
        ), ('mpl_errorbar_container_type', matplotlib.container.
        ErrorbarContainer), ('mpl_barbs_type', matplotlib.quiver.Barbs), (
        'mpl_event_collection_type', matplotlib.collections.EventCollection
        ), ('mpl_line_collection_type', matplotlib.collections.LineCollection)]
    for baws__lwu, whli__vqat in jzxa__paxhn:
        install_py_obj_class(types_name=baws__lwu, python_type=whli__vqat,
            module=this_module)


_install_mpl_types()


def generate_matplotlib_signature(return_typ, args, kws, obj_typ=None):
    kws = dict(kws)
    dea__jhrb = ', '.join(f'e{pmg__oli}' for pmg__oli in range(len(args)))
    if dea__jhrb:
        dea__jhrb += ', '
    awfik__hfzh = ', '.join(f"{fvy__sglwc} = ''" for fvy__sglwc in kws.keys())
    mbsq__oghj = 'matplotlib_obj, ' if obj_typ is not None else ''
    jweil__khl = f'def mpl_stub({mbsq__oghj} {dea__jhrb} {awfik__hfzh}):\n'
    jweil__khl += '    pass\n'
    nhu__jht = {}
    exec(jweil__khl, {}, nhu__jht)
    wztiv__fax = nhu__jht['mpl_stub']
    yjuwc__rfd = numba.core.utils.pysignature(wztiv__fax)
    xuz__tjb = ((obj_typ,) if obj_typ is not None else ()) + args + tuple(kws
        .values())
    return signature(return_typ, *unliteral_all(xuz__tjb)).replace(pysig=
        yjuwc__rfd)


def generate_axes_typing(mod_name, nrows, ncols):
    xlmlc__zsqm = '{}.subplots(): {} must be a constant integer >= 1'
    if not is_overload_constant_int(nrows):
        raise_bodo_error(xlmlc__zsqm.format(mod_name, 'nrows'))
    if not is_overload_constant_int(ncols):
        raise_bodo_error(xlmlc__zsqm.format(mod_name, 'ncols'))
    qxm__ynx = get_overload_const_int(nrows)
    jmkai__oxb = get_overload_const_int(ncols)
    if qxm__ynx < 1:
        raise BodoError(xlmlc__zsqm.format(mod_name, 'nrows'))
    if jmkai__oxb < 1:
        raise BodoError(xlmlc__zsqm.format(mod_name, 'ncols'))
    if qxm__ynx == 1 and jmkai__oxb == 1:
        ilx__xxve = types.mpl_axes_type
    else:
        if jmkai__oxb == 1:
            kyz__aowj = types.mpl_axes_type
        else:
            kyz__aowj = types.Tuple([types.mpl_axes_type] * jmkai__oxb)
        ilx__xxve = types.Tuple([kyz__aowj] * qxm__ynx)
    return ilx__xxve


def generate_pie_return_type(args, kws):
    ptwiy__dyn = args[4] if len(args) > 5 else kws.get('autopct', types.none)
    if ptwiy__dyn == types.none:
        return types.Tuple([types.List(types.mpl_wedge_type), types.List(
            types.mpl_text_type)])
    return types.Tuple([types.List(types.mpl_wedge_type), types.List(types.
        mpl_text_type), types.List(types.mpl_text_type)])


def generate_xcorr_return_type(func_mod, args, kws):
    gtuho__bofm = args[4] if len(args) > 5 else kws.get('usevlines', True)
    if not is_overload_constant_bool(gtuho__bofm):
        raise_bodo_error(
            f'{func_mod}.xcorr(): usevlines must be a constant boolean')
    if is_overload_true(gtuho__bofm):
        return types.Tuple([types.Array(types.int64, 1, 'C'), types.Array(
            types.float64, 1, 'C'), types.mpl_line_collection_type, types.
            mpl_line_2d_type])
    return types.Tuple([types.Array(types.int64, 1, 'C'), types.Array(types
        .float64, 1, 'C'), types.mpl_line_2d_type, types.none])


@infer_global(plt.plot)
class PlotTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws)


@infer_global(plt.step)
class StepTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws)


@infer_global(plt.scatter)
class ScatterTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_path_collection_type,
            args, kws)


@infer_global(plt.bar)
class BarTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_bar_container_type,
            args, kws)


@infer_global(plt.contour)
class ContourTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws)


@infer_global(plt.contourf)
class ContourfTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws)


@infer_global(plt.quiver)
class QuiverTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_quiver_type, args, kws)


@infer_global(plt.fill)
class FillTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_polygon_type), args, kws)


@infer_global(plt.fill_between)
class FillBetweenTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws)


@infer_global(plt.pie)
class PieTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(generate_pie_return_type(args,
            kws), args, kws)


@infer_global(plt.text)
class TextTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws)


@infer_global(plt.errorbar)
class ErrorbarTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.
            mpl_errorbar_container_type, args, kws)


@infer_global(plt.barbs)
class BarbsTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_barbs_type, args, kws)


@infer_global(plt.eventplot)
class EventplotTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_event_collection_type), args, kws)


@infer_global(plt.hexbin)
class HexbinTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws)


@infer_global(plt.xcorr)
class XcorrTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(generate_xcorr_return_type(
            'matplotlib.pyplot', args, kws), args, kws)


@infer_global(plt.imshow)
class ImshowTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_image_type,
            args, kws)


@infer_global(plt.gca)
class GCATyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_type, args, kws)


@infer_global(plt.suptitle)
class SuptitleTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws)


@infer_global(plt.tight_layout)
class TightLayoutTyper(AbstractTemplate):

    def generic(self, args, kws):
        return generate_matplotlib_signature(types.none, args, kws)


@infer_global(plt.subplots)
class SubplotsTyper(AbstractTemplate):

    def generic(self, args, kws):
        nrows = args[0] if len(args) > 0 else kws.get('nrows', types.literal(1)
            )
        ncols = args[1] if len(args) > 1 else kws.get('ncols', types.literal(1)
            )
        fns__qgbf = generate_axes_typing('matplotlib.pyplot', nrows, ncols)
        return generate_matplotlib_signature(types.Tuple([types.
            mpl_figure_type, fns__qgbf]), args, kws)


SubplotsTyper._no_unliteral = True


@infer_getattr
class MatplotlibFigureKwargsAttribute(AttributeTemplate):
    key = MplFigureType

    @bound_function('fig.suptitle', no_unliteral=True)
    def resolve_suptitle(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws,
            obj_typ=fig_typ)

    @bound_function('fig.tight_layout', no_unliteral=True)
    def resolve_tight_layout(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)

    @bound_function('fig.set_figheight', no_unliteral=True)
    def resolve_set_figheight(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)

    @bound_function('fig.set_figwidth', no_unliteral=True)
    def resolve_set_figwidth(self, fig_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =fig_typ)


@infer_getattr
class MatplotlibAxesKwargsAttribute(AttributeTemplate):
    key = MplAxesType

    @bound_function('ax.annotate', no_unliteral=True)
    def resolve_annotate(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.grid', no_unliteral=True)
    def resolve_grid(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.plot', no_unliteral=True)
    def resolve_plot(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.step', no_unliteral=True)
    def resolve_step(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_line_2d_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.scatter', no_unliteral=True)
    def resolve_scatter(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_path_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.contour', no_unliteral=True)
    def resolve_contour(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.contourf', no_unliteral=True)
    def resolve_contourf(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_quad_contour_set_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.quiver', no_unliteral=True)
    def resolve_quiver(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_quiver_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.bar', no_unliteral=True)
    def resolve_bar(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_bar_container_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.fill', no_unliteral=True)
    def resolve_fill(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_polygon_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.fill_between', no_unliteral=True)
    def resolve_fill_between(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.pie', no_unliteral=True)
    def resolve_pie(self, ax_typ, args, kws):
        return generate_matplotlib_signature(generate_pie_return_type(args,
            kws), args, kws, obj_typ=ax_typ)

    @bound_function('ax.text', no_unliteral=True)
    def resolve_text(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_text_type, args, kws,
            obj_typ=ax_typ)

    @bound_function('ax.errorbar', no_unliteral=True)
    def resolve_errorbar(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.
            mpl_errorbar_container_type, args, kws, obj_typ=ax_typ)

    @bound_function('ax.barbs', no_unliteral=True)
    def resolve_barbs(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_barbs_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.eventplot', no_unliteral=True)
    def resolve_eventplot(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.
            mpl_event_collection_type), args, kws, obj_typ=ax_typ)

    @bound_function('ax.hexbin', no_unliteral=True)
    def resolve_hexbin(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_poly_collection_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.xcorr', no_unliteral=True)
    def resolve_xcorr(self, ax_typ, args, kws):
        return generate_matplotlib_signature(generate_xcorr_return_type(
            'matplotlib.axes.Axes', args, kws), args, kws, obj_typ=ax_typ)

    @bound_function('ax.imshow', no_unliteral=True)
    def resolve_imshow(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_axes_image_type,
            args, kws, obj_typ=ax_typ)

    @bound_function('ax.tick_params', no_unliteral=True)
    def resolve_tick_params(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xlabel', no_unliteral=True)
    def resolve_set_xlabel(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xticklabels', no_unliteral=True)
    def resolve_set_xticklabels(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.mpl_text_type
            ), args, kws, obj_typ=ax_typ)

    @bound_function('ax.set_yticklabels', no_unliteral=True)
    def resolve_set_yticklabels(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.List(types.mpl_text_type
            ), args, kws, obj_typ=ax_typ)

    @bound_function('ax.set_ylabel', no_unliteral=True)
    def resolve_set_ylabel(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_xscale', no_unliteral=True)
    def resolve_set_xscale(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_yscale', no_unliteral=True)
    def resolve_set_yscale(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_title', no_unliteral=True)
    def resolve_set_title(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.legend', no_unliteral=True)
    def resolve_legend(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.get_figure', no_unliteral=True)
    def resolve_get_figure(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.mpl_figure_type, args,
            kws, obj_typ=ax_typ)

    @bound_function('ax.set_xticks', no_unliteral=True)
    def resolve_set_xticks(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)

    @bound_function('ax.set_yticks', no_unliteral=True)
    def resolve_set_yticks(self, ax_typ, args, kws):
        return generate_matplotlib_signature(types.none, args, kws, obj_typ
            =ax_typ)


@overload(plt.savefig, no_unliteral=True)
def overload_savefig(fname, dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', format=None, transparent=False, bbox_inches=
    None, pad_inches=0.1, metadata=None):

    def impl(fname, dpi=None, facecolor='w', edgecolor='w', orientation=
        'portrait', format=None, transparent=False, bbox_inches=None,
        pad_inches=0.1, metadata=None):
        with bodo.objmode():
            plt.savefig(fname=fname, dpi=dpi, facecolor=facecolor,
                edgecolor=edgecolor, orientation=orientation, format=format,
                transparent=transparent, bbox_inches=bbox_inches,
                pad_inches=pad_inches, metadata=metadata)
    return impl


@overload_method(MplFigureType, 'subplots', no_unliteral=True)
def overload_subplots(fig, nrows=1, ncols=1, sharex=False, sharey=False,
    squeeze=True, subplot_kw=None, gridspec_kw=None):
    fns__qgbf = generate_axes_typing('matplotlib.figure.Figure', nrows, ncols)
    baws__lwu = str(fns__qgbf)
    if not hasattr(types, baws__lwu):
        baws__lwu = f'objmode_type{ir_utils.next_label()}'
        setattr(types, baws__lwu, fns__qgbf)
    jweil__khl = f"""def impl(
        fig,
        nrows=1,
        ncols=1,
        sharex=False,
        sharey=False,
        squeeze=True,
        subplot_kw=None,
        gridspec_kw=None,
    ):
        with numba.objmode(axes="{baws__lwu}"):
            axes = fig.subplots(
                nrows=nrows,
                ncols=ncols,
                sharex=sharex,
                sharey=sharey,
                squeeze=squeeze,
                subplot_kw=subplot_kw,
                gridspec_kw=gridspec_kw,
            )
            if isinstance(axes, np.ndarray):
                axes = tuple([tuple(elem) if isinstance(elem, np.ndarray) else elem for elem in axes])
        return axes
    """
    nhu__jht = {}
    exec(jweil__khl, {'numba': numba, 'np': np}, nhu__jht)
    impl = nhu__jht['impl']
    return impl


gen_objmode_func_overload(plt.show, output_type=types.none, single_rank=True)
gen_objmode_func_overload(plt.draw, output_type=types.none, single_rank=True)
gen_objmode_func_overload(plt.gcf, output_type=types.mpl_figure_type)
gen_objmode_method_overload(MplFigureType, 'show', matplotlib.figure.Figure
    .show, output_type=types.none, single_rank=True)
gen_objmode_method_overload(MplAxesType, 'set_xlim', matplotlib.axes.Axes.
    set_xlim, output_type=types.UniTuple(types.float64, 2))
gen_objmode_method_overload(MplAxesType, 'set_ylim', matplotlib.axes.Axes.
    set_ylim, output_type=types.UniTuple(types.float64, 2))
gen_objmode_method_overload(MplAxesType, 'draw', matplotlib.axes.Axes.draw,
    output_type=types.none, single_rank=True)
gen_objmode_method_overload(MplAxesType, 'set_axis_on', matplotlib.axes.
    Axes.set_axis_on, output_type=types.none)
gen_objmode_method_overload(MplAxesType, 'set_axis_off', matplotlib.axes.
    Axes.set_axis_off, output_type=types.none)
