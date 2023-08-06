"""File containing utilities."""
import argparse
from copy import deepcopy
from datetime import datetime
import functools
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import shutil
from tqdm import tqdm

from torch.optim.lr_scheduler import CosineAnnealingLR
from cosine_annealing_warmup import CosineAnnealingWarmupRestarts

import torch
import torch.nn as nn
from torchvision.transforms import functional as functional_TF

################################################################################
# Set up seeds, CUDA, and number of workers
################################################################################
# Set up CUDA usage
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
torch.backends.cudnn.benchmark = True
num_workers = 24

# Turn off WandB console logging, since we don't need it and it breaks TQDM.
os.environ["WANDB_CONSOLE"] = "off"

# Make non-determinism work out. This function should be called first
def set_seed(seed):
    """Seeds the program to use seed [seed]."""
    if isinstance(seed, int):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        tqdm.write(f"Set the NumPy, PyTorch, and Random modules seeds to {seed}")
    elif isinstance(seed, dict):
        random.setstate(seed["random_seed"])
        np.random.set_state(seed["numpy_seed"])
        torch.set_rng_state(seed["pytorch_seed"])
        tqdm.write(f"Reseeded program with old seed")
    else:
        raise ValueError(f"Seed should be int or contain resuming keys")

    return seed

################################################################################
# File I/O Utils
################################################################################
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = f"{project_dir}/data"
new_line = "\n"

def data_without_split_or_path(data_str):
    """Returns [data_str] without its split."""
    splits = ["train", "val", "test"]
    if any([data_str.endswith(f"/{s}") for s in splits]):
        return os.path.basename(os.path.dirname(data_str))
    else:
        raise ValueError(f"Case for handing data_str {data_str} unknown")

def suffix_str(args):
    """Returns the suffix string for [args]."""
    return "" if args.suffix is None or args.suffix == "" else f"-{args.suffix}"
    
def tuple_to_str(t):
    if isinstance(t, (set, tuple, list)):
        return "_".join([str(t_) for t_ in t])
    else:
        return t

def contrastive_folder(args, resume=False):
    """Returns the folder to which to save a resnet trained with [args]."""
    uid = args.uid if args.job_id is None else args.job_id
    folder = f"{project_dir}/models_contrastive/{data_without_split_or_path(args.data_tr)}-{args.backbone}-{args.loss}-bs{args.bs}-epochs{args.epochs}-lr{args.lr:.2e}-pos_weight{args.pos_sim_weight}-res{args.res}-{uid}{suffix_str(args)}"
    conditional_safe_make_directory(folder)
    if not os.path.exists(f"{folder}/config.json"):
        with open(f"{folder}/config.json", "w+") as f:
            json.dump(vars(args), f)
    return folder

def generator_folder(args):
    """Returns the folder to which to save a Generator saved with [args]."""
    uid = args.uid if args.job_id is None else args.job_id

    folder = f"{project_dir}/generators/{data_without_split_or_path(args.data_tr)}-bs{args.bs}-epochs{args.epochs}-grayscale{args.grayscale}-ipc{args.ipc}-lr{args.lr:.2e}-mask_frac{args.mask_frac}-ns{tuple_to_str(args.ns)}-res{tuple_to_str(args.res)}-seed{args.seed}-{uid}{suffix_str(args)}"

    conditional_safe_make_directory(folder)
    if not os.path.exists(f"{folder}/config.json"):
        with open(f"{folder}/config.json", "w+") as f:
            json.dump(vars(args), f)
    return folder

################################################################################
# File I/O
################################################################################

def save_checkpoint(dictionary, path):
    """Saves contents of [dictionary] along with random states to [file]."""
    seed_states = {"seed": {
        "pytorch_seed": torch.get_rng_state(),
        "numpy_seed": np.random.get_state(),
        "random_seed": random.getstate()}
    }
    torch.save(dictionary | seed_states, path)
    tqdm.write(f"LOG: Saved files to {path.replace(project_dir, '')}")

################################################################################
# Printing I/O Utilities
################################################################################

def dict_to_pretty_str(d, max_line_length=120, prepend="", format_floats=True):
    """Returns a string that pretty prints dictionary [d] assuming a maximum
    line length of [max_line_length] and that each line begins with [prepend].
    """
    s, last_line_length = prepend, len(prepend)
    for k in sorted(d.keys()):
        item_len = len(f"{k}: {d[k]}, ")
        value = d[k]

        # Handle floats and singular-value Tensors
        if isinstance(value, torch.Tensor) and len(value.view(-1).shape) == 1:
            value = value.item()

        if isinstance(value, float) and format_floats and abs(value) < 1e-5:
            value = f"{value:.2e}"
        if isinstance(value, float) and format_floats and abs(value) >= 1e-5:
            value = f"{value:.2f}"
        if last_line_length + item_len > max_line_length - len(prepend):
            s += f"\n{prepend}{k}: {value}, "
            last_line_length = len(prepend) + item_len
        else:
            s += f"{k}: {value}, "
            last_line_length += item_len
    return s

