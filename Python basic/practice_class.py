class Unit:
    def __init__(self):
        print("Unit 생성자")

class Flyable:
    def __init__(self):
        print("Flyable 생성자")

#class FlyableUnit(Unit, Flyable):
class FlyableUnit(Flyable, Unit):    
    def __init__(self):
        #super().__init__()
        Unit.__init__(self)
        Flyable.__init__(self)

# 드랍쉽
dropship = FlyableUnit()


# 2개 이상의 다중 부모를 상속 받을 때는, super를 사용하면 순서상에 맨 마지막에 상속받는 class에 대해서만 init 함수가 호출 된다.
# 이런 문제로 다중 상속시, 모든 부모 클래스에 대해서 초기화가 필요할 시에는, 두번 작성해 초기화를 하는 방법이 있다. (따로 작성 해 준다.) 