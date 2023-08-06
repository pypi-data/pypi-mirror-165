from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify_interaction_request(request, public_application_id) -> bool:
    """
    Verify that the interaction request is valid, returns True if it is, false if it isn't.
    request: The interaction request to verify (get this from flask for example).
    public_application_id: The public application id of your application.
    """
    verify_key = VerifyKey(bytes.fromhex(public_application_id))
    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")
    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return False
    return True


def create_interaction_response(response_type: int = 4, data: dict = None) -> dict:
    """
    :param response_type:
    The interaction response type.
    :param data:
    The interaction response data.
    :return:
    Interaction response object that can be sent to Discord.
    """
    if data is None:
        data = {}
    response = {
        "type": response_type,
        "data": data
    }
    return response


def create_response_message(tts: bool, content: str, embeds: list, allowed_mentions: dict, flags: int, components: list, attachments: list) -> dict:
    """
    :param tts:
    Make the message tts or not.
    :param content:
    The message content.
    :param embeds:
    The embeds for the message.
    :param allowed_mentions:
    The allowed mentions for the message.
    :param flags:
    The flags for the message as a bitfield.
    :param components:
    The list of components for the message.
    :param attachments:
    The list of attachments for the message.
    :return:
    The message object that can be sent to Discord.
    """
    message = {
        "tts": tts,
        "content": content,
        "embeds": embeds,
        "allowed_mentions": allowed_mentions,
        "flags": flags,
        "components": components,
        "attachments": attachments
    }
    return message
