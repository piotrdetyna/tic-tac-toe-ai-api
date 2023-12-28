from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app, get_db
from config import *
from models import Game

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ====== DB SETUP END ======

client = TestClient(app)
TEST_INVALID_ID = 'x'*GAME_ID_LENGTH
VALID_INITIAL_STATE = [[None, None, None], [None, None, None], [None, None, None]]
VALID_SYMBOLS = ['X', 'O']
TEST_GAMES_NUMBER = 3

def populate_games_db():
    ids = []
    with TestingSessionLocal() as db:
        for i in range(TEST_GAMES_NUMBER):
            game = Game()
            db.add(game)
            db.commit()
            ids.append(game.id)
    return ids

def clear_games_db():
    with TestingSessionLocal() as db:
        db.query(Game).delete()
        db.commit()

def is_db_empty():
    with TestingSessionLocal() as db:
        return db.query(Game).count() == 0




def is_valid_id(response):
    return response.json()['id'] != TEST_INVALID_ID and len(response.json()['id']) == GAME_ID_LENGTH

def is_valid_initial_state(response):
    return response.json()['state'] == VALID_INITIAL_STATE

def is_valid_initial_winner(response):
    return response.json()['winner'] == None

def is_valid_ai_symbol(response):
    return response.json()['ai_symbol'] in VALID_SYMBOLS

def is_status_200(response):
    return response.status_code == 200

def is_status_204(response):
    return response.status_code == 204

def is_status_4xx(response):
    return str(response.status_code)[0] == '4'

def is_status_404(response):
    return response.status_code == 404

def is_default_ai_symbol(response):
    return response.json()['ai_symbol'] == DEFAULT_AI_SYMBOL

def is_valid_current_player(response):
    return response.json()['current_player'] in VALID_SYMBOLS

def contains_state(response):
    return '"state":' in response.text

def contains_ai_symbol(response):
    return '"ai_symbol":' in response.text

def contains_id(response):
    return '"id":' in response.text

def not_contains_id(response):
    return '"id":' not in response.text

def is_response_empty(response):
    return not response.json()

def contains_test_games_number_entries(response):
    return TEST_GAMES_NUMBER == len(response.json())



CREATE_GAME_VALID_PAYLOADS = [
    {
        'payload': {},
        'validators': [
            is_status_200,
            is_valid_initial_state,
            is_valid_initial_winner,
            is_default_ai_symbol,
            is_valid_current_player,
            contains_id,
        ]
    },
    {
        'payload': {'ai_symbol': 'X'},
        'validators': [is_status_200]
    },
    {
        'payload': {'ai_symbol': 'O'},
        'validators': [is_status_200]
    },
]

CREATE_GAME_INVALID_PAYLOADS = [
    {
        'payload': {'ai_symbol': 'foo'},
        'validators': [is_status_4xx]
    },
    {
        'payload': {'ai_symbol': 'n'},
        'validators': [is_status_4xx]
    },
    {
        'payload': {'ai_symbol': ''},
        'validators': [is_status_4xx]
    },
]

CREATE_GAME_EXCESS_PARAMETERS_PAYLOADS = [
    {
        'payload': {'id': TEST_INVALID_ID},
        'validators': [is_valid_id]
    },
    {
        'payload': {'id': ''},
        'validators': [is_valid_id]
    },
    {
        'payload': {'state': [[None, 'X', None], [None, None, None], [None, 'O', None]]},
        'validators': [is_valid_initial_state]
    },
    {
        'payload': {'winner': 'X'},
        'validators': [is_valid_initial_winner]
    },
    {
        'payload': {'winner': 'O'},
        'validators': [is_valid_initial_winner]
    },
]

GET_GAMES_NON_EMPTY_DB_RESPONSE_VALIDATORS = [
    is_status_200,
    not_contains_id,
    contains_test_games_number_entries,
    contains_ai_symbol,
    contains_state,
]

GET_GAMES_EMPTY_DB_RESPONSE_VALIDATORS = [
    is_status_200,
    is_response_empty,
]

