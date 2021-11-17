from account.tests.factory import UserFactory


def test_jwt_auth():

    user1 = UserFactory()
    user2 = UserFactory()

    assert user1 != user2
