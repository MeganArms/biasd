# import matplotlib.pyplot as plt
import numpy as _np
_np.seterr(all="ignore")
from scipy import special as _special

class _distribution(object):
	"""
	Parameters should already have been checked.
	PDF/PMF should check support
	"""
	
	__minimum__ = 0.
	__small__ = 1e-4
	
	def __init__(self,parameters,label_parameters,lnpdf,mean,variance,rvs,okay):
		self._lnpdf_fxn = lnpdf
		self.parameters = parameters
		self.label_parameter = label_parameters
		self.support_parameters = self.support_parameters
		self.support = support
		self._mean = mean
		self._variance = variance
		# self._moment2param_fxn = moment2param
		self._rvs_fxn = rvs
		self.okay = okay

	def check_params(self):
		self.okay = True
		for i,r in zip(self.parameters,self.support_parameters):
			if i <= r[0] or i >= r[1]:
				self.okay = False
				
	def pdf(self,x):
		"""
		Returns the probability distribution/mass function
		"""
		if self.okay:
			return _np.exp(self._lnpdf_fxn(x,self.parameters,self.support))
	def lnpdf(self,x):
		"""
		Returns the natural log of the probability distribution/mass function
		"""
		if self.okay:
			return self._lnpdf_fxn(x,self.parameters,self.support)
	def rvs(self,size):
		"""
		Returns random variates in the shape of size (tuple)
		"""
		if self.okay:
			return self._rvs_fxn(size,self.parameters)
			
	def mean(self):
		"""
		First Moment
		"""
		if self.okay:
			return self._mean(self.parameters)
	def variance(self):
		"""
		Second moment - square of first moment:
		E[x^2] - E[x]^2
		"""
		if self.okay:
			return self._variance(self.parameters)
	def mode(self):
		"""
		Mode
		"""
		if self.okay:
			return self._mode(self.parameters)
	
	def get_xlim(self):
		if self.okay:
			return self._get_xlim(self.parameters)
	
	def get_ranged_x(self,n):
		"""
		Returns an array of n datapoints that covers most of the PDF mass
		"""
		if self.okay:
			return self._get_ranged_x(self.parameters,n)

class beta(_distribution):
	"""
	Parameters are alpha, and beta
	"""
	def __init__(self,alpha,beta):
		self.name = 'beta'
		# initial loading/defining parameters
		self.parameters = _np.array((alpha,beta),dtype='f')
		self.support_parameters = _np.array(((_distribution.__minimum__, _np.inf), (_distribution.__minimum__, _np.inf)))
		self.support = _np.array((_distribution.__minimum__, 1.-_distribution.__minimum__))

		self.label_parameters = [r"$\alpha$",r"$\beta$"]
		self.check_params()
	
	@staticmethod
	def new(parameters):
		return beta(*parameters)
		
	# normal-specific things
	@staticmethod
	def _mean(parameters):
		return parameters[0]/(parameters[0]+parameters[1])
	
	@staticmethod
	def _variance(parameters):
		a,b = parameters
		return a*b/((a*b)**2.*(a+b+1.))
	
	@staticmethod
	def _mode(parameters):
		a,b = parameters
		if a > 1. and b > 1.:
			return (a-1.)/(a+b-2.)
		else:
			return _np.nan
	
	@staticmethod
	def _lnpdf_fxn(x,parameters,support):
		a,b = parameters
		if isinstance(x,_np.ndarray):
			keep = (x >= support[0])*(x<=support[1])
			y = (a-1.)*_np.log(x)+(b-1.)*_np.log(1.-x) - _special.betaln(a,b)
			y[_np.nonzero(~keep)] = -_np.inf
		else:
			keep = (x >= support[0])*(x<=support[1])
			if keep:
				y = (a-1.)*_np.log(x)+(b-1.)*_np.log(1.-x) - _special.betaln(a,b)
			else:
				y = -_np.inf
		return y
	
	@staticmethod
	def _rvs_fxn(size,parameters):
		a,b = parameters
		return _np.random.beta(a,b,size=size)
		
	@staticmethod
	def _moment2param_fxn(first,second):
		variance = second - first**2.
		alpha = first*(first*(1.-first)/variance-1.)
		beta = (1.-first)*(first*(1.-first)/variance-1.)
		return _np.array([alpha,beta])
	
	@staticmethod
	def _get_xlim(parameters):
		l = _special.betaincinv(parameters[0],parameters[1],_distribution.__small__)
		h = _special.betaincinv(parameters[0],parameters[1],1.-_distribution.__small__)
		return _np.array((l,h))
		
	@staticmethod
	def _get_ranged_x(parameters,n):
		l,h = beta._get_xlim(parameters)
		return _np.linspace(l,h,int(n))