def pretty_print_args(args):
    """Returns a pretty string representation of [dict]."""
    s = dict_to_pretty_str(vars(args))
    tqdm.write(f"{'-' * 40}\n{s}\n{'-' * 40}")

################################################################################
# Image I/O Utilities
################################################################################
plt.rcParams["savefig.bbox"] = "tight"
plt.tight_layout(pad=0.00)

def make_2d_list_of_tensor(x):
    """Returns [x] as a 2D list where inner element is a CxHxW Tensor.

    x   -- a 2D list of 3D tensors, a 1D list of 3D tensors,
            a 1D tensor of 3D tensors, a 2D tensor of 3D tensors, or a 3D tensor


    """
    is_image = lambda x: (isinstance(x, torch.Tensor)
        and len(x.shape) == 3
        and x.shape[0] in {1, 3})
    is_image_batch = lambda x: all([is_image(x_) for x_ in x])

    if is_image(x):
        if x.shape[0] == 1 or x.shape[0] == 3:
            result = [[x]]
        else:
            raise ValueError()
    elif is_image_batch(x):
        result = [[x_ for x_ in x]]
    elif all([is_image_batch(x_) for x_ in x]):
        result = [[x__ for x__ in x_] for x_ in x]
    else:
        raise ValueError(f"Unknown collection of types in 'image': {type(x)}{new_line}{type(x_) for x_ in x}")

    return [[r_.float().expand(3, -1, -1) for r_ in r] for r in result]

def show_image_grid(images):
    """Shows list of images [images], either a Tensor giving one image, a List
    where each element is a Tensors giving one images, or a 2D List where each
    element is a Tensor giving an image.
    """
    images = make_2d_list_of_tensor(images)

    fix, axs = plt.subplots(ncols=max([len(image_row) for image_row in images]),
        nrows=len(images), squeeze=False)
    for i,images_row in enumerate(images):
        for j,image in enumerate(images_row):
            axs[i, j].imshow(np.asarray(functional_TF.to_pil_image(image.detach())), cmap='Greys_r')
            axs[i, j].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
    plt.show()

def save_image_grid(images, path):
    """Builds a grid of images out of [images] and saves the image containing
    the grid to [path].
    """
    images = make_2d_list_of_tensor(images)

    fix, axs = plt.subplots(ncols=max([len(image_row) for image_row in images]),
        nrows=len(images), squeeze=False)
    for i,images_row in enumerate(images):
        for j,image in enumerate(images_row):
            axs[i, j].imshow(np.asarray(functional_TF.to_pil_image(image.detach())), cmap='Greys_r')
            axs[i, j].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

    if os.path.dirname(path) == "":
        pass
    elif not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    plt.savefig(path, dpi=512)
    plt.close("all")

################################################################################
# Miscellaneous utilities
################################################################################

def has_resolution(data_str):
    """Returns if [data_str] has a resolution."""
    if not "x" in data_str:
        return False
    else:
        x_idxs = [idx for idx,c in enumerate(data_str) if c == "x"]
        for x_idx in x_idxs:
            for n in range(1, min(x_idx, len(data_str) - x_idx)):
                res1 = data_str[x_idx - n:x_idx]
                res2 = data_str[x_idx + 1:x_idx + 1 + n]
                if res1.isdigit() and res2.isdigit():
                    return True
                else:
                    break
        return False

def remove_duplicates(x):
    """Removes duplicates from order 1 list [x]."""
    seen_elements = set()
    result = []
    for e in x:
        if e in seen_elements:
            continue
        else:
            result.append(e)
            seen_elements.add(e)

    return result

def make_cpu(input):
    if isinstance(input, (list, tuple)):
        return [make_cpu(x) for x in input]
    else:
        return input.cpu()

def make_device(input):
    if isinstance(input, (list, tuple)):
        return [make_device(x) for x in input]
    else:
        return input.to(device)

def make_3dim(input):
    if isinstance(input, list):
        return [make_3dim(x) for x in input]
    elif isinstance(input, torch.Tensor) and len(input.shape) == 4 and input.shape[0] == 1:
        return input.squeeze(0)
    elif isinstance(input, torch.Tensor) and len(input.shape) == 3:
        return input
    else:
        raise ValueError()

