import argparse
import configfile
import datetime
from create import login_create
from updateres import login_update

def cli():
    parser = argparse.ArgumentParser(description="Create reservations at csfoy gym.")
    parser.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")
    parser.add_argument("-u", "--userID", type=str, default=configfile.userID, help="userID used for reservation")
    parser.add_argument("-t", "--time", type=str, default=datetime.datetime.now().strftime("%H"), help="starting hour of the reservation")
    parser.add_argument("-r", "--resource", type=str, default="30", help="resource number (1-80)")
    parser.add_argument("-s", "--scheduleId", type=str, default=configfile.gym_scheduleId, help="sport id (default is 64 for gym)")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="prints the html response")

    args = parser.parse_args()


    # adds zero to single digits
    if len(args.time) < 2:
        starthour = "0" + args.time + ":00:00"
    else:
        starthour = args.time + ":00:00"
    
    endhour = str(int(args.time) + 1)
    if len(endhour) < 2:
        endhour = "0" + endhour + ":00:00"
    else:
        endhour = endhour + ":00:00"
    
    # correcting resource id
    OG_resource_number = int(args.resource)
    resource_number = OG_resource_number
    if OG_resource_number > 25:
        resource_number += 208
    if OG_resource_number > 60:
        resource_number += 144
    resource_number = str(resource_number + 4745)

    try:
        print(
            f"\033[0;36mSending reservation request for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m"
            )
        login_create(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=resource_number, day=args.day, starthour=starthour, endhour=endhour, verbose=args.verbose)

    except:
        print("Request did not work")
        # todo: add possibility to reserve with force
        # try:
        #     print(
        #         f"\033[0;36mSending with force for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m"
        #     )
        #     login_update()
        # except:
        #     print("An internal error happend")
