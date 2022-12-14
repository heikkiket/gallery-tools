import tomli, sys

from Imagegallery import Imagegallery
from gallerycmd.parser import subparsers
from Imagegallery.gallery_toml import filter_by_tag

def format(gallery, gallery_toml=None):
    """Formats image gallery for printing out into console

    Arguments:
    gallery - an Imagegallery object
    gallery_toml - an alternative gallery_toml dictionary
    """
    toml = gallery_toml if gallery_toml else gallery.gallery_toml
    rows = []
    for path, image in toml.items():
        rows.append("[" + path + "]:")
        rows.append(image["title"])
        rows.append(image["description"])
        rows.append("")
        if "missing" in gallery.metadata[path]:
            rows.append(" *FILE MISSING* ")
            rows.append("")
    return rows

def main(args):
    try:
        gallery = Imagegallery()
        gallery.load()
        gallery.flag_missing()
    except FileNotFoundError:
        print("No gallery.toml file found in this directory.")
        exit(0)

    formatted = format(gallery,
                       gallery_toml=filter_by_tag(gallery.gallery_toml, args.tag))
    print("\n".join(formatted))


parser = subparsers.add_parser('list',
    description="Lists image gallery information into console",
                               )
parser.add_argument('-t', '--tag')
parser.set_defaults(func=main)

