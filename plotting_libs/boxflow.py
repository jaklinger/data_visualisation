from collections import OrderedDict
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath


class Bucket:
    def __init__(self, start, depth):
        self.start = start
        self.depth = depth
        self.level = start

    def fill(self, amount):
        before = self.level
        self.level = self.level + amount
        return before, self.level


class BoxFlow(OrderedDict):
    def __init__(self, data, ax=None, threshold=0.005):
        self.data = data
        self.initialise_buckets()
        self.total = self.build_buckets()
        self.patch_map = self.build_patches(threshold)
        self.line_args = self.build_lines()
        self.labels = self.build_labels()
        # Check if an axis has been provided
        if ax is None:
            fig, ax = plt.subplots()
        # Plot patches
        for label, patches in self.patch_map.items():
            for p in patches:
                # Generate the patch
                ax.add_patch(p)
        # Add bucket lines
        for args in self.line_args:
            ax.plot(*args, alpha=0.9)
        # Add labels
        for label in self.labels:
            ax.text(**label)
        # Format axes
        ax.set_ylim(-0.01*self.total, 1.01*self.total)
        ax.set_axis_off()
        self.ax = ax

    def initialise_buckets(self):
        for label, info in self.data.items():
            self[label] = 0
            for bucket_name, value in info.items():
                if bucket_name not in self:
                    self[bucket_name] = 0
                self[bucket_name] += value
                self[label] += value

    def build_buckets(self):
        start = 0
        for bucket_name, count in self.items():
            if bucket_name not in self.data.keys():
                continue
            self[bucket_name] = Bucket(start, count)
            start += count
        start = 0
        for bucket_name, count in self.items():
            if bucket_name in self.data.keys():
                continue
            self[bucket_name] = Bucket(start, count)
            start += count
        return start

    def build_patches(self, threshold):
        patch_map = {}
        for (label, info), color in zip(self.data.items(),
                                        plt.get_cmap("Set2").colors):
            patch_map[label] = []
            for bucket_name, value in info.items():
                start, _start = self[label].fill(value)
                end, _end = self[bucket_name].fill(value)
                if value < threshold * self.total:
                    continue
                path_data = [(mpath.Path.MOVETO, (0, start)),
                             (mpath.Path.LINETO, (1, end)),
                             (mpath.Path.LINETO, (1, _end)),
                             (mpath.Path.LINETO, (0, _start)),
                             (mpath.Path.CLOSEPOLY, (0, start))]
                codes, verts = zip(*path_data)
                path = mpath.Path(verts, codes)
                patch = mpatches.PathPatch(path, alpha=0.3,
                                           linewidth=0, color=color)
                patch_map[label].append(patch)
        return patch_map

    def build_lines(self):
        line_args = []
        line_args.append(((-0.02, 0.02), (0, 0), "k-"))
        line_args.append(((0.98, 1.02), (0, 0), "k-"))
        for bucket_name, bucket in self.items():
            if bucket_name not in self.data.keys():
                continue
            line_args.append(((-0.02, 0.02),
                              (bucket.level, bucket.level), "k-"))
        for bucket_name, bucket in self.items():
            if bucket_name in self.data.keys():
                continue
            line_args.append(((0.98, 1.02),
                              (bucket.level, bucket.level), "k-"))
        return line_args

    def build_labels(self):
        labels = []
        for bucket_name, bucket in self.items():
            if bucket_name not in self.data.keys():
                continue
            y = 0.5*(bucket.start + bucket.level) - len(self.data.keys())/8
            labels.append(dict(x=-0.05, y=y,
                               s=bucket_name, fontsize=14, ha="right"))
        for bucket_name, bucket in self.items():
            if bucket_name in self.data.keys():
                continue
            y = 0.5*(bucket.start + bucket.level) - len(self.data.keys())/8
            labels.append(dict(x=1.05, y=y,
                               s=bucket_name, fontsize=14))
        return labels


def boxflow(data, ax=None, threshold=0.005):
    return BoxFlow(data, ax, threshold).ax
