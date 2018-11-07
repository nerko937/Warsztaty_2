import argparse
from models.user import User
from models.message import Message


# arguments
def arg_parser(return_help=None):
    parser = argparse.ArgumentParser(description='Zażądzajka urzytkownikami!')
    parser.add_argument('-u', '--username', help="Email", required=False)
    parser.add_argument('-p', '--password', help="Hasło", required=False)
    parser.add_argument('-n', '--new_pass', help="Nowe hasło", required=False)
    parser.add_argument('-l', '--list', help="Lista użytkowników lub wiadomości do użytkownika", required=False, action='store_true')
    parser.add_argument('-d', '--delete', help="Usuwa użytkownika", required=False, action='store_true')
    parser.add_argument('-e', '--edit', help="Edytuje użytkownika (do zmiany hasła)", required=False, action='store_true')
    parser.add_argument('-t', '--to', help="Email odbiorcy", required=False)
    parser.add_argument('-s', '--send', help="Wysyła wiadomość", required=False, nargs='?', default=None, const='empty')
    if return_help is not None:
        parser.print_help()
    return parser.parse_args()


# checks password length
def password_len(password):
    if len(password) in range(8, 21):
        return True
    else:
        print("Hasło powinno mieć od 8 do 20 znaków")
        return False


# final function
def run(cursor):
    args = arg_parser()
    # lists all user emails
    if args.list and not args.username and not args.password:
        buddies = User.load_all_users(cursor)
        ret = ''
        for user in buddies:
            ret += '{}\n'.format(user.email)
        print(ret)
        return ret
    # bunch of operations after login
    user = User.login(cursor, args.username, args.password)
    if user is not False and user is not None:
        # change password
        if args.username and args.password and args.edit and args.new_pass:
            if password_len(args.password) is True:
                User.change_pass(user, cursor, args.new_pass)
        # delete user
        elif args.username and args.password and args.delete:
            User.delete(user, cursor)
            print('Usunięto użytkownika')
        # list messages for user
        elif args.username and args.password and args.list:
            messages = Message.load_all_messages_for_user(cursor, user.id)
            ret = ''
            for row in messages:
                buddy = User.load_user_by_id(cursor, row.from_id)
                ret += 'Wiadomość od: {} z {}\n{}\n\n'.format(buddy.email, row.creation_date, row.text)
            print(ret)
            return ret
        # sends message
        elif args.username and args.password and args.to and args.send:
            if args.send == 'empty':
                print('Nie podałeś wiadomości')
                return False
            sql = 'SELECT id FROM Users WHERE email=%s;'
            cursor.execute(sql, (args.to,))
            try:
                to_id = cursor.fetchone()[0]
            except TypeError:
                print('Nie ma takiego użytkownika')
                return False
            new_message = Message()
            new_message.from_id = user.id
            new_message.to_id = to_id
            new_message.text = args.send
            new_message.save_to_db(cursor)
            print('Wysłano')
    # creates user
    if args.username and args.password:
        if password_len(args.password) is True:
            User.create_user(cursor, args.username, args.password)
        return True
    # shows help
    else:
        arg_parser('help')
