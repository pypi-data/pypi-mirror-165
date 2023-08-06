from generalized_matth.matt_funct import  AVERAG_TYPE
from aenum import  extend_enum



def extend_matt_enum():
    for name, value in (
            ('HARMONIC', 0),
            ('ARITHMETIC', 1),

    ):
        extend_enum(AVERAG_TYPE, name, value)
    return
class main_generalzied_object:
    def __init__(self,average_val):
        extend_matt_enum()
        
        return



if __name__ =='__main__':
    bb= main_generalzied_object(0)
    for data in AVERAG_TYPE:
        print (data.value,data.name)

