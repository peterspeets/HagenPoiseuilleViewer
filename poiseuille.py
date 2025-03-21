import numpy as np
import h5py

def calculatePressureGradient(q,h,l, mu=1.002e-3, maxn = 64, maxCoshArgument = 500):
    """
    q:  Total discharde in ul/min
    h: height of the channel in mm
    l: width of the channel in mm
    mu: viscosity in Pa s
    maxn: maximum number of terms
    maxCoshArgument: overrides largest nmax when the argument 
        of the cosh becomes too large to be stable
    """

    nmaxCosh = 0.5*maxCoshArgument * h/(l*np.pi) + 0.5
    if(nmaxCosh < maxn):
        maxn = int(nmaxCosh)

        
    beta = lambda n: (2*n-1)*np.pi/h
    sumBeta = np.sum([(1/((2*n-1)**5)
                       *(np.cosh(beta(n)*l)-1)
                       /(np.sinh(beta(n)*l)))
                      for n in range(1,maxn)])
    if(np.isnan(sumBeta)):
        sumBetaList = np.array( [(1/((2*n-1)**5)
                       *(np.cosh(beta(n)*l)-1)
                       /(np.sinh(beta(n)*l)))
                      for n in range(1,maxn)])
        isnan = np.isnan(sumBetaList)
        if(np.any(isnan)):
            cutoffindex = np.where(isnan)[0][0]
            sumBeta = np.sum(sumBetaList[:cutoffindex])
    
    
    factor = (h**3)*l/(12*mu)-(16*h**4)*sumBeta/(np.pi**5*mu)
    return q/factor

def calculateVelocityProfileAtPoint(y,z,l,h,G, minn, maxn,tolerance,mu=1.002e-3):  
    """
    y: y coordinate in mm
    z: z coordinate in mm
    l: width in mm
    h: height in mm
    maxn: maximum number of terms
    G: calculate with calculatePressureGradient
    tolerance: when the distance between each beta term becomes too small, 
        ignore maxn, and stop calculation
    mu: viscosity in  Pa s
    """    
    f = lambda n: (1/((2*n-1)**3)
                     *np.sin(((2*n-1)*np.pi/l)*(y + 0.5*l))
                     *(np.sinh(((2*n-1)*np.pi/l)*(z + 0.5*h)) + np.sinh(((2*n-1)*np.pi/l)*(h-(z + 0.5*h))))
                     /(np.sinh(((2*n-1)*np.pi/l)*h)))

    betaSum = 0.0
    for n in range(1,maxn):
        newf = f(n)
        betaSum += newf
        if(n > minn and np.abs(newf) < tolerance):
            break
            
    return G/(2*mu)*(y + 0.5*l)*(l-(y + 0.5*l)) - (4*G*l**2/(mu*np.pi**3))*betaSum


def calculateVelocityProfile(y,z,l,h,q, mu=1.002e-3, minn = 128,maxn = 1024, unitq = 'ul/min',
                             maxCoshArgument =500, tolerance = 1e-12, G = None):
    
    """
    y: y coordinate in mm
    z: z coordinate in mm
    l: width in mm
    h: height in mm
    q:  Total discharde in ul/min
    mu: viscosity in  Pa s
    minn: minimum number of terms. Sometimes, two consequetive terms
        can be too close to each other, ending the calculaton prematurely
    maxn: maximum number of terms
    unitq: unit of  discharge
    tolerance: when the distance between each beta term becomes too small, 
        ignore maxn, and stop calculation
    G: calculated with calculatePressureGradient
    """        
    if(unitq == 'ul/min'):
        #q *= 1e-9/60.0 # when xx and zz are in metres
        q /=60.0 #when xx and zz are min milimetres.    

    if(G is None):
        G = calculatePressureGradient(q,l,h, mu=mu,maxn=maxn,maxCoshArgument = maxCoshArgument)


    z = np.array(z)
    y = np.array(y)
    
    nmaxCosh = 0.5*maxCoshArgument * l/(h*np.pi) + 0.5
    if(nmaxCosh < maxn):
        maxn = int(nmaxCosh) 
        
    try:
        iter(z)
    except:
        try:
            iter(y)
            vprofile = np.empty(len(y))
            for i, y_ in enumerate(y):
                vprofile[i] = calculateVelocityProfileAtPoint(y_,z,l,h,G,minn, maxn,tolerance,mu=mu)
            return vprofile
        except:
            return calculateVelocityProfileAtPoint(y,z,l,h,G,minn, maxn,tolerance,mu=mu)        
        
        
    try:
        iter(y)
        if( len(y.shape)==1 ):
        
            vprofile = np.empty(len(y))
            for i, y_ in enumerate(y):
                vprofile[i] = calculateVelocityProfileAtPoint(y[i],z[i],l,h, G,minn,maxn,tolerance,mu=mu)        
            return vprofile
        else:
            vprofile = np.ones(y.shape)
            for i, y_ in enumerate(y):
                for j, z_ in enumerate(z[0]):
                    vprofile[i][j] = calculateVelocityProfileAtPoint(y[i,j],z[i,j],l,h, G,minn,maxn,tolerance,mu=mu)
            return vprofile
            
    except:
        vprofile = np.empty(len(z))
        for i, z_ in enumerate(z):
            vprofile[i] = calculateVelocityProfileAtPoint(y,z_,l,h,G,minn, maxn,tolerance,mu=mu)        
        return vprofile 

    

