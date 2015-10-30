import numpy as np

# i'll be dumping coefficients here until i port the generator.
# coefficients via https://gist.github.com/notwa/3be345efb6c97d757398
# which is a port of http://ldesoras.free.fr/prod.html#src_hiir

halfband_c = {}

halfband_c['16,0.1'] = [
    # reject: roughly -155 dB
    0.006185967461045014,
    0.024499027624721819,
    0.054230780876613788,
    0.094283481125726432,
    0.143280861566087270,
    0.199699579426327684,
    0.262004358403954640,
    0.328772348316831664,
    0.398796973552973666,
    0.471167216679969414,
    0.545323651071132232,
    0.621096845120503893,
    0.698736833646440347,
    0.778944517099529166,
    0.862917812650502936,
    0.952428157718303137,
]

halfband_c['8,0.01'] = [
    # reject: -69 dB
    0.077115079832416222,
    0.265968526521094595,
    0.482070625061047198,
    0.665104153263495701,
    0.796820471331579738,
    0.884101508550615867,
    0.941251427774047134,
    0.982005414188607539,
]

halfband_c['olli'] = [
    # via http://yehar.com/blog/?p=368
    # "Transition bandwidth is 0.002 times the width of passband,
    #  stopband is attenuated down to -44 dB
    #  and passband ripple is 0.0002 dB."
    # roughly equivalent to ./halfband 8 0.0009074
    # reject: -44 dB
    0.4021921162426**2,
    0.6923878000000**2,
    0.8561710882420**2,
    0.9360654322959**2,
    0.9722909545651**2,
    0.9882295226860**2,
    0.9952884791278**2,
    0.9987488452737**2,
]

class Halfband:
    def __init__(self, c='olli'):
        self.x = np.zeros(4)

        if isinstance(c, str):
            c = halfband_c[c]
        self.c = np.asfarray(c)

        self.len = len(c)//2
        self.a2 = np.zeros(self.len)
        self.b2 = np.zeros(self.len)
        self.a1 = np.zeros(self.len)
        self.b1 = np.zeros(self.len)

    def process_halfband(self, xs):
        real, imag = self.process_all(xs, mode='filter')
        return (real + imag)*0.5

    def process_power(self, xs):
        real, imag = self.process_all(xs, mode='hilbert')
        return np.sqrt(real**2 + imag**2)

    def process_all(self, xs, mode='hilbert'):
        self.__init__()
        real = np.zeros(len(xs))
        imag = np.zeros(len(xs))
        for i, x in enumerate(xs):
            real[i], imag[i] = self.process(x, mode=mode)
        return real, imag

    def process(self, x0, mode='hilbert'):
        a = np.zeros(self.len)
        b = np.zeros(self.len)
        self.x[0] = x0

        sign = 1
        if mode == 'hilbert':
            #y[n] = c*(x[n] + y[n-2]) - x[n-2]
            pass
        elif mode == 'filter':
            #y[n] = c*(x[n] - y[n-2]) + x[n-2]
            sign = -1

        in2 = self.x[2]
        in0 = self.x[0]
        for i in range(self.len):
            in0 = a[i] = self.c[i*2+0]*(in0 + sign*self.a2[i]) - sign*in2
            in2 = self.a2[i]

        in2 = self.x[3]
        in0 = self.x[1]
        for i in range(self.len):
            in0 = b[i] = self.c[i*2+1]*(in0 + sign*self.b2[i]) - sign*in2
            in2 = self.b2[i]

        self.x[3] = self.x[2]
        self.x[2] = self.x[1]
        self.x[1] = self.x[0]

        self.a2, self.a1 = self.a1, a
        self.b2, self.b1 = self.b1, b

        return a[-1], b[-1]
