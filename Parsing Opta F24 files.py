
# coding: utf-8

# In[15]:


import csv
import xml.etree.ElementTree as et
import numpy as np
from datetime import datetime as dt


# In[16]:


tree = et.ElementTree(file = "Bolton_ManCityF24.xml")
games = tree.getroot()


# In[17]:


match_details = games[0].attrib
match_details


# In[18]:


tree2 = et.ElementTree(file = "Bolton_ManCityF7.xml")
soccerfeed = tree2.getroot()


# ## List of players

# In[20]:


player_ids = []
player_names = []

for child in soccerfeed:
    for grchild in child:
        if grchild.tag == "Team":
            for grgrchild in grchild:
                if grgrchild.tag == "Player":
                    player_ids.append(grgrchild.attrib["uID"].lstrip('p'))
                                    
                    for grgrgrchild in grgrchild:
                        player_names.append(grgrgrchild[0].text + " " + grgrgrchild[-1].text)
                        
player_dict = dict(zip(player_ids, player_names))
player_dict


# ## Match preview summary

# In[63]:


print ("%s v %s, %s %s" % (match_details["home_team_name"],
                          match_details["away_team_name"],
                          match_details["competition_name"][8:],
                          match_details["season_name"][7:]))


print ("Date: %s" % dt.strftime(dt.strptime(match_details["game_date"], '%Y-%m-%dT%H:%M:%S'),
                               "%A %d %B %Y"))

print ("Kick-off: %s" % dt.strftime(dt.strptime(match_details["game_date"], '%Y-%m-%dT%H:%M:%S'),
                               "%I%p").lstrip("0"))


# In[25]:


team_dict = {match_details["home_team_id"]: match_details["home_team_name"],
             match_details["away_team_id"]: match_details["away_team_name"]}

print (team_dict)


# ## Passes

# In[57]:


# PASSES

passes_x = []
passes_y = []
passes_outcome = []
passes_min = []
passes_sec = []
passes_period = []
passes_team = []
passes_x_end = []
passes_y_end = []
passes_length = []
passes_angle = []
passes_zone = []
pass_real = []
pass_player = []

for game in games:
    for event in game:
        
        if event.attrib.get("type_id") == '1':
            
            passes_x.append(event.attrib.get("x"))
            passes_y.append(event.attrib.get("y"))
            passes_outcome.append(event.attrib.get("outcome"))
            passes_min.append(event.attrib.get("min"))
            passes_sec.append(event.attrib.get("sec"))
            passes_period.append(event.attrib.get("period_id"))
            passes_team.append(team_dict[event.attrib.get("team_id")])
            pass_player.append(player_dict[event.attrib.get("player_id")])
            
            for q in event:
                
                qualifier = q.attrib.get("qualifier_id")
                
                if qualifier == "140":
                    passes_x_end.append(q.attrib.get("value"))
                if qualifier == "141":
                    passes_y_end.append(q.attrib.get("value"))
                if qualifier == "212":
                    passes_length.append(q.attrib.get("value"))
                if qualifier == "213":
                    passes_angle.append(q.attrib.get("value"))
                if qualifier == "56":
                    passes_zone.append(q.attrib.get("value"))
                    
                             
passes_df = np.array(list(zip(passes_team, pass_player, passes_period, passes_min, passes_sec, passes_zone, passes_x, 
                        passes_y, passes_x_end, passes_y_end, passes_length, passes_angle,passes_outcome)))

print (passes_df)

fieldnames = ["team", "player", "period", "min", "sec", "pass zone", "x", "y", "x_end", "y_end",
              "pass length", "pass angle", "outcome"]

with open("pass_data_%s_%s.csv" % (match_details["home_team_name"], match_details["away_team_name"]),"w",newline='') as passes_csv:
        csv_file = csv.writer(passes_csv)
        csv_file.writerow(fieldnames)
        for i in range(len(passes_df)):
            csv_file.writerow(passes_df[i])


# ## Goals

# In[60]:


# GOALS

goal_x = []
goal_y = []
goal_zone = []
goal_outcome = []
goal_min = []
goal_sec = []
goal_period = []
goal_team = []
goalmouth_y = []
goalmouth_z = []
goal_assisted = []
body_part = []
goal_player = []

body_dict = {"15": "head",
            "72": "left foot",
            "20": "right foot",
            "21": "other body part"}

for game in games:
    for event in game:
        
        if event.attrib.get("type_id") == '16':
            
            goal_x.append(event.attrib.get("x"))
            goal_y.append(event.attrib.get("y"))
            goal_outcome.append(event.attrib.get("outcome"))
            goal_min.append(event.attrib.get("min"))
            goal_sec.append(event.attrib.get("sec"))
            goal_period.append(event.attrib.get("period_id"))
            goal_team.append(team_dict[event.attrib.get("team_id")])
            goal_player.append(player_dict[event.attrib.get("player_id")])
            
            for q in event:
                
                qualifier = q.attrib.get("qualifier_id")
                
                
                if qualifier == "103":
                    goalmouth_z.append(q.attrib.get("value"))
                if qualifier == "102":
                    goalmouth_y.append(q.attrib.get("value"))
                if qualifier == "56":
                    goal_zone.append(q.attrib.get("value"))
                if qualifier in ["15", "72", "20", "21"]:
                    body_part.append(body_dict[qualifier])
                
                
                             
