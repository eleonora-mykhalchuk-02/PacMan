import random, numpy, math
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *

#клас для базового мозку нейромережі
class Brain:
    def __init__(self, netBrainStates, netBrainActions):
        #стани гри
        self.netBrainStates = netBrainStates
        #можливі дії 
        self.netBrainActions = netBrainActions
        #модель мережі
        self.model = self._createModel()

    #створення моделі нейромережі для подальшого навчання
    def _createModel(self):
        model = Sequential()

        # Simple Model with Two Hidden Layers and a Linear Output Layer. The Input layer is simply the State input.
        model.add(Dense(units=64, activation='relu', input_dim=self.netBrainStates))
        model.add(Dense(units=32, activation='relu'))
        model.add(Dense(units=self.netBrainActions,
                        activation='linear'))  # Linear Output Layer as we are estimating a Function Q[S,A]

        model.compile(loss='mse', optimizer='adam')  # use adam as an alternative optimsiuer as per comment
        return model

    #метод для тренування нейромережі
    def train(self, x, y, epoch=1, verbose=0):
        self.model.fit(x, y, batch_size=32, epochs=epoch, verbose=verbose)

    #навчальний метод для прогнозування результатів для переданого стану
    def predict(self, s):
        return self.model.predict(s)

    #метод для прогнозування наступного стану та результатів для гри
    def predictOne(self, s):
        return self.predict(s.reshape(1, self.netBrainStates)).flatten()

#метод для форматування та зберігання даних в історії для навчання мережі 
class ExpReplay:  
    samples = []

    def __init__(self, capacity):
        self.capacity = capacity

    def add(self, sample):
        self.samples.append(sample)

        if len(self.samples) > self.capacity:
            self.samples.pop(0)

    def sample(self, n):
        n = min(n, len(self.samples))
        return random.sample(self.samples, n)


ExpReplay_CAPACITY = 2000 #загальний обсяг пам'яті історії
OBSERVEPERIOD = 25  #кількість ітерацій, що відвидяться на ознайомлення з середовищем
BATCH_SIZE = 25 #розмір групи, на які діляться всі стани
GAMMA = 0.95  #коефіцієнт для порівняння прогнозованої нагороди
MAX_EPSILON = 1 #максимальне значення коефіцієнту швидкості навчання
MIN_EPSILON = 0.05 #мінімальне значення коефіцієнту швидкості навчання
LAMBDA = 0.0002  #швидкість спадання значення епсілон


#клас агента для навчання та гри 
class Agent:
    def __init__(self, netBrainStates, netBrainActions):
        #передані стани
        self.netBrainStates = netBrainStates

        #передані можливі ходи
        self.netBrainActions = netBrainActions

        #створення "мозку" нейромережі
        self.brain = Brain(netBrainStates, netBrainActions)

        #створення історії проходження навчання
        self.ExpReplay = ExpReplay(ExpReplay_CAPACITY)

        #початкова кількість пройдених ітерацій
        self.steps = 0

        self.epsilon = MAX_EPSILON

    #метод для визначення найоптимальнішого ходу
    def Act(self, s):
        if (random.random() < self.epsilon or self.steps < OBSERVEPERIOD):
            return random.randint(0, self.netBrainActions - 1) 
        else:
            return numpy.argmax(self.brain.predictOne(s)) 

    #метод запису даних до історії 
    def CaptureSample(self, sample): 
        self.ExpReplay.add(sample)

        # slowly decrease Epsilon based on our eperience
        self.steps += 1
        if (self.steps > OBSERVEPERIOD):
            self.epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * math.exp(-LAMBDA * (self.steps - OBSERVEPERIOD))

    #міні тренування на виокремленій групі станів із невеликим заданим розміром
    def Process(self):
        batch = self.ExpReplay.sample(BATCH_SIZE)
        batchLen = len(batch)

        no_state = numpy.zeros(self.netBrainStates)

        states = numpy.array([batchitem[0] for batchitem in batch])
        states_ = numpy.array([(no_state if batchitem[3] is None else batchitem[3]) for batchitem in batch])

        predictedQ = self.brain.predict(states) 
        predictedNextQ = self.brain.predict(states_)  

        x = numpy.zeros((batchLen, self.netBrainStates))
        y = numpy.zeros((batchLen, self.netBrainActions))

        for i in range(batchLen):
            batchitem = batch[i]
            state = batchitem[0];
            a = batchitem[1];
            reward = batchitem[2];
            nextstate = batchitem[3]

            targetQ = predictedQ[i]
            if nextstate is None:
                targetQ[a] = reward 
            else:
                targetQ[a] = reward + GAMMA * numpy.amax(predictedNextQ[i])  

            x[i] = state
            y[i] = targetQ

        self.brain.train(x, y)