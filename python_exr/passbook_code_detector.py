print('For cancel the process please type [quit]')

while True:
    print("enter 10 digit passcode no:")

    try:
    
        user = input().lower()
        input_data = [x for x in user]

        if len(input_data) == 10:

            if input_data[-1] == 'x':
                    input_data[-1] = 10
                    input_data = [int(x) for x in input_data]
                    result = 0
                    x= len(input_data)
                    for i in input_data:
                        result += x * i
                        x-= 1
                    if result%11 != 0:
                        print('Entered Passbook number is Valid')
                    else:
                        print('Passbook number is not Valid')
                    
            elif user.isdigit():
                    input_data = [int(x) for x in input_data]
                    result = 0
                    x= len(input_data)
                    for i in input_data:
                        result += x * i
                        x-= 1
                    if result%11 != 0:
                        print('Entered Passbook number is Valid')
                    else:
                        print('Passbook number is not Valid')
                    
            else:
                print("Entered Passcode number in incorrect kindly Re-enter")
        
        elif 'quit' in user:
            break

        else:
            print("Entered Passcode number in incorrect kindly Re-enter 10 Digit Passcode number")
    except BaseException:
                print("Base Error")
    