goal_df = np.array(list(zip(goal_team, goal_player, goal_period, goal_min, goal_sec, body_part, goal_zone, goal_x, 
                         goal_y, goalmouth_y, goalmouth_z, goal_outcome)))
print (goal_df)

goal_fieldnames = ["team", "player", "period", "min", "sec", "body part", "zone", "x", "y", 
                   "goalmouth y", "goalmouth z", "outcome", "assisted"]

with open("goal_data_%s_%s.csv" % (match_details["home_team_name"], match_details["away_team_name"]),"w",newline='') as goal_csv:
        csv_file = csv.writer(goal_csv)
        csv_file.writerow(goal_fieldnames)
        for i in range(len(goal_df)):
            csv_file.writerow(goal_df[i])


# ## ALL SHOTS

# In[62]:


# ALL SHOTS

shot_name = []
shot_x = []
shot_y = []
shot_zone = []
shot_min = []
shot_sec = []
shot_period = []
shot_team = []
goalmouth_y = []
goalmouth_z = []
saved_x = []
saved_y = []
body_part = []
shot_play = []
shot_player = []

shot_dict = {'13': 'Shot off target',
             '14': 'Post',
             '15': 'Shot saved',
             '16': 'Goal'}

body_dict = {"15": "head",
            "72": "left foot",
            "20": "right foot",
            "21": "other body part"}

shot_play_dict = {'22': 'regular play',
            '23': 'fast break',
            '24': 'set piece',
            '25': 'from corner',
            '26': 'free kick',
            '96': 'corner situation',
            '112': 'scramble',
            '160': 'throw-in set piece',
            '9': 'penalty',
            '28': 'own goal'}

for game in games:
    
    for event in game:
        
        if event.attrib.get("type_id") in ['13', '14', '16']:
                    
            shot_name.append(shot_dict[event.attrib.get("type_id")])
            shot_x.append(event.attrib.get("x"))
            shot_y.append(event.attrib.get("y"))
            shot_min.append(event.attrib.get("min"))
            shot_sec.append(event.attrib.get("sec"))
            shot_period.append(event.attrib.get("period_id"))
            shot_team.append(team_dict[event.attrib.get("team_id")])
            shot_player.append(player_dict[event.attrib.get("player_id")])
            
            for q in event:
                
                qualifier = q.attrib.get("qualifier_id")
                if qualifier == '102':
                    saved_x.append('')
                    saved_y.append('')
                    goalmouth_y.append(q.attrib.get("value"))
                if qualifier == '103':
                    goalmouth_z.append(q.attrib.get("value"))
                if qualifier in body_dict.keys():
                    body_part.append(body_dict[qualifier])
                if qualifier in shot_play_dict.keys():
                    shot_play.append(shot_play_dict[qualifier])
                                   
        if event.attrib.get("type_id") == '15':
                    
            shot_name.append(shot_dict[event.attrib.get("type_id")])
            shot_x.append(event.attrib.get("x"))
            shot_y.append(event.attrib.get("y"))
            shot_min.append(event.attrib.get("min"))
            shot_sec.append(event.attrib.get("sec"))
            shot_period.append(event.attrib.get("period_id"))
            shot_team.append(team_dict[event.attrib.get("team_id")])
            shot_player.append(player_dict[event.attrib.get("player_id")])
                        
            
            for q in event:
                
                qualifier = q.attrib.get("qualifier_id")
                if qualifier == '146':
                    goalmouth_y.append('')
                    goalmouth_z.append('')
                    saved_x.append(q.attrib.get("value"))
                if qualifier == '147':
                    saved_y.append(q.attrib.get("value"))
                if qualifier in ["15", "72", "20", "21"]:
                    body_part.append(body_dict[qualifier])
                if qualifier in shot_play_dict.keys():
                    shot_play.append(shot_play_dict[qualifier])
                               
                             
shot_df = np.array(list(zip(shot_team, shot_player, shot_period, shot_min, shot_sec, shot_play, shot_name, body_part, shot_x, shot_y, 
                       goalmouth_y, goalmouth_z, saved_x, saved_y)))
    
print (shot_df)

shot_fieldnames = ["team", "player", "period", "min", "sec", "shot play", "shot type", "body part", "x", "y", "goalmouth y", 
                   "goalmouth z", "saved x", "saved y"]

with open("shot_data_%s_%s.csv" % (match_details["home_team_name"], match_details["away_team_name"]), 
          "w",newline='') as shot_csv:
        csv_file = csv.writer(shot_csv)
        csv_file.writerow(shot_fieldnames)
        for i in range(len(shot_df)):
            csv_file.writerow(shot_df[i])

