from collections import namedtuple
import config

Transaction = namedtuple('transaction',
                         'id amount timestamp recipientId senderId rawasset type fee')
Block = namedtuple('block',
                       'timestamp height id')

# GENERATING MOCK TRANSACTIONS
ID = ['6e05b2b2dc4796c6ad1c0eb41bc238fdfb89180d91372f02cce3bdca2261407b',
      'e7384ed14075ee7d467f6742f8e9dd218f3618a31e90e41542c89282a8054ef5',
      '93c85855643326435f5efca2c014b2dd02461f437a242ad4ab44b70cc4dae102',
      'bf41b39fc1650ce0f00e3e15cf2d3b5f2be1b775d87718977735f4b86a775d57'
      ]
AMOUNT = [0, 150000000000, 0, 0]
TIMESTAMP = [16240524, 16739416, 15406051, 15462150]

RECIPIENTID = ['AahNjcAB44tCyT7tdGxXcZbmV1C3eLHT34',
               'AcqKC38o5z2Hd8HueULuaNhH1LPvmcn4Wz',
               'None',
               'None', ]

SENDERID = ['AahNjcAB44tCyT7tdGxXcZbmV1C3eLHT34',
            'Ad1dASP3FEjFWkD4bZmohgnKDdCajKwmSQ',
            'AGUr5pfF3avHEARutWfvfQEj8Z6fTrA3bV',
            'AKyhhMTHi2ercaLRi9jtFjY7ySW9G1yiSF'
]

RAWASSET = ['{"votes":["-022bb6c5050444b24ba91b3959800c4df8c678a5d7293b4b43df17bffec03ae027"]}',
            '{}',
            '{"delegate":{"username":"arkoftriomphe","publicKey":"02c0e2535c9a457003ede65e9c9bac44457e80397abbbfdff1939a702e68bf2a06"}}',
            '{"signature":{"publicKey":"0218f877ab3ae29c1e272ac658706454d53a8687674e6ede4fc69dbb974e146950"}}']

TYPE = [3, 0, 2, 1]

FEE = [100000000, 10000000, 2500000000, 500000000]
GET_TRANSACTIONS = [

    # vote transactions: 3
    (ID[0], AMOUNT[0], TIMESTAMP[0], RECIPIENTID[0], SENDERID[0], RAWASSET[0], TYPE[0], FEE[0]),
    (ID[1], AMOUNT[1], TIMESTAMP[1], RECIPIENTID[1], SENDERID[1], RAWASSET[1], TYPE[1], FEE[1]),
    (ID[2], AMOUNT[2], TIMESTAMP[2], RECIPIENTID[2], SENDERID[2], RAWASSET[2], TYPE[2], FEE[2]),
    (ID[3], AMOUNT[3], TIMESTAMP[3], RECIPIENTID[3], SENDERID[3], RAWASSET[3], TYPE[3], FEE[3])

]

NAMED_TRANSACTIONS = [
    Transaction(id=ID[0],
                amount=AMOUNT[0],
                timestamp=TIMESTAMP[0],
                recipientId=RECIPIENTID[0],
                senderId=SENDERID[0],
                rawasset=RAWASSET[0],
                type=TYPE[0],
                fee=FEE[0]),

    Transaction(id=ID[1],
                amount=AMOUNT[1],
                timestamp=TIMESTAMP[1],
                recipientId=RECIPIENTID[1],
                senderId=SENDERID[1],
                rawasset=RAWASSET[1],
                type=TYPE[1],
                fee=FEE[1]),

    Transaction(id=ID[2],
                amount=AMOUNT[2],
                timestamp=TIMESTAMP[2],
                recipientId=RECIPIENTID[2],
                senderId=SENDERID[2],
                rawasset=RAWASSET[2],
                type=TYPE[2],
                fee=FEE[2]),

    Transaction(id=ID[3],
                amount=AMOUNT[3],
                timestamp=TIMESTAMP[3],
                recipientId=RECIPIENTID[3],
                senderId=SENDERID[3],
                rawasset=RAWASSET[3],
                type=TYPE[3],
                fee=FEE[3]),
]
##############################

#GENERATING MOCK VOTERLIST

