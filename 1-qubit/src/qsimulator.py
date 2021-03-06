import numpy as np
import math
import cmath
import matplotlib.pyplot as plt
import random

Pi = math.pi


class QC(object):

    def __init__(self, qubits, depth):
        self.size = qubits
        self.depth = depth
        """
        The quantum state is initialized with all qubits at 0.
        """
        self.state = [0]*2**self.size
        self.state[0] = 1
        """
        The angles are initialized at random with normal distribution
        """
        self.angles = [np.random.randn(3) for i in range(self.depth)]

    def initialize(self):
        """Restores the quantum state to the initial one.
        """
        self.state = [0]*2**self.size
        self.state[0] = 1

    ###############################
    # 1-Qubit Gates
    ###############################
            
        
    def h(self, m):
        """Apply the Hadamard Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        s = 1/np.sqrt(2)
        if m>=self.size: raise ValueError('Qubit does not exist.')
        for i in range(2**(self.size-1)):
            I = 2*i-i%(2**m)
            J = I+2**m
            a = s*self.state[I] + s*self.state[J]
            b = s*self.state[I] - s*self.state[J]
            self.state[I] = a
            self.state[J] = b

    def x(self, m):
        """Apply the X Pauli Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        for i in range(2**(self.size-1)):
            I = 2*i-i%(2**m)
            J = I+2**m
            a = self.state[I]
            self.state[I] = self.state[J]
            self.state[J] = a

    def y(self, m):
        """Apply the Y Pauli Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        for i in range(2**(self.size-1)):
            I = 2*i -i%(2**m)
            J = I+2**m
            a = -1.j * self.state[I]
            self.state[I] = 1.j*self.state[J]
            self.state[J] = a

    def z(self, m):
        """Apply the Z Pauli Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        for i in range(2**(self.size-1)):
            J = 2*i - i%(2**m) + 2**m
            self.state[J] *= -1

    def s(self, m):
        """Apply the Phase Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        for i in range(2**(self.size-1)):
            J = 2*i - i%(2**m) + 2**m
            self.state[J] *= 1.j
                
    def t(self, m):
        """Apply the pi/8 Gate on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        aux = cmath.exp(0.25j*math.pi)
        for i in range(2**(self.size-1)):
            J = 2*i - i%(2**m) + 2**m
            self.state[J] *= aux
               
    def rx(self, m, th):
        """Apply a x-rotation on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
            th (float): angle we rotate.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        th2 = 0.5*th
        c = math.cos(th2)
        s = -1.j * math.sin(th2) # beware of conventions
        for i in range(2**(self.size-1)):
            I = 2*i - i%2**m
            J = I + 2**m
            a = c*self.state[I] + s*self.state[J]
            b = s*self.state[I] + c*self.state[J]
            self.state[I] = a
            self.state[J] = b
        
    def ry(self, m, th):
        """Apply a y-rotation on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
            th (float): angle we rotate.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        th2 = 0.5*th
        c = math.cos(th2)
        s = math.sin(th2) # beware of conventions
        for i in range(2**(self.size-1)):
            I = 2*i - i%2**m
            J = I + 2**m
            a = c*self.state[I] - s*self.state[J]
            b = s*self.state[I] + c*self.state[J]
            self.state[I] = a
            self.state[J] = b
        
    def rz(self, m, th):
        """Apply a z-rotation on the m'th qubit.
        Args.
            m (int): the qubit we apply our gate on.
            th (float): angle we rotate.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        aux1 = cmath.exp(0.5j*th)
        aux2 = cmath.exp(-0.5j*th)
        for i in range(2**(self.size-1)):
            I = 2*i - i%2**m
            J = I + 2**m
            self.state[I] *= aux1
            self.state[J] *= aux2
        
                
    #######################################
    # 2-Qubit Gates, Entanglement
    #######################################
            
    def cnot(self, c, t):
        """Apply a Controlled-NOT gate.
        Args.
            c (int): control qubit.
            t (int): target qubit.
        """
        if c>=self.size: raise ValueError('Control does not exist.')
        if t>=self.size: raise ValueError('Target does not exist.')
        if c==t: raise ValueError('Control and Target cannot be the same.')
        for i in range(2**(self.size-2)):
            I = (2**c + i%2**c + ((i-i%2**c)*2)%2**t + 2*((i-i%2**c)*2 -
                 ((2*(i-i%2**c))%2**t)))
            J = I + 2**t
            self.state[I], self.state[J] = self.state[J], self.state[I]
                
    def cz(self, c, t):
        """Apply a Controlled-Z gate.
        Args.
            c (int): control qubit.
            t (int): target qubit.
        """
        if c>=self.size: raise ValueError('Control does not exist.')
        if t>=self.size: raise ValueError('Target does not exist.')
        if c==t: raise ValueError('Control and Target cannot be the same.')
        if t<c: t,c = c,t
        for i in range(2**(self.size-2)):
            I = (2**c + i%2**c + ((i-i%2**c)*2)%2**t + 2*((i-i%2**c)*2 -
                 ((2*(i-i%2**c))%2**t)) + 2**t)
            self.state[I] *= -1

    def swap(self, m, n):
        """Apply a SWAP gate.
        Args.
            m (int): first qubit.
            n (int): second qubit.
        """
        if m>=self.size: raise ValueError('First Qubit does not exist.')
        if n>=self.size: raise ValueError('Second Qubit does not exist.')
        if m==n: raise ValueError('Both Qubits cannot be the same.')
        for i in range(2**(self.size-2)):
            I = (i%2**m + ((i-i%2**m)*2)%2**n + 2*((i-i%2**m)*2 - 
                 ((2*(i-i%2**m))%2**n)) + 2**n)
            J = I + 2**m - 2**n
            self.state[I], self.state[J] = self.state[J], self.state[I]
    ############################################
    # Circuits
    ############################################
   
    # The following are intended to be used with 1-qubit circuits.
    def unitary(self, m, theta, phi, lamb):
        """Apply an arbitrary unitary gate on the m'th qubit.
        Every unitary gate is characterized by three angles.
        Args.
            m (int): qubit the gate is applied on.
            theta (float): first angle.
            phi (float): second angle.
            lamb (float): third angle.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        c = math.cos(0.5*theta)
        s = math.sin(0.5*theta)
        ephi = cmath.exp(1j*phi)
        elamb = cmath.exp(1j*lamb)
        for i in range(2**(self.size-1)):
            I = 2*i -i%(2**m)
            J = I+2**m
            a = c*self.state[I] - s*elamb*self.state[J]
            b = s*ephi*self.state[I] + c*ephi*elamb*self.state[J]
            self.state[I] = a
            self.state[J] = b

    def transunit(self, m, theta, phi, lamb, vector):
        """Transpose of the unitary gate right above.
        Args.
            m (int): qubit the gate is applied on.
            theta (float): first angle.
            phi (float): second angle.
            lamb (float): third angle.
            vector (array complex): what the operator acts on.
        Ret.
            vector (array complex): image of the operation.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        c = math.cos(0.5*theta)
        s = math.sin(0.5*theta)
        ephi = cmath.exp(1j*phi)
        elamb = cmath.exp(1j*lamb)
        for i in range(2**(self.size-1)):
            I = 2*i -i%(2**m)
            J = I+2**m
            a = c*self.state[I] + s*ephi*self.state[J]
            b = -s*elamb*self.state[I] + c*ephi*elamb*self.state[J]
            self.state[I], self.state[J] = a, b
        return vector

    def difunit1(self, m, theta, phi, lamb, vector):
        """Unitary gate differentiated with respect to theta on m'th qubit.
        Not unitary anymore.
        Args.
            m (int): qubit the operator is applied on.
            theta (float): first angle.
            phi (float): second angle.
            lamb (float): third angle.
            vector (array complex): what the operator acts on.
        Ret.
            vector (array complex): image of the operation.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        c = 0.5*math.cos(0.5*theta)
        s = 0.5*math.sin(0.5*theta)
        ephi = cmath.exp(1j*phi)
        elamb = cmath.exp(1j*lamb)
        for i in range(2**(self.size-1)):
            I = 2*i-i%(2**m)
            J = I+2**m
            a = -s*vector[I] -c*elamb*vector[J]
            b = c*ephi*vector[I] -s*ephi*elamb*vector[J]
            vector[I], vector[J] = a, b
        return vector

    def difunit2(self, m, theta, phi, lamb, vector):
        """Unitary operator differentiated with respect to phi on m'th qubit.
        Not unitary anymore.
        Args.
            m (int): qubit the operator is applied on.
            theta (float): first angle.
            phi (float): second angle.
            lamb (float): third angle.
            vector (array complex): what the operator acts on.
        Ret.
            vector (array complex): image of the operation.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        c = math.cos(0.5*theta)
        s = math.sin(0.5*theta)
        ephi = 1j*cmath.exp(1j*phi)
        elamb = cmath.exp(1j*lamb)
        for i in range(2**(self.size-1)):
            I = 2*i-i%(2**m)
            J = I+2**m
            vector[J] = s*ephi*vector[I]+c*ephi*elamb*vector[J]
            vector[I] = 0
        return vector

    def difunit3(self, m, theta, phi, lamb, vector):
        """Unitary operator differentiated with respect to lamb on m'th qubit.
        Not unitary anymore.
        Args.
            m (int): qubit the operator is applied on.
            theta (float): first angle.
            phi (float): second angle.
            lamb (float): third angle.
            vector (array complex): what the operator acts on.
        Ret.
            vector (array complex): image of the operation.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        c = math.cos(0.5*theta)
        s = math.sin(0.5*theta)
        ephi = cmath.exp(1j*phi)
        elamb = 1j*cmath.exp(1j*lamb)
        for i in range(2**(self.size-1)):
            I = 2*i-i%(2**m)
            J = I+2**m
            vector[I] = -s*elamb*vector[J]
            vector[J] = c*ephi*elamb*vector[J]
        return vector


    def block(self, m, point, angles, style=1):
        """Apply a learning block on the m'th qubit.
        Args.
            m (int): qubit the block is applied on.
            point (dim=2 float): coordinates of input.
            angles (dim=3 float): angles that determine a unitary gate.
            style (int): customizes the block.
        """
        if m>=self.size: raise ValueError('Qubit does not exist.')
        if style:
            self.unitary(m, Pi*point[0]+angles[0],
                         Pi*point[1]+angles[1], angles[2])
        else:
            self.ry(m, point[0]*0.5*Pi)
            self.rz(m, (1+point[1])*Pi)
            self.unitary(m, angles[0], angles[1], angles[2])

    def run(self, point, parameters, style=1):
        """Runs the circuit and restores to the initial state.
        Args.
            point (dim=2 float): coordinates of input.
            style (int): customizes the block.
        Ret.
            p0 (float): probability of the final state being |0>.
        """
        for layer in parameters:
            self.block(0, point, layer, style)
        p0 = self.state[0]
        p0 = p0*np.conj(p0)
        self.initialize()
        return p0

    def Cp(self, point, label, parameters):
        """Computes the cost value of a single input.
        Args.
            point(dim=2 float): coordinates of input point.
            label(int): what class does point belong to.
            parameters(array float): NEEDS BE GOTTEN RID OF.
        Ret.
            cp (float): cost value for a single input.
        """
        cp = np.linalg.norm(label - 3*self.run(point, parameters))
        cp = 0.5*cp*cp
        return cp


