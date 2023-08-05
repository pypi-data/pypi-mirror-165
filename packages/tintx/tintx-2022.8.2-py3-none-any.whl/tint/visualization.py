"""
tint.visualization
==================

Visualization tools for tracks objects.

"""

from datetime import timedelta
import os
from pathlib import Path
import shlex
import shutil
import tempfile
from subprocess import run, CalledProcessError, PIPE
import sys
from typing import Optional

from cartopy import crs
from cartopy.mpl.geoaxes import GeoAxesSubplot
from IPython.display import display, Image
import pandas as pd
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
import numpy as np

from .grid_utils import get_grid_alt


class Tracer(object):
    colors = ["m", "r", "lime", "darkorange", "k", "b", "darkgreen", "yellow"]
    colors.reverse()

    def __init__(self, tobj, persist):
        self.tobj = tobj
        self.persist = persist
        self.color_stack = self.colors * 10
        self.cell_color = pd.Series()
        self.history = None
        self.current = None

    def update(self, nframe):
        self.history = self.tobj.tracks.loc[:nframe]
        self.current = self.tobj.tracks.loc[nframe]
        if not self.persist:
            dead_cells = [
                key
                for key in self.cell_color.keys()
                if key not in self.current.index.get_level_values("uid")
            ]
            self.color_stack.extend(self.cell_color[dead_cells])
            self.cell_color.drop(dead_cells, inplace=True)

    def _check_uid(self, uid):
        if uid not in self.cell_color.keys():
            try:
                self.cell_color[uid] = self.color_stack.pop()
            except IndexError:
                self.color_stack += self.colors * 5
                self.cell_color[uid] = self.color_stack.pop()

    def plot(self, ax):
        for uid, group in self.history.groupby(level="uid"):
            self._check_uid(uid)
            tracer = group[["grid_x", "grid_y"]]
            tracer = tracer * self.tobj.grid_size[[2, 1]]
            if self.persist or (uid in self.current.index):
                ax.plot(tracer.grid_x, tracer.grid_y, self.cell_color[uid])


def _get_axes(
    X: np.ndarray,
    Y: np.ndarray,
    ax: Optional[GeoAxesSubplot],
    **kwargs,
) -> GeoAxesSubplot:
    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection=crs.PlateCarree())
    if not isinstance(ax, GeoAxesSubplot):
        raise TypeError("Ax should be a cartopy GeoAxesSubplot object")
    ax.set_ylim(Y.min(), Y.max())
    ax.set_xlim(X.min(), X.max())
    ax.coastlines(**kwargs)
    return ax


def full_domain(
    tobj,
    grids,
    vmin=0.01,
    vmax=15,
    ax=None,
    cmap="Blues",
    alt=None,
    isolated_only=False,
    tracers=False,
    persist=False,
    dt=0,
    plot_style={},
):
    alt = alt or tobj.params["GS_ALT"]
    if tracers:
        tracer = Tracer(tobj, persist)
    nframes = tobj.tracks.index.levels[0].max() + 1
    grid = next(grids)
    X = grid["lon"]
    Y = grid["lat"]
    ax = _get_axes(X, Y, ax, **plot_style)
    try:
        data = grid["data"][0].filled(np.nan)
    except AttributeError:
        data = grid["data"][0]
    im = ax.pcolormesh(
        X,
        Y,
        data,
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        shading="gouraud",
    )

    ann = []

    def _update(enum):

        for i in range(len(ann)):
            try:
                an = ann.pop(i)
            except IndexError:
                pass
            try:
                an.remove()
            except ValueError:
                pass
        nframe, grid = enum
        print(f"Animating frame {nframe} / {nframes}", end="\r", flush=True)
        try:
            im.set_array(grid["data"][0].filled(np.nan).ravel())
        except AttributeError:
            im.set_array(grid["data"][0].ravel())
        ax.set_title(
            "Rain-rate at %s"
            % ((grid["time"] + timedelta(hours=dt)).strftime("%Y-%m-%d %H:%M"))
        )
        if nframe in tobj.tracks.index.levels[0]:
            frame_tracks = tobj.tracks.loc[nframe]
            if tracers:
                try:
                    tracer.update(nframe)
                    tracer.plot(ax)
                except KeyError:
                    pass

            for ind, uid in enumerate(frame_tracks.index):
                if isolated_only and not frame_tracks["isolated"].iloc[ind]:
                    continue
                x = frame_tracks["lon"].iloc[ind]
                y = frame_tracks["lat"].iloc[ind]
                ann.append(ax.annotate(uid, (x, y), fontsize=20))

    _update((0, grid))
    animation = FuncAnimation(ax.get_figure(), _update, frames=enumerate(grids))
    plt.close()
    return animation