class gamma(_distribution):
	"""
	Parameters are alpha (shape), and beta (rate)
	"""
	def __init__(self,alpha,beta):
		self.name = 'gamma'
		# initial loading/defining parameters
		self.parameters = _np.array((alpha,beta),dtype='f')
		self.support_parameters = _np.array(((_distribution.__minimum__,_np.inf), (_distribution.__minimum__,_np.inf)))
		self.support = _np.array((_distribution.__minimum__, _np.inf))

		self.label_parameters = [r"$\alpha$",r"$\beta$"]
		self.check_params()
	
	@staticmethod
	def new(parameters):
		return gamma(*parameters)
	
	# normal-specific things
	@staticmethod
	def _mean(parameters):
		return parameters[0]/parameters[1]
	
	@staticmethod
	def _variance(parameters):
		return parameters[0]/(parameters[1]**2.)
	
	@staticmethod
	def _mode(parameters):
		a,b = parameters
		if a >= 1.:
			return (a-1.)/b
		else:
			return _np.nan
	
	@staticmethod
	def _lnpdf_fxn(x,parameters,support):
		a,b = parameters
		if isinstance(x,_np.ndarray):
			keep = (x >= support[0])*(x<=support[1])
			y = a*_np.log(b)+(a-1.)*_np.log(x)-b*x-_special.gammaln(a)
			y[_np.nonzero(~keep)] = -_np.inf
		else:
			keep = (x >= support[0])*(x<=support[1])
			if keep:
				y = a*_np.log(b)+(a-1.)*_np.log(x)-b*x-_special.gammaln(a)
			else:
				y = -_np.inf
		return y
	
	@staticmethod
	def _rvs_fxn(size,parameters):
		a,b = parameters
		return _np.random.gamma(shape=a,scale=1./b,size=size)
		
	@staticmethod
	def _moment2param_fxn(first,second):
		variance = second - first**2.
		alpha = first*first/variance
		beta = first/variance
		return _np.array([alpha,beta])

	@staticmethod
	def _get_xlim(parameters):
		l = _special.gammaincinv(parameters[0],_distribution.__small__)/parameters[1]
		h = _special.gammaincinv(parameters[0],1.-_distribution.__small__)/parameters[1]
		return _np.array((l,h))

	@staticmethod
	def _get_ranged_x(parameters,n):
		l,h = gamma._get_xlim(parameters)
		return _np.linspace(l,h,int(n))

