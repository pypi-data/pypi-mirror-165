import argparse
import json
import re

from moydomjkh import Session, User


def main():
    parser = argparse.ArgumentParser(description='Please specify input parameters')

    parser.add_argument('-l', '--login', required=True, type=str,
                        help='User login')
    parser.add_argument('-p', '--password', required=True, type=str,
                        help='User password')
    parser.add_argument('-i', '--info', action='store_true',
                        help='User account(s) information')
    parser.add_argument('-u', '--upload', action='store_true',
                        help='Submit measurement')
    parser.add_argument('-m', '--meter', type=str,
                        help='Meter id (required for upload)')
    parser.add_argument('-r', '--result', type=str,
                        help='Measurement result (required for upload)')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Verbosity level (up to vvvvv)')

    args = parser.parse_args()
    try:
        user = User(Session(login=args.login, password=args.password))

        if args.info:
            print(json.dumps(user.to_json(verbose=args.verbose), indent=2, ensure_ascii=False))
            exit(0)
        elif args.upload:
            if not args.meter:
                print(f'Meter id is mandatory')
                exit(1)
            if not args.result:
                print(f'Result is mandatory')
                exit(1)

            meter = None
            if re.match("[0-9]+-[0-9]+-[0-9]+", args.meter):
                meter_ids = args.meter.split('-')
                account = user.accounts.get(f'{meter_ids[0]}-{meter_ids[1]}')
                if account:
                    meter = account.meters.get(args.meter)

            if meter is None:
                print(f'Meter with id {args.meter} is not found')
                exit(1)

            meter.upload_measure(args.result)

    except SystemExit as e:
        pass
    except BaseException as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
