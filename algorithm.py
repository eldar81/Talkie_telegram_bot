"""File with algorithm which match users in pairs for communication practice everyday in 7 p.m.
The algorithm is written in such a way that the minimum possible number of users is left without a pair
However SQL logic and operations with data are written very poorly because it was my very first Python project"""

import asyncio
import re
from datetime import date
from loader import db


async def transfer_users():
    todaydate = int(str(date.today()).replace("-", ""))
    users_table = db.select_all_users()
    print(users_table)
    for user in users_table:
        print(user[12])
        print(user[13])
        # We select users who do not have a ban and who don't have a pair yet
        if user[8] + user[9] + user[10] + user[11] == 0 and user[13] != 1 and user[3] is not None:
            print(f"Start work with user: {user[0]}")
            id = user[0]
            id_date = int(f"{str(todaydate)}{str(id)}")
            # db.update_user_send_to_Mathes(id)
            db.update_user_id_date(id, id_date) # We set such users today's id_date
            db.transfer_users_to_Match_gen((id,))  # And transfer to Match_gen
    matches_table = db.select_all_gen_matches()
    for user in matches_table:
        if str(user[0])[:8] == str(todaydate): # In Match_gen we select those who were transferred today
            print(f"Changing date of user: {user[1]}")
            id_date = user[0]
            db.set_date_to_transfered_users(todaydate, id_date) # And give them today's date


async def generate_lists_of_matches():
    todaydate = int(str(date.today()).replace("-", ""))
    matches_table = db.select_all_gen_matches()
    for user in matches_table:
        if user[2] == todaydate: # Select those who were transferred today
            id_date = user[0]
            id = user[1]
            age = user[3]
            gender = user[4]
            req = user[5]
            l_o_m = []
            amount = 0
            for user in matches_table:
                if user[2] == todaydate and user[1] != id:
                    # Create a list of matches
                    if gender + user[5] != 1 and req + user[4] != 1 and abs(age - user[3]) <= 3:
                        l_o_m.append(user[1])
                        amount += 1
            l_o_m_string = str(l_o_m)[1:-1]
            db.set_list_of_matches(l_o_m_string, id_date) # Enter the list of matches in the database
            db.set_amount_of_matches(amount, id_date) # We enter the number of matches in the database


async def choose_match():
    todaydate = int(str(date.today()).replace("-", ""))
    matches_table = db.select_all_gen_matches()
    sorted_table = sorted(matches_table, key=lambda k: k[7])
    for user in sorted_table:
        if user[2] == todaydate:
            print(f"Start of work with user: {user[1]}")
            match_field_of_user = db.select_user_match((user[0],))[0]
            print(f"{user[1]} match is: {match_field_of_user}")
            if user[7] != 0 and user[2] == todaydate and match_field_of_user is None:
                id_date = user[0]
                id = user[1]
                print(f"Match of {user[1]}: {user[8]}")
                for match_id in user[6].split(", "):
                    print(f"start second 'for' cicle: {match_id}")
                    id_date_2 = str(todaydate) + str(match_id)
                    match_field_of_users_match2 = db.select_user_match((int(id_date_2),))[0]
                    print(match_field_of_users_match2)
                    if match_field_of_users_match2 is None:
                        db.set_match(int(match_id), id_date)
                        db.set_match(id, int(id_date_2))
                        db.update_in_work((id,))
                        db.update_in_work((int(match_id),))
                        print(f"pair {match_id} and {id} generated")
                        break


async def transfer_matches():
    todaydate = int(str(date.today()).replace("-", ""))
    print(todaydate)
    matches_table = db.select_all_gen_matches()
    matches_list = []
    for user in matches_table:
        if user[2] == todaydate and user[8] is not None and user[8] not in matches_list:
            print(f"Start work with user: {user[1]}")
            matches_list.append(user[1])
            print(matches_list)
            id1_id2_date = f"{user[1]}_{user[8]}_{user[2]}"
            db.set_id1_id2_date(id1_id2_date, user[0])
            db.transfer_matches_to_Match((user[0],))

# asyncio.run(transfer_users())
# asyncio.run(generate_lists_of_matches())
# asyncio.run(choose_match())
# asyncio.run(transfer_matches())