class normal(_distribution):
	"""
	Parameters are mean, and the standard deviation
	"""
	def __init__(self,mu,sigma):
		self.name = 'normal'
		# initial loading/defining parameters
		self.parameters = _np.array((mu,sigma),dtype='f')
		self.support_parameters = _np.array(((-_np.inf,_np.inf), (_distribution.__minimum__,_np.inf)))
		self.support = _np.array((-_np.inf, _np.inf))

		self.label_parameters = [r"$\mu$",r"$\sigma$"]
		self.check_params()
	
	@staticmethod
	def new(parameters):
		return normal(*parameters)
	
	# normal-specific things
	@staticmethod
	def _mean(parameters):
		return parameters[0]
	
	@staticmethod
	def _variance(parameters):
		return parameters[1]**2.
	
	@staticmethod
	def _mode(parameters):
		return parameters[0]
	
	@staticmethod
	def _lnpdf_fxn(x,parameters,support):
		mu,sigma = parameters
		if isinstance(x,_np.ndarray):
			keep = (x >= support[0])*(x<=support[1])
			y = -.5*_np.log(2.*_np.pi)-_np.log(sigma) - .5 * ((x-mu)/sigma)**2.
			y[_np.nonzero(~keep)] = -_np.inf
		else:
			keep = (x >= support[0])*(x<=support[1])
			if keep:
				y = -.5*_np.log(2.*_np.pi)-_np.log(sigma) - .5 * ((x-mu)/sigma)**2.
			else:
				y = -_np.inf
		return y
	
	@staticmethod
	def _rvs_fxn(size,parameters):
		mu,sigma = parameters
		return _np.random.normal(loc=mu,scale=sigma,size=size)
		
	@staticmethod
	def _moment2param_fxn(first,second):
		variance = second - first**2.
		mu = first
		sigma = _np.sqrt(variance)
		return _np.array([mu,sigma])
	
	@staticmethod
	def _get_xlim(parameters):
		l = parameters[0] + parameters[1]*_np.sqrt(2.)*_special.erfinv(2.*(_distribution.__small__)-1.)
		h = parameters[0] + parameters[1]*_np.sqrt(2.)*_special.erfinv(2.*(1.-_distribution.__small__)-1.)
		return _np.array((l,h))
	
	@staticmethod
	def _get_ranged_x(parameters,n):
		l,h = normal._get_xlim(parameters)
		return _np.linspace(l,h,int(n))

class uniform(_distribution):
	"""
	Parameters are a,b
	"""
	def __init__(self,a,b):
		self.name = 'uniform'
		# initial loading/defining parameters
		self.parameters = _np.array((a,b),dtype='f')
		self.support_parameters = _np.array(((-_np.inf,b), (a,_np.inf)))
		self.support = _np.array((a,b))

		self.label_parameters = [r"$a$",r"$b$"]
		self.check_params()
	
	@staticmethod
	def new(parameters):
		return uniform(*parameters)
		
	# normal-specific things
	@staticmethod
	def _mean(parameters):
		return .5 *(parameters[0]+parameters[1])
	
	@staticmethod
	def _variance(parameters):
		a,b = parameters
		return 1./12. *(b-a)**2.
	
	@staticmethod
	def _mode(parameters):
		# not really correct, but w/e... you gotta pick something
		return uniform._mean(parameters)
	
	@staticmethod
	def _lnpdf_fxn(x,parameters,support):
		a,b = parameters
		if isinstance(x,_np.ndarray):
			keep = (x >= support[0])*(x<=support[1])
			y = -_np.log(b-a)*keep
			if _np.any(~keep):
				y[_np.nonzero(~keep)] = -_np.inf
		else:
			keep = (x >= support[0])*(x<=support[1])
			if keep:
				y = -_np.log(b-a)
			else:
				y = -_np.inf
		return y
	
	@staticmethod
	def _rvs_fxn(size,parameters):
		a,b = parameters
		return _np.random.uniform(a,b+_distribution.__minimum__,size=size)
		
	@staticmethod
	def _moment2param_fxn(first,second):
		variance = second - first**2.
		a = first - _np.sqrt(3.*variance)
		b = first + _np.sqrt(3.*variance)
		return _np.array([a,b])
	
	@staticmethod
	def _get_xlim(parameters):
		return parameters
	
	@staticmethod
	def _get_ranged_x(parameters,n):
		return _np.linspace(parameters[0],parameters[1],int(n))

def convert_distribution(this,to_this_type_string):
	""" 
	this is a _distribution
	to_this_type_string is 'beta', 'gamma', 'normal', or 'uniform'
	------------------
	FUN!:
	import biasd_distributions
	n = biasd_distributions.normal(.5,.01)
	x = _np.linspace(0,1,10000)
	c = biasd_distributions.convert_distribution(n,'gamma')
	cc = biasd_distributions.convert_distribution(n,'uniform')
	ccc = biasd_distributions.convert_distribution(n,'beta')
	plt.plot(x,n.pdf(x))
	plt.plot(x,c.pdf(x))
	plt.plot(x,cc.pdf(x))
	plt.plot(x,ccc.pdf(x))
	plt.yscale('log')
	plt.show()
	-------------------
	"""
	
	to_this_type = dict(zip(('beta','gamma','normal','uniform'),(beta,gamma,normal,uniform)))[to_this_type_string]
	
	params = to_this_type._moment2param_fxn(this.mean(), this.variance()+this.mean()**2.)
	
	return to_this_type(*params)
	

