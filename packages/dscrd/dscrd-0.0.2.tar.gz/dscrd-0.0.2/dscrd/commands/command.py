import requests

def create_command(id: str, application_id: str, name: str, description: str, default_member_permissions: str, version: str = None, type: int = 1, guild_id: str = None, name_localizations: dict = None, description_localizations: dict = None, options: list = None, dm_permission: bool = True, default_permission: bool = True, bot_token: str = None, bearer_token: str = None):
    """
    Creates a command.
    id: str, the id of the command.
    application_id: str, the id of the application.
    name: str, the name of the command (1 to 32 characters).
    description: str, the description of the command.
    default_member_permissions: str, the default member permissions of the command, bit set.
    version: str, the version of the command.
    type: int, the type of the command (1 to 3).
    guild_id: str, the id of the guild.
    name_localizations: dict, the name localizations of the command.
    description_localizations: dict, the description localizations of the command (1-100 characters for CHAT_INPUT, empty string for other types).
    options: list, the options of the command (max 25).
    dm_permission: bool, whether the command is enabled in DMs or not.
    default_permission: bool, whether the command is enabled by default or not (soon to be deprecated).
    """
    data = {
        "id": id,
        "name": name,
        "description": description,
        "default_member_permissions": default_member_permissions,
        "version": version,
        "type": type,
        "guild_id": guild_id,
        "name_localizations": name_localizations,
        "description_localizations": description_localizations,
        "options": options,
        "dm_permission": dm_permission,
        "default_permission": default_permission
    }

    if bot_token is not None:
        headers = {"Authorization": "Bot " + bot_token}
    elif bearer_token is not None:
        headers = {"Authorization": "Bearer " + bearer_token}
    else:
        raise Exception("No token provided.")

    return requests.post(f"https://discord.com/api/v10/applications/{application_id}/commands", json=data, headers=headers)