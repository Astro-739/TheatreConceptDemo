import random
import create_theatre
from create_theatre import Theatre
from draw_theatre import draw_theatre


def main() -> None:
    
    theatre = Theatre()
    
    theatre.create_random_theatre()
    helper_boxes = False
    draw_theatre(theatre,helper_boxes)
    
    #theatre.create_threatre_mesh()
    


# start main    
if __name__ == '__main__':
    main()
    