class PoiseuilleCalculator():

    def __init__(self,window):
        self.window = window
    
        self.loadFromSettings()
        self.calculateYProfile()
        self.calculateZProfile()
        self.loadCrossSectionLUT()
        self.calculateCrossSectionFromLUT()
        #self.calculateYZCrossSection()  turned off in favour of a LUT approach. Calculating this can be slow.
        
        
        
    def loadFromSettings(self):
        self.h = self.window.settings.channelHeight
        self.w = self.window.settings.channelWidth
        self.flowRate = self.window.settings.flowRate
        self.Ny = self.window.settings.Ny
        self.Nz = self.window.settings.Nz
        self.maxCoshArgument = self.window.settings.maxCoshArgument
        self.viscosity = self.window.settings.viscosity
        
        self.y = np.linspace(-0.5*self.w,0.5*self.w, self.window.settings.Ny)
        self.z = np.linspace(-0.5*self.h,0.5*self.h, self.window.settings.Nz)
        self.z0 = self.window.settings.z0
        self.y0 = self.window.settings.y0
        self.errorTolerance = self.window.settings.errorTolerance
        
        self.minN = self.window.settings.minimumSummationCutoff
        self.maxN = self.window.settings.maximumSummationCutoff
        

    def loadCrossSectionLUT(self):
        self.flowProfileLUT = {}
        with h5py.File(self.window.settings.pathToLUT, "r") as f:  
            self.aspectRatios = []
            for key in f.keys():
                
                aspectRatio = f[key]['aspectRatio'][...].item()
                self.aspectRatios.append(aspectRatio)
                flowProfile = f[key]['flowProfile'][...]
                self.flowProfileLUT[aspectRatio] = flowProfile
                
        self.aspectRatios = np.array(self.aspectRatios )

                
    def calculateCrossSectionFromLUT(self):
        h = self.window.settings.channelHeight
        w = self.window.settings.channelWidth

        aspectRatio = np.amax([h,w])/np.amin([h,w])
        


        if(aspectRatio in self.aspectRatios):
            profile = self.flowProfileLUT[aspectRatio]
        else:
            differences = np.abs(self.aspectRatios - aspectRatio)
            indices = np.argsort(differences)[:2]
            weight1_ = np.abs(self.aspectRatios[indices[0]] - aspectRatio)
            weight2_ = np.abs(self.aspectRatios[indices[1]] - aspectRatio)
            weight1 = weight1_/(weight1_ + weight2_)
            weight2 = weight2_/(weight1_ + weight2_)

            profile = weight1*self.flowProfileLUT[self.aspectRatios[indices[0]]] + weight2*self.flowProfileLUT[self.aspectRatios[indices[1]]]
            if(w < h):
                profile = np.transpose(profile)
        self.calculateYZCrossSection = profile

        
        

    def calculateYProfile(self):
        self.yProfile = calculateVelocityProfile(self.y,self.z0,self.w,self.h,self.flowRate, mu=self.viscosity, minn = self.minN,maxn = self.maxN, unitq = 'ul/min',
                             maxCoshArgument =self.maxCoshArgument, tolerance = self.errorTolerance, G = None)
    
    
    
    def calculateZProfile(self):
        self.zProfile = calculateVelocityProfile(self.y0,self.z,self.w,self.h,self.flowRate, mu=self.viscosity, minn = self.minN,maxn = self.maxN, unitq = 'ul/min',
                         maxCoshArgument =self.maxCoshArgument, tolerance = self.errorTolerance, G = None)
    
    
    def calculateYZCrossSection(self):
        yy, zz = np.meshgrid(self.y,self.z)
        self.flowCrossSection = calculateVelocityProfile(yy,zz,self.w,self.h,self.flowRate, mu=self.viscosity, minn = self.minN,maxn = self.maxN, unitq = 'ul/min',
                         maxCoshArgument =self.maxCoshArgument, tolerance = self.errorTolerance, G = None)
    
    
    