import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd

#point to personal google credential for Vision API
# ATTENTION YOUR CREDENTIALS FILE NEEDS TO BE REFERENCE HERE:
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'GoogleVisionAPI.json'

#Create cliebnt instance
client = vision.ImageAnnotatorClient()

#Point to directory where you move your valorant scoreboard screencaptures
#Take screencaptures using 'Win + print screen'
FOLDER_PATH = r'C:\Users\aaron\Pictures\Screenshots\ValorantScoreboard'

#Get list of all screenshots in directory
FILE_LIST = os.listdir(FOLDER_PATH)

#Initialise DF outside of for loop
raw_df = pd.DataFrame(columns=['locale','description'])

clean_df = pd.DataFrame(columns=['date',
                                'game_type',
                                'map',
                                'duration',
                                'result',
                                'player_name',
                                'avg_combat_score',
                                'k',
                                'd',
                                'a',
                                'econ_rating'])
#iterate over all screenshots in directory
for i in FILE_LIST:
    FILE_NAME = i

    with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    #Defining the dataframe within the for loop erases and re-initialises it for each screencapture
    temp_df = pd.DataFrame(columns=['locale','description'])

    for text in texts:
        temp_df = temp_df.append(
            dict(locale=text.locale,
                description = text.description
            ),
            ignore_index=True)

        raw_df = raw_df.append(temp_df)

    #Determine index of unique player name
    # Here, change player_name to your individual Valorant handle as it appears on the scoreboard
    player_name = 'VeryQuickMan'
    player_name_index = temp_df[temp_df['description']==player_name].index.values
    player_name_index = player_name_index[0]

    ##The following code is dodgy, done because the returned index of the text is unreliable. This could be
    # done more cleanly using dictionaries. The best solution (I can currently imagine) would be to use
    # the positional information that comes in the google response structure


    ## Here begins the dodgiest of code ##

    #Not all statastics are reliably "hard" indexed nor reliably indexed relative to player name
    # map_index = []
    # while map_index == []:
    map_list = ['BIND','SPLIT','HAVEN']

    map_index = temp_df[temp_df['description']== map_list[0]].index.values
    map_name = map_list[0]
    if map_index.size == 0:
        map_index = temp_df[temp_df['description']== map_list[1]].index.values
        map_name = map_list[1]
        if map_index.size == 0:
            map_index = temp_df[temp_df['description']== map_list[2]].index.values
            map_name = map_list[2]

    #the text INDIVIDUALLY seems to always appear at the same index so I use that as a reference for duration
    duration_index = (temp_df[temp_df['description']=='INDIVIDUALLY'].index.values - 1)
    duration_index = duration_index [0]

    #There are slashes(/) or vertical bars (|) between k/d/a (these dont always show up...)
    #If both slashes are present then the default position is correct
    if (((temp_df.iloc[(player_name_index+3),1] == '/') or (temp_df.iloc[(player_name_index+3),1] == '|')) & ((temp_df.iloc[(player_name_index+5),1] == '/') or (temp_df.iloc[(player_name_index+5),1] == '|'))):
        deaths = temp_df.iloc[(player_name_index+4),1]
        assists = temp_df.iloc[(player_name_index+6),1]
        econ = temp_df.iloc[(player_name_index+7),1]

    #If first slash is missing
    if ((temp_df.iloc[(player_name_index+3),1] != '/') and (temp_df.iloc[(player_name_index+3),1] != '|')):
        deaths = temp_df.iloc[(player_name_index+3),1]
        #and second slash is present
        if ((temp_df.iloc[(player_name_index+4),1] == '/') or (temp_df.iloc[(player_name_index+4),1] == '|')):
            assists = temp_df.iloc[(player_name_index+5),1]
            econ = temp_df.iloc[(player_name_index+6),1]
        #else if second slash is absent
        if ((temp_df.iloc[(player_name_index+4),1] != '/') and (temp_df.iloc[(player_name_index+4),1] != '|')):
            assists = temp_df.iloc[(player_name_index+4),1]
            econ = temp_df.iloc[(player_name_index+5),1]


    #Result ('VICTORY' OR 'DEFEAT') does not reliably index, here we search for it
    result_index = temp_df[temp_df['description']== 'VICTORY'].index.values
    if result_index.size == 0:
        result_index = temp_df[temp_df['description']== 'DEFEAT'].index.values
    result_index = result_index[0]


    ## Here ends the dodgiest of code ##

    #Extracted and indexed data of interest is organised into a 'clean' dataframe
    clean_df = clean_df.append(dict(date=temp_df.iloc[14,1]+' '+temp_df.iloc[15,1]+temp_df.iloc[16,1],
                                    game_type=temp_df.iloc[20,1],
                                    map=map_name,
                                    duration=temp_df.iloc[duration_index,1],
                                    result=temp_df.iloc[result_index,1],
                                    player_name=temp_df.iloc[player_name_index,1],
                                    avg_combat_score=temp_df.iloc[(player_name_index+1),1],
                                    k=temp_df.iloc[(player_name_index+2),1],
                                    d=deaths,
                                    a=assists,
                                    econ_rating=econ),
                                ignore_index=True
                                )
    #drop duplicates (multiple screencaps of the same game?)
    clean_df.drop_duplicates()

    #This writes out all extracted from all screen shots to a csv
    raw_df.to_csv('raw.csv', index=False)
    clean_df.to_csv('clean.csv', index=False)
