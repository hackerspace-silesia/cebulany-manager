import argparse
import getpass

from cebulany.models import User
from cebulany.app import app, db


class CliException(Exception):
    pass


def list_user():
    return User.query.all()


def add_user(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        raise CliException('user exists')
    user = User()
    user.username = username
    user.password = getpass.getpass()
    db.session.add(user)
    db.session.commit()
    return user


def del_user(username):
    user = find_user(username)
    db.session.delete(user)
    db.session.commit()


def change_password(username):
    user = find_user(username)
    user.password = getpass.getpass()
    db.session.add(user)
    db.session.commit()


def find_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise CliException('user not found')
    return user


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='User CLI for cebulany manager',
    )
    subparsers = parser.add_subparsers(metavar='CMD', dest='cmd')

    add_parser = subparsers.add_parser('list', help='list of all users')

    add_parser = subparsers.add_parser('add', help='add user to database')
    add_parser.add_argument('username')

    del_parser = subparsers.add_parser('del', help='remove user from database')
    del_parser.add_argument('username')

    change_paswd_parser = subparsers.add_parser('change-password', help='change password of user in database')
    change_paswd_parser.add_argument('username')

    args = parser.parse_args()

    try:
        with app.app_context():
            if args.cmd is None:
                parser.print_help()
            elif args.cmd == 'list':
                users = list_user()
                print('ID', 'USERNAME', sep='\t\t')
                for user in users:
                    print(
                        user.id,
                        user.username,
                        sep='\t\t',
                    )
            elif args.cmd == 'add':
                user = add_user(args.username)
                print('OK. 2FA url: ', user.totp_uri)
            elif args.cmd == 'del':
                del_user(args.username)
                print('OK.')
            elif args.cmd == 'change-password':
                change_password(args.username)
                print('OK.')
    except CliException as exp:
        print('ERROR:', exp)