ADDRESS = [
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AaR9jUCvWFGjqDGgDS9g232br4ARBuLDcJ',
    'AbRRhauh9SKprUEGXzKGswPbNAiRjvG9Q7',
    'ARLBk2K2DwwTzYf8MGUzkeY1K8LqhFN7Vk',
]

TIMESTAMPS_VOTES = [14958683,
                    14976141,
                    14978136,
                    14989253]



GET_VOTERLIST = [(ADDRESS[0], TIMESTAMPS_VOTES[0]),
                 (ADDRESS[1], TIMESTAMPS_VOTES[1]),
                 (ADDRESS[2], TIMESTAMPS_VOTES[2]),
                 (ADDRESS[3], TIMESTAMPS_VOTES[3])]

VOTERDICT = {
    ADDRESS[0]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES[0]},
    ADDRESS[1]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES[1], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES[1]},
    ADDRESS[2]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES[2], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES[2]},
    ADDRESS[3]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES[3], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES[3]}
}

#######################################

#GENERATING MOCK BLOCKS
TIMESTAMP_BLOCK = [15011440,
                   15011656,
                   15012288]

HEIGHT = [1866225,
          1866252,
          1866331]

BLOCK_ID = ['1639097675237354662',
            '11606272525796443280',
            '14224982005667243873',]


GET_BLOCKS = [(TIMESTAMP_BLOCK[0], HEIGHT[0], BLOCK_ID[0]),
              (TIMESTAMP_BLOCK[1], HEIGHT[1], BLOCK_ID[1]),
              (TIMESTAMP_BLOCK[2], HEIGHT[2], BLOCK_ID[2]),]

NAMED_BLOCKS = [
    Block(timestamp=TIMESTAMP_BLOCK[0],
          height=HEIGHT[0],
          id=BLOCK_ID[0]),
    Block(timestamp=TIMESTAMP_BLOCK[1],
          height=HEIGHT[1],
          id=BLOCK_ID[1]),
    Block(timestamp=TIMESTAMP_BLOCK[2],
          height=HEIGHT[2],
          id=BLOCK_ID[2]),
]

# GENERATING VOTER TX
ID_VOTER_TX = [
    '83b34ba19653dd1cca3438b4cd7ad5ad6cbabce19311f94d9bfb1dee4059063e',
    'ecbc2700370f909d1341c504126a66f5739c8744dfcc84e5447603f668197cf1',
    '771e2d81c8f4dc1b47e713afeb97412e9dd7fbbf8cfa30f20ff551e233897ea9',
    '05764564355d4ef788527af03b42394e45d3b27050f72b97a08215e20629ffc4',
    '7cdb75d57ab0c09129efe57606fdbbd9b979cace77161cd0be0c08ebfc25d0df',
    '3bc3da4b0c77cae30b715ff4b6a9ce4020f48ba118903ae42733130555a89eb1',
    '9f3840a3a517a820c09d3ce4937a1d68fe2afaa772750056e746676340e4f5b5',
    '468063880162825f242e880bb98c6336087bfa910f88fe05d9862928a251af7d',
    '06a25dd4726e93eedc479214876d63ab3be97a14c7c8daed208d9e4321a92133',
]

AMOUNT_VOTER_TX = [
    0,
    0,
    2753357079,
    600000000,
    1200000000,
    3050000000,
    2731584136,
    0,
    0]
TIMESTAMP_VOTER_TX = [
    14954817,
    14958683,
    16783184,
    16784668,
    16937055,
    17293850,
    17294231,
    17371118,
    17176944]

RECIPIENTID_VOTER_TX = [
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'APGjeMNZY99WuzZi18NUb8RowEscLV7F7M',
    'AYh5dfUWmpPqmYNtrUuUTk6S84mH2aScvj',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    None,
    None,
    ]


SENDERID_VOTER_TX = [
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY',
    'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE',
    'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE',
    'AaXH52ZoMuu4j17Si99DzHjDHDReWcHt1a',
    'AQb8wgkPTHGa9xfXvtQWdz49j8JZ7cvwf3'
]