class parameter_collection(object):
	def __init__(self,e1,e2,sigma,k1,k2):
		self.e1 = e1
		self.e2 = e2
		self.sigma = sigma
		self.k1 = k1
		self.k2 = k2
		self.labels = [r'$\epsilon_1$', r'$\epsilon_2$', r'$\sigma$', r'$k_1$', r'$k_2$']
		
		self.okay = self.check_dists()
	
	def check_dists(self):
		self.okay = True
		for d,dname in zip([self.e1,self.e2,self.sigma,self.k1,self.k2], ('e1','e2','sigma','k1','k2')):
			if isinstance(d,_distribution):
				if not d.okay:
					self.okay = False
					raise ValueError('The prior for '+dname+' is malformed. Check the parameters values.')
			else:
				self.okay = False
				raise ValueError('The prior for '+dname+' is not a _distribution.')
		
	def rvs(self,n=1):
		# if self.okay and isinstance(n,int):
			rout = _np.zeros((5,n))
			rout[0] = self.e1.rvs(n)
			rout[1] = self.e2.rvs(n)
			rout[2] = self.sigma.rvs(n)
			rout[3] = self.k1.rvs(n)
			rout[4] = self.k2.rvs(n)
			return rout
	
	def lnpdf(self,theta):
		e1,e2,sigma,k1,k2 = theta
		# if self.okay:
		return self.e1.lnpdf(e1) + self.e2.lnpdf(e2) + self.sigma.lnpdf(sigma) + self.k1.lnpdf(k1) + self.k2.lnpdf(k2)
		
	def mean(self):
		return _np.array((self.e1.mean(),self.e2.mean(),self.sigma.mean(),self.k1.mean(),self.k2.mean()))
		
	def mode(self):
		return _np.array((self.e1.mode(),self.e2.mode(),self.sigma.mode(),self.k1.mode(),self.k2.mode()))
	def variance(self):
		return _np.array((self.e1.variance(),self.e2.variance(),self.sigma.variance(),self.k1.variance(),self.k2.variance()))
		
	def format_for_smd(self):
		names = [d.name for d in [self.e1,self.e2,self.sigma,self.k1,self.k2]]
		params = [d.parameters.tolist() for d in [self.e1,self.e2,self.sigma,self.k1,self.k2]]
		return names,params

	@staticmethod
	def new_from_smd(names,parameters):
		dist_dict = {'beta':beta, 'gamma':gamma, 'normal':normal, 'uniform':uniform}
		p = [dist_dict[name](*params) for name,params in zip(names,parameters)]
		return parameter_collection(*p)
		
