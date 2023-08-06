import argparse


def get_cla():
    parser = argparse.ArgumentParser("Jinja template filler")
    parser.add_argument("-c", "--config", type=str, required=True, help="JSON config file path")
    parser.add_argument("-t", "--template", type=str, required=True, help="Template file path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    return parser