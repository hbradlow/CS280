import dynamics
import numpy as np

def isotropic_mvn_densities(x_nd, m_kd, cov):
    """
    Given an array of N D-dimensional points, K means, and a single float representing the covariance matrix cov*eye(D),
      returns a NxK array of Gaussian densities
    """
    m_kd = np.atleast_2d(m_kd)
    n, k, d = x_nd.shape[0], m_kd.shape[0], m_kd.shape[1]
    assert x_nd.shape[1] == d

    diffs = (x_nd[:,None,:] - m_kd[None,:,:]).reshape((-1, d))
    out = np.exp(-.5/cov * (diffs*diffs).sum(axis=-1))
    out /= np.power(2.*np.pi*cov, d/2.)
    return out.reshape((n, k)).squeeze()

def generate(N=100):
    mean = np.array([.04,.2])
    s = .01
    cov = s * np.eye(2)
    pnoise = .1

    pts = np.empty((N, 2))
    for i in range(N):
        if np.random.rand(1) < pnoise:
            p = np.random.rand(2)*2 - 1
        else:
            p = np.random.multivariate_normal(mean, cov)
        pts[i,:] = p
    return pts


class Tracker(object):
    def __init__(self, mean_x_prior, var_x, var_z, noise_density, noise_prob):
        self.var_x = var_x
        self.mean_x_prior = mean_x_prior
        self.var_z = var_z
        self.noise_density = noise_density
        self.noise_prob = noise_prob

    def set_observations(self, obs):
        self.zs = obs

    def run_em(self, init_x=np.zeros(2)):
        curr_x = init_x
        x_history = [curr_x]
        obj_val_history = []

        steps = 5
        for i in range(steps):
            # e step
            Z = isotropic_mvn_densities(self.zs, curr_x, self.var_z)*self.noise_prob
            rs = Z / (Z + self.noise_density*(1. - self.noise_prob))
            # m step
            new_x = (self.var_z*self.mean_x_prior + self.var_x*(rs[:,None] * self.zs).sum(axis=0)) / (self.var_z + self.var_x*rs.sum())

            # for debugging: compute objective value
            obj_val = np.linalg.norm(new_x - self.mean_x_prior)**2/self.var_x
            for k in range(self.zs.shape[0]):
                obj_val += rs[k]/self.var_z * np.linalg.norm(self.zs[k] - new_x)**2
            obj_val_history.append(obj_val)

            x_history.append(new_x)
            curr_x = new_x

        return curr_x, x_history, obj_val_history


def test_tracker():
    tracker = Tracker(mean_x_prior=np.array([10,10]), var_x=100000, var_z=.01, noise_density=1, noise_prob=.1)
    pts = generate(100)
    tracker.set_observations(pts)
    curr_x, x_history, obj_val_history = tracker.run_em(init_x=np.array([0,0]))
    print 'result', curr_x
    print x_history
    import matplotlib.pyplot as plt
    plt.plot(obj_val_history)
    plt.show()

if __name__ == '__main__':
    test_tracker()
