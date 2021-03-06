from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter


def _scale_dummies(row, dummy, weight):
    if not pd.isnull(row[dummy]):
        return row[dummy]*row[weight]
    return row[dummy]


def stack(df, x, y, weight=None,
          x_order=True, y_order=None, cmap_name=None,
          ax=None, fractions=False, legend=True, title=True):
    # Make dummies
    dummies = pd.get_dummies(df[y]).replace(0, np.nan)
    # Order the dummies if provided
    if y_order is not None:
        dummies = dummies[y_order]
    if title:
        dummies.columns = [c.title() for c in dummies.columns]

    # Remove unrequired columns (all except x and the dummies)
    all_cols = list(df.columns)
    all_cols.remove(x)
    if weight is not None:
        all_cols.remove(weight)
    _df = pd.concat([df.drop(all_cols, axis=1), dummies], axis=1)
    # Sort x if specified
    if x_order:
        if type(x_order) is bool:
            x_order = [_x for _x, _ in Counter(_df[x]).most_common()]
        else:
            assert type(x_order) is list, "x_order must be a bool or list"
        _df["sort_value"] = _df[x].apply(lambda x: x_order.index(x))
        _df = _df.sort_values(by="sort_value").drop(["sort_value"], axis=1)

    # If a weight has been specified then scale each dummy
    if weight is not None:
        for dummy in dummies:
            _df[dummy] = _df.apply(_scale_dummies, axis=1,
                                   dummy=dummy, weight=weight)
        _df.drop(weight, axis=1, inplace=True)

    # Generate an axis if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 3))

    # Count by group (don't autosort, since specified above)
    count = _df.groupby(x, sort=False).count()
    if weight is not None:
        count = _df.groupby(x, sort=False).sum()
    if fractions:
        # Normalise to row size if using fractions
        count = count.div(count.sum(axis=1), axis=0)
        # Don't show y-axis for fractions
        ax.yaxis.set_visible(False)

    # Plot and style
    color = None
    if cmap_name is not None:
        color = plt.get_cmap(cmap_name).colors
    count.plot(kind="bar", stacked=True, ax=ax, legend=legend, color=color)
    ticks = [t.get_text() for t in ax.get_xticklabels()]
    ax.set_xticklabels(ticks, rotation=25, ha="right", fontsize=10)
    ax.tick_params(axis=u'both', which=u'both', length=0)
    return ax