RAWASSET_VOTER_TX = [
    '{"votes":["-031641ff081b93279b669f7771b3fbe48ade13eadb6d5fd85bdd025655e349f008"]}',
    '{"votes":["+0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a"]}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{}',
    '{"signature":{"publicKey":"02b63da5d9ecef548e5fdb4a56dcc15d3737e1ae4692a87e4f2beb20bc7cc13e7d"}}',
    '{"delegate":{"username":"mackenzy","publicKey":"0315e749e0b2671f0cffd25b2c8de7700178e55af8ff994e0e2449556d64c97721"}}',


]

TYPE_VOTER_TX = [
    3,
    3,
    0,
    0,
    0,
    0,
    0,
    1,
    2,
]

FEE_VOTER_TX = [
    100000000,
    100000000,
    100000000,
    100000000,
    100000000,
    100000000,
    100000000,
    500000000,
    2500000000
]

GET_VOTER_TX = [
    (ID_VOTER_TX[0], AMOUNT_VOTER_TX[0], TIMESTAMP_VOTER_TX[0], RECIPIENTID_VOTER_TX[0],
     SENDERID_VOTER_TX[0], RAWASSET_VOTER_TX[0], TYPE_VOTER_TX[0], FEE_VOTER_TX[0]),
    (ID_VOTER_TX[1], AMOUNT_VOTER_TX[1], TIMESTAMP_VOTER_TX[1], RECIPIENTID_VOTER_TX[1],
     SENDERID_VOTER_TX[1], RAWASSET_VOTER_TX[1], TYPE_VOTER_TX[1], FEE_VOTER_TX[1]),
    (ID_VOTER_TX[2], AMOUNT_VOTER_TX[2], TIMESTAMP_VOTER_TX[2], RECIPIENTID_VOTER_TX[2],
     SENDERID_VOTER_TX[2], RAWASSET_VOTER_TX[2], TYPE_VOTER_TX[2], FEE_VOTER_TX[2]),
    (ID_VOTER_TX[3], AMOUNT_VOTER_TX[3], TIMESTAMP_VOTER_TX[3], RECIPIENTID_VOTER_TX[3],
     SENDERID_VOTER_TX[3], RAWASSET_VOTER_TX[3], TYPE_VOTER_TX[3], FEE_VOTER_TX[3]),
    (ID_VOTER_TX[4], AMOUNT_VOTER_TX[4], TIMESTAMP_VOTER_TX[4], RECIPIENTID_VOTER_TX[4],
     SENDERID_VOTER_TX[4], RAWASSET_VOTER_TX[4], TYPE_VOTER_TX[4], FEE_VOTER_TX[4]),
    (ID_VOTER_TX[5], AMOUNT_VOTER_TX[5], TIMESTAMP_VOTER_TX[5], RECIPIENTID_VOTER_TX[5],
     SENDERID_VOTER_TX[5], RAWASSET_VOTER_TX[5], TYPE_VOTER_TX[5], FEE_VOTER_TX[5]),
    (ID_VOTER_TX[6], AMOUNT_VOTER_TX[6], TIMESTAMP_VOTER_TX[6], RECIPIENTID_VOTER_TX[6],
     SENDERID_VOTER_TX[6], RAWASSET_VOTER_TX[6], TYPE_VOTER_TX[6], FEE_VOTER_TX[6]),
    (ID_VOTER_TX[7], AMOUNT_VOTER_TX[7], TIMESTAMP_VOTER_TX[7], RECIPIENTID_VOTER_TX[7],
     SENDERID_VOTER_TX[7], RAWASSET_VOTER_TX[7], TYPE_VOTER_TX[7], FEE_VOTER_TX[7]),
    (ID_VOTER_TX[8], AMOUNT_VOTER_TX[8], TIMESTAMP_VOTER_TX[8], RECIPIENTID_VOTER_TX[8],
     SENDERID_VOTER_TX[8], RAWASSET_VOTER_TX[8], TYPE_VOTER_TX[8], FEE_VOTER_TX[8])
]

