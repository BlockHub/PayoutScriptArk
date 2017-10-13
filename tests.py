from unittest import TestCase


# todo: set up and tear down objects between each test, and make proper mock objects.

class TestName_transactionslist(TestCase):
    def test_name_transactionslist(self):
        from payoutcalculator import name_transactionslist
        from mock_sets import GET_TRANSACTIONS, NAMED_TRANSACTIONS, GET_VOTER_TX, NAMED_TRANSACTIONS_VOTER_TX
        self.assertCountEqual(name_transactionslist(GET_TRANSACTIONS), NAMED_TRANSACTIONS)
        self.assertCountEqual(name_transactionslist(GET_VOTER_TX), NAMED_TRANSACTIONS_VOTER_TX)


class TestCreate_voterdict(TestCase):
    def test_create_voterdict(self):
        from payoutcalculator import create_voterdict
        from mock_sets import GET_VOTERLIST, VOTERDICT
        self.assertTrue(create_voterdict(GET_VOTERLIST) == VOTERDICT)


class TestName_blocks(TestCase):
    def test_name_blocks(self):
        from payoutcalculator import name_blocks
        from mock_sets import GET_BLOCKS, NAMED_BLOCKS, GET_PAYOUT_BLOCKS, NAMED_PAYOUT_BLOCKS
        self.assertTrue(name_blocks(GET_BLOCKS) == NAMED_BLOCKS)
        self.assertTrue(name_blocks(GET_PAYOUT_BLOCKS) == NAMED_PAYOUT_BLOCKS)


class TestParse(TestCase):
    def test_parse(self):
        from payoutcalculator import parse
        from mock_sets import PARSED_SINGLE_VOTERDICTS, EMPTY_VOTERDICTS_PARSE, TRANSACTIONS_PARSE

        # is receiving properly adjusted?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[0], EMPTY_VOTERDICTS_PARSE[0]), PARSED_SINGLE_VOTERDICTS[0])

        # is sending properly adjusted?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[1], EMPTY_VOTERDICTS_PARSE[1]), PARSED_SINGLE_VOTERDICTS[1])

        # are between two voters both voters properly updated?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[2], EMPTY_VOTERDICTS_PARSE[2]), PARSED_SINGLE_VOTERDICTS[2])

        # is last_payout from delegate address properly updated?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[3], EMPTY_VOTERDICTS_PARSE[3]), PARSED_SINGLE_VOTERDICTS[3])

        # is a vote updated?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[4], EMPTY_VOTERDICTS_PARSE[4]), PARSED_SINGLE_VOTERDICTS[4])

        # is an unvote updated?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[5], EMPTY_VOTERDICTS_PARSE[5]), PARSED_SINGLE_VOTERDICTS[5])

        # is delegate registration balance reduction updated?

        self.assertCountEqual(parse(TRANSACTIONS_PARSE[6], EMPTY_VOTERDICTS_PARSE[4]), PARSED_SINGLE_VOTERDICTS[6])

        # is second passphrase balance reduction updated?
        self.assertCountEqual(parse(TRANSACTIONS_PARSE[7], EMPTY_VOTERDICTS_PARSE[4]), PARSED_SINGLE_VOTERDICTS[7])


class TestParse_tx(TestCase):
    def setUp(self):
        import mock_sets
        print('setting up')
        self.voterdict = mock_sets.VOTERDICT_PARSETX
        self.alltx = mock_sets.ALL_TX
        self.blocks = mock_sets.NAMED_BLOCK_PARSETX
        self.balance_dict = mock_sets.BALANCE_DICT_PARSETX_1
        print('finished setting up')

    def tearDown(self):
        print('starting teardown')
        del self.voterdict
        del self.alltx
        del self.blocks
        del self.balance_dict
        print('finished teardown')

    def test_parse_tx(self):
        from payoutcalculator import parse_tx
        self.assertCountEqual(parse_tx(self.alltx[0], self.voterdict[0], self.blocks[0]),
                              self.balance_dict)


class TestStretch(TestCase):
    def test_stretch(self):
        from mock_sets import DICT_UNSTRETCHED, DICT_STRETCHED, TOTAL_BLOCKS
        from payoutcalculator import stretch
        self.assertCountEqual(stretch(DICT_UNSTRETCHED, TOTAL_BLOCKS), DICT_STRETCHED)


class TestGet_frequency(TestCase):
    def test_get_frequency(self):
        from payoutsender import get_frequency
        from mock_sets import API_RESULT, FRQ_DICT
        self.assertCountEqual(get_frequency(API_RESULT), FRQ_DICT)
