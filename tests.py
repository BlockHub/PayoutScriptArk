from unittest import TestCase


class TestPlugAndPlay(TestCase):
    def setUp(self):
        from plugandplay import save_delegate_share
        save_delegate_share(1)

    def tearDown(self):
        from plugandplay import save_delegate_share
        save_delegate_share(0)

    def test_get_delegate_share(self):
        from plugandplay import get_delegate_share
        self.assertEqual(1, get_delegate_share())

    def test_save_delegate_share(self):
        from plugandplay import save_delegate_share, get_delegate_share
        save_delegate_share(100)
        self.assertEqual(100, get_delegate_share())


class TestUtils(TestCase):
    def setUp(self):
        import utils
        utils.release_lock(strict=False)

    def test_set_lock(self):
        '''This test also makes sure a race condition isn't present.'''
        import utils
        utils.set_lock()
        self.assertRaises(utils.LockError, utils.set_lock, strict=True)

    def test_release_lock(self):
        import utils
        utils.release_lock(strict=False)
        self.assertRaises(utils.LockError, utils.release_lock, strict=True)


class MiscTests(TestCase):
    def test_last_payout_timestamp(self):
        import arkdbtools.dbtools
        import config

        arkdbtools.dbtools.set_connection(
            host=config.CONNECTION['HOST'],
            database=config.CONNECTION['DATABASE'],
            user=config.CONNECTION['USER'],
            password=config.CONNECTION['PASSWORD'])

        last_payout = arkdbtools.dbtools.Address.payout('AZHTEcD4sJnsTuano7RWD5R7hbYJcKGbrr')[-1].timestamp
        true_last_payout_timestamp = 22552327
        #this test will fail, update the true_last_payout_timestamp if you want to test it.
        self.assertEqual(last_payout, true_last_payout_timestamp)