#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Anima import Anima
from Nemesis import Nemesis
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', default='train', help='Phase: Can be train, val or test')
    parser.add_argument('--arch', type=str, default='VGG16', help='Passes the architecture to be learned')
    parser.add_argument('--load_weights', type=str, default=None, help='Location to pretrained model')
    parser.add_argument('--number_of_classes', type=int, default=1000)
    parser.add_argument('--epochs', type=int, default=150)
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--steps', type=int, default=None)

    args = parser.parse_args()

    #sun = Sun()
    #sun.start()
    #sun.generate_csvs()

    nemesis = Nemesis(args)
    nemesis.start()


if __name__ == '__main__':
    main()