# The day shall come, when we don't need parameters to be an argument
# of the cost. That is the day when we will know how to analytically
# compute the gradient. Until that day comes, MasterCard.
    def C(self, data, parameters):
        """Computes the cost function over the whole data set.
        Args.
            data (array float): set of input points.
            parameters (array float): NEEDS BE GOTTEN RID OF.
        Ret.
            c (float): cost value for the entire set.
        """
        c = 0
        n = len(data[0])
        for i in range(n):
            c+=self.Cp(data[0][i], data[1][i], parameters)
        c/=n
        return c

    def gradC(self, data, parameters, step):
        """Computes the gradient of the cost function.
        Args.
            data (array float): set of input points.
            parameters (array float): NEEDS BE GOTTEN RID OF.
            step (float): nummerical differentiation step.
        Ret.
            nabla (array float): gradient vector.
        """
        nabla = ([np.zeros(a.shape) for a in parameters])
        dif = np.asarray([np.zeros(a.shape) for a in parameters])
        half=0.5*step
        inv=1/step
        for i in range(len(dif)):
            for j in range(len(dif[i])):
                dif[i][j] = half
                nabla[i][j] = (self.C(data, parameters+dif)-
                               self.C(data, parameters-dif))*inv
                dif[i][j] = 0
        return nabla

    ###########################################
    # Learning
    ###########################################
    def NGD(self, training_data, parameters, learning_rate, step, epochs,
              test_data=None):
        """Perform a nummerical gradient descent.
        Args.
            training_data (array float): training input data set.
            parameters (array float): NEEDS BE GOTTEN RID OF.
            learning_rate (float): distance advanced towards the gradient.
            step (float): nummerical differentiation step.
            epochs (int): number of iterations performed.
            test_data (array float): test input data set.
        Ret.
            new_parameters (array float): new set of parameters proposed.
            cost_train (array float): cost value after every epoch for train.
            cost_test (array float): cost value after every epoch for test.
            accu_train (array float): accuracy after every epoch for train.
            accu_test (array float): accuracy after every epoch for test.
        """
        new_parameters = []
        cost_train, cost_test, accu_train, accu_test = [],[],[],[]
        for i in range(epochs):
            parameters = (parameters - 
                          np.dot(learning_rate,self.gradC(training_data,
                                                          parameters, step)))
            new_parameters.append(parameters)
            cost_train.append(self.C(training_data, parameters))
            if test_data:
                cost_test.append(self.C(test_data, parameters))
            accu_train.append(self.accuracy(training_data, parameters))
            accu_test.append(self.accuracy(test_data, parameters))
        return new_parameters, cost_train, cost_test, accu_train, accu_test

    def accuracy(self, data, parameters):
        """Computes the accuracy of classification for a set of parameters.
        Args.
            data (array float): input data set.
            parameters (array float): NEEDS BE GOTTEN RID OF.
        Ret.
            accu (int): number of inputs correctly classified.
        """
        results = []
        for (x,y) in zip(data[0], data[1]):
            p0 = self.run(x, parameters)
            if p0<0.25: p=0
            elif p0<0.5: p=1
            elif p0<0.75: p=2
            else: p=3
            results.append([p,y])
        accu=sum(int(x == y) for (x,y) in results)
        return accu

    def test(self, data, parameters):
        """Arranges the data into classes, right and wrong lists.
        Args.
            data (array float): input data set.
            parameters (array float): NEEDS BE GOTTEN RID OF.
        Ret.
            circles (array float): one list of points per circle.
            right (array float): points correctly classified.
            wrong (array float): points incorrectly classified.
        """
        circles =[[],[],[],[]]
        right, wrong = [],[]
        results = []
        for (x,y) in zip(data[0], data[1]):
            p0 = self.run(x, parameters)
            if p0<0.25: p=0
            elif p0<0.5: p=1
            elif p0<0.75: p=2
            else: p=3
            results.append([p,y])
        for (x,y) in zip(data[0], results):
            circles[y[0]].append(x)
            if(y[0]==y[1]):
                right.append(x)
            else:
                wrong.append(x)
        return circles, right, wrong

    def plot(self, data, parameters):
        """Plots the already sorted inputs.
        Args.
            data (array float): input data set.
            parameters (array float): NEEDS BE GOTTEN RID OF.
        """
        circles, right, wrong = self.test(data, parameters)
        cx = [0, -0.5, -1, 1]
        cy = [0, -0.5, 1, 0]
        r = [2, 0.5, 1, 1]
        plt.figure(figsize=(9,4))
        x = [[],[],[],[]]
        y = [[],[],[],[]]
        z = [[],[]]
        t = [[],[]]
        for i in range(len(circles)):
            for point in circles[i]:
                x[i].append(point[0])
                y[i].append(point[1])
        ax = plt.subplot(121)
        circle = []
        for i in range(len(circles)):
            circle.append(plt.Circle((cx[i],cy[i]),r[i],
                                     color='k',fill=False))
            ax.add_artist(circle[-1])
        ax.plot(x[0],y[0],'bo', x[1],y[1],'ko', x[2],y[2],'mo',
                x[3],y[3],'yo',markersize=3)
        plt.xlabel('x')
        plt.ylabel('y')
        for rights in right:
            z[0].append(rights[0])
            z[1].append(rights[1])
        for wrongs in wrong:
            t[0].append(wrongs[0])
            t[1].append(wrongs[1])
        bx = plt.subplot(122)
        for i in range(len(circles)):
            circle.append(plt.Circle((cx[i],cy[i]),r[i],
                          color='k',fill=False))
            bx.add_artist(circle[-1])
        bx.plot(z[0],z[1],'go', t[0],t[1],'ro', markersize=3)
        plt.xlabel('x')
        plt.suptitle('sucess rate {:2.2f}%'.format(
            len(right)*100/len(data[0])))
        plt.show()