class viewer(object):
	"""
	Allows you to view BIASD parameter probability distributions
	------------
	Example:
	
	import biasd_distributions as bd

	e1 = bd.normal(5.,1.)
	e2 = bd.beta(95.,5.)
	sigma = bd.gamma(5.,100.)
	k1 = bd.gamma(1.,1.)
	k2 = bd.uniform(-1,1.)
	d = bd.parameter_collection(e1,e2,sigma,k1,k2)
	v = bd.viewer(d)
	"""
	import matplotlib.pyplot as plt
	class mpl_button(object):
		from matplotlib.widgets import Button
		def __init__(self,identity,name,x_loc,y_loc,viewer):
			self.height = .1
			self.width = .2
			self.ax = viewer.plt.axes([x_loc,y_loc,self.width,self.height])
			self.identity = identity
			self.name = name
			self.button = self.Button(self.ax,name)
			self.viewer = viewer
			self.button.on_clicked(self.clicked)
		def clicked(self,event):
			if self.identity != self.viewer.selected:
				self.viewer.deselect()
				self.viewer.select(self.identity)

	def __init__(self,data):
		if not isinstance(data,parameter_collection):
			raise ValueError('This is not a valid parameter collection')
		else:
			self.data = data
			self.f = viewer.plt.figure("Parameter Probability Distribution Function Viewer", 				figsize=(8,6))
			self.e1 = self.mpl_button("e1",r"$\varepsilon_1$",0.0,0.9,self)
			self.e2 = self.mpl_button("e2",r"$\varepsilon_2$",0.2,0.9,self)
			self.sigma = self.mpl_button("sigma",r"$\sigma$",0.4,0.9,self)
			self.k1 = self.mpl_button("k1",r"$k_1$",0.6,0.9,self)
			self.k2 = self.mpl_button("k2",r"$k_2$",0.8,0.9,self)
			
			self.colors = dict(zip(['e1','e2','sigma','k1','k2'], 				['purple','yellow','green','cyan','orange']))
			self.xlabels = dict(zip(['e1','e2','sigma','k1','k2'], 				['Signal','Signal','Signal Noise',r'Rate Constant (s$^{-1}$)',r'Rate Constant (s$^{-1}$)']))
			
			self.ax = viewer.plt.axes([.1,.1,.8,.7])
			self.ax.set_yticks((),())
			self.ax.set_ylabel('Probability',fontsize=18,labelpad=15)
			self.line = self.ax.plot((0,0),(0,0),color=self.colors['e1'],lw=1.5)[0]
			self.fill = self.ax.fill_between((0,0),(0,0),color='white')
			self.select("e1")
			viewer.plt.show()
			
	def deselect(self):
		self.__dict__[self.selected].ax.set_axis_bgcolor('lightgrey')
		viewer.plt.draw()
		self.selected = None

	def select(self,identity):
		self.__dict__[identity].ax.set_axis_bgcolor('lightblue')
		self.selected = identity
		self.update_plot()
		
	def update_plot(self):
		dist = self.data.__dict__[self.selected]
		distx = dist.get_ranged_x(1001)
		disty = dist.pdf(distx)
		
		self.line.set_xdata(distx)
		self.line.set_ydata(disty)
		self.line.set_color('k')
		# self.line.set_color(self.colors[self.selected])
		
		for collection in (self.ax.collections):
			self.ax.collections.remove(collection)
		self.ax.fill_between(distx,disty,color=self.colors[self.selected], 			alpha=0.75)
		
		if isinstance(dist,beta):
			self.ax.set_xlim(0,1)
		elif isinstance(dist,gamma):
			self.ax.set_xlim(0,distx[-1])
		else:
			self.ax.set_xlim(distx[0],distx[-1])
		self.ax.set_ylim(0.,disty.max()*1.2)
		self.ax.set_xlabel(self.xlabels[self.selected],fontsize=18)
		self.ax.set_title(dist.label_parameters[0]+": "+str(dist.parameters[0])+", "+dist.label_parameters[1]+": "+str(dist.parameters[1])+r", $E[x] = $"+str(dist.mean()))
		self.f.canvas.draw_idle()
		
def uninformative_prior(data_range,timescale):
	"""
	data_range should be the [lower,upper] bounds of the data
	timescale is the framerate (the prior will be centered here)
	"""
	lower,upper = data_range
	e1 = bd.uniform(lower,(upper-lower)/2.+lower)
	e2 = bd.uniform((upper-lower)/2.+lower,upper)
	sigma = bd.gamma(1,1./((upper-lower)/10.))
	k1 = bd.gamma(1.,timescale)
	k2 = bd.gamma(1.,timescale)
	return bd.parameter_collection(e1,e2,sigma,k1,k2)
	
#### Guess Priors
class _results_gmm(object):
	def __init__(self,nstates,pi,r,mu,var,ll):
		self.nstates = nstates
		self.pi = pi
		self.r = r
		self.mu = mu
		self.var = var
		self.ll = -_np.inf
		self.ll_last = -_np.inf
	
	def sort(self):
		xsort = _np.argsort(self.mu)
		self.pi = self.pi[xsort]
		self.r = self.r[:,xsort]
		self.var = self.var[xsort]
		self.mu = self.mu[xsort]
		
		

