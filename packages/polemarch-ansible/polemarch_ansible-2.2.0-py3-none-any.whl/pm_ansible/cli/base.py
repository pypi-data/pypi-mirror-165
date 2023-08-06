import argparse


def get_parser():
    return argparse.ArgumentParser(
        prog='Polemarch-Ansible',
        description='%(prog)s cli wrapper.',
        conflict_handler='resolve'
    )
