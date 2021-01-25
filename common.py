import math

import bencodex
import requests


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


def core_addr(n):
    return f'0x{n:0>40x}'


def get_state(address):
    data = {"query": f"query{{ state(address: \"{address}\") }}"}
    response = requests.post(
        'http://localhost:23061/graphql', headers=headers, json=data
    )
    try:
        return bencodex.loads(
            bytes.fromhex(response.json()['data']['state'])
        )
    except TypeError:
        return {}


def get_gold_balance(address):
    data = {"query": f"query{{ goldBalance(address: \"{address}\") }}"}
    response = requests.post(
        'http://localhost:23061/graphql', headers=headers, json=data
    )
    return response.json()['data']['goldBalance']


def get_last_block_number():
    data = {"query": "query { peerChainState { state }}"}
    response = requests.post(
        'http://localhost:23061/graphql', headers=headers, json=data
    )
    return int(response.json()['data']['peerChainState']['state'][0].split(',')[1])

def get_characters_info(address):
    characters = []
    for key, value in get_state(address)['avatarAddresses'].items():
        characters.append(get_state(f'0x{value.hex()}'))
    return characters


def get_characters_block(address):
    characters = get_characters_info(address)
    ncg = get_gold_balance(address)
    result = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🆔: * `{address}`\n*💰: * {ncg} NCG"
                }
            }
        ]
    }
    for character in characters:    
        prosperity_meter = min(1700, get_last_block_number() - character['dailyRewardReceivedIndex'])
        result['blocks'].append({
			"type": "divider"
		})
        result['blocks'].append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"LV {character['level']} {character['name']}#{character['address'].hex()[:4]}",
                "emoji": True
            }
        })
        result['blocks'].append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
                                "text": f"⭐ {':black_large_square:'*math.ceil((character['actionPoint']/120)*5)}{':white_large_square:'*(5-math.ceil((character['actionPoint']/120)*5))} {character['actionPoint']} / 120 \n🎁 {':black_large_square:'*math.ceil((prosperity_meter/1700)*5)}{':white_large_square:'*(5-math.ceil((prosperity_meter/1700)*5))} {prosperity_meter} / 1700\n"
			}
		})
    return result

