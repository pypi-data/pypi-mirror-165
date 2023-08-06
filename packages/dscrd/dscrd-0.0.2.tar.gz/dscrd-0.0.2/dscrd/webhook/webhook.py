import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

class Webhook:
    def __init__(self, id: str, token: str):
        self.url = "https://discord.com/api/webhooks/"
        self.id = id
        self.token = token

    def execute(self, content: str ="", username: str = None, avatar_url: str = None, tts: bool = False, embeds: list = None, allowed_mentions: dict = None, components: list = None, files: list = None, attachments: list = None, flags: int = None, thread_name: str = None):
        """
        Execute the webhook.
        content: str, the content to send (up to 2000 characters).
        username: str, the username override of the webhook.
        avatar_url: str, the avatar URL override of the webhook.
        tts: bool, whether the message is a text-to-speech message or not.
        embeds: list, list of embeds to send.
        allowed_mentions: dict, the allowed mentions of the message.
        components: list, list of components to send, requires an application-owned webhook.
        files: list, list of files to send.
        attachments: list, list of attachments to send (requires files to be set).
        flags: int, the flags of the message combined as a bitfield (only SUPPRESS_EMBEDS can be set).
        """
        if not files:
            data = {
                "content": content,
                "username": username,
                "avatar_url": avatar_url,
                "tts": tts,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "components": components,
                "flags": flags,
                "thread_name": thread_name
            }
            return requests.post(self.url + self.id + "/" + self.token, json=data)
        else:
            data = {
                "content": content,
                "username": username,
                "avatar_url": avatar_url,
                "tts": tts,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "components": components,
                "attachments": attachments,
                "flags": flags,
                "thread_name": thread_name
            }

            # put the data in a json object
            data = json.dumps(data)

            # add the payload_json to the encoder
            encoder_dict = {'files[{}]'.format(i): file for i, file in enumerate(files)}
            encoder_dict["payload_json"] = (None, data, "application/json")
            encoder = MultipartEncoder(fields=encoder_dict)

            return requests.post(self.url + self.id + "/" + self.token, data=encoder, headers={"Content-Type": encoder.content_type})
    

    def get_webhook(self):
        """
        Get the webhook.
        """
        return requests.get(self.url + self.id + "/" + self.token).json()

    def modify_webhook(self, name: str = None, avatar: str = None):
        """
        Modify the webhook.
        name: str, the name of the webhook.
        avatar: str, the string image data of the avatar (data URI scheme)).
        """
        data = {
            "name": name,
            "avatar": avatar
        }
        return requests.patch(self.url + self.id + "/" + self.token, json=data)

    def delete_webhook(self):
        """
        Delete the webhook.
        """
        return requests.delete(self.url + self.id + "/" + self.token)

    def execute_slack(self):
        """
        Execute the webhook.
        Not implemented.
        """
        return None

    def execute_github(self):
        """
        Execute the webhook.
        Not implemented.
        """
        return None

    def get_message(self, message_id: str):
        """
        Get a message.
        message_id: str, the message ID.
        """
        return requests.get(self.url + self.id + "/" + self.token + "/messages/" + message_id)

    def edit_message(self, message_id: str, content: str = None, embeds: list = None, allowed_mentions: dict = None, components: list = None, files: list = None, attachments: list = None):
        """
        Edit a message.
        message_id: str, the message ID.
        content: str, the content to send (up to 2000 characters).
        embeds: list, list of embeds to send.
        allowed_mentions: dict, the allowed mentions of the message.
        components: list, list of components to send, requires an application-owned webhook.
        files: list, list of files to send.
        attachments: list, list of attachments to send (requires files to be set).
        """
        if not files:
            data = {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "components": components
            }
            return requests.patch(self.url + self.id + "/" + self.token + "/messages/" + message_id, json=data)
        else:
            data = {
                "content": content,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "components": components,
                "attachments": attachments
            }

            # put the data in a json object
            data = json.dumps(data)

            # add the payload_json to the encoder
            encoder_dict = {'files[{}]'.format(i): file for i, file in enumerate(files)}
            encoder_dict["payload_json"] = (None, data, "application/json")
            encoder = MultipartEncoder(fields=encoder_dict)

            return requests.patch(self.url + self.id + "/" + self.token + "/messages/" + message_id, data=encoder, headers={"Content-Type": encoder.content_type})

    def delete_message(self, message_id: str):
        """
        Delete a message.
        message_id: str, the message ID.
        """
        return requests.delete(self.url + self.id + "/" + self.token + "/messages/" + message_id)
    