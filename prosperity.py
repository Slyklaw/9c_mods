import requests
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    addressQuery = """
        query {
            minerAddress
        }"""
    response = requests.post('http://localhost:23061/graphql',
                             json={'query': addressQuery})
    results = response.json()
    address = results['data']['minerAddress']

    query = '''
    query {
        stateQuery {
            agent(address: "'''
    query += address
    query += '''") {
                avatarStates {
                    address
                }
            } } }'''
    response = requests.post('http://localhost:23061/graphql', json={'query': query})
    results2 = response.json()
    # results2 = query
    avatars = results2['data']['stateQuery']['agent']['avatarStates']

    query = '''
    query {
        stateQuery {
            avatar(avatarAddress:"'''
    # query += "0x3FB1dCd0243E0d1D7BCabbACEbCF6bBed84a76aC"
    query += avatars[1]['address']
    query += '''") {
                characterId
                actionPoint
                level
                dailyRewardReceivedIndex
            }
        }
        nodeStatus {
            tip {
            index
            }
        }
    }'''

    response = requests.post('http://localhost:23061/graphql', json={'query': query})
    results = response.json()

    tip = results['data']['nodeStatus']['tip']['index']
    daily = results['data']['stateQuery']['avatar']['dailyRewardReceivedIndex']
    prosperity = tip - daily

    return f'<html><head><meta http-equiv="refresh" content="60"></head><body>prosperity = {prosperity}</body></html>'
if __name__ == '__main__':
    app.run()