DELETE_GAMES_RESPONSE_VALIDATORS = [
    is_status_204,
]

GET_GAME_VALID_ID_PAYLOAD_RESPONSE_VALIDATORS = [
    is_status_200,
    contains_state,
    contains_ai_symbol,
]

GET_GAME_INVALID_ID_PAYLOAD_RESPONSE_VALIDATORS = [
    is_status_404,
    not_contains_id,
]

RESET_GAME_VALID_PAYLOADS = [
    {
        'payload': {},
        'validators': [
            is_status_200,
            is_valid_initial_state,
            is_valid_initial_winner,
            is_default_ai_symbol,
            is_valid_current_player,
        ]
    },
    {
        'payload': {'ai_symbol': 'X'},
        'validators': [is_status_200]
    },
    {
        'payload': {'ai_symbol': 'O'},
        'validators': [is_status_200]
    },
]

RESET_GAME_INVALID_PAYLOADS = [
    {
        'payload': {'ai_symbol': 'foo'},
        'validators': [is_status_4xx]
    },
    {
        'payload': {'ai_symbol': 'n'},
        'validators': [is_status_4xx]
    },
    {
        'payload': {'ai_symbol': ''},
        'validators': [is_status_4xx]
    },
]

RESET_GAME_EXCESS_PARAMETERS_PAYLOADS = [
    {
        'payload': {'id': TEST_INVALID_ID},
        'validators': [is_valid_id]
    },
    {
        'payload': {'id': ''},
        'validators': [is_valid_id]
    },
    {
        'payload': {'state': [[None, 'X', None], [None, None, None], [None, 'O', None]]},
        'validators': [is_valid_initial_state]
    },
    {
        'payload': {'winner': 'X'},
        'validators': [is_valid_initial_winner]
    },
    {
        'payload': {'winner': 'O'},
        'validators': [is_valid_initial_winner]
    },
]


