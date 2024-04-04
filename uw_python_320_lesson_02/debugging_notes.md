IF STATEMENT FOR __main__:
1) changed user_selection to return input that is capitalized

FUNCTION load_users:
1) renamed the collection to user_collection instead of user_selection
2) added a user_collection parameter

FUNCTION load_status_updates:
1) added a status_collection parameter

FUNCTION update_user:
1) added user_collectionto the update_user call

FUNCTION search_user:
1) name was not a valid attribute so it is now ID

FUNCTION update_status:
1) it called add_status instead of update_status
2) changed order of parameters