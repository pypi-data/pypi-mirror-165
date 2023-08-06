from functools import lru_cache  # Replace with cache for Python>=3.9
from pathlib import Path

import cv2
import numpy as np
import xarray as xr
from astropy.visualization import PercentileInterval
from owl_dev.logging import logger

from .utils import hsv_to_rgb, umask


class TileSet:
    def __init__(self, store, output):
        self.store = store
        self.output = output
        self.levels = ["", "l.2", "l.4", "l.8", "l.16", "l.32"]

    @lru_cache(maxsize=None)
    def calculate_percentiles(self, fov, percentile=99.5):
        def _normalize(arr):
            pint = PercentileInterval(percentile)
            p1, p2 = pint.get_limits(arr.values.ravel())
            return xr.DataArray([p1, p2])

        ds = xr.open_zarr(self.store, group="l.16")
        arr = ds[fov]
        p = arr.groupby("channel").map(_normalize).compute()
        self.pvalues = p.values

    def _create_tile_image(self, data):
        def _normalize(x):
            norm = x / self.pvalues[:, 1][:, None, None]
            return norm.clip(0, 1)

        data = _normalize(data)

        colours = ["red", "green", "blue", "cyan", "yellow", "magenta", "grey"]
        select_colour = {
            "red": (0, 1),
            "green": (0.3, 1),
            "blue": (0.66, 1),
            "cyan": (0.5, 1),
            "yellow": (0.15, 1),
            "magenta": (0.86, 1),
            "grey": (0.3, 0),
        }

        hs_range = [select_colour[col] for col in colours]
        channels_rgb = []
        for hs, img in zip(hs_range, data):
            ch_hsl = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.float32)
            ch_hsl[:, :, 0] = hs[0]
            ch_hsl[:, :, 1] = hs[1]
            ch_hsl[:, :, 2] = img
            channels_rgb.append(hsv_to_rgb(ch_hsl))

        channels_rgb = np.stack(channels_rgb) * 255
        rgb = channels_rgb.sum(axis=0).clip(0, 255).astype("uint8")

        return rgb

    def _write_tiles(self, x, plane=0, level=0, block_info=None):
        try:
            loc = block_info[None]["chunk-location"][1:]
            p = Path(f"{self.output}/{plane}/{5-level}/{loc[0]}/")
            p.mkdir(parents=True, exist_ok=True)

            xx = self._create_tile_image(x)
            xx = np.pad(xx, ((0, 256 - xx.shape[0]), (0, 256 - xx.shape[1]), (0, 0)))
            cv2.imwrite(f"{p}/{loc[1]}.png", xx)
        except TypeError:
            loc = []
        return x

    def write_level(self, level):
        ds = xr.open_zarr(self.store, group=self.levels[level])
        for fov in list(ds):
            self.calculate_percentiles(fov)
            arr = ds[fov]
            im = arr.sel(z=0).drop("z").data.rechunk((-1, 256, 256))
            im.map_blocks(self._write_tiles, plane=fov, level=level).compute()


@umask
def create_tileset(input_path, subdir):
    # TODO: Add chmod in a decorator
    ts = TileSet(input_path / "mos", input_path / subdir)
    for level in [5, 4, 3, 2, 1]:
        logger.debug("Level %s", level)
        ts.write_level(level)