def test_create_game_valid_payloads():
    for i, pv in enumerate(CREATE_GAME_VALID_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying valid payload {i}: {payload}')
        
        response = client.post(
            "/games/",
            json=payload,
        )

        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_create_game_invalid_payloads():
    for i, pv in enumerate(CREATE_GAME_INVALID_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying invalid payload {i}: {payload}')
        
        response = client.post(
            "/games/",
            json=payload,
        )
        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_create_game_excess_parameters_payloads():
    for i, pv in enumerate(CREATE_GAME_EXCESS_PARAMETERS_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying payload with excess parameters {i}: {payload}')
        
        response = client.post(
            "/games/",
            json=payload,
        )
        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_get_games_on_non_empty_db():
    clear_games_db()
    populate_games_db()

    response = client.get('/games/')
    print('Testing get games endpoint on non empty db')
    for j, validator in enumerate(GET_GAMES_NON_EMPTY_DB_RESPONSE_VALIDATORS):
        print(f'\tValidating using validator {j}: {validator.__name__}')
        assert validator(response)

def test_get_games_on_empty_db():
    clear_games_db()

    response = client.get('/games/')
    print('Testing get games endpoint on empty db')
    for j, validator in enumerate(GET_GAMES_EMPTY_DB_RESPONSE_VALIDATORS):
        print(f'\tValidating using validator {j}: {validator.__name__}')
        assert validator(response)

def test_get_game_valid_id_payload():
    valid_game_id = populate_games_db()[0]
    response = client.get(f'/games/{valid_game_id}')
    print('Testing get game endpoint with valid ID')
    for j, validator in enumerate(GET_GAME_VALID_ID_PAYLOAD_RESPONSE_VALIDATORS):
        print(f'\tValidating using validator {j}: {validator.__name__}')
        assert validator(response)

def test_get_game_invalid_id_payload():
    response = client.get(f'/games/{TEST_INVALID_ID}')
    print('Testing get game endpoint with invalid ID')
    for j, validator in enumerate(GET_GAME_INVALID_ID_PAYLOAD_RESPONSE_VALIDATORS):
        print(f'\tValidating using validator {j}: {validator.__name__}')
        assert validator(response)

def test_delete_games():
    populate_games_db()

    response = client.delete('/games/')
    print('Testing delete games endpoint on non empty db')
    for j, validator in enumerate(DELETE_GAMES_RESPONSE_VALIDATORS):
        print(f'\tValidating using validator {j}: {validator.__name__}')
        assert validator(response)

    assert is_db_empty

def test_reset_game_valid_payloads():
    print('Testing reset game endpoint with valid payload')
    valid_game_id = populate_games_db()[0]
    for i, pv in enumerate(RESET_GAME_VALID_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying payload {i}: {payload}')
        
        response = client.put(
            f"/games/{valid_game_id}",
            json=payload,
        )

        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_reset_game_invalid_payloads():
    print('Testing reset game endpoint with invalid payload')
    valid_game_id = populate_games_db()[0]
    for i, pv in enumerate(RESET_GAME_INVALID_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying payload {i}: {payload}')
        
        response = client.put(
            f"/games/{valid_game_id}",
            json=payload,
        )

        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_reset_game_excess_parameters_payloads():
    print('Testing reset game endpoint with excess payload')
    valid_game_id = populate_games_db()[0]
    for i, pv in enumerate(RESET_GAME_EXCESS_PARAMETERS_PAYLOADS):
        payload, validators = pv['payload'], pv['validators']
        print(f'Trying payload {i}: {payload}')
        
        response = client.put(
            f"/games/{valid_game_id}",
            json=payload,
        )

        for j, validator in enumerate(validators):
            print(f'\tValidating using validator {j}: {validator.__name__}')
            assert validator(response)

def test_game_simulation():
    print('Testing game simulation')
    game_id = populate_games_db()[0]
    for i, ar in enumerate(GAME_SIMULATION):
        action, expected_response = ar['action'], ar['response']
        print(f'Trying action: {action}')
        
        response = client.patch(
            f'/games/{game_id}',
            json=action
        )
        print(f'expected response: {expected_response}')
        print(f'actual response: {response.json()}')
        assert response.json() == expected_response

    
GAME_SIMULATION = [
    {
        'action': {"x":1,"y":1},
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    None,
                    None,
                    None
                ],
                [
                    None,
                    "X",
                    None
                ],
                [
                    None,
                    None,
                    None
                ]
            ],
            "winner": None,
            "current_player": "O"
        }
        
    },
    {
        'action': None,
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    "O",
                    None,
                    None
                ],
                [
                    None,
                    "X",
                    None
                ],
                [
                    None,
                    None,
                    None
                ]
            ],
            "winner": None,
            "current_player": "X"
        }
        
    },
    {
        'action': {"x":0,"y":2},
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    "O",
                    None,
                    "X"
                ],
                [
                    None,
                    "X",
                    None
                ],
                [
                    None,
                    None,
                    None
                ]
            ],
            "winner": None,
            "current_player": "O"
        }
        
    },
    {
        'action': None,
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    "O",
                    None,
                    "X"
                ],
                [
                    None,
                    "X",
                    None
                ],
                [
                    "O",
                    None,
                    None
                ]
            ],
            "winner": None,
            "current_player": "X"
        }
        
    },
    {
        'action': {"x":2,"y":2},
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    "O",
                    None,
                    "X"
                ],
                [
                    None,
                    "X",
                    None
                ],
                [
                    "O",
                    None,
                    "X"
                ]
            ],
            "winner": None,
            "current_player": "O"
        }
        
    },
    {
        'action': None,
        'response': 
        {
            "ai_symbol": "O",
            "state": [
                [
                    "O",
                    None,
                    "X"
                ],
                [
                    "O",
                    "X",
                    None
                ],
                [
                    "O",
                    None,
                    "X"
                ]
            ],
            "winner": "O",
            "current_player": "X"
        }
        
    },
    {
        'action': {"x":1,"y":2},
        'response': 
        {
            "detail": "This game is over."
        }
        
    },
]