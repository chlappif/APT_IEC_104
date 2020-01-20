#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import shuffle
from math import floor


# FUNCTIONS
def get_different_sets(file_list, total):
    split_training = 0.6
    split_validation = 0.2
    split_training_index = floor(total * split_training)
    split_validation_index = floor(total * split_validation)
    training = file_list[:split_training_index]
    validation = file_list[split_training_index:split_validation_index + split_training_index]
    testing = file_list[split_validation_index + split_training_index:]
    return training, validation, testing


def writee(liste, fichier):
    for elem in liste:
        print(elem)
        fichier.write(elem)
    return None


def sort_data(source_file_path, raspi):  # Raspi correspond soit à left, ou à right (pour les deux raspi)
    # Traitement des données : mise en place du tri
    file = open(source_file_path, 'r')
    data = file.readlines()
    total = len(data)  # Sert pour la division des sets

    # Randomize de data for the splitting
    shuffle(data)

    # Split the data
    training_set, validation_set, testing_set = get_different_sets(data, total)

    train_file = open('./training_data_' + raspi + '.txt', "w+")
    validation_file = open('./validation_data_' + raspi + '.txt', "w+")
    test_file = open('./testing_data_' + raspi + '.txt', "w+")

    writee(training_set, train_file)
    writee(validation_set, validation_file)
    writee(testing_set, test_file)

    train_file.close()
    validation_file.close()
    test_file.close()
    file.close()


# LEFT RASPI
sort_data('./Capture Data/left_raspi_data1.txt', 'left_1')
sort_data('./Capture Data/left_raspi_data3.txt', 'left_3')
sort_data('./Capture Data/left_raspi_data4.txt', 'left_4')

# RIGHT RASPI
sort_data('./Capture Data/right_raspi_data1.txt', 'right_1')
sort_data('./Capture Data/right_raspi_data3.txt', 'right_3')
sort_data('./Capture Data/right_raspi_data4.txt', 'right_4')
