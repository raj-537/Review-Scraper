import logging

def getLog(log):
    
    logger = logging.getLogger(log)

    level=""
    with open('properties.txt', 'r') as f:
        level = f.read()


    #setting level as DEBUG or ERROR
    if level.upper()=='DEBUG':
        logger.setLevel(level=logging.DEBUG)
    elif level.upper == 'ERROR':
        logger.setLevel(level=logging.ERROR)
    else:
        raise ValueError('Invalid Logging level %s', level)


    #Creating Formatter
    formatter = logging.Formatter(fmt='%(asctime)s %(process)s %(levelname)s --> %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    #creating handlers
    file_handler = logging.FileHandler('test.log')

    #adding formaters to handlers
    file_handler.setFormatter(formatter)

    #Adding Handlers to logger
    logger.addHandler(file_handler)

    return logger