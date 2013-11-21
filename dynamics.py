import numpy as np

class ARModel(object):
    def __init__(self, p, d):
        '''AR(p) model. d = state dimensionality'''
        self.p = p
        self.d = d
        self.cov = 1
        self.A = np.zeros((p, d, d))
        self.b = np.zeros(d)

    def predict(self,point):
        y = self.b.copy()
        for j in range(self.p):
            y += self.A[j].dot(point[j,:])
        return y

    def fit(self, data):
        '''data: N x (p+1) x d
        N instances of (p+1)-windows of consecutive states'''
        d, p = self.d, self.p
        if data.ndim == 2: data = data[None,:,:]
        assert data.shape[1:] == (p+1, d)
        N = data.shape[0]
        
        mat = np.zeros((d*N, d*d*p + d))
        rhs = np.zeros(d*N)
        for i in range(N):
            mat[d*i:d*(i+1),-d:] = np.eye(d)
            x_1_p = data[i,:p,:].ravel()
            for j in range(d):
                mat[d*i+j,d*p*j:d*p*(j+1)] = x_1_p
            rhs[d*i:d*(i+1)] = data[i,p,:]
        soln, residuals, _, _ = np.linalg.lstsq(mat, rhs)
        A_stacked = soln[:d*d*p].reshape((d, d*p))
        self.A = np.hsplit(A_stacked, p)
        self.b = soln[d*d*p:]

        # manually calculate residual for sanity
        r = 0.
        for i in range(N):
            y = self.b.copy()
            for j in range(p):
                y += self.A[j].dot(data[i,j,:])
            r += np.linalg.norm(data[i,p,:] - y)**2
        print 'r', r

        self.cov = 1./N * residuals[0]
        assert len(self.b) == d

    def eval_log_likelihood(self, data):
        r = 0.
        for i in range(N):
            y = self.b.copy()
            for j in range(self.p):
                y += self.A[j].dot(data[i,j,:])
            r += np.linalg.norm(data[i,self.p,:] - y)**2
        return -1/2./self.cov*r - N/2.*(self.d*np.log(2.*np.pi) + np.log(self.cov))