def evenly_divides(x, y):
    """Returns if [x] evenly divides [y]."""
    return int(y / x) == y / x

def round_so_evenly_divides(x, y):
    """Returns [x] adjusted up or down by up to so [y] divides it evenly."""
    return x + (y - (x % y)) if ((x % y) > y / 2) else x - (x % y)

def flatten(xs):
    """Returns collection [xs] after recursively flattening into a list."""
    if isinstance(xs, list) or isinstance(xs, set) or isinstance(xs, tuple):
        result = []
        for x in xs:
            result += flatten(x)
        return result
    else:
        return [xs]

def get_all_files(f):
    """Returns absolute paths to all files under [f]."""
    if os.path.isdir(f):
        return flatten([get_all_files(f"{f}/{x}") for x in os.listdir(f)])
    else:
        return f

def make_list(x, length=1):
    """Returns a list of length [length] where each elment is [x], or, if [x]
    is a list of length [length], returns [x].
    """
    if isinstance(x, list) and len(x) == length:
        return x
    elif isinstance(x, list) and len(x) == 1:
        return x * length
    elif isinstance(x, list) and not len(x) == length and len(x) > 1:
        raise ValueError(f"Can not convert list {x} to length {length}")
    else:
        return [x] * length

def json_to_dict(f):
    """Returns the dictionary given by JSON file [f]."""
    if isinstance(f, str) and json_file.endswith(".json") and os.path.exists(f):
        with open(f, "r") as json_file:
            return json.load(json_file)
    else:
        return ValueError(f"Can not read dictionary from {f}")

def dict_to_json(dictionary, f):
    """Saves dict [dictionary] to file [f]."""
    with open(f, "w+") as f:
        json.dump(dictionary, f)

def chunk_list(l, chunk_size=None, num_chunks=None, drop_last=False):
    """
    """
    if not chunk_size is None and num_chunks is None:
        chunk_size = chunk_size
    elif chunk_size is None and not num_chunks is None:
        chunk_size = len(l) // num_chunks
    else:
        raise ValueError()

    if chunk_size > len(l):
        raise ValueError()

    indices = range(0, len(l), chunk_size)
    result = [l[idx:idx+chunk_size] for idx in indices]

    if drop_last and len(result) >= 2 and len(result[0]) > len(result[-1]):
        return result[:-1]
    else:
        return result

def conditional_safe_make_directory(f):
    """Wrapper for conditional os.makedirs() is safe for use in a parallel
    environment when two processes may try to create the directory
    simultaneously.
    """
    if not os.path.exists(f):
        try:
            os.makedirs(f)
        except FileExistsError as e:
            pass

def get_lr(scheduler):
    if isinstance(scheduler, CosineAnnealingWarmupRestarts):
        return scheduler.get_lr()
    else:
        return scheduler.get_last_lr()

def get_split(l, split_idx=0, num_splits=1):
    """Returns the [split_idx]-indexed split of list [l] assuming [l] is split
    into [num_splits] equally sized splits (with the possible exception of the
    last).
    """
    if num_splits == 1:
        return l
    else:
        idxs = torch.tensor_split(torch.arange(len(l)), num_splits)
        return [l[idx] for idx in idxs[split_idx]]

def get_resume_file(args, args_to_folder):
    """Returns the file to resume training from, or None if no file is
    requested.

    Args:
    args            -- argparse Namespace
    args_to_folder  -- function mapping argparse Namespace to the folder
                        scripts run with it would save things to
    """
    folder = args_to_folder(args)
    if args.resume is None:
        return None
    elif args.resume.isdigit():
        if os.path.exists(f"{folder}/{args.resume}.pt"):
            return f"{folder}/{args.resume}.pt"
        else:
            raise ValueError(f"File {folder}/{args.resume}.pt doesn't exist")
    elif os.path.exists(args.resume):
        return args.resume
    else:
        raise ValueError(f"Got weird case for a resume file: {args.resume}")

def hierarchical_zip(h_data):
    """Returns a datastructure structurally matching each element of [t], but
    with the leaves lists where the ith element is the structurally matching
    leaf of the ith element of [t]. This is roughly a hierarchical zip.

    Args:
    t   -- list of structurally identical hierarchical datastructures. Only
            lists and tuples are supported as collections
    """
    if (isinstance(h_data, (tuple, list))
        and all([isinstance(t_, (tuple, list)) for t_ in h_data])
        and all([len(t_) == len(h_data[0]) for t_ in h_data])):
        return [hierarchical_zip(t_) for t_ in zip(*h_data)]
    elif (isinstance(h_data, (tuple, list))
        and all([isinstance(t_, (tuple, list)) for t_ in h_data])
        and all([len(t_) == len(h_data[0]) for t_ in h_data])
        and len(h_data) == 1):
        return [hierarchical_zip(t_) for t_ in h_data]
    elif (isinstance(h_data, (tuple, list))
        and all([isinstance(t_, (tuple, list)) for t_ in h_data])
        and not all([len(t_) == len(t[0]) for t_ in h_data])):
        raise ValueError(f"Got mismatched hierarchies {h_data}")
    elif isinstance(h_data, (tuple, list)):
        return h_data
    else:
        return h_data


