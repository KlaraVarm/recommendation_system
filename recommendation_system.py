# coding: utf-8

# In[ ]:

import csv
import time

target_user = '72297573'
# 416886

source_interaction = 6000000
nearest_neighbors = 100
recommendations = 10
users = {}

with open('youradio_interaction_export.txt', "r") as opened:
    reader = csv.reader(opened, delimiter=';')
    # header
    next(reader)

    idx = 0
    for row in reader:
        if not row[0] in users:
            users[row[0]] = {}

        users[row[0]][row[1]] = row[5]
        idx += 1
        if idx >= source_interactions:
            break

items = {}

with open('youradio_items_export3.txt', "r", encoding="utf8") as opened:
    reader = csv.reader(opened, delimiter=';')
    # header
    next(reader)

    for row in reader:
        if not row[0] in items:
            items[row[0]] = {}

        items[row[0]][row[1]] = row[2]


def interactions(user):
    interaction_map = {}

    for item_id, interaction in user.items():
        if interaction == 'Like':
            interaction_map[item_id] = 1
        elif interaction == 'Dislike':
            interaction_map[item_id] = -1

    return interaction_map


def sum_u1_u2(u1, u2):
    sum_users = 0

    for item, interaction in u2.items():
        if item in u1 and interaction == u1[item]:
            sum_users += 1
        else:
            continue

    return sum_users


def square_sum(interactions):
    sum_user = 0

    for item_id, interaction in interactions.items():
        sum_user += interaction * interaction

    return sum_user


import operator
from math import sqrt


def cos_sim():
    cos_sim_list = {}
    target_user_interactions = interactions(users[target_user])
    target_user_sum = square_sum(target_user_interactions)

    for user, items in users.items():
        try:
            similarity = sum_u1_u2(target_user_interactions, interactions(users[user])) / sqrt(target_user_sum * square_sum(interactions(users[user])))

        except ZeroDivisionError:
            similarity = 0
        cos_sim_list[user] = similarity

    sorted_cos_sim = sorted(cos_sim_list.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_cos_sim


def item_rec(target_user_id, candidates, users, recommendations):
    target_user = users[target_user_id]
    rec = {}
    sorted_rec = ()

    for candidate_id, score in candidates:
        interactions = users[candidate_id]
        for item_id, interaction_type in interactions.items():
            if interaction_type == 'Like' and item_id not in target_user:
                if item_id not in rec:
                    rec[item_id] = 0
                rec[item_id] += score

    sorted_rec = sorted(rec.items(), key=operator.itemgetter(1), reverse=True)[:recommendations]

    return sorted_rec


song_rec = {}


def recommendation(rec):
    sorted_song_rec = ()

    for id_song, song in items.items():
        for id_rec, score in rec:

            if id_rec == id_song:
                song_rec[score, id_rec] = song

    sorted_song_rec = sorted(song_rec.items(), key=operator.itemgetter(0), reverse=True)

    return sorted_song_rec


start_time = time.time()
similarities = cos_sim();
similarities = similarities[:nearest_neighbors]
print("similarity: " + str(time.time() - start_time))
rec_time = time.time()
print(recommendation(item_rec(target_user, similarities, users, recommendations)))
print("recommendations: " + str(time.time() - rec_time))
print("total: " + str(time.time() - start_time))

