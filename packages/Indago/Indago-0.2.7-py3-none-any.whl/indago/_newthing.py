# -*- coding: utf-8 -*-

import numpy as np
from ._optimizer import Optimizer, CandidateState 
from scipy.interpolate import interp1d # need this for akb_model




class NewThing(Optimizer):
    """Particle Swarm Optimization class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)
        #super(PSO, self).__init__() # ugly version of the above

        self.method = 'Vanilla'
        self.params = {}

    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        mandatory_params = 'dx'.split()
        if 'dx' not in self.params:
            self.params['dx'] = 0.1
            defined_params += 'dx'.split()
                
        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        
        err_msg = None
        
        # Using specified particles initial positions
        if self.X0 is not None:
            if p < np.shape(self.X0)[0]:
                self.cS[p].X = self.X0[p]
                    
        self.Y = []
                    
        # Bounds for position and velocity
        self.v_max = 0.2 * (self.ub - self.lb)

        self._progress_log()            

    def _run(self):
        self._check_params()
        err_msg = self._init_method()
        if err_msg:
            print('Error: ' + err_msg + ' OPTIMIZATION ABORTED\n')
            return

        if 'inertia' in self.params:
            w = self.params['inertia']
        if 'cognitive_rate' in self.params:
            c1 = self.params['cognitive_rate']
        if 'social_rate' in self.params:
            c2 = self.params['social_rate']

        for self.it in range(1, self.iterations + 1):
            R1 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
            R2 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
                        
            """ LDIW """
            if self.params['inertia'] == 'LDIW':                
                w = 1.0 - (1.0 - 0.4) * self._progress_factor()

            """ TVAC """
            if self.method == 'TVAC':
                c1 = 2.5 - (2.5 - 0.5) * self._progress_factor()
                c2 = 0.5 + (2.5 - 0.5) * self._progress_factor()

            """ Anakatabatic Inertia """
            if self.params['inertia'] == 'anakatabatic':

                theta = np.arctan2(self.dF, np.min(self.dF))
                theta[theta < 0] = theta[theta < 0] + 2 * np.pi  # 3rd quadrant
                # fix for atan2(0,0)=0
                theta0 = theta < 1e-300
                theta[theta0] = np.pi / 4 + \
                    np.random.rand(np.sum(theta0)) * np.pi
                w_start = self.params['akb_fun_start'](theta)
                w_stop = self.params['akb_fun_stop'](theta)
                w = w_start * (1 - self._progress_factor()) + w_stop * self._progress_factor()
            
            w = w * np.ones(self.params['swarm_size']) # ensure w is a vector
            
            # Calculate new velocity and new position
            for p, cP in enumerate(self.cS):
                
                cP.V = w[p] * cP.V + \
                               c1 * R1[p, :] * (self.cB[p].X - cP.X) + \
                               c2 * R2[p, :] * (self.cB[self.BI[p]].X - cP.X)
                cP.X = cP.X + cP.V        
                
                # Correct position to the bounds
                cP.X = np.clip(cP.X, self.lb, self.ub)
                
            # Get old fitness
            f_old = np.array([cP.f for cP in self.cS])

            # Evaluate swarm
            err_msg = self.collective_evaluation(self.cS)
            if err_msg:
                break

            for p, cP in enumerate(self.cS):
                # Calculate dF
                if np.isnan(cP.f):
                    self.dF[p] = np.inf
                elif np.isnan(f_old[p]):
                    self.dF[p] = -np.inf
                else:
                    self.dF[p] = cP.f - f_old[p]
                
            for p, cP in enumerate(self.cS):
                # Update personal best
                if cP <= self.cB[p]:
                    self.cB[p] = cP.copy()  

            self._progress_log()
            
            # Check stopping conditions
            if self._stopping_criteria():
                break
            
            # Update swarm topology
            if np.max(self.dF) >= 0.0:
                self.reinitialize_topology()
                
            # Find best particles in neighbourhood 
            self.find_neighbourhood_best()

        if not err_msg:        
            return self.best
        else:
            print('Error: ' + err_msg + ' OPTIMIZATION ABORTED\n')
            return