NAMED_TRANSACTIONS_VOTER_TX = [
    Transaction(id=ID_VOTER_TX[0],
                amount=AMOUNT_VOTER_TX[0],
                timestamp=TIMESTAMP_VOTER_TX[0],
                recipientId=RECIPIENTID_VOTER_TX[0],
                senderId=SENDERID_VOTER_TX[0],
                rawasset=RAWASSET_VOTER_TX[0],
                type=TYPE_VOTER_TX[0],
                fee=FEE_VOTER_TX[0]),
    Transaction(id=ID_VOTER_TX[1],
                amount=AMOUNT_VOTER_TX[1],
                timestamp=TIMESTAMP_VOTER_TX[1],
                recipientId=RECIPIENTID_VOTER_TX[1],
                senderId=SENDERID_VOTER_TX[1],
                rawasset=RAWASSET_VOTER_TX[1],
                type=TYPE_VOTER_TX[1],
                fee=FEE_VOTER_TX[1]),
    Transaction(id=ID_VOTER_TX[2],
                amount=AMOUNT_VOTER_TX[2],
                timestamp=TIMESTAMP_VOTER_TX[2],
                recipientId=RECIPIENTID_VOTER_TX[2],
                senderId=SENDERID_VOTER_TX[2],
                rawasset=RAWASSET_VOTER_TX[2],
                type=TYPE_VOTER_TX[2],
                fee=FEE_VOTER_TX[2]),
    Transaction(id=ID_VOTER_TX[3],
                amount=AMOUNT_VOTER_TX[3],
                timestamp=TIMESTAMP_VOTER_TX[3],
                recipientId=RECIPIENTID_VOTER_TX[3],
                senderId=SENDERID_VOTER_TX[3],
                rawasset=RAWASSET_VOTER_TX[3],
                type=TYPE_VOTER_TX[3],
                fee=FEE_VOTER_TX[3]),
    Transaction(id=ID_VOTER_TX[4],
                amount=AMOUNT_VOTER_TX[4],
                timestamp=TIMESTAMP_VOTER_TX[4],
                recipientId=RECIPIENTID_VOTER_TX[4],
                senderId=SENDERID_VOTER_TX[4],
                rawasset=RAWASSET_VOTER_TX[4],
                type=TYPE_VOTER_TX[4],
                fee=FEE_VOTER_TX[4]),
    Transaction(id=ID_VOTER_TX[5],
                amount=AMOUNT_VOTER_TX[5],
                timestamp=TIMESTAMP_VOTER_TX[5],
                recipientId=RECIPIENTID_VOTER_TX[5],
                senderId=SENDERID_VOTER_TX[5],
                rawasset=RAWASSET_VOTER_TX[5],
                type=TYPE_VOTER_TX[5],
                fee=FEE_VOTER_TX[5]),
    Transaction(id=ID_VOTER_TX[6],
                amount=AMOUNT_VOTER_TX[6],
                timestamp=TIMESTAMP_VOTER_TX[6],
                recipientId=RECIPIENTID_VOTER_TX[6],
                senderId=SENDERID_VOTER_TX[6],
                rawasset=RAWASSET_VOTER_TX[6],
                type=TYPE_VOTER_TX[6],
                fee=FEE_VOTER_TX[6]),
    Transaction(id=ID_VOTER_TX[7],
                amount=AMOUNT_VOTER_TX[7],
                timestamp=TIMESTAMP_VOTER_TX[7],
                recipientId=RECIPIENTID_VOTER_TX[7],
                senderId=SENDERID_VOTER_TX[7],
                rawasset=RAWASSET_VOTER_TX[7],
                type=TYPE_VOTER_TX[7],
                fee=FEE_VOTER_TX[7]),
    Transaction(id=ID_VOTER_TX[8],
                amount=AMOUNT_VOTER_TX[8],
                timestamp=TIMESTAMP_VOTER_TX[8],
                recipientId=RECIPIENTID_VOTER_TX[8],
                senderId=SENDERID_VOTER_TX[8],
                rawasset=RAWASSET_VOTER_TX[8],
                type=TYPE_VOTER_TX[8],
                fee=FEE_VOTER_TX[8]),
]

PAYOUT_BLOCKS_TIMESTAMP = [
    15011440,
    16605840,
    17379472,
]

PAYOUT_BLOCKS_HEIGT = [
    1866225,
    2061422,
    2156398
]

PAYOUT_BLOCKS_ID = [
    '1639097675237354662',
    '9744301782684317078',
    '1820458585265934614',
]