#####################################
# Quantum Backpropagation
#####################################

    def SGD(self, training_data, epochs, mini_batch_size, learning_rate,
            test_data):
        """Train a variational circuit using Stochastic Gradient Descent.
        Args.
            training_data (array float): set of training input points.
            epochs (int): number of learning epochs performed.
            mini_batch_size (int): size of the learning batches.
            learning_rate (float): distance moved on every step.
            test_data (array float): set of test input points.
        """
        n = len(training_data)
        if test_data:
            test = []
            n_test = len(test_data)
            for i in range(n_test):
                test.append([test_data[0][i],test_data[1][i]])
        for j in range(epochs):
            comb = list(zip(training_data[0],training_data[1]))
            random.shuffle(comb)
            #training_data[0][:], training_data[1][:]=zip(*comb)
            mini_batches = [
                training_data[k:k+mini_batch_size] for k in
                range(0,n,mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learning_rate)
            print('after epoch',j,'score is: ', self.accuracy(test_data))
            print('\tcost = ',self.C(test_data,self.angles))

    def update_mini_batch(self, mini_batch, learning_rate):
        """Propose a new set of parameters for an input batch.
        Args.
            mini_batch (array float): set of input points.
            learning_rate (float): distance moved along the gradient.
        """
        new_angles = [np.zeros(a.shape) for a in self.angles]
        for x,y in zip(mini_batch[0], mini_batch[1]):
            delta_new_angles = self.backpropagate(x,y)
            new_angles = [na +dna for na, dna in zip(new_angles,
                                                     delta_new_angles)]
        self.angles = [a-(learning_rate/len(mini_batch))*na
                       for a,na in zip(self.angles, new_angles)]

    def backpropagate(self, x, y):
        """Propose a new set of angles using a backpropagation algorithm.
        Args.
            x (dim=2 float): coordinates of input point.
            y (int): desired output for input point.
        Ret.
            new_angles (array float): proposal of new angles for one input.
        """
        # CAREFUL! the gradient is not perfectly calculated
        # and so the derivatives dC/dth are complex, 
        # which does not make much sense. This leads to poor performance
        # since the parameters update is kind of unkown to us right now.
        new_angles = [np.zeros(a.shape) for a in self.angles]
        #---------------FeedForward------------
        activations = [self.state.copy()]
        #activations.append(list(self.state))
        for a in self.angles:
            self.unitary(0,a[0],a[1],a[2])
            activations.append(list(self.state))
        #---------------Backward pass----------
            # First step
        delta = [-3*np.conj(activations[-1][0])*
                 (y-3*activations[-1][0]*np.conj(activations[-1][0])),0]
        dif_act = self.difunit1(0, self.angles[-1][0]+x[0],
                                self.angles[-1][1]+x[1],
                                self.angles[-1][2], activations[-2].copy())
        new_angles[-1][0] = np.dot(delta,dif_act)
        dif_act = self.difunit2(0, self.angles[-1][0]+x[0],
                                self.angles[-1][1]+x[1],
                                self.angles[-1][2], activations[-2].copy())
        new_angles[-1][1] = np.dot(delta,dif_act)
        dif_act = self.difunit3(0, self.angles[-1][0]+x[0],
                                self.angles[-1][1]+x[1],
                                self.angles[-1][2], activations[-2].copy())
        new_angles[-1][2] = np.dot(delta,dif_act)
            # Recursive steps
        for l in range(1, self.depth):
            psi = activations[-l-2].copy()
            delta = self.transunit(0, self.angles[-l][0]+x[0],
                                   self.angles[-l][1]+x[1],
                                   self.angles[-l][2], delta)
            dif_act = self.difunit1(0, self.angles[-l-1][0]+x[0],
                                    self.angles[-l-1][1]+x[1],
                                    self.angles[-l-1][2],psi)
            new_angles[-l-1][0] = np.dot(delta,dif_act)
            dif_act = self.difunit2(0, self.angles[-l-1][0]+x[0],
                                    self.angles[-l-1][1]+x[1],
                                    self.angles[-l-1][2],psi)
            new_angles[-l-1][1] = np.dot(delta,dif_act)
            dif_act = self.difunit3(0, self.angles[-l-1][0]+x[0],
                                    self.angles[-l-1][1]+x[1],
                                    self.angles[-l-1][2],psi)
            new_angles[-l-1][2] = np.dot(delta,dif_act)
        self.initialize()
        return new_angles

    def accuracy(self, data):
        """Computes the classification accuracy.
        Args.
            data (array float): input data set.
        Ret.
            score (int): number of inputs correctly classified.
        """
        results = []
        for (x,y) in zip(data[0],data[1]):
            p0 = self.run(x,self.angles)
            if p0<0.25: p=0
            elif p0<0.5: p=1
            elif p0<0.75: p=2
            else: p=3
            results.append([p,y])
        score=sum(int(x==y) for (x,y) in results)
        return score
