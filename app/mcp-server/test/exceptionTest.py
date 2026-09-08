



def main():

    try:
        0/0
        100/0
        0/100
    except Exception as e:

        print(e)

        import traceback
        ee = traceback.format_exc()

        print(ee)

        # str(context.get("exception"))


    pass



if __name__ == '__main__':
    main()