class ARModel(object):
    def __init__(self, p, d):
        '''AR(p) model. d = state dimensionality'''
        self.p = p
        self.d = d
        self.cov = 1
        self.A = np.zeros((p, d, d))
        self.b = np.zeros(d)

    def fit(self, data):
        '''data: N x (p+1) x d
        N instances of (p+1)-windows of consecutive states'''
        if data.ndim == 2: data = data[None,:,:]
        assert data.shape[1:] == (self.p+1, self.d)
        N = data.shape[0]
        
        mat = np.zeros((self.d*N, self.d*self.d*self.p + self.d))
        rhs = np.zeros(self.d*N)
        for i in range(N):
            mat[self.d*i:self.d*(i+1),-self.d:] = np.eye(self.d)
            x_1_p = data[i,:self.p,:].ravel()
            for j in range(self.d):
                mat[self.d*i+j,self.d*self.p*j:self.d*self.p*(j+1)] = x_1_p
            rhs[self.d*i:self.d*(i+1)] = data[i,self.p,:]
        soln, residuals, rank, s = np.linalg.lstsq(mat, rhs)
        A_stacked = soln[:self.d*self.d*self.p].reshape((self.d, self.d*self.p))
        self.A = np.hsplit(A_stacked, self.p)
        self.b = soln[self.d*self.d*self.p:]

        # manually calculate residual for sanity
        #r = 0.
        #for i in range(N):
        #    y = self.b.copy()
        #    for j in range(self.p):
        #        y += self.A[j].dot(data[i,j,:])
        #    r += np.linalg.norm(data[i,self.p,:] - y)**2
        #print 'r', r

        self.cov = 1./N * residuals[0]
        assert len(self.b) == self.d

    def eval_log_likelihood(self, data):
        r = 0.
        for i in range(N):
            y = self.b.copy()
            for j in range(self.p):
                y += self.A[j].dot(data[i,j,:])
            r += np.linalg.norm(data[i,self.p,:] - y)**2
        return -1/2./self.cov*r - N/2.*(self.d*np.log(2.*np.pi) + np.log(self.cov))