GET_PAYOUT_BLOCKS = [
    (PAYOUT_BLOCKS_TIMESTAMP[0], PAYOUT_BLOCKS_HEIGT[0], PAYOUT_BLOCKS_ID[0]),
    (PAYOUT_BLOCKS_TIMESTAMP[1], PAYOUT_BLOCKS_HEIGT[1], PAYOUT_BLOCKS_ID[1]),
    (PAYOUT_BLOCKS_TIMESTAMP[2], PAYOUT_BLOCKS_HEIGT[2], PAYOUT_BLOCKS_ID[2]),
]

NAMED_PAYOUT_BLOCKS = [
    Block(timestamp=PAYOUT_BLOCKS_TIMESTAMP[0],
          height=PAYOUT_BLOCKS_HEIGT[0],
          id=PAYOUT_BLOCKS_ID[0]),
    Block(timestamp=PAYOUT_BLOCKS_TIMESTAMP[1],
          height=PAYOUT_BLOCKS_HEIGT[1],
          id=PAYOUT_BLOCKS_ID[1]),
    Block(timestamp=PAYOUT_BLOCKS_TIMESTAMP[2],
          height=PAYOUT_BLOCKS_HEIGT[2],
          id=PAYOUT_BLOCKS_ID[2]),
]




BALANCE_DICT = {
    PAYOUT_BLOCKS_TIMESTAMP[0]:
        {AMOUNT_VOTER_TX[0]: {'balance': 0, 'status': True, 'last_payout': TIMESTAMP_VOTER_TX[0], 'share': 2,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[0]},
         AMOUNT_VOTER_TX[1]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[1], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[1]},
         AMOUNT_VOTER_TX[2]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[2], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[2]},
         AMOUNT_VOTER_TX[3]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[3], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[3]},
         AMOUNT_VOTER_TX[4]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[0], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[0]},
         AMOUNT_VOTER_TX[5]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[1], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[1]},
         AMOUNT_VOTER_TX[6]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[2], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[2]},
         AMOUNT_VOTER_TX[7]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[3], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES[3]},
         AMOUNT_VOTER_TX[8]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMP_VOTER_TX[2], 'share': 0,
                  'vote_timestamp': TIMESTAMP_VOTER_TX[2]},


    },
    PAYOUT_BLOCKS_TIMESTAMP[1]:
        {
    },
    PAYOUT_BLOCKS_TIMESTAMP[2]:
        {

    },
}

# GENERATING SINGLE TRANSACTIONS FOR THE PARSE FUNCTION

ADDRESS_PARSE = ['A', 'B', 'C', 'D']
TIMESTAMPS_VOTES_PARSE = [50, 1000, 2000, 4000]
BLOCK_NR = [1, 1001, 1999, 4000]