def plot_traj(
    traj,
    X,
    Y,
    mpp=None,
    label=False,
    superimpose=None,
    cmap=None,
    ax=None,
    t_column=None,
    particles=None,
    pos_columns=None,
    plot_style={},
    mintrace=2,
    size=100,
    thresh=("mean", -1),
    color=None,
    **kwargs,
):

    """This code is a fork of plot_traj method in the plot module from the
    trackpy project see http://soft-matter.github.io/trackpy fro more details

    Plot traces of trajectories for each particle.
    Optionally superimpose it on a frame from the video.
    Parameters
    ----------
    tobj : trajectory containing the tracking object
    X : 1D array of the X vector
    Y : 1D array of the Y vector
    colorby : {'particle', 'frame'}, optional
    mpp : float, optional
        Microns per pixel. If omitted, the labels will have units of pixels.
    label : boolean, optional
        Set to True to write particle ID numbers next to trajectories.
    basemap_res: str
        Set the resolution of the basemap
    superimpose : ndarray, optional
        Background image, default None
    cmap : colormap, optional
        This is only used in colorby='frame' mode. Default = mpl.cm.winter
    ax : matplotlib axes object, optional
        Defaults to current axes
    t_column : string, optional
        DataFrame column name for time coordinate. Default is 'frame'.
    particles : a preset of stroms (particles) to be drawn, instead of all
        (default)
    size : size of the sctter indicating start and end of the storm
    color : A pre-defined color, if None (default) each track will be assigned
        a different color
    thresh : tuple for thresholds to be applied to the plotted objects. first
        entry of the tuple is the variable (default 'mean') second one the
        the minimum value (default -1)
    create_map: boolean, reate a map object, this can be useful for loops where
        a basemap object has already been created
    pos_columns : list of strings, optional
        Dataframe column names for spatial coordinates. Default is ['x', 'y'].
    plot_style : dictionary
        Keyword arguments passed through to the `Axes.plot(...)` command
    mintrace : int
        Minimum length of a trace to be plotted
    Returns
    -------
    Axes object

    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    plot_style.setdefault("lw", 0.5)
    ax = _get_axes(X, Y, ax, **plot_style)
    proj = ax.projection
    cmap = cmap or plt.cm.winter
    t_column = t_column or "scan"
    pos_columns = pos_columns or ["lon", "lat"]
    if len(traj) == 0:
        raise ValueError("DataFrame of trajectories is empty.")
    _plot_style = dict(linewidth=1)
    _plot_style.update(**_normalize_kwargs(plot_style, "line2d"))

    # Axes labels
    if mpp is None:
        # _set_labels(ax, '{} [px]', pos_columns)
        mpp = 1.0  # for computations of image extent below
    else:
        if mpl.rcParams["text.usetex"]:
            _set_labels(ax, r"{} [\textmu m]", pos_columns)
        else:
            _set_labels(ax, r"{} [\xb5m]", pos_columns)
    # Background image
    if superimpose is not None:
        ax.imshow(
            superimpose,
            cmap=plt.cm.gray,
            origin="lower",
            interpolation="nearest",
            vmin=kwargs.get("vmin"),
            vmax=kwargs.get("vmax"),
        )
        ax.set_xlim(-0.5 * mpp, (superimpose.shape[1] - 0.5) * mpp)
        ax.set_ylim(-0.5 * mpp, (superimpose.shape[0] - 0.5) * mpp)
    # Trajectories
    # Read http://www.scipy.org/Cookbook/Matplotlib/MulticoloredLine
    y = traj["lat"]
    x = traj["lon"]
    val = traj[thresh[0]]
    if particles is None:
        uid = np.unique(x.index.get_level_values("uid")).astype(np.int32)
        uid.sort()
        particles = uid.astype(str)

    for particle in particles:
        try:
            x1 = x[:, particle].values
            y1 = y[:, particle].values
            mean1 = val[:, particle].values.mean()
        except KeyError:
            x1 = x[:, int(particle)].values
            y1 = y[:, int(particle)].values
            mean1 = val[:, int(particle)].values.mean()
        if x1.shape[0] > int(mintrace) and mean1 >= thresh[1]:
            im = ax.plot(x1, y1, color=color, **plot_style)
            ax.scatter(x1[0], y1[0], marker="o", color=color, s=[size])
            ax.scatter(x1[-1], y1[-1], marker="*", color=color, s=[size])
            if label:
                if len(x1) > 1:
                    cx, cy = proj.transform_point(
                        x1[int(x1.size / 2)], y1[int(y1.size / 2)], proj
                    )
                    dx, dy = proj.transform_point(
                        ((x1[1] - x1[0]) / 8.0), ((y1[1] - y1[0]) / 8.0), proj
                    )
                else:
                    cx, cy = proj.transform_point(x1[0], y1[0], proj)
                    dx, dy = 0, 0
                ax.annotate(
                    "%s" % str(particle),
                    xy=(cx, cy),
                    xytext=(cx + dx, cy + dy),
                    fontsize=16,
                    horizontalalignment="center",
                    verticalalignment="center",
                )
        else:
            im = None
    return ax, im


def make_mp4_from_frames(tmp_dir, dest_dir, basename, fps, glob="*"):
    res = run(
        shlex.split(
            "ffmpeg -framerate "
            + str(fps)
            + " -pattern_type glob -i '"
            + glob
            + ".png'"
            + " -movflags faststart -pix_fmt yuv420p -vf"
            + " 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -y "
            + basename
        ),
        stdout=PIPE,
        stderr=PIPE,
        cwd=tmp_dir,
    )
    try:
        if os.path.isfile(os.path.join(dest_dir, basename)):
            os.remove(os.path.join(dest_dir, basename))
        shutil.move(os.path.join(tmp_dir, basename), dest_dir)
    except FileNotFoundError:
        print("Make sure ffmpeg is installed properly.")


def animate(
    tobj,
    grids,
    outfile_name,
    fps=1,
    keep_frames=False,
    overwrite=False,
    embed_gif=False,
    ax=None,
    **kwargs,
):
    """
    Creates gif animation of tracked cells.

    Parameters
    ----------
    tobj : Cell_tracks
        The Cell_tracks object to be visualized.
    grids : iterable
        An iterable containing all of the grids used to generate tobj
    outfile_name : str
        The name of the output file to be produced.
    alt : float
        The altitude to be plotted in meters.
    vmin, vmax : float
        Limit values for the colormap.
    arrows : bool
        If True, draws arrow showing corrected shift for each object. Only used
        in 'full' style.
    isolation : bool
        If True, only annotates uids for isolated objects. Only used in 'full'
        style.
    uid : str
        The uid of the object to be viewed from a lagrangian persepective. Only
        used when style is 'lagrangian'.
    fps : int
        Frames per second for output gif.

    """
    outfile_name = Path(outfile_name).absolute()
    dest_dir = os.path.dirname(outfile_name)
    basename = os.path.basename(outfile_name)
    if len(dest_dir) == 0:
        dest_dir = os.getcwd()

    if os.path.exists(os.path.join(outfile_name)):
        if not overwrite:
            print("Filename already exists.")
            return
        else:
            os.remove(outfile_name)

    return full_domain(tobj, grids, **kwargs)
    with tempfile.TemporaryDirectory() as tmp_dir:
        if len(os.listdir(tmp_dir)) == 0:
            print("Grid generator is empty.")
            return
        make_mp4_from_frames(tmp_dir, outfile_name, basename, fps)
        if keep_frames:
            frame_dir = os.path.join(dest_dir, basename + "_frames")
            shutil.copytree(tmp_dir, frame_dir)
    if embed_gif:
        return embed_mp4_as_gif(outfile_name)


def embed_mp4_as_gif(filename):
    """Makes a temporary gif version of an mp4 using ffmpeg for embedding in
    IPython. Intended for use in Jupyter notebooks."""
    if not os.path.exists(filename):
        print("file does not exist.")
        return

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    newfile = tempfile.NamedTemporaryFile()
    newname = newfile.name + ".gif"
    _ = run(
        shlex.split("ffmpeg -i " + basename + " " + newname),
        cwd=dirname,
        stdout=PIPE,
        stderr=PIPE,
    )

    try:
        with open(newname, "rb") as f:
            display(Image(f.read()))
    finally:
        os.remove(newname)


def _normalize_kwargs(kwargs, kind="patch"):
    """Convert matplotlib keywords from short to long form."""
    # Source:
    # github.com/tritemio/FRETBursts/blob/fit_experim/fretbursts/burst_plot.py
    if kind == "line2d":
        long_names = dict(
            c="color",
            ls="linestyle",
            lw="linewidth",
            mec="markeredgecolor",
            mew="markeredgewidth",
            mfc="markerfacecolor",
            ms="markersize",
        )
    elif kind == "patch":
        long_names = dict(
            c="color",
            ls="linestyle",
            lw="linewidth",
            ec="edgecolor",
            fc="facecolor",
        )
    _ = kwargs.pop("resolution", None)
    for short_name in long_names:
        if short_name in kwargs:
            kwargs[long_names[short_name]] = kwargs.pop(short_name)
    return kwargs


def _set_labels(ax, label_format, pos_columns):
    """This sets axes labels according to a label format and position column
    names. Applicable to 2D and 3D plotting.
    Parameters
    ----------
    ax : Axes object
        The axes object on which the plot will be called
    label_format : string
        Format that is compatible with ''.format (e.g.: '{} px')
    pos_columns : list of strings
        List of column names in x, y(, z) order.
    Returns
    -------
    None
    """
    ax.set_xlabel(label_format.format(pos_columns[0]))
    ax.set_ylabel(label_format.format(pos_columns[1]))
    if hasattr(ax, "set_zlabel") and len(pos_columns) > 2:
        ax.set_zlabel(label_format.format(pos_columns[2]))


def invert_yaxis(ax):
    """Inverts the y-axis of an axis object."""
    bottom, top = ax.get_ylim()
    if top > bottom:
        ax.set_ylim(top, bottom, auto=None)
    return ax
