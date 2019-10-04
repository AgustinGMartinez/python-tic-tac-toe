# custom imports
import blueprint
import state
import functions
# module
import logging

logging.basicConfig(filename="logger.txt",
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


while True:
    try:
        functions.clear_console()
        functions.draw_dashbord()
        try:
            functions.handle_move()
        except UnicodeDecodeError as err:
            print("Invalid move:", err)
        functions.check_winner()
    except Exception as err:
        logging.exception('Got exception on main handler')
        raise
