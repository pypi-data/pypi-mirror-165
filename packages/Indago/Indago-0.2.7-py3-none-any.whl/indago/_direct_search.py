#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ._optimizer import Optimizer, CandidateState 
import numpy as np

class NelderMead(Optimizer):
    """Squirrel Search Algorithm class"""
    
    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        
        self.X = None
        self.X0 = None
        self.method = 'Vanilla'
        self.params = {}
        self.params['init_step'] = 0.4
        self.params['alpha'] = 1.0
        self.params['gamma'] = 2.0
        self.params['rho'] = 0.5
        self.params['sigma'] = 0.5
        self.iterations = 100
    
    
    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = ''.split()
            optional_params = 'init_step alpha gamma rho sigma'.split()

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print(f'Warning: Excessive parameter {param}')

    def _init_method(self):
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

        # Generate set of points
        self.cS = np.array([CandidateState(self) for _ in range(self.dimensions + 1)], \
                            dtype=CandidateState)
            
        # Generate initial positions
        #self.cS[0].X = 0.5 * (self.lb + self.ub)
        self.cS[0].X = np.random.uniform(self.lb, self.ub)
        if self.X0 is not None:
                if np.shape(self.X0)[0] > 0:
                    self.cS[0].X = self.X0[0]
        self.collective_evaluation(self.cS[:1])
        # self.cS[0].evaluate()
        # print(self.cS[0].X)
         
        for p in range(1, self.dimensions + 1):
            
            # Random position
            dx = np.zeros([self.dimensions])
            dx[p - 1] = self.params['init_step']
            self.cS[p].X = self.cS[p].X + dx * (self.ub - self.lb)
            
            # Using specified particles initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cS[p].X = self.X0[p]
                                          
        # Evaluate
        self.collective_evaluation(self.cS)

    def _run(self):
        self._check_params()
        self._init_method()

        for self.it in range(self.iterations):
            self.cS = np.sort(self.cS)
            # print(self.it, np.min(self.cS).f)
            #print(i, self.cS[0].f, self.cS[-1].f)

            self._progress_log()

            # Check stopping conditions
            if self._stopping_criteria():
                break

            # Center
            X0 = np.zeros(self.dimensions)
            for p in range(self.dimensions):
                X0 += self.cS[p].X
            X0 /= self.dimensions
            
            dX = X0 - self.cS[-1].X
            
            # Reflection
            Xr = X0 + self.params['alpha'] * dX
            cR = CandidateState(self)
            cR.X = Xr
            # cR.evaluate()
            self.collective_evaluation([cR])
                       
            if self.cS[0] <= cR <= self.cS[-2]:
                self.cS[-1] = cR.copy()
                #print('Rf')
                continue
                
            
            # Expansion
            if cR < self.cS[0]:
                Xe = X0 + self.params['gamma'] * dX
                cE = CandidateState(self)
                cE.X = Xe
                # cE.evaluate()
                self.collective_evaluation([cE])
            
                if cE < cR:
                    self.cS[-1] = cE.copy()
                    #print('Ex')
                    continue
                else:
                    self.cS[-1] = cR.copy()
                    #print('Rf')
                    continue


            # Contraction
            if cR < self.cS[-1]:
                
                Xc = X0 + self.params['rho'] * dX
                cC = CandidateState(self)
                cC.X = Xc
                # cC.evaluate()
                self.collective_evaluation([cC])
                
                if cC < self.cS[-1]:
                    self.cS[-1] = cC.copy()
                    #print('Ct')
                    continue
                
            else:
                
                Xc = X0 - self.params['rho'] * dX
                cC = CandidateState(self)
                cC.X = Xc
                # cC.evaluate()
                self.collective_evaluation([cC])
                
                if cC < self.cS[-1]:
                    self.cS[-1] = cC.copy()
                    #print('Ct')
                    continue

            # Reduction
            for p in range(1, self.dimensions + 1):
                self.cS[p].X = self.cS[0].X + self.params['sigma'] * (self.cS[p].X - self.cS[0].X)
                # self.cS[p].evaluate()
            self.collective_evaluation(self.cS[1:])


        return self.best
    
    
    
    

class GGS(Optimizer):
    """Grid Grdient Search class"""
    
    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        
        self.X0 = None
        self.X = None
        self.method = 'Vanilla'
        self.params = {}
        self.params['n'] = 10
        self.iterations = 100
    
    
    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = ''.split()
            optional_params = 'n'.split()

        for param in mandatory_params:
            # if param not in defined_params:
            #    print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print(f'Warning: Excessive parameter {param}')
                
    def _basic_log(self, msg):
        if self.monitoring == 'basic':
            self.rich_console.print(msg)

    def _init_method(self):
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

