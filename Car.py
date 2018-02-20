import Map
import LineDetector
import CarControl
class Car: #три основных метода которые будут использоваться на соревнованиях MainRoad,CityRoad и Parking

    def __init__(self,device): #тут бы по хорошему проинициализировать все что у нас написано
        Road=LineDetector.RoadControl()
        CarCon=CarControl(device) # кар контролу передаем девайс которым пользуемся



    '''ниже методы связанные с детектированием'''
    def TroubleChecking(self): #дорога чиста и едем прямо? Если нет то говорим почему и что нам нужно сделать
        '''здесь проверить все это дело'''

        return trouble #по задумке 0-прямая дорога, 1-перекресток, 2-знак,3-препятствие

    def LookAround(self):  # осматриваемся как-то



        return



    '''методы связанные с движение'''
    def TurnOn(self,direction): # поворот
        if direction==0: #едем прямо
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==1: #поворот вправо
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==-1: #поворот влево
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==2: #выезд на круговое
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        if direction==-2: #разворот
            while (NotCrossed): #как-то задетектить что мы проехали участок
                self.CarCon.move()
                self.CarCon.turn()
        return
    def StayOnTheLine(self):
        trouble=self.TroubleChecking()
        while(trouble==0|trouble==2): #проверяем что ничего нового не встретилось
            if (trouble==2):
                '''обрабатываем знак'''
            else:
                self.CarCon.move()
            trouble=self.TroubleChecking()

        return trouble #иначе завершаем движение и выдаем почему завершили



    '''основные методы!'''
    def MainRoad(self):# просто едем по по линии и поворачиваем на первых? поворотах направо
        for i in range(2):#всего два поворота ведь так7
            trouble=self.StayOnTheLine(); #держимся нашей прямой
            if trouble==1: #поворот открылся
                # на самом деле достаточно знать только что правый поворот открыт но пока можно говорить что это все перекрестки
                self.TurnOn(1)
        return 1 #по идее должна вернуть значение обозначающее на каком повороте мы заехали

    def CityRoad(self):
        self.map = Map.MyMap(open('map graph.txt')) #нам нужна карта для построения маршрута
        for dot in self.map.dots:
            if dot.id==1:
                startDot=dot
            if dot.id==23:
                finishDot=dot
        self.map.SetDirections(open('Directions.txt'))
        Path=self.map.FindTheWay(startDot,finishDot,0) #теперь наш путь лежит в path
        prev=str(-2) #-2 если на втором повороте заехали, -1 если на первом для клучей
        #идея такая пытаемся поехать в нужном направлении не получилось удаляем ребро, по новой считаем
        while (startDot!=finishDot): #пока не доехали до финиша
            for joint in Path:
                direction=self.map.directions[prev+str(joint.id)] #смотрим направление поворота на данном перекресте
                self.Car.TurnOn(direction) #поворачиваем на повороте 0 прямо 1 право -1 влево 2 круговое движение
                trouble=self.StayOnTheLine() #едем и держимся линии пока ничего не мешает
                prev=str(joint.id) #для вычисления следующего направления запоминаем ребро по которому поехали
                if (trouble!=1): #есди что-то помешало придется вернутся и перестроить маршрут удаляя это ребро
                    #аналогично if(trouble==3) можно использовать
                    joint.Delete()
                    Path=self.map.FindTheWay(startDot,finishDot,0)
                    TurnOn(-2) #придется развернутся -2 разворот
                    break
            else:
                startDot=joint.GetNegative(startDot)#если оказались на перекрестке продолжаем движение'''
        return 2
    def Parking(self):
        self.LookAround()#надо как-то осмотреться
        return 3




ThisCar=Car("/dev/ttyUSB0") #создаем машинку
Car.MainRoad()
Car.CityRoad()
Car.Parking()
