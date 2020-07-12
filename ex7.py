"""
*Student name: Avichai Geldzahler
*Student ID: 308178136
*Exercise name: ex7
"""

import sys
import os


def menu(input_file, output_file):
    """
    Following is a program that gives the user data about movies and actors from a data base and data they input

    Keyword Arguments:
    input_file: the file we receive as data base
    output_file: the file we write including the changes made to the data base
    Return: ---
    """
    movie_dict = {}
    # create dictionary data base from file
    print("Processing...")
    read_file(input_file, movie_dict)
    print("Please select an option:\n1) Query by movies\n2) Query by actor\n3) Insert a new movie")
    print("4) Save and Exit\n5) Exit")
    num = input()
    while num != '5':
        if num == '1':
            query_movies(movie_dict)
        elif num == '2':
            query_actor(movie_dict)
        elif num == '3':
            add_movie(movie_dict)
        elif num == '4':
            write_file(movie_dict, output_file)
            return
        print("Please select an option:\n1) Query by movies\n2) Query by actor\n3) Insert a new movie")
        print("4) Save and Exit\n5) Exit")
        num = input()


def read_file(input_file, movie_dict):
    """
    Read file and turn it into a dictionary where movies are the keys and actors are the values

    Keyword Arguments:
    input_file: the file we receive as data base
    movie_dict: empty dictionary
    Return: data base of movies and actors as a dictionary
    """
    with open(input_file, "r") as file:
        # read line by line
        for line in file:
            make_dict(line, movie_dict)
    return movie_dict


def make_dict(line, movie_dict):
    """
    Receive line from file and turn it into keys and values in dictionary

    Keyword Arguments:
    line: current line of received file
    movie_dict: the dictionary we're creating of the data base
    Return: the dictionary after filling in the current line from the file
    """
    temp_list = line.split(',')
    # first object in list is always the actor
    actor = temp_list[0]
    for i in range(1, len(temp_list)):
        # remove space from left, and \n from right for last object
        tmp_movie = temp_list[i].lstrip().rstrip("\n")
        # add actor as value to the movie key. If movie doesn't exist as a key, create it and then add actor
        if tmp_movie in movie_dict:
            movie_dict[tmp_movie].add(actor)
        else:
            movie_dict[tmp_movie] = set()
            movie_dict[tmp_movie].add(actor)
    # turn the set of movies and actors into a sorted dictionary
    movie_dict = dict(sorted(zip(movie_dict.keys(), movie_dict.values())))
    return movie_dict


def query_movies(movie_dict):
    """
    Find actors that play in given movies (user chose option number 1)

    Keyword Arguments:
    movie_dict: dictionary of movies and actors, made from data base
    Return: ---
    """
    print("Please select two movies and an operator(&,|,^) separated with ',':")
    try:
        movie_1, movie_2, sign = input().split(",")
    # if not enough values were entered
    except ValueError:
        print("Error")
        return
    # check validity of sign variable
    sign = sign.lstrip().rstrip("\n")
    if sign != '^' and sign != '&' and sign != '|':
        print("Error")
        return
    # remove spaces
    movie_2 = movie_2.strip()
    movie_1 = movie_1.strip()
    # get values of the movie keys
    movie_1_actors = set(movie_dict.get(movie_1))
    movie_2_actors = set(movie_dict.get(movie_2))
    if movie_1 in movie_dict and movie_2 in movie_dict:
        if sign == '&':
            movie_1_actors = movie_1_actors.intersection(movie_2_actors)
            if len(movie_1_actors) == 0:
                print("There are no actors in this group")
            else:
                print(', '.join(sorted(movie_1_actors)))
        elif sign == '|':
            movie_1_actors = movie_1_actors.union(movie_2_actors)
            if len(movie_1_actors) == 0:
                print("There are no actors in this group")
            else:
                print(', '.join(sorted(movie_1_actors)))
        elif sign == '^':
            movie_1_actors = movie_1_actors.symmetric_difference(movie_2_actors)
            if len(movie_1_actors) == 0:
                print("There are no actors in this group")
            else:
                print(', '.join(sorted(movie_1_actors)))
    else:
        print("Error")


def query_actor(movie_dict):
    """
    Find all actors who have played in a movie with given actor (user chose option 2)

    Keyword Arguments:
    movie_dict: dictionary of movies and actors, made from data base
    Return: ---
    """
    co_actors = set()
    values_list = movie_dict.values()
    print("Please select an actor:")
    actor = input().strip()
    # add co-actors of actor to co_actor set
    for x in values_list:
        if actor in x:
            co_actors.update(x)
    # if actor has no co-actors
    if len(co_actors) == 1:
        print("There are no actors in this group")
        return
    # if actor is not in data-base
    elif len(co_actors) == 0:
        print("Error")
        return
    # erase input actor from set
    co_actors.discard(actor)
    # no co-actors
    print(', '.join(sorted(co_actors)))


def add_movie(movie_dict):
    """
    Add a new movie to dictionary or add actors to existing movie

    Keyword Arguments:
    movie_dict: dictionary of movies and actors, made from data base
    Return: the dictionary, after the changes that were made
    """
    print("Please insert a new movie:")
    new_movie = input().split(',')
    if len(new_movie) < 2:
        print("Error")
        return
    length = len(new_movie)
    movie = new_movie[0]
    # erase space and \n from input
    for i in range(1, length):
        tmp_actor = new_movie[i].strip()
        # add actor as value to the movie key. If movie doesn't exist as a key, create it and then add actor
        if movie in movie_dict:
            movie_dict[movie].add(tmp_actor)
        else:
            movie_dict[movie] = set()
            movie_dict[movie].add(tmp_actor)
    # turn the set of movies and actors into a sorted dictionary
    movie_dict = dict(sorted(zip(movie_dict.keys(), movie_dict.values())))
    return movie_dict


def write_file(movie_dict, output_file):
    """
    Write data base to file

    Keyword Arguments:
    movie_dict: dictionary of movies and actors, made from data base
    output_file: the file to write on our current data base
    Return: ---
    """
    os.chmod(output_file, 0o777)
    out_dict = {}
    with open(output_file, "w") as file:
        # turn every actor to a key(if doesn't exist already) and turn its key to be its value(the movie)
        for key in movie_dict:
            for value in movie_dict[key]:
                if value in out_dict:
                    out_dict[value].add(key)
                else:
                    out_dict[value] = set()
                    out_dict[value].add(key)

        # sort dictionary
        out_dict = dict(sorted(zip(out_dict.keys(), out_dict.values())))
        # write dictionary to file line by line
        for key in out_dict:
            file.write(key)
            file.write(', ')
            file.write(', '.join(out_dict[key]))
            file.write('\n')


menu(sys.argv[1], sys.argv[2])