#        if self.X0 is not None:
#                if np.shape(self.X0)[0] > 0:
#                    self.cS[0].X = self.X0[0]
        
        n = self.params['n']
        self._X_map = np.zeros([self.dimensions, n])
        for i in range(self.dimensions):
            self._X_map[i, :] = np.linspace(self.lb[i], self.ub[i], n)
                
        # Generate array of candidates
        self._CN = np.array([CandidateState(self) for _ in range(self.dimensions)], \
                            dtype=CandidateState)
        self._CP = np.array([CandidateState(self) for _ in range(self.dimensions)], \
                            dtype=CandidateState)
        self._H = []
        
        
        if self.X0 is not None:
            self.x_next = CandidateState(self)
            self.x_next.X = self.X0[0, :]
            self.y_next = self._x_to_y(self.x_next)
                    
        else:
            self.y_next = np.random.randint(0, n, self.dimensions)
            self.x_next = self._y_to_x(self.y_next)
        #self.y_next = np.full(self.dimensions, n - 1)
        
        self.dy = np.zeros([self.dimensions], dtype=int)
        self.collective_evaluation([self.x_next])
        #self.x_last = self.x_next.copy()
        self._H.append(list(self.y_next))
        
    def _x_to_y(self, x):
        y = np.zeros(self.dimensions, dtype=int)
        for i in range(self.dimensions):
            y[i] = np.argmin(np.abs(x.X[i] - self._X_map[i, :]))
        return y
    
    def _y_to_x(self, y):  
        x = CandidateState(self)
        for i in range(self.dimensions):
            x.X[i] = self._X_map[i, y[i]]
        return x
    
    def _run(self):
        self._check_params()
        self._init_method()
        
        n = self.params['n']
        k_max = self.params['k_max']
        d = self.dimensions
        find_dir = True
        k = 0

        for self.it in range(self.iterations):
            
            if find_dir:
                # Finding a new direction based on the gradinet calculation
                k += 1
                self._basic_log(f'Calculating gradient k={k}')

                for i in range(d):
                    dy = np.zeros(d, dtype=int)
                    
                    dy[i] = -1
                    yn = self.y_next + dy
                    yn[yn < 0] = 0
                    yn[yn >= n] = n - 1
                    
                    dy[i] = 1
                    yp = self.y_next + dy
                    yp[yp < 0] = 0
                    yp[yp >= n] = n - 1
                    
                    #print(f' - {dy}')
                    # for j in range(self.dimensions):
                    #     self.CN[i].X[j] = self.X[j, yn[j]]
                    #     self.CP[i].X[j] = self.X[j, yp[j]]
                    self._CN[i] = self._y_to_x(yn)
                    self._CP[i] = self._y_to_x(yp)
                    
                C = np.append(self._CN, self._CP)
                self.collective_evaluation(C)
                           
                self.dy = np.zeros(d, dtype=int)
                for i in range(d):                    
                    c0 = self.x_next
                    cn = self._CN[i]
                    cp = self._CP[i]
                    self.dy[i] = np.argmin([cn, c0, cp]) - 1
                    # if cn < c0 and cn < cp:
                    #     self.dy[i] = -1
                    # elif cp < c0 and cp < cn:
                    #     self.dy[i] = 1
                    # else:
                    #     self.dy[i] = 0
                                
            else:
                pass
                self._basic_log('Keeping direction')
                #k = 0
                
            if np.sum(np.abs(self.dy)) == 0:
                # None of x_next's neighbouring points are better
                if self.x_next == self.best:
                    # x_next is the best, hence convergence is finished
                    self._basic_log('Converged to local optima')
                    break
                else:
                    # Switching to the best point
                    self._basic_log('Focusing on best')
                    self.y_next = self._x_to_y(self.best)
                    self.x_next = self.best.copy()
                    find_dir = True
                    k = 0
                    continue
            
            # Moving in dy direction
            self.y_next = self.y_next + self.dy
            # Trimming bounds
            for i in range(d):
                self.y_next[self.y_next < 0] = 0
                self.y_next[self.y_next >= n] = n - 1
            
            # Calculate x_next
            x_last = self.x_next.copy()
            self.x_next = self._y_to_x(self.y_next)
            # Evaluate x_next
            self.collective_evaluation([self.x_next])
            
            # Calculate y_best
            y_best = self._x_to_y(self.best)
            # for i in range(d):
            #     y_best[i] = np.argmin(np.abs(self.best.X[i] - self.X[i, :]))
                
            # Set finding new direction if there is no improvement in new point
            find_dir = self.x_next >= x_last
               
            if list(self.y_next) in self._H:
                # If new point is already calculated
                    
                if np.sum(self.y_next - y_best) == 0 or list(y_best) in self._H and find_dir:
                    self._basic_log('Finished')
                    # input('> Press return to continue.')    
                    break            
                else:
                    #print(yb, ' >> ', self.y)
                    self._basic_log('Switching point')
                    self.y_next = y_best
                    find_dir = True
                    k = 0
                    # input('> Press return to continue.')  
                    
            else:
                self._H.append(list(self.y_next))
            
            
            if k >= k_max:
                self._basic_log('Switching point (k > k_max)')
                self.y_next = y_best
                find_dir = True
                k = 0
            
            self._progress_log()
            #print(self.y_next)
            # print(self.dy)
            # print(self.best.f)
            # input('> Press return to continue.')
            
            # Check stopping conditions
            if self._stopping_criteria():
                self._basic_log('Stop')
                break
            
        return self.best