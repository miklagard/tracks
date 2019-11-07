# tracks
Tracks for Trucks Chatbot

A sample chatbot project for Tracks and Trucks. Database is using only for Django's default session management. All the logs are saved under a directory.

## Structure

### Logging

Log files are saving under /tracker/tracker/log/. This path can be modified under settings.py by LOG_DIR.

The log format is:
{session_id}.summary.log for summary output
{session_id}.full.log for whole chat converstation

The log generator is located under /tracker/tracker/util/log.py

### Chat tree

This can be modified under tracker/api/chat.

#### Variables using there:

text: Bot's responde message to user
set_answer_to_session: Session key to be stored the answer
terminate: It ends the converstation if it is set as True

For the direction, use any of those following variables:
direct_to: The name of the Chat class to direct without paying attention to user's answer
direct_if_condition: A dictionary to direct user to other Chat classes regarding their answers. The keys of this dictiary are the files which contains list of words which expected as an answer. They are located under /tracker/tracer/nlp_data/{key_name}.txt.
