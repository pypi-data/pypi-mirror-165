
#### CHALLENGE ######
https://vedexcel.com/how-to-calculate-binomial-distribution-in-python/
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binominal(Distribution):
    """ Binomial distribution class for calculating and  visualizing a Binomial distribution.
        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard deviation of the distribution
            data_list (list of floats) a list of floats to be extracted from the data file
            p (float) representing the probability of an event occurring        
    """
    
    def __init__(self, probabilitySuccess=0.5, numberTrials=20):
        self.p = probabilitySuccess
        self.n = numberTrials
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    def  calculate_mean(self):
        """Function to calculate the mean from p and n
        Args: 
            None
        Returns: 
            float: mean of the data set
        """
        self.mean = self.p * self.n
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.
        Args: 
            None
        Returns: 
            float: standard deviation of the data set
        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev
    
    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        Args: 
            None
        Returns: 
            float: the p value
            float: the n value
        """
        # data is opened in GeneralDistribution
        dataFromReadFile = self.data
        # CALCULATE n, p, mean and standard deviation from a data. N= Length of fiel data &  P =  the number of positive trials divided by the total trials
        # UPDATE n(number of trials is the length of the file read)
        # UPDATE p(successes outcomes)
        self.n = len(dataFromReadFile)
        self.p = 1.0 * sum(dataFromReadFile) / len(dataFromReadFile)
        
        # UPDATE mean and stdev attributes
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
    
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using matplotlib pyplot library.
        Args:
            None  
        Returns:
            None
        """
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')

    def pdf(self, numberOfSuccess):
        """Probability density function calculator for the binomial distribution.
        Args:
            r or numberOfSuccess (float): point for calculating the probability density function
        Returns:
            float: probability density function output
        """
        r= numberOfSuccess
        binomialCoeficient = math.factorial(self.n) / (math.factorial(r) * (math.factorial(self.n - r)))
        probabilitySuccessFailure = (self.p ** r) * (1 - self.p) ** (self.n - r)
        return binomialCoeficient * probabilitySuccessFailure

    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution
        Args:
            None
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot 
        """
        x = []
        y = []
        
        # calculate the x values to visualize # Hint: You'll need to use the pdf() method defined above to calculate the density function for every value of k.
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        # Be sure to label the bar chart with a title, x label and y label
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')
        plt.show()
        # This method should also return the x and y values used to make the chart
        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        Args:
            other (Binomial): Binomial instance
        Returns:
            Binomial: Binomial distribution  
        """
        try: #the try, except statement above will raise an exception if the p values are not equal
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n #The new n value is the sum of the n values of the two distributions
        result.p = self.p #When adding two binomial distributions, the p value remains the same
        result.calculate_mean() #what is the scope here ?
        result.calculate_stdev()  #what is the scope here ?
        return result

    def __repr__(self):                  
        """Function to output the characteristics of the Binomial instance
        Args:
            None
        Returns:
            string: characteristics of the Binomial object
        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