def _GMM_EM_1D(x,k=2,maxiter=1000,relative_threshold=1e-6):

	# Make sure x is proper
	if not isinstance(x,_np.ndarray) or x.ndim != 1:
		raise ValueError('Input is not really a 1D ndarray, is it?')
		return None
	
	def Nk_gaussian(x,mu,var):
		return 1./_np.sqrt(2.*_np.pi*var[None,:]) * _np.exp(-.5/var[None,:]*(x[:,None] - mu[None,:])**2.)
		
	# Initialize
	mu_k = x[_np.random.randint(0,x.size,size=k)] # Pick random mu_k
	var_k = _np.repeat(_np.var(x),k)
	pi_k = _np.repeat(1./k,k)
	theta = _results_gmm(k,pi_k,None,mu_k,var_k,None)
	
	iteration = 0
	while iteration < maxiter:
		# E step
		r = theta.pi[None,:]*Nk_gaussian(x,theta.mu,theta.var)
		theta.r = r/(r.sum(1)[:,None])
		
		# M step
		n = _np.sum(theta.r,axis=0)
		theta.mu = 1./n * _np.sum(theta.r*x[:,None],axis=0)
		theta.var= 1./n * _np.sum(theta.r *(x[:,None]-theta.mu[None,:])**2.,axis=0)
		theta.pi = n / n.sum()
		
		# Compute log-likelihood
		theta.ll_last = theta.ll
		theta.ll = _np.sum(_np.log(_np.sum(theta.pi[None,:] * Nk_gaussian(x,theta.mu,theta.var),axis=-1)))

		# Check convergence
		if _np.abs((theta.ll - theta.ll_last)/theta.ll_last) < relative_threshold:
			break
		iteration += 1
	theta.sort()
	return theta

def _virtual_min(k1,k2,tau_c):
	"""
	Correct reversible two-state rate constants using virtual states.

	k1, k2 are rate constants.
	tau_c is the cutoff time, i.e. ~ measurement period / 2

	returns _np.array((k1_corr,k2_corr))
	"""
	def minfxn(kc,ko1,ko2,tc):
		y1 = kc[0] - ko1 - (1.-_np.exp(-kc[1]*tc))*kc[0]
		y2 = kc[1] - ko2 - (1.-_np.exp(-kc[0]*tc))*kc[1]
		f = (y1/kc[0])**2. + (y2/kc[1])**2.
		return f
		
	from scipy.optimize import minimize
	
	kc = minimize(lambda ks: minfxn(ks,k1,k2,tau_c),x0=_np.array((k1,k2)),method='Nelder-Mead')
	
	if kc.success:
		return _np.array(kc.x)
	else:
		return None

def guess_prior(y,tau=1.):
	"""
	Use a GMM to learn both states and noise.
	Idealize and calculate transition probabilities.
	Calculate rate constants, and try to correct these with virtual states.
	"""
	
	
	theta = _GMM_EM_1D(y)

	# Signal
	m1,m2 = theta.mu
	s1 = _np.min(theta.var**.5)
	s2 = s1

	# Noise
	a = 3.
	b = 3./s1

	# Rate constants
	r = theta.r.argmax(1)
	s = _np.roll(r,-1)
	counts = _np.zeros((2,2))
	for i in range(r.size-1):
		counts[r[i],s[i]] += 1
	p12 = (1.+counts[0,1]) / (2.+ counts[0].sum())
	p21 = (1.+counts[1,0]) / (2.+ counts[1].sum())
	k12 = -_np.log(1.-p12)/tau
	k21 = -_np.log(1.-p21)/tau
	
	kcorr = _virtual_min(k12,k21,tau/2.)
	if not kcorr is None:
		k12,k21 = kcorr
	
	a1 = 2.
	b1 = 2./k12
	a2 = 2.
	b2 = 2./k21
	
	e1 = normal(m1,s1)
	e2 = normal(m2,s2)
	sigma = gamma(a,b)
	k1 = gamma(a1,b1)
	k2 = gamma(a2,b2)
	return parameter_collection(e1,e2,sigma,k1,k2)