def cat_tensor_datastructures(tensor_datastructures,
    zero_dimensions_differ=True, add_zero_axis=False, top_level=True):
    """Returns the concatentation of [tensor_datastructures].

    This function is memory-efficient, but not necessarily perfectly fast. It is
    meant for infrequent use, giving amortized O(1) performance.

    Tuples and lists are treated identically, but returned as lists.

    tensor_datastructures   -- sequence of hierarchical datastructures with all
                                leaf elements as tensors. The structures of each
                                datastructure must be identical
    zero_dimensions_differ  -- whether the zero dimensions of the Tensor leaf
                                elements can differ
    add_zero_axis           -- whether to add a zero axis
    top_level               -- whether the
    """
    if top_level:
        tensor_datastructures = hierarchical_zip(tensor_datastructures)

    if all([isinstance(t, torch.Tensor) for t in tensor_datastructures]):
        ########################################################################
        # Check to make sure the tensors' shapes are okay
        ########################################################################
        shapes = [t.shape for t in tensor_datastructures]
        shapes = [s[1:] for s in shapes] if zero_dimensions_differ else shapes
        if not all(s == shapes[0] for s in shapes):
            raise ValueError(f"Got mismatched corresponding leaf element shapes {shapes} | zero_dimensions_differ is {zero_dimensions_differ}")

        concat_fn = torch.stack if add_zero_axis else torch.cat
        return concat_fn(tensor_datastructures, dim=0)
    elif all([isinstance(t, (tuple, list)) for t in tensor_datastructures]):
        ########################################################################
        # Check to make sure the lists' shapes are okay
        ########################################################################
        lengths = [len(t) for t in tensor_datastructures]
        if not all([l == lengths[0] for l in lengths]):
            raise ValueError(f"Got uneven list lengths: {lengths}")

        concat_fn = functools.partial(cat_tensor_datastructures,
            top_level=False,
            zero_dimensions_differ=zero_dimensions_differ,
            add_zero_axis=add_zero_axis)
        return [concat_fn(t) for t in tensor_datastructures]
    else:
        raise ValueError(f"Got unknown types in [tensor_datastructures] with types {[type(t) for t in tensor_datastructures]}")

def tensor_datastructure_shape(x):
    """Analogue of x.size() but where [x] can be a hierarchical datastructure
    composed of lists, tuples, and tensors.
    """
    result = []

    if isinstance(x, torch.Tensor):
        return tuple(x.shape)
    elif isinstance(x, (list, tuple)):
        if not any([isinstance(x, (tuple, list, torch.Tensor)) for x_ in x]):
            return (len(x),)
        else:
            constituent_shapes = [tensor_datastructure_shape(x_) for x_ in x]
            if all([c == constituent_shapes[0] for c in constituent_shapes]):
                return tuple([len(x)] + list(constituent_shapes[0]))
            else:
                raise ValueError(f"Got inconsistent constituent shapes {constituent_shapes}")
    else:
        raise ValueError(f"Got unknown constituent type {type(x)}")

def tensor_datastructure_to_str(x, indent="", name=None):
    """Returns a string giving a useful representation of tensor-involved
    datastructure [x].

    Args:
    x       -- tensor-involved datastructure (eg. nested list of tensors)
    indent  -- amount to indent for showing hierarchy
    name    -- optional name for the tensor-involved datastructure
    """
    s = "" if name is None else f"==== {name} ====\n"
    if isinstance(x, (tuple, list)):
        v = [tensor_datastructure_to_str(v, indent + "  ") for v in x]
        s += f"{indent}[----\n" + f"\n".join(v) + f"\n{indent}----]"
    elif isinstance(x, dict):
        raise NotImplementedError()
    elif isinstance(x, torch.Tensor):
        is_binary = all([v in [0, 1] for v in x.view(-1).tolist()])
        s += f"{indent}[TENSOR {x.shape} | IS BINARY {is_binary}]"
    elif isinstance(x, (str, int, float)):
        s += f"{x}" if isinstance(x, (str, int)) else f"{x:.10f}"
    else:
        raise ValueError(f"Got unknown type {type(x)}")

    return s
