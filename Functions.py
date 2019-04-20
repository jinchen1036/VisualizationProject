import seaborn as sns
import matplotlib.pyplot as plt
import pandas
from scipy.stats import ttest_1samp, wilcoxon


def plot_correlation(variable1,variable2, name1,name2,rValue,year):
    df = pandas.DataFrame({'x':variable1,'y':variable2})
    # plt.figure()
    sns.lmplot(x="x",y="y",data=df,fit_reg=True,height = 6)
    plt.title("Year: %s" %year)
    plt.text(0.1,0.9,r'R^2 = %s'%str(rValue),fontsize = 13)
    plt.xlabel(name1)
    plt.ylabel(name2)
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig('Plots/%s.png'%(year+'_'+name1+'_'+name2))

def get_pValue(values1,values2):
    # Reference: https://pythonfordatascience.org/wilcoxon-sign-ranked-test-python/

    # The hypothesis being test is:
    #   Null hypothesis (H0): The difference between the pairs follows a symmetric distribution around zero.
    #   Alternative hypothesis (HA): The difference between the pairs does not follow a symmetric distribution around zero.

    # If the p-value is less than what is tested at, most commonly 0.05,
    # one can reject the null hypothesis in support of the alternative.


    # Calculate the correlation coeifficients
    # paired t-test: doing two measurments on the same experimental unit
    # t_statistic, p_value = ttest_1samp(values1 - values2, 0)
    # # p < 0.05 => alternative hypothesis: the difference in mean is not equal to 0
    # print("paired t-test", p_value)


    # alternative to paired t-test when data has an ordinary scale or when not normally distributed
    z_statistic, p_value = wilcoxon(values1 - values2)
    print("paired wilcoxon-test", p_value)
    return p_value