SINGLE_EMPTY_VOTERDICT_PARSE_1 = {
    ADDRESS_PARSE[0]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_EMPTY_VOTERDICT_PARSE_2 = {
    ADDRESS_PARSE[1]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_EMPTY_VOTERDICT_PARSE_3 = {
    ADDRESS_PARSE[2]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_EMPTY_VOTERDICT_PARSE_4 = {
    ADDRESS_PARSE[2]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]},
    ADDRESS_PARSE[3]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_EMPTY_VOTERDICT_PARSE_5 = {
    ADDRESS_PARSE[3]: {'balance': 0, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_EMPTY_VOTERDICT_PARSE_6 = {
    ADDRESS_PARSE[3]: {'balance': 0, 'status': True, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}

#for shorter import
EMPTY_VOTERDICTS_PARSE = [SINGLE_EMPTY_VOTERDICT_PARSE_1, SINGLE_EMPTY_VOTERDICT_PARSE_2,
                          SINGLE_EMPTY_VOTERDICT_PARSE_3, SINGLE_EMPTY_VOTERDICT_PARSE_4,
                          SINGLE_EMPTY_VOTERDICT_PARSE_5, SINGLE_EMPTY_VOTERDICT_PARSE_6]

TRANSACTIONS_PARSE = [
    Transaction(id=1,
                amount=100,
                timestamp=TIMESTAMPS_VOTES_PARSE[0],
                recipientId=ADDRESS_PARSE[0],
                senderId=None,
                rawasset='{}',
                type=0,
                fee=0.1,),
    Transaction(id=2,
                amount=100,
                timestamp=TIMESTAMPS_VOTES_PARSE[1],
                recipientId=None,
                senderId=ADDRESS_PARSE[1],
                rawasset='{}',
                type=0,
                fee=0.1,),
    Transaction(id=3,
                amount=100,
                timestamp=10000,
                recipientId=ADDRESS_PARSE[2],
                senderId=config.DELEGATE['ADDRESS'],
                rawasset='{}',
                type=0,
                fee=0.1,),
    Transaction(id=4,
                amount=100,
                timestamp=TIMESTAMPS_VOTES_PARSE[3],
                recipientId=ADDRESS_PARSE[2],
                senderId=ADDRESS_PARSE[3],
                rawasset='{}',
                type=0,
                fee=0.1,),
    Transaction(id=5,
                amount=0,
                timestamp=10000,
                recipientId=ADDRESS_PARSE[3],
                senderId=ADDRESS_PARSE[3],
                rawasset="""{"votes":["+0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a"]}""",
                type=3,
                fee=1,),
    Transaction(id=6,
                amount=0,
                timestamp=10000,
                recipientId=ADDRESS_PARSE[3],
                senderId=ADDRESS_PARSE[3],
                rawasset='{"votes":["-0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a"]}',
                type=3,
                fee=1,),
    Transaction(id=7,
                amount=0,
                timestamp=10000,
                recipientId=None,
                senderId=ADDRESS_PARSE[3],
                rawasset='{"signature":{"publicKey":"031817ddce59e7505b77af7f1b465913e9ff6589d2f80919261bd04d14243660d8"}}',
                type=1,
                fee=5,),
    Transaction(id=8,
                amount=0,
                timestamp=10000,
                recipientId=None,
                senderId=ADDRESS_PARSE[3],
                rawasset='{"delegate":{"username":"genesis_26","publicKey":"033c9e5a710bff3131b406a8023a60e6b76a2ccf937cd85b56add7c4a33ae3090f"}}',
                type=2,
                fee=25,)
]

SINGLE_VOTERDICT_PARSE_1 = {
    ADDRESS_PARSE[0]: {'balance': 100, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}
}
SINGLE_VOTERDICT_PARSE_2 = {
    ADDRESS_PARSE[1]: {'balance': -100.1, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}

SINGLE_VOTERDICT_PARSE_3 = {
    ADDRESS_PARSE[2]: {'balance': 100, 'status': False, 'last_payout': 10000, 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}

SINGLE_VOTERDICT_PARSE_4 = {
    ADDRESS_PARSE[2]: {'balance': 100, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]},
    ADDRESS_PARSE[3]: {'balance': -100.1, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                       'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}

SINGLE_VOTERDICT_PARSE_5 = {
    ADDRESS_PARSE[3]: {'balance': -1, 'status': True, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': 10000}}

SINGLE_VOTERDICT_PARSE_6 = {
    ADDRESS_PARSE[3]: {'balance': -1, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_VOTERDICT_PARSE_7 = {
    ADDRESS_PARSE[3]: {'balance': -5, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}
SINGLE_VOTERDICT_PARSE_8 = {
    ADDRESS_PARSE[3]: {'balance': -25, 'status': False, 'last_payout': TIMESTAMPS_VOTES_PARSE[0], 'share': 0,
                  'vote_timestamp': TIMESTAMPS_VOTES_PARSE[0]}}


PARSED_SINGLE_VOTERDICTS = [SINGLE_VOTERDICT_PARSE_1, SINGLE_VOTERDICT_PARSE_2, SINGLE_VOTERDICT_PARSE_3, SINGLE_VOTERDICT_PARSE_4,
                            SINGLE_VOTERDICT_PARSE_5, SINGLE_VOTERDICT_PARSE_6, SINGLE_VOTERDICT_PARSE_7, SINGLE_VOTERDICT_PARSE_8]

NAMED_BLOCKS_PARSE = [
    Block(timestamp=TIMESTAMPS_VOTES_PARSE[0]-1,
          height=HEIGHT[0],
          id=BLOCK_ID[0]),
    Block(timestamp=TIMESTAMPS_VOTES_PARSE[1]-1,
          height=HEIGHT[1],
          id=BLOCK_ID[1]),
    Block(timestamp=TIMESTAMPS_VOTES_PARSE[2]-1,
          height=HEIGHT[2],
          id=BLOCK_ID[2]),
    Block(timestamp=TIMESTAMPS_VOTES_PARSE[3]-1,
          height=HEIGHT[2],
          id=BLOCK_ID[2])
]

# Mocks to test parse_tx

ALL_TX_1 = [
     Transaction(id=1,
                 amount=1,
                 timestamp=1,
                 recipientId='A',
                 senderId=None,
                 rawasset='{}',
                 type=0,
                 fee=0,)
    ]

ALL_TX_2 = [
        Transaction(id=2,
                    amount=10,
                    timestamp=2,
                    recipientId='B',
                    senderId=None,
                    rawasset='{}',
                    type=0,
                    fee=0,),
        Transaction(id=3,
                    amount=100,
                    timestamp=5,
                    recipientId='B',
                    senderId=None,
                    rawasset='{}',
                    type=0,
                    fee=0,),
        Transaction(id=4,
                    amount=0,
                    timestamp=100,
                    recipientId='B',
                    senderId=None,
                    rawasset='{}',
                    type=0,
                    fee=0,)
    ]
ALL_TX_3 = [Transaction(id=2,
                 amount=1000,
                 timestamp=100001,
                 recipientId='C',
                 senderId=None,
                 rawasset='{}',
                 type=0,
                 fee=0,),
     Transaction(id=2,
                 amount=10000,
                 timestamp=100001,
                 recipientId='C',
                 senderId=None,
                 rawasset='{}',
                 type=0,
                 fee=0,)]

ALL_TX = [ALL_TX_1, ALL_TX_2, ALL_TX_3]

VOTERDICT_PARSETX = [
    {'A': {'balance': 0, 'status': False, 'last_payout': 0, 'share': 0,
          'vote_timestamp': 0}},
    {'B': {'balance': 0, 'status': False, 'last_payout': 0, 'share': 0,
          'vote_timestamp': 0}},
    {'C': {'balance': 0, 'status': False, 'last_payout': 0, 'share': 0,
          'vote_timestamp': 0}}
]

NAMED_BLOCK_PARSETX = [
    [
    Block(timestamp=0,
          height=1,
          id=1),
],
    [
    Block(timestamp=1,
          height=1,
          id=1),
    Block(timestamp=6,
          height=1,
          id=1),
    Block(timestamp=7,
          height=1,
          id=1)

],  [
    Block(timestamp=0,
          height=1,
          id=1),
    Block(timestamp=9999,
          height=1,
          id=1),
]
]

BALANCE_DICT_PARSETX_1 = {
    0: {'A': {'balance': 0, 'status': False, 'last_payout': 0, 'share': 0,
        'vote_timestamp': 0}}}

BALANCE_DICT_PARSETX_2= {
    1: {'B': {'balance': 10, 'status': False, 'last_payout': 0, 'share': 0,
               'vote_timestamp': 0}},

    6: {'B': {'balance': 110, 'status': False, 'last_payout': 0, 'share': 0,
               'vote_timestamp': 0}}}






# TESTING STRETCH

DICT_UNSTRETCHED = {
    1: 'A',
    2: 'B',
    4: 'D'
}

TOTAL_BLOCKS = {
    Block(timestamp=1,
          height=0,
          id=1),
    Block(timestamp=2,
          height=1,
          id=2),
    Block(timestamp=3,
          height=2,
          id=3),
    Block(timestamp=4,
          height=3,
          id=4),
}

DICT_STRETCHED = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D'
}

API_RESULT = {"meta":
                  {"limit": 20, "next": None, "offset": 0, "previous": None, "total_count": 1},
              "objects": [{"id": 1, "payout_frequency": 1, "resource_uri": "/api/user/1/",
                           "wallet": "A"},
                          {"id": 2, "payout_frequency": 2, "resource_uri": "/api/user/2/",
                           "wallet": "B"},
                          {"id": 3, "payout_frequency": 3, "resource_uri": "/api/user/3/",
                           "wallet": "C"}]}

FRQ_DICT = {
    'A': 1,
    'B': 2,
    'C': 3